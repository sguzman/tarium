# Tarium

**A public registry and governance hub for independent projects.**

Tarium describes a collection of public, self-contained projects. Each project lives in its **own repository**. This repository holds the public catalog, shared rules, and reusable templates. It does not host project implementations, datasets, research inventories, galleries, or incubating projects.

## Names and separation

**Taria** designates the private ecosystem and its private projects. **Tarium** designates this public ecosystem and its public member projects. They are separate, and a Taria project is not a Tarium project unless a deliberately externalized public repository has been separately authorized for enrollment. Private Taria information and dependencies must never be exposed through Tarium.

## Project registry

**No projects are enrolled yet.** Registration is by explicit authorization from the repository owner only. A public repository does not become a Tarium project just because it has a related name, subject, or maintainer.

- [Machine-readable project registry](registry/projects.json)
- [Registry format](registry/schema.json)
- [Admission and governance](GOVERNANCE.md)

When the owner approves a project, its entry will provide a short overview and a link to its independent public repository. The project itself must provide its ontology and gallery.

## Core guarantees

1. **Public-only boundary.** No personal conversations, private notes, venting, internal instructions, secrets, or unpublished source material may be copied to public artifacts.
2. **Explicit membership.** Only the owner may authorize adding or removing a project from this registry. No automatic discovery or implied affiliation.
3. **Independent repositories.** Tarium hosts no member-project source trees or assets.
4. **Self-sufficiency.** Each member owns its complete domain ontology, documentation, gallery, and necessary runtime/build assets. Links to other projects are optional integrations, not hidden prerequisites.
5. **Public dependencies only.** Member projects may refer to other approved, publicly accessible Tarium projects, never to private workspaces, unpublished repositories, or private project resources.
6. **Clean externalization.** Candidate material must be inventoried and individually approved, redacted or rewritten for publication, then reviewed for provenance and leaks before release. Never transplant private Git histories.

For day-to-day agent and contributor behavior, see [AGENTS.md](AGENTS.md). These operating rules explicitly prohibit copying private language or tone into any public artifact.

These are binding rules, not a claim that automated scanners can detect every contextual disclosure. See the [constitution](CONSTITUTION.md), [externalization procedure](EXTERNALIZATION.md), and [contribution rules](CONTRIBUTING.md).

## Templates

- [Project agent instructions](templates/project/AGENTS.md)
- [Project constitution](templates/project/CONSTITUTION.md)
- [Project README](templates/project/README.md)
- [Project membership manifest](templates/project/tarium.json)
- [Ontology starter](templates/project/ontology/README.md)
- [Gallery starter](templates/project/gallery/README.md)

These are scaffolds for **future independent repositories**, not projects hosted here. This hub's registry remains empty until the owner authorizes specific additions.

## Verification

Run `python3 scripts/validate.py` for registry and template structure, and `python3 scripts/publication_guard.py` for high-confidence public-content leak signatures. GitHub Actions runs these checks on pushes and pull requests. Automated checks supplement, but never replace, source-by-source publication review.

## License

The hub is licensed under [MIT](LICENSE). Each independently maintained project chooses and declares its own license.
