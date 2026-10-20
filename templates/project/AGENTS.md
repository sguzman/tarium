# PROJECT_NAME — Agent Operating Rules

This is a template for agents and contributors working in an **independent public Tarium project repository**. Replace the project title and any placeholders before publishing. Read this project's `CONSTITUTION.md` and the public Tarium constitution. More restrictive publication rules take priority.

## Mandatory public-information boundary

**Never publish private language or context.** Do not copy private conversations, personal venting, emotionally charged private tone, internal instructions, private identifiers, secrets, private notes, unpublished resources, or their paraphrases into any publicly accessible artifact.

Public descriptions must use neutral, professional language focused on approved technical facts. Never reproduce private phrasing or personal voice as a shortcut when turning nonpublic work into a public implementation.

Inspect the complete publication surface: code, comments, tests, fixtures, data, ontology, gallery, screenshots, file names, documentation, metadata, dependencies, issues, pull requests, commit messages, branches, releases, build outputs, logs, and Git history. Automated scans cannot establish that prose or provenance is safe. Exclude anything with uncertain publication rights or origin.

## Independent project boundaries

- Work in this independent repository, not the Tarium hub.
- Maintain the full project ontology at `ontology/`, in human-readable and machine-readable forms, with definitions, identifiers, relationships, provenance, and versioning.
- Maintain the project gallery at `gallery/`, including a human-readable overview and machine-readable index. Empty, honestly labeled entries are preferable to fabricated or private examples.
- Make core functionality self-contained using public source and publicly documented dependencies. No private project, service, path, schema, or data source may be required or referenced.
- References to another **Tarium** project must point only to independently public, explicitly registered Tarium members. Other open third-party dependencies must be documented and appropriately licensed.
- Use of these templates does **not** confer Tarium membership. Only the Tarium repository owner's explicit project-specific authorization allows registration.

## Migration and publication procedure

1. Inventory and classify candidate source material **privately**, outside public repositories.
2. Select only materials affirmatively cleared for public release, including their license and provenance. Exclude uncertain cases.
3. Start with a clean public Git history; never carry over private Git histories, logs, private environment files, or unrelated private data.
4. Review all changed content, dependencies, assets, and planned commit messages for source leakage and neutral public wording.
5. Run project-specific validation and public-content checks before pushing. Treat these as supplementary to actual content review.
6. Publish project changes without silently changing Tarium registry membership; the owner authorizes enrollment separately.

## If a potential leak is found

Stop further publication. Avoid quoting suspect material in a public report. Handle investigation, access revocation, and history remediation through appropriate private channels. A deletion commit alone will not purge old history.
