document.addEventListener("DOMContentLoaded", function () {
  const grids = {
    politics: document.getElementById("grid-politics"),
    economics: document.getElementById("grid-economics"),
    business: document.getElementById("grid-business"),
  };

  function renderToGrid(grid, list) {
    if (!grid) return;
    if (list.length === 0) {
      grid.innerHTML = `<p style="color:var(--muted); font-size:14px; padding: 20px;">No articles in this desk yet.</p>`;
      return;
    }

    grid.innerHTML = list
      .map((n) => {
        // Logic for the image
        const image = n.image || "";
        const bgImg = image
          ? `style="background-image:url('${image}'); background-size:cover; background-position:center;"`
          : "";

        return `
      <a href="/news/${n.id}" style="text-decoration:none; color:inherit; display:block; margin-bottom:20px;">
        <article class="card card--article">
          <!-- Added: Card Cover for images -->
          ${
            image
              ? `
          <div class="card-cover" ${bgImg}>
            <span class="card-cat-tag">${n.category}</span>
          </div>`
              : ""
          }

          <div class="card-body">
            <div class="card-meta">
                <span>${n.date}</span>
                <span class="dot"></span>
                <span>${n.author || "PEB Staff"}</span>
            </div>
            <h3 style="font-size:22px; margin:12px 0;">${n.title}</h3>
            <p>${n.summary}</p>
            <div class="card-author" style="margin-top:15px; padding-top:15px; border-top:1px solid var(--line); font-size:12px; color:var(--blue); font-weight:600; text-transform:uppercase;">
                Read Full Analysis →
            </div>
          </div>
        </article>
      </a>
    `;
      })
      .join("");
  }

  // Fetch only posts of type 'article'
  fetch("/api/content?type=article&t=" + Date.now())
    .then((r) => r.json())
    .then((data) => {
      console.log("Articles loaded:", data); // Debugging

      // Sort and render into separate category grids
      if (grids.politics)
        renderToGrid(
          grids.politics,
          data.filter((a) => a.category === "politics"),
        );
      if (grids.economics)
        renderToGrid(
          grids.economics,
          data.filter((a) => a.category === "economics"),
        );
      if (grids.business)
        renderToGrid(
          grids.business,
          data.filter((a) => a.category === "business"),
        );
    })
    .catch((err) => console.error("Articles Load Error:", err));
});
