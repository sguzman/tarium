#!/usr/bin/env python3
"""Validate the Tarium catalog and public-project scaffolding (stdlib only)."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from project_colors import assign_colors

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/projects.json"
REQUIRED = (
    "CONSTITUTION.md",
    "AGENTS.md",
    "templates/project/AGENTS.md",
    "GOVERNANCE.md",
    "EXTERNALIZATION.md",
    "registry/schema.json",
    "templates/project/CONSTITUTION.md",
    "templates/project/README.md",
    "templates/project/tarium.json",
    "templates/project/ontology/README.md",
    "templates/project/ontology/ontology.json",
    "templates/project/gallery/README.md",
    "templates/project/gallery/index.json",
)
SLUG = re.compile(r"^[a-z][a-z0-9-]*$")
SAFE_PATH = re.compile(r"^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*$")


def read_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_relative(value, label):
    require(isinstance(value, str) and SAFE_PATH.fullmatch(value), f"{label}: unsafe path")
    require(not any(segment in (".", "..") for segment in value.split("/")), f"{label}: traversal")


def main():
    for path in REQUIRED:
        require((ROOT / path).is_file(), f"missing required file: {path}")
    # The privacy boundary is an essential part of both agent instruction files.
    for instructions in ("AGENTS.md", "templates/project/AGENTS.md"):
        text = (ROOT / instructions).read_text(encoding="utf-8").lower()
        require("never" in text and "private language" in text and "commit" in text,
                f"{instructions}: mandatory publication instructions are missing")
    registry = read_json(REGISTRY)
    schema = read_json(ROOT / "registry/schema.json")
    require(schema.get("properties", {}).get("schema_version", {}).get("const") == 2, "registry schema version mismatch")
    repo_pattern = schema["properties"]["projects"]["items"]["properties"]["repository"]["pattern"]
    require(re.fullmatch(repo_pattern, "https://github.com/sguzman/valid-repo") is not None, "registry schema rejects a valid repository URL")
    require(isinstance(registry, dict) and set(registry) == {"schema_version", "projects"}, "invalid registry root")
    require(type(registry["schema_version"]) is int and registry["schema_version"] == 2, "unsupported registry version")
    projects = registry["projects"]
    require(isinstance(projects, list), "registry projects must be a list")
    seen_slugs = set()
    seen_repos = set()
    for item in projects:
        require(isinstance(item, dict), "project entry must be an object")
        required = {"slug", "name", "summary", "repository", "domains", "ontology_path", "gallery_path", "gallery_index_path", "accent_color"}
        require(required <= set(item) <= required | {"website_url"}, "project entry has missing or unexpected fields")
        slug = item["slug"]
        require(isinstance(slug, str) and SLUG.fullmatch(slug), f"invalid slug: {slug!r}")
        require(slug not in seen_slugs, f"duplicate slug: {slug}")
        seen_slugs.add(slug)
        for key in ("name", "summary"):
            require(isinstance(item[key], str) and item[key].strip() == item[key] and item[key], f"{slug}: invalid {key}")
        require(10 <= len(item["summary"]) <= 500, f"{slug}: summary length out of range")
        domains = item["domains"]
        require(isinstance(domains, list) and domains and all(isinstance(x, str) and x.strip() == x and x for x in domains), f"{slug}: invalid domains")
        require(len(domains) == len(set(domains)), f"{slug}: duplicate domains")
        url = item["repository"]
        require(isinstance(url, str), f"{slug}: repository URL missing")
        parts = urlsplit(url)
        require(parts.scheme == "https" and parts.netloc == "github.com" and not parts.query and not parts.fragment and not parts.username and not parts.password, f"{slug}: invalid public repository URL")
        segments = parts.path.strip("/").split("/")
        require(len(segments) == 2 and all(re.fullmatch(r"[A-Za-z0-9_.-]+", s) for s in segments) and not parts.path.endswith("/"), f"{slug}: repository must point to a GitHub repository root")
        require(segments[1].lower() != "taria", f"{slug}: private parent project is forbidden")
        require(url.lower() not in seen_repos, f"{slug}: duplicate repository")
        seen_repos.add(url.lower())
        for key in ("ontology_path", "gallery_path", "gallery_index_path"):
            safe_relative(item[key], f"{slug}: {key}")
            pattern = schema["properties"]["projects"]["items"]["properties"][key]["pattern"]
            require(re.fullmatch(pattern, item[key]) is not None, f"{slug}: {key} violates registry schema")
        if "website_url" in item:
            site_url = item["website_url"]
            require(isinstance(site_url, str), f"{slug}: invalid website_url")
            site_pattern = schema["properties"]["projects"]["items"]["properties"]["website_url"]["pattern"]
            require(re.fullmatch(site_pattern, site_url) is not None, f"{slug}: website_url must be a GitHub Pages project URL")
        accent = item["accent_color"]
        require(isinstance(accent, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", accent), f"{slug}: invalid accent_color")
    require([x["slug"] for x in projects] == sorted(seen_slugs), "registry must be sorted by slug")
    expected_colors = assign_colors([x["name"] for x in projects])
    for item in projects:
        require(item["accent_color"] == expected_colors[item["slug"]],
                f'{item["slug"]}: project color must match deterministic OKLab human-distinction identity')
    manifest = read_json(ROOT / "templates/project/tarium.json")
    ontology = read_json(ROOT / "templates/project/ontology/ontology.json")
    gallery = read_json(ROOT / "templates/project/gallery/index.json")
    require(manifest.get("format_version") == 1 and manifest.get("membership") == "unregistered", "template must not self-enroll")
    require(manifest.get("ontology", {}).get("data") == "ontology/ontology.json", "template ontology path mismatch")
    require(manifest.get("gallery", {}).get("data") == "gallery/index.json", "template gallery path mismatch")
    require(ontology.get("format_version") == 1 and isinstance(ontology.get("concepts"), list) and isinstance(ontology.get("relations"), list), "invalid ontology starter")
    require(gallery == {"format_version": 1, "entries": []}, "gallery template must start empty")
    print(f"Tarium structure valid: {len(projects)} explicitly registered project(s).")
    print("Note: registry checks do not establish publication approval, repository visibility, or remote project compliance.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"Tarium validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
