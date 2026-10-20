# Tarium

**A public registry and governance hub for independent projects.**

Tarium describes a collection of public, self-contained projects. Each project lives in its **own repository**. This repository holds the public catalog, shared rules, and reusable templates. It does not host project implementations, datasets, research inventories, galleries, or incubating projects.

## Names and separation

**Taria** designates the private ecosystem and its private projects. **Tarium** designates this public ecosystem and its public member projects. They are separate, and a Taria project is not a Tarium project unless a deliberately externalized public repository has been separately authorized for enrollment. Private Taria information and dependencies must never be exposed through Tarium.

## Project registry

**Two projects are enrolled:** [Architectarium](https://github.com/sguzman/architectarium) and [Stratlas](https://github.com/sguzman/stratlas). Registration is by the repository owner's explicit authorization only; related names or maintainers do not imply membership.

| Project | Overview | Public resources | Identity color |
| --- | --- | --- | --- |
| [Architectarium](https://github.com/sguzman/architectarium) | Architectural ontology, building dossiers, and schematic interactive 3D study | [Ontology](https://github.com/sguzman/architectarium/blob/main/ontology/components.json) · [Gallery](https://github.com/sguzman/architectarium/blob/main/site/index.html) · [Catalog](https://github.com/sguzman/architectarium/blob/main/specimens/queue.json) | Sandstone `#B9905D` |
| [Stratlas](https://github.com/sguzman/stratlas) | Metropolitan-area specimens, maps, and source-backed urban/geographic data | [Ontology](https://github.com/sguzman/stratlas/blob/main/docs/ontology/model.json) · [Interactive map](https://sguzman.github.io/stratlas/) · [Gallery index](https://github.com/sguzman/stratlas/blob/main/gallery/index.json) | Cartographic blue `#6B9DC4` |

The canonical machine-readable registry is the source of truth. Each project has its own identity color, and the [public project landing page](https://sguzman.github.io/tarium/) renders directly from registry data with no duplicated project catalog in the site code.

## Public website

**[Browse Tarium projects](https://sguzman.github.io/tarium/)**. The lightweight GitHub Pages site is built from `site/` and the authorized public `registry/projects.json`. A dedicated workflow validates and publishes only these public files. A new approved entry appears automatically after a successful deployment; member implementations stay in their own repositories.

Locally, run `python3 scripts/build_site.py` to build `_site/`. There are no frontend dependencies or external network requirements.

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

These are scaffolds for **future independent repositories**, not projects hosted here. Only the owner may authorize additions to the public registry.

## Verification

Run `python3 scripts/validate.py` for registry and template structure, and `python3 scripts/publication_guard.py` for high-confidence public-content leak signatures. GitHub Actions runs these checks on pushes and pull requests. Automated checks supplement, but never replace, source-by-source publication review.

## License

The hub is licensed under [MIT](LICENSE). Each independently maintained project chooses and declares its own license.
