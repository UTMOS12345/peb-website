/* page-contact.js — handles contact form submission (frontend-only) */
(function () {
  const form = document.getElementById("contactForm");
  if (!form) return;

  form.addEventListener("submit", e => {
    e.preventDefault();
    const name  = document.getElementById("cf-name").value.trim();
    const email = document.getElementById("cf-email").value.trim();
    const msg   = document.getElementById("cf-msg").value.trim();
    if (!name || !email || !msg) return;

    const success = document.getElementById("formSuccess");
    success.classList.add("show");
    form.reset();
    setTimeout(() => success.classList.remove("show"), 5000);
  });
})();
