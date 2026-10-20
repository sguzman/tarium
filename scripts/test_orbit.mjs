import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";
import { test } from "node:test";

// A small browser-shaped DOM tests generated link behavior without a network or dependencies.
class Element {
  constructor(tag) {
    this.tag = tag;
    this.children = [];
    this.attributes = {};
    this.styles = {};
    this.style = { setProperty: (name, value) => { this.styles[name] = value; } };
    this.textContent = "";
  }
  setAttribute(name, value) { this.attributes[name] = value; }
  append(...children) {
    for (const child of children) {
      if (child.tag === "#fragment") this.children.push(...child.children);
      else this.children.push(child);
    }
  }
  replaceChildren(...children) { this.children = []; this.append(...children); }
}
const source = readFileSync(new URL("../site/app.js", import.meta.url), "utf8");
const domain = "https://github.com/example/project";

async function render(projects) {
  const els = new Map([
    ["project-list", new Element("div")],
    ["project-count", new Element("strong")],
    ["orbit-projects", new Element("div")],
  ]);
  const document = {
    getElementById: id => els.get(id),
    createElement: tag => new Element(tag),
    createDocumentFragment: () => new Element("#fragment"),
  };
  runInNewContext(source, {
    document,
    fetch: async () => ({ ok: true, json: async () => ({ schema_version: 2, projects }) }),
    console,
    encodeURIComponent,
  });
  // The app makes two asynchronous awaits to fetch and parse the registry.
  await new Promise(resolve => setImmediate(resolve));
  return els;
}
function project(name, options = {}) {
  return {
    slug: name.toLowerCase().replaceAll(" ", "-"),
    name,
    summary: "Public demonstration project for behavior tests.",
    repository: domain,
    domains: ["research"],
    ontology_path: "ontology/components.json",
    gallery_path: "site/index.html",
    accent_color: "#B9905D",
    ...options,
  };
}
test("registered projects receive a colored, accessible orbiting link to their website", async () => {
  const els = await render([
    project("Atlas A", {website_url:"https://example.github.io/atlas-a/"}),
    project("Atlas B", {website_url:"https://example.github.io/atlas-b/",accent_color:"#77AA99"}),
  ]);
  const orbits = els.get("orbit-projects").children;
  assert.equal(orbits.length, 2);
  const first = orbits[0];
  const anchor = first.children[0];
  assert.match(first.className, /orbit-project-track/);
  assert.equal(anchor.href, "https://example.github.io/atlas-a/");
  assert.equal(anchor.attributes["aria-label"], "Visit Atlas A website");
  assert.equal(anchor.title, undefined, "Avoid a duplicate native tooltip");
  assert.equal(anchor.styles["--planet-accent"], "#B9905D");
  assert.equal(anchor.children[0].children[1].textContent, "Atlas A");
  assert.ok(first.styles["--orbit-offset"].endsWith("s"));
  assert.equal(orbits[1].children[0].href, "https://example.github.io/atlas-b/");
  assert.equal(els.get("project-count").textContent, "02");
});
test("without a project website, orbit links to the public gallery source", async () => {
  const els = await render([project("Atlas C")]);
  assert.equal(els.get("orbit-projects").children[0].children[0].href,
               domain + "/blob/main/site/index.html");
});
test("a registry failure does not leave links to unknown projects", async () => {
  const els = await render([project("Not Valid", {accent_color:"invalid"})]);
  assert.equal(els.get("orbit-projects").children.length, 0);
  assert.equal(els.get("project-count").textContent, "—");
});
test("hover and focus pause both rotating track and counter-rotating label", () => {
  const css = readFileSync(new URL("../site/styles.css", import.meta.url), "utf8");
  assert.match(css, /\.orbit-project-track:hover[^}]*animation-play-state:paused/s);
  assert.match(css, /\.orbit-project-track:focus-within[^}]*animation-play-state:paused/s);
  assert.match(css, /@keyframes orbit-counterturn/);
  assert.match(css, /prefers-reduced-motion:reduce/);
  assert.match(css, /\\.orbit-project-name\\s*\\{[^}]*visibility:hidden;opacity:0/s);
  assert.match(css, /\\.orbit-project-link:hover \\.orbit-project-name,[\\s\\S]*?visibility:visible;opacity:1/);
  assert.match(css, /\\.orbit-project-link:focus-visible \\.orbit-project-name/);
  assert.match(css, /\\.orbit-project-face\\s*\\{[^}]*width:36px;height:36px/s);
  assert.doesNotMatch(css, /\\.orbit-project-face\\s*\\{[^}]*max-width:210px/s);
});
