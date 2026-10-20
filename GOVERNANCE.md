# Governance and registry policy

Tarium is a catalog rather than a source aggregator.

## Enrollment

The repository owner alone decides which projects are connected to Tarium. A project is **not** enrolled until the owner explicitly names it for enrollment and its entry is intentionally added to `registry/projects.json`.

There is no automatic import from GitHub accounts, repository names, private workspaces, existing codebases, issue discussions, or guessed affiliations. Never populate the registry from a search result alone.

Before an authorized entry is added, verify: the target repository is public; its overview is accurate; its constitution incorporates the mandatory clauses; its ontology and gallery are present in the **target repository**; and the core project does not require private resources.

Removing a project from the registry does not delete or modify its independent repository.

## Registry entries

An entry contains a unique slug, display name, concise public summary, canonical public GitHub repository URL, public subject areas, and relative locations of the member's ontology and gallery. It is descriptive metadata, not an executable dependency catalog.

Registry order is alphabetical by slug. The initial registry intentionally has no entries.

## Operations

The hub may host governance documents, standards, schemas, templates, scripts, and automation that validate this hub. It must not host member implementations, working research copies, example exports from private sources, or unapproved incubators.

Use neutral, public-facing language in all repository surfaces, including issue bodies and commit messages. Protect the same boundary in Git history, not merely current files.

The owner authorizes membership and substantive policy changes; maintainers can keep documentation and validation tools correct without enrolling projects on their own.
