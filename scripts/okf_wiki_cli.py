#!/usr/bin/env python3
"""Open Knowledge Format (OKF v0.2) LLM Wiki Management CLI for google-cloud-knowledge-base.

Implements Andrej Karpathy's three-layer architecture:
  Layer 1: Raw Sources (wiki/raw/)
  Layer 2: The Wiki (wiki/concepts/)
  Layer 3: The Schema (wiki/SCHEMA.md)

Supports multi-format ingestion (text, URLs, PDFs, audio, video), concept collision
prevention via CONCEPT_REGISTRY.json, deterministic queue processing, index generation,
and OKF compliance verification.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Tuple
import urllib.request

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WIKI_DIR = os.path.join(WORKSPACE_ROOT, "wiki")
RAW_DIR = os.path.join(WIKI_DIR, "raw")
CONCEPTS_DIR = os.path.join(WIKI_DIR, "concepts")
ASSETS_DIR = os.path.join(WIKI_DIR, "assets")
MANIFEST_PATH = os.path.join(RAW_DIR, "MANIFEST.json")
QUEUE_PATH = os.path.join(RAW_DIR, "PROCESSING_QUEUE.json")
REGISTRY_PATH = os.path.join(WIKI_DIR, "CONCEPT_REGISTRY.json")
INDEX_PATH = os.path.join(WIKI_DIR, "index.md")
LOG_PATH = os.path.join(WIKI_DIR, "log.md")
SCHEMA_PATH = os.path.join(WIKI_DIR, "SCHEMA.md")

AUDIO_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac", ".webm"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm"}
PDF_EXTENSIONS = {".pdf"}


def ensure_directories():
    """Ensures that all wiki directories and fundamental tracking files exist."""
    for d in [WIKI_DIR, RAW_DIR, CONCEPTS_DIR]:
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump({"version": "0.2", "last_sync": None, "sources": {}}, f, indent=2)
    if not os.path.exists(QUEUE_PATH):
        with open(QUEUE_PATH, "w", encoding="utf-8") as f:
            json.dump({"items": [], "last_updated": None}, f, indent=2)
    if not os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump({"version": "0.2", "concepts": {}}, f, indent=2)


def slugify(text: str) -> str:
    """Converts a title or string into a clean lowercase filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text.strip("_")


