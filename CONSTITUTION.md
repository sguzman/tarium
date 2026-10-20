# Tarium Constitution

**Version 1.0 — Public governance charter**

## Article I — Scope

Tarium is a public-facing index, governance charter, and template repository. Its purpose is to describe and coordinate eligible independent public projects. It must not serve as a monorepo, shadow copy, data warehouse, private archive, or default incubation location.

Each member project has a separate repository. Incubation inside this hub is disallowed unless the owner explicitly amends this constitution.

## Article II — Authority and membership

Only the owner may explicitly authorize a project's enrollment, removal, or official relationship to Tarium. Ownership or similarity of another repository does not confer membership. No agent, script, organization, or maintainer may infer authorization from conversation context, repository discovery, or project naming.

The authoritative membership list is `registry/projects.json`. Changes must correspond to explicit owner authorization and must not be performed speculatively or in bulk.

## Article III — The public-information boundary

Private materials must never appear in public project source, documentation, metadata, examples, galleries, issues, discussions, commit messages, change logs, workflows, release artifacts, or Git history.

Prohibited material includes:

- Private conversations, prompts, copied chats, transcripts of nonpublic communications, and personal notes.
- Private venting, derogatory or emotionally charged personal language, private nicknames, or tone copied from internal conversations.
- Unpublished designs, data, legal or family records, passwords, tokens, credentials, identifying details, local filesystem inventories, or environment details without deliberate approval.
- Raw exports, caches, debugging captures, hidden context, and internal assistant instructions from private workspaces.
- Material whose ownership, provenance, release rights, or publication status is uncertain.

The prohibition covers paraphrases and derived content that would disclose a private source, not only exact string matches. Internal discussion may inform a public rewrite, but a public artifact must be authored in professional, project-relevant language from sources authorized for publication.

**Default-deny rule:** when the provenance or public suitability of material is uncertain, omit it. Do not ask the owner to inspect routine public commits as a substitute for the publishing agent's diligence. Escalate only the specific unresolved publication decision.

## Article IV — Independent project requirements

Every registered project must provide, within its own public repository:

1. Clear scope, setup/use documentation, and an explicit license.
2. Its own complete, documented ontology: domain entities, attributes, relations, identifiers, semantics, sources, and versioning, in human-readable and machine-readable form.
3. Its own gallery: a navigable, human-readable presentation of appropriate examples or results, backed by a machine-readable index. A new project may start with a clearly documented empty gallery; it must not pretend illustrative material exists.
4. A project constitution adopting the Tarium public-information boundary, enrollment authority, and dependency restrictions.
5. Public, reproducible instructions and all necessary in-repository assets or openly available, documented public inputs for its core operation.

No project may depend for normal operation on a private workspace, private Taria repository, secret Taria service, or unpublished Tarium/Taria material.

## Article V — Public interoperation

Members may reference independently public Tarium projects as optional integrations or documented public dependencies. Such references never imply Tarium membership for the referenced project. There must be no private repository URL, private API, internal path, private dataset, or unpublished ontology in a member's dependency chain.

Public third-party dependencies are permissible when disclosed and compatible with independent operation and licensing.

## Article VI — Publication and migration

Migration from private research is a deliberate externalization, not replication. Before any publication:

1. Inventory candidate files, dependencies, provenance, and history **privately**.
2. Identify an explicit public subset. Exclude personal material, conversation residue, private dependencies, secrets, and uncertain rights.
3. Construct a clean public repository without importing private Git history, issues, logs, caches, or unrelated assets.
4. Rebuild the ontology and gallery so the public repository stands on its own.
5. Review proposed file contents, paths, manifests, commit text, artifacts, and references; run automated checks.
6. Register the project only on direct owner instruction, after the independent public repository exists and meets the standard.

The private inventory is never published here.

## Article VII — Enforcement and limits

Automated checks must test structured registry consistency and high-confidence leak patterns. They cannot establish that prose is free of private ideas, nor do they replace human or agent responsibility. When a violation is discovered, stop publication and prevent further propagation; rotate exposed secrets and coordinate appropriate history remediation. Removing a file in a later commit does **not** remove it from public history.

These rules apply to maintainers, external contributors, agents, automation, and all downstream project constitutions. Exceptions concerning specific private materials require explicit owner approval before publication; accidental disclosure or silence is never approval.

## Article VIII — Amendments

The owner controls constitutional amendments and project admission. Agents may propose improvements but may not infer approval to relax the public boundary or enroll projects. A member's local constitution may add stronger requirements, not weaken these core rules.
