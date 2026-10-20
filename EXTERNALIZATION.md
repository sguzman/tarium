# Externalizing an independent public project

This procedure concerns candidate projects developed in nonpublic environments. **Never commit the private inventory or its evidence to Tarium.**

## Phase A — Private inventory

Work in the authorized private environment only. Inventory source files, data, build requirements, documentation, configuration, third-party licenses, licenses for content/media, secrets, Git history, internal references, conversation traces, and dependencies.

Classify each candidate item as `publicly releasable`, `rewrite or sanitize`, `keep private`, or `unresolved`. Unresolved is excluded by default. Do not rely on file names or pattern matching alone.

## Phase B — Clean extraction

Create an independent **public** repository with clean version-control history. Move only approved content; do not clone/push a private repository's full history or copy unrelated files. Rewrite internal comments and documentation in neutral, project-relevant language. Replace any private service or ontology assumption with complete public equivalents.

Before release, review all intended publication surfaces: files and file names, example data, images, commit titles/bodies, issue descriptions, tags/releases, generated artifacts, workflow logs, and linked resources. Avoid uploading raw exports or screenshots that could contain sensitive context.

## Phase C — Independent completeness

The child repository owns its complete ontology and gallery. The ontology must be intelligible and usable without a private parent. The gallery must display real public examples where available, or clearly state that it is empty.

All required source/build assets and public inputs must be described. Other registered, public Tarium projects may be referenced when truly relevant, but unpublished/private projects may never be dependencies.

Copy and adapt the [project template](templates/project/README.md). Preserve its mandatory constitutional clauses. Include a manifest with its ontology/gallery paths.

## Phase D — Verification and enrollment

Run source/content review plus automated guards in the public repository **before** sharing. Checks are aids, not proof of privacy. Confirm public repository visibility and paths.

Only after a direct owner enrollment instruction may the hub register the independent project. Never infer enrollment from an extraction task. Do not publish the private inventory, rejected material, or private repository provenance into the public hub.

## If a leak is found

Stop related publication. Remove exposed content at its source, assess permanent history and third-party copies, rotate credentials if implicated, and perform history remediation where appropriate. A follow-up deletion commit alone leaves the original content retrievable.
