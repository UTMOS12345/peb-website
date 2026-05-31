/* =========================================================
   PEB Union — Layout JS
   Runs on every page. Handles:
   - Active nav link highlighting (based on current filename)
   - Mobile nav toggle
   - Mobile dropdown click-to-open
   - Footer year
   ========================================================= */

(function () {
  // -------- Footer year --------
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // -------- Active link highlighting --------
  // Determine current page from the filename (e.g. "news.html" → "news")
  const path = location.pathname.split("/").pop() || "index.html";

  // Map filename → top-level nav route key (matches data-route attrs in nav)
  const pageToRoute = {
    "index.html": "home",
    "":           "home",
    "about.html":  "about",
    "staff.html":  "about",
    "charter.html": "about",
    "news.html":   "news",
    "activities.html":          "activities",
    "mun.html":                 "activities",
    "peer-support.html":        "activities",
    "market-simulation.html":   "activities",
    "interviews.html": "interviews",
    "articles.html":   "articles",
    "contact.html":    "contact",
  };
  const currentRoute = pageToRoute[path] || "";

  document.querySelectorAll("[data-route]").forEach(a => {
    if (a.getAttribute("data-route") === currentRoute) {
      a.classList.add("active");
    }
  });

  // -------- Mobile nav toggle --------
  const navToggle = document.getElementById("navToggle");
  const navLinks  = document.getElementById("navLinks");

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      const open = navLinks.classList.toggle("open");
      navToggle.classList.toggle("open", open);
      navToggle.setAttribute("aria-expanded", String(open));
    });
  }

  // -------- Mobile dropdown click-to-open --------
  document.querySelectorAll(".nav-dropdown > a").forEach(link => {
    link.addEventListener("click", e => {
      if (window.innerWidth <= 720) {
        e.preventDefault();
        link.parentElement.classList.toggle("open");
      }
    });
  });
})();
