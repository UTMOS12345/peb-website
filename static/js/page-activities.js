/* page-activities.js — renders Latest Activities feed at the bottom of activities.html */
(function () {
  const grid = document.getElementById("activityPostsGrid");
  if (!grid || typeof ACTIVITY_POSTS === "undefined") return;

  grid.innerHTML = ACTIVITY_POSTS.map(p => `
    <article class="card" data-activity-post="${p.id}">
      <div class="card-cover cover-${p.cover}">
        <span class="card-cat-tag">${p.category}</span>
      </div>
      <div class="card-body">
        <div class="card-meta"><span>${p.date}</span><span class="dot"></span><span>${p.readTime}</span></div>
        <h3>${p.title}</h3>
        <p>${p.excerpt}</p>
        <span class="card-link">Read post →</span>
      </div>
    </article>
  `).join("");

  grid.querySelectorAll("[data-activity-post]").forEach(card => {
    card.addEventListener("click", () => {
      const item = ACTIVITY_POSTS.find(p => p.id === card.dataset.activityPost);
      if (item && window.PEBModal) window.PEBModal.openActivityPost(item);
    });
  });
})();
