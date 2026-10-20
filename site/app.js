"use strict";
(function () {
  const list = document.getElementById("project-list");
  const count = document.getElementById("project-count");
  const allowRepo = /^https:\/\/github\.com\/[A-Za-z0-9-]+\/[A-Za-z0-9_.-]+$/;
  const allowPath = /^[A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*$/;
  const allowAccent = /^#[A-Fa-f0-9]{6}$/;
  const allowWebsite = /^https:\/\/[A-Za-z0-9-]+\.github\.io\/[A-Za-z0-9_.-]+\/$/;

  const create = (tag, className, value) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined) el.textContent = value;
    return el;
  };
  const safeResource = (repo, file) => {
    if (!allowRepo.test(repo) || !allowPath.test(file) || file.split("/").some(x => x === "." || x === "..")) return null;
    return repo + "/blob/main/" + file.split("/").map(encodeURIComponent).join("/");
  };
  const link = (label, href, className) => {
    const a = create("a", className);
    a.href = href;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.append(create("span", null, label), create("span", null, "↗"));
    return a;
  };
  const formatCount = number => String(number).padStart(2, "0");

  function makeCard(project, index) {
    if (!project || typeof project !== "object" ||
        !allowRepo.test(project.repository) ||
        !allowAccent.test(project.accent_color) ||
        typeof project.name !== "string" || !project.name.trim() ||
        typeof project.summary !== "string" || !project.summary.trim() ||
        !Array.isArray(project.domains) || !project.domains.every(x => typeof x === "string") ||
        typeof project.ontology_path !== "string" ||
        typeof project.gallery_path !== "string") {
      throw new Error("The published catalog contains an invalid project record.");
    }
    const ontology = safeResource(project.repository, project.ontology_path);
    const gallery = safeResource(project.repository, project.gallery_path);
    if (!ontology || !gallery) throw new Error("A catalog resource path is invalid.");
    const website = typeof project.website_url === "string" && allowWebsite.test(project.website_url)
      ? project.website_url : gallery;
    const card = create("article", "project-card");
    card.style.setProperty("--project-accent", project.accent_color);

    const top = create("div", "card-top");
    top.append(create("span", "project-index", "INDEX / " + formatCount(index + 1)),
               create("span", "project-status", "Public project"));

    const art = create("div", "card-art");
    art.setAttribute("aria-hidden", "true");
    const initial = project.name.trim().slice(0, 1).toUpperCase();
    art.append(create("span", "art-corner tl", "TARIUM / MEMBER"),
               create("span", "card-monogram", initial),
               create("span", "art-corner br", formatCount(index + 1)));

    const body = create("div", "card-body");
    body.append(create("div", "card-eyebrow", project.domains[0] || "Independent project"),
                create("h3", null, project.name),
                create("p", "card-summary", project.summary));
    const tags = create("div", "card-tags");
    project.domains.slice(0, 4).forEach(domain => tags.append(create("span", "card-tag", domain)));
    body.append(tags);

    const links = create("div", "card-links");
    links.append(link("View project", project.repository),
                 link(project.website_url && website !== gallery ? "Visit gallery" : "Gallery source", website),
                 link("Ontology", ontology));
    card.append(top, art, body, links);
    return card;
  }

  async function load() {
    try {
      const response = await fetch("./data/projects.json", { cache: "no-store" });
      if (!response.ok) throw new Error("Unable to load the public project registry.");
      const registry = await response.json();
      if (!registry || registry.schema_version !== 2 || !Array.isArray(registry.projects)) {
        throw new Error("The public project registry has an unsupported format.");
      }
      const sorted = registry.projects.slice().sort((a, b) => a.slug.localeCompare(b.slug));
      const fragment = document.createDocumentFragment();
      sorted.forEach((project, index) => fragment.append(makeCard(project, index)));
      list.replaceChildren();
      if (sorted.length) list.append(fragment);
      else list.append(create("p", "catalog-empty", "No projects are currently registered."));
      count.textContent = formatCount(sorted.length);
    } catch (error) {
      list.replaceChildren();
      const panel = create("div", "catalog-error");
      panel.append(create("strong", null, "The project registry is temporarily unavailable."),
                   create("p", null, "Browse the source registry directly on GitHub."));
      const a = create("a", null, "View public registry ↗");
      a.href = "https://github.com/sguzman/tarium/blob/main/registry/projects.json";
      a.target = "_blank"; a.rel = "noopener noreferrer";
      panel.append(a);
      list.append(panel);
      count.textContent = "—";
      console.error("Tarium catalog:", error.message);
    } finally {
      list.setAttribute("aria-busy", "false");
    }
  }
  load();
})();