def calculate_hash(content: bytes) -> str:
    """Calculates the SHA256 hash of byte content."""
    return hashlib.sha256(content).hexdigest()


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file using pdftotext."""
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"pdftotext error: {e.stderr}\n")
        return f"[PDF text extraction failed for: {os.path.basename(pdf_path)}]"


def _parse_simple_yaml(yaml_str: str) -> Dict[str, Any]:
    """Zero-dependency fallback YAML frontmatter parser."""
    meta: Dict[str, Any] = {}
    for line in yaml_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        # Strip inline comment if not inside quotes
        if not (val.startswith('"') or val.startswith("'") or val.startswith("[")):
            val = re.sub(r"\s+#.*$", "", val).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                meta[key] = []
            else:
                items = [i.strip().strip('"').strip("'") for i in inner.split(",")]
                meta[key] = [i for i in items if i]
        else:
            meta[key] = val.strip('"').strip("'")
    return meta


def parse_frontmatter(file_path: str) -> Tuple[Dict[str, Any], str]:
    """Extracts YAML frontmatter and body from a markdown file."""
    if not os.path.exists(file_path):
        return {}, ""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    yaml_str, body = match.group(1), match.group(2)
    try:
        import yaml
        meta = yaml.safe_load(yaml_str) or {}
    except Exception:
        meta = _parse_simple_yaml(yaml_str)
    return meta, body


def cmd_ingest(args):
    """Ingests a file, URL, or raw text into wiki/raw/, extracts content, updates MANIFEST and QUEUE."""
    ensure_directories()
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    source_identifier = args.source or args.title or "direct_text_input"
    title = args.title or os.path.splitext(os.path.basename(source_identifier))[0]
    category = args.category or "Google Cloud"
    safe_slug = slugify(title)

    extracted_text = ""
    raw_filename = f"{safe_slug}.md"
    raw_file_path = os.path.join(RAW_DIR, raw_filename)
    source_type = "text"
    content_bytes = b""

    if args.text:
        source_type = "raw_text"
        extracted_text = args.text
        with open(raw_file_path, "w", encoding="utf-8") as f:
            f.write(f"# Source: {title}\n\nDate: {now_iso}\nCategory: {category}\n\n{extracted_text}\n")
        content_bytes = extracted_text.encode("utf-8")

    elif args.source:
        source = args.source
        if source.startswith("http://") or source.startswith("https://"):
            source_type = "url"
            try:
                req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
                with urllib.request.urlopen(req) as resp:
                    raw_bytes = resp.read()
                    content_bytes = raw_bytes
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(raw_bytes, "html.parser")
                    article = soup.find("article") or soup.find("main") or soup.body
                    text_content = article.get_text(separator="\n", strip=True) if article else soup.get_text(separator="\n", strip=True)
                except ImportError:
                    text_content = re.sub(r"<[^>]+>", " ", raw_bytes.decode("utf-8", errors="ignore"))
                    text_content = re.sub(r"\s+", " ", text_content).strip()

                extracted_text = f"URL: {source}\n\n{text_content}"
                with open(raw_file_path, "w", encoding="utf-8") as f:
                    f.write(f"# Source URL: {source}\n\nDate: {now_iso}\nCategory: {category}\n\n{extracted_text}\n")
            except Exception as e:
                sys.stderr.write(f"Error fetching URL {source}: {e}\n")
                return 1
        else:
            if not os.path.exists(source):
                sys.stderr.write(f"Error: Source file does not exist: {source}\n")
                return 1
            ext = os.path.splitext(source)[1].lower()
            with open(source, "rb") as f:
                content_bytes = f.read()

            if ext in PDF_EXTENSIONS:
                source_type = "pdf"
                stored_pdf = os.path.join(RAW_DIR, f"{safe_slug}{ext}")
                shutil.copy2(source, stored_pdf)
                pdf_text = extract_text_from_pdf(source)
                extracted_text = f"## PDF Source: {os.path.basename(source)}\n\n{pdf_text}"
                with open(raw_file_path, "w", encoding="utf-8") as f:
                    f.write(f"# PDF Document: {title}\n\nDate: {now_iso}\nCategory: {category}\nSource Path: {source}\n\n{extracted_text}\n")
            else:
                source_type = "text_file"
                with open(source, "r", encoding="utf-8", errors="ignore") as sf:
                    extracted_text = sf.read()
                with open(raw_file_path, "w", encoding="utf-8") as f:
                    f.write(f"# Source File: {os.path.basename(source)}\n\nDate: {now_iso}\nCategory: {category}\nSource Path: {source}\n\n{extracted_text}\n")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    file_hash = calculate_hash(content_bytes) if content_bytes else calculate_hash(extracted_text.encode("utf-8"))
    manifest["last_sync"] = now_iso
    manifest["sources"][raw_filename] = {
        "title": title,
        "source": source_identifier,
        "source_type": source_type,
        "category": category,
        "hash": file_hash,
        "ingested_at": now_iso,
        "raw_file": raw_filename
    }
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    existing = next((item for item in queue_data["items"] if item["raw_file"] == raw_filename), None)
    if existing:
        existing["status"] = "PENDING"
        existing["updated_at"] = now_iso
    else:
        queue_data["items"].append({
            "raw_file": raw_filename,
            "title": title,
            "category": category,
            "source_type": source_type,
            "status": "PENDING",
            "enqueued_at": now_iso,
            "concept_pages": []
        })
    queue_data["last_updated"] = now_iso
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, indent=2)

    print(f"Successfully ingested '{title}' into {raw_file_path}")
    print(f"Enqueued in {QUEUE_PATH} with status PENDING")
    return 0


def cmd_get_next_queue(args):
    """Gets next pending item from the queue, locking it as IN_PROGRESS."""
    ensure_directories()
    if not os.path.exists(QUEUE_PATH):
        print(json.dumps({"state": "DRAINED", "item": None}))
        return 0

    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    items = queue_data.get("items", [])
    pending = [i for i in items if i.get("status") == "PENDING"]
    in_progress = [i for i in items if i.get("status") == "IN_PROGRESS"]

    if in_progress:
        print(json.dumps({
            "state": "LOCKED",
            "active_item": in_progress[0],
            "pending_count": len(pending),
            "in_progress_count": len(in_progress)
        }, indent=2))
        return 0

    if not pending:
        print(json.dumps({
            "state": "DRAINED",
            "pending_count": 0,
            "in_progress_count": 0
        }, indent=2))
        return 0

    item = pending[0]
    item["status"] = "IN_PROGRESS"
    item["started_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, indent=2)

    print(json.dumps({
        "state": "ITEM_AVAILABLE",
        "item": item,
        "pending_count": len(pending) - 1
    }, indent=2))
    return 0


def cmd_update_queue(args):
    """Updates queue status for a specific item."""
    ensure_directories()
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    updated = False
    for item in queue_data.get("items", []):
        if item.get("raw_file") == args.filename or item.get("title") == args.filename:
            item["status"] = args.status
            item["completed_at"] = now_iso
            if args.concept_pages:
                pages = [p.strip() for p in args.concept_pages.split(",") if p.strip()]
                item["concept_pages"] = list(set(item.get("concept_pages", []) + pages))
            updated = True
            break

    if updated:
        with open(QUEUE_PATH, "w", encoding="utf-8") as f:
            json.dump(queue_data, f, indent=2)
        print(f"Updated queue item '{args.filename}' to status '{args.status}'")
        return 0
    else:
        sys.stderr.write(f"Error: Item '{args.filename}' not found in queue.\n")
        return 1


def cmd_manage_concepts(args):
    """Manages the CONCEPT_REGISTRY.json file (sync or query)."""
    ensure_directories()
    action = args.action

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    concepts = registry.setdefault("concepts", {})

    if action == "sync":
        concepts.clear()
        for root, _, files in os.walk(CONCEPTS_DIR):
            for file in sorted(files):
                if not file.endswith(".md") or file == "index.md":
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, WIKI_DIR)
                meta, _ = parse_frontmatter(file_path)
                slug = os.path.splitext(file)[0]
                title = meta.get("title", slug.replace("_", " ").title())
                category = meta.get("category", "General")
                tags = [str(t) for t in meta.get("tags", [])]
                description = meta.get("description", "")
                aliases = [str(a) for a in meta.get("aliases", [])]
                concept_type = meta.get("type", "Concept")
                resource = meta.get("resource", "")

                concepts[slug] = {
                    "slug": slug,
                    "title": title,
                    "type": concept_type,
                    "category": category,
                    "tags": tags,
                    "description": description,
                    "aliases": aliases,
                    "resource": resource,
                    "path": f"concepts/{file}",
                    "rel_path": rel_path,
                    "last_updated": meta.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat())
                }

        registry["last_synced"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)
        print(f"Synced {len(concepts)} concepts to {REGISTRY_PATH}")
        return 0

    elif action == "query":
        term = (args.term or "").lower().strip()
        matches = []
        for slug, data in concepts.items():
            score = 0
            if term in slug:
                score += 3
            if term in data.get("title", "").lower():
                score += 4
            if any(term in str(alias).lower() for alias in data.get("aliases", [])):
                score += 3
            if any(term in str(tag).lower() for tag in data.get("tags", [])):
                score += 2
            if term in data.get("description", "").lower():
                score += 1
            if score > 0 or not term:
                matches.append((score, data))

        matches.sort(key=lambda x: x[0], reverse=True)
        results = [m[1] for m in matches]
        print(json.dumps({"count": len(results), "matches": results}, indent=2))
        return 0


def cmd_rebuild_index(args):
    """Rebuilds wiki/index.md, wiki/concepts/index.md, and syncs registry."""
    ensure_directories()
    args.action = "sync"
    cmd_manage_concepts(args)

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    concepts = registry.get("concepts", {})
    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    categories: Dict[str, List[Dict[str, Any]]] = {}
    for slug, item in sorted(concepts.items(), key=lambda x: x[1].get("title", "")):
        cat = item.get("category", "General")
        categories.setdefault(cat, []).append(item)

    index_md = []
    index_md.append("# Google Cloud Knowledge Base Index (OKF v0.2)")
    index_md.append("")
    index_md.append(f"> Auto-generated progressive disclosure catalog compliant with Open Knowledge Format (OKF v0.2). Last updated: {now_str}")
    index_md.append("")
    index_md.append("## Overview")
    index_md.append(f"Total concepts documented: **{len(concepts)}** across **{len(categories)}** categories.")
    index_md.append("")

    for cat_name, cat_items in sorted(categories.items()):
        index_md.append(f"### {cat_name}")
        index_md.append("")
        index_md.append("| Concept | Type | Description | Tags |")
        index_md.append("| :--- | :--- | :--- | :--- |")
        for item in cat_items:
            slug = item.get("slug")
            title = item.get("title", slug)
            c_type = item.get("type", "Concept")
            desc = item.get("description", "").replace("|", "\\|")
            tags = ", ".join(str(t) for t in item.get("tags", []))
            link = f"[{title}](concepts/{slug}.md)"
            index_md.append(f"| {link} | `{c_type}` | {desc} | {tags} |")
        index_md.append("")

    index_md.append("---")
    index_md.append("## Navigation & Governance")
    index_md.append("- [Wiki Schema & Governance](SCHEMA.md)")
    index_md.append("- [Changelog](log.md)")
    index_md.append("- [Concept Registry JSON](CONCEPT_REGISTRY.json)")
    index_md.append("- [Raw Ingestion Sources](raw/MANIFEST.json)")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(index_md) + "\n")

    concepts_index_md = []
    concepts_index_md.append("# Google Cloud Concepts Index")
    concepts_index_md.append("")
    concepts_index_md.append(f"> Auto-generated concept catalog. Last updated: {now_str}")
    concepts_index_md.append("")
    for cat_name, cat_items in sorted(categories.items()):
        concepts_index_md.append(f"### {cat_name}")
        concepts_index_md.append("")
        concepts_index_md.append("| Concept | Type | Description | Tags |")
        concepts_index_md.append("| :--- | :--- | :--- | :--- |")
        for item in cat_items:
            slug = item.get("slug")
            title = item.get("title", slug)
            c_type = item.get("type", "Concept")
            desc = item.get("description", "").replace("|", "\\|")
            tags = ", ".join(str(t) for t in item.get("tags", []))
            link = f"[{title}]({slug}.md)"
            concepts_index_md.append(f"| {link} | `{c_type}` | {desc} | {tags} |")
        concepts_index_md.append("")

    concepts_index_md.append("---")
    concepts_index_md.append("## Navigation")
    concepts_index_md.append("- [Root Wiki Index](../index.md)")
    concepts_index_md.append("- [Wiki Schema & Governance](../SCHEMA.md)")
    concepts_index_md.append("- [Changelog](../log.md)")

    concepts_index_path = os.path.join(CONCEPTS_DIR, "index.md")
    with open(concepts_index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(concepts_index_md) + "\n")

    print(f"Successfully rebuilt {INDEX_PATH} and {concepts_index_path}")
    return 0


def cmd_log_entry(args):
    """Appends an entry to wiki/log.md."""
    ensure_directories()
    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry_lines = []
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0:
        entry_lines.append("# Google Cloud Knowledge Base - OKF Wiki Change Log\n\nChronological history of knowledge additions, updates, and distillations.\n")

    entry_lines.append(f"### [{now_str}] {args.title}")
    if args.message:
        entry_lines.append(f"- {args.message}")
    if args.pages:
        for p in args.pages.split(","):
            p = p.strip()
            if p:
                entry_lines.append(f"- Concept page: `[{p}]({p})`")
    entry_lines.append("")

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write("\n".join(entry_lines) + "\n")

    print(f"Logged entry to {LOG_PATH}")
    return 0


def cmd_verify(args):
    """Verifies OKF compliance, frontmatter structure, and link hygiene."""
    ensure_directories()
    errors = []
    warnings = []
    concept_count = 0

    for root, _, files in os.walk(CONCEPTS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file == "index.md":
                continue
            concept_count += 1
            file_path = os.path.join(root, file)
            meta, body = parse_frontmatter(file_path)

            if not meta:
                errors.append(f"Missing or invalid YAML frontmatter in {file_path}")
                continue

            if "type" not in meta:
                errors.append(f"Missing required OKF field 'type' in {file_path}")
            if "title" not in meta:
                errors.append(f"Missing standard field 'title' in {file_path}")
            if "description" not in meta or not meta["description"]:
                warnings.append(f"Missing or empty 'description' in {file_path}")

            stripped_body = re.sub(r"```[\s\S]*?```", "", body)
            stripped_body = re.sub(r"`[^`\n]+`", "", stripped_body)

            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", stripped_body)
            for text, link in links:
                if link.startswith("http://") or link.startswith("https://") or link.startswith("#") or link.startswith("mailto:"):
                    continue
                target_link = link.split("#")[0]
                if not target_link:
                    continue
                target = os.path.normpath(os.path.join(os.path.dirname(file_path), target_link))
                if not os.path.exists(target):
                    warnings.append(f"Broken link in {file}: [{text}]({link}) -> {target} not found")

    print("OKF Verification Summary:")
    print(f"- Total Concept Pages Checked: {concept_count}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  ❌ {e}")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ⚠️ {w}")

    return 0 if (not errors and not warnings) else 1


def cmd_search(args):
    """Searches the OKF Wiki concepts."""
    ensure_directories()
    term = args.query.lower().strip()
    results = []

    for root, _, files in os.walk(CONCEPTS_DIR):
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
            file_path = os.path.join(root, file)
            meta, body = parse_frontmatter(file_path)
            slug = os.path.splitext(file)[0]
            title = meta.get("title", slug)
            description = meta.get("description", "")
            category = meta.get("category", "")
            tags = meta.get("tags", [])
            aliases = meta.get("aliases", [])
            concept_type = meta.get("type", "Concept")

            score = 0
            if term in title.lower():
                score += 10
            if term in slug.lower():
                score += 8
            if any(term in str(a).lower() for a in aliases):
                score += 7
            if any(term in str(t).lower() for t in tags):
                score += 6
            if term in description.lower():
                score += 5
            if term in category.lower():
                score += 4
            if term in body.lower():
                score += 2

            if score > 0 or not term:
                results.append({
                    "score": score,
                    "slug": slug,
                    "title": title,
                    "type": concept_type,
                    "category": category,
                    "tags": tags,
                    "description": description,
                    "path": os.path.relpath(file_path, WORKSPACE_ROOT)
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Search results for '{args.query}' ({len(results)} found):\n")
        for r in results:
            print(f"• [{r['title']}] ({r['path']}) [{r['category']}]")
            print(f"  Type: {r['type']} | Tags: {', '.join(str(t) for t in r['tags'])}")
            print(f"  Description: {r['description']}\n")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Open Knowledge Format (OKF v0.2) LLM Wiki Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_p = subparsers.add_parser("ingest", help="Ingest text/file/URL/PDF into raw sources")
    ingest_p.add_argument("--source", help="Path to file or URL")
    ingest_p.add_argument("--text", help="Raw text string to ingest")
    ingest_p.add_argument("--title", help="Title for the source document")
    ingest_p.add_argument("--category", help="Category domain")

    subparsers.add_parser("get-next-in-queue", help="Get next item from raw queue")

    update_q_p = subparsers.add_parser("update-queue", help="Update queue item status")
    update_q_p.add_argument("--filename", required=True, help="Raw filename or title")
    update_q_p.add_argument("--status", default="COMPLETED", choices=["COMPLETED", "PENDING", "IN_PROGRESS", "FAILED"])
    update_q_p.add_argument("--concept_pages", help="Comma-separated paths of generated concept pages")

    mc_p = subparsers.add_parser("manage-concepts", help="Sync or query concept registry")
    mc_p.add_argument("--action", choices=["sync", "query"], default="sync")
    mc_p.add_argument("--term", help="Search term for query")

    subparsers.add_parser("rebuild-index", help="Rebuild wiki index and concept registry")

    log_p = subparsers.add_parser("log-entry", help="Append an entry to wiki/log.md")
    log_p.add_argument("--title", required=True, help="Title of the update")
    log_p.add_argument("--message", help="Summary message")
    log_p.add_argument("--pages", help="Comma-separated concept pages affected")

    subparsers.add_parser("verify", help="Verify OKF compliance and link hygiene")

    search_p = subparsers.add_parser("search", help="Search the wiki")
    search_p.add_argument("query", nargs="?", default="", help="Search query term")
    search_p.add_argument("--json", action="store_true", help="Output results in JSON")

    args = parser.parse_args()
    if args.command == "ingest":
        sys.exit(cmd_ingest(args))
    elif args.command == "get-next-in-queue":
        sys.exit(cmd_get_next_queue(args))
    elif args.command == "update-queue":
        sys.exit(cmd_update_queue(args))
    elif args.command == "manage-concepts":
        sys.exit(cmd_manage_concepts(args))
    elif args.command == "rebuild-index":
        sys.exit(cmd_rebuild_index(args))
    elif args.command == "log-entry":
        sys.exit(cmd_log_entry(args))
    elif args.command == "verify":
        sys.exit(cmd_verify(args))
    elif args.command == "search":
        sys.exit(cmd_search(args))


if __name__ == "__main__":
    main()
