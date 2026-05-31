document.addEventListener("DOMContentLoaded", function () {
  const grid = document.getElementById("newsGrid");
  const loadingMsg = document.getElementById("loading-msg");
  if (!grid) return;

  function renderCards(list) {
    if (list.length === 0) {
      grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;padding:50px;color:var(--muted);">No news updates available.</p>`;
      return;
    }
    grid.innerHTML = list
      .map((n) => {
        const image = n.image || "";
        const bgImg = image
          ? `style="background-image:url('${image}');background-size:cover;background-position:center;"`
          : "";

        return `
        <a href="/news/${n.id}" style="text-decoration:none;color:inherit;display:block;">
          <article class="card">
            <div class="card-cover ${image ? "" : "cover-default"}" ${bgImg}>
              <!-- Fixed: News items always show 'NEWS' tag for consistency -->
              <span class="card-cat-tag">NEWS</span>
              <span class="card-new-badge">Latest</span>
            </div>
            <div class="card-body">
              <div class="card-meta"><span>${n.date}</span></div>
              <h3>${n.title}</h3>
              <p>${n.summary}</p>
              <span class="card-link">Read Story →</span>
            </div>
          </article>
        </a>`;
      })
      .join("");
  }

  fetch("/api/content?type=news&t=" + Date.now())
    .then((r) => r.json())
    .then((dbData) => {
      if (loadingMsg) loadingMsg.remove();
      renderCards(dbData);
    })
    .catch(() => {
      if (loadingMsg) loadingMsg.innerHTML = "Unable to load newsroom.";
    });
});
