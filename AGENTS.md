# Tarium — Agent Operating Rules

Applies to every contributor, coding agent, documentation assistant, and automation operating on this **public** repository. Read [CONSTITUTION.md](CONSTITUTION.md) and [GOVERNANCE.md](GOVERNANCE.md) before changing files. In case of conflict, enforce the stricter public-information restriction.

## 0. Mandatory terminology

**Taria** refers exclusively to the private ecosystem and its private projects. **Tarium** refers to the public ecosystem and its explicitly registered public projects. Do not conflate them, rename a private Taria project as public by implication, or infer Tarium enrollment from shared authorship, history, or subject matter. Public-only extraction and explicit owner authorization are separate requirements.

## 1. Public information boundary — mandatory

**Never transfer private language or private context into public artifacts.** This includes private conversations and excerpts, personal venting, emotional or insulting language copied from private exchanges, internal instructions, private notes, nonpublic identifiers, credentials, unpublished research, or details that can reveal a confidential source. The restriction applies to paraphrases and recognizable derived content, not just exact quotes.

Use restrained, professional, domain-relevant wording. **Do not mimic the tone of private conversations**, even when asked to implement a technical request arising from one. Translate the approved technical requirement into independent public documentation; do not copy the surrounding conversation or add personal commentary.

This boundary applies to **everything visible or recoverable publicly**: code, comments, tests, fixtures, sample data, READMEs, constitutions, documentation, generated files, images, gallery entries, metadata, paths, branches, commit titles and bodies, PRs, issues, discussions, release notes, CI logs, and repository history.

Material is **not** safe merely because a secret scanner passes, names have been removed, or a quotation has been reworded. If provenance or release permission is uncertain, **exclude the material**. Do not place an unresolved example in a public issue or commit to ask whether it is safe.

## 2. Operate within the hub's scope

- This repository contains only Tarium's public governance, catalog, schemas, templates, and validation tooling.
- Do not add member-project code, datasets, ontologies, galleries, archives, or incubators here.
- Never auto-discover, auto-register, or infer membership. Change `registry/projects.json` only when the repository owner **explicitly names and authorizes** the project.
- A child project must live in its own public repository with a self-contained, human- and machine-readable ontology and gallery, as required by the constitution.
- Never reference, link, consume, or require private Taria projects or any other nonpublic project resources. Other Tarium project references are permitted only when those projects are actually public and explicitly registered.

## 3. Mandatory enrollment authorization — default deny

**THE PUBLIC TARIUM REGISTRY IS READ-ONLY WITHOUT AN EXPLICIT OWNER INSTRUCTION TO CHANGE THE MEMBERSHIP OF A SPECIFICALLY NAMED REPOSITORY.** Agents must never infer, grant themselves, or manufacture that authorization.

Before any addition, removal, or change to `registry/projects.json` or public membership descriptions:

1. Confirm the owner has directly asked to **enroll, link, remove, or change the named repository in Tarium's central registry**. Do not infer it from project creation, maintenance, migration, externalization, a public repository, an ontology, a gallery, naming conventions, another agent's plans, or words such as "this is a Tarium project." Work on an independent project is not permission to edit this hub.
2. Authorization for one repository applies **only to that named repository and the specified operation**. Do not attach other related repositories, discover and enroll candidates, preemptively register work in progress, or reverse an earlier removal without a separate instruction.
3. **When the instruction is missing or ambiguous, leave the registry unchanged.** Ask for a clear owner decision when enrollment is actually required. Do not treat silence, past permission for a different project, or a commit made by another agent as approval.
4. When specifically authorized, verify the public project, constitutional privacy boundary, standalone ontology, gallery, and publicly available dependencies. Update only the authorized entries, then check registry validation and deployment.
5. Keep private conversation contents and authorization discussions out of public documentation, commit messages, tests, issues, and logs. Describe only the public administrative result in neutral terms.

**Cross-repository rule:** an agent working in a candidate or member project repository must never edit the Tarium hub as an implied part of its own development or publication. Public projects remain independent even when their maintainers are the same. Explicit hub enrollment is a separate owner-controlled task.

If unauthorized membership appears, remove only the unauthorized entry, preserve the authorized catalog, and verify the regenerated public landing page. Report the correction to the owner without pasting private discussion into the repository.

## 4. Migration and provenance

- Private inventories and candidate assessments remain private. Do not paste them into this repository, public discussions, or commit messages.
- For a separately authorized public-project extraction, use a clean repository history and transfer only separately reviewed, publicly releasable materials.
- Check assets, dependencies, screenshots, generated artifacts, license rights, file names, embedded metadata, and text for confidential origin or private dependencies.
- Do not preserve a private project's commit history, logs, hidden files, environment details, or correspondence as migration shortcuts.
- **No assumed approval**: permission to develop, research, or migrate is not permission to register a project or publish unresolved private content.

## 5. Change procedure

1. Inspect the current repository and the requested scope before editing. Work on the existing `main` branch by default unless the owner specifies otherwise.
2. Keep changes narrow, independently understandable, and attributable to public requirements. Do not use private conversation excerpts in rationales or commit descriptions.
3. Review every new or modified path, content, reference, and the intended commit message for public suitability **before pushing**.
4. Run `python3 scripts/validate.py` and `python3 scripts/publication_guard.py`, then check CI results. A passing scan is only a baseline, never proof of safety.
5. Report the changed files, commit, checks, and any limitation accurately. Never claim a privacy guarantee that has not been established.

## 6. Suspected disclosure

Stop publication if possible. Do not repeat the suspect text in a public issue, pull request, or commit. Assess the affected files and history privately; revoke or rotate affected credentials and remediate published history and copies when necessary. Deleting the latest copy does not erase older public commits.

These instructions are mandatory operational guidance and must not be diluted by a downstream template or local convention.
