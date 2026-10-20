"use strict";
(() => {
  const key = "tarium:theme-mode";
  const modes = new Set(["system", "light", "dark"]);
  let mode = "system";
  try {
    const saved = localStorage.getItem(key);
    if (modes.has(saved)) mode = saved;
  } catch {
    // Theme preference persistence is optional; the site must still work.
  }

  const system = typeof window.matchMedia === "function"
    ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  const root = document.documentElement;

  const apply = () => {
    const dark = mode === "dark" || (mode === "system" && Boolean(system && system.matches));
    root.setAttribute("data-theme", dark ? "dark" : "light");
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", dark ? "#10191c" : "#f3f1eb");
    const select = document.getElementById("theme-mode");
    if (select) select.value = mode;
  };
  // Runs in the document head, ahead of the CSS and initial render.
  apply();

  const onSystemChange = () => {
    if (mode === "system") apply();
  };
  if (system) {
    if (typeof system.addEventListener === "function") system.addEventListener("change", onSystemChange);
    else if (typeof system.addListener === "function") system.addListener(onSystemChange);
  }

  document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("theme-mode");
    if (!select) return;
    select.value = mode;
    select.addEventListener("change", () => {
      if (!modes.has(select.value)) return;
      mode = select.value;
      try {
        if (mode === "system") localStorage.removeItem(key);
        else localStorage.setItem(key, mode);
      } catch {
        // Continue using the selected theme for this visit.
      }
      apply();
    });
  });
})();
