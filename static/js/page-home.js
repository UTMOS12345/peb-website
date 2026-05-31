(function () {
  const container = document.getElementById("featuredNews");
  if (!container) return;

  fetch("/api/content?type=news&t=" + Date.now())
    .then((res) => res.json())
    .then((dbData) => {
      const staticNews = typeof NEWS !== "undefined" ? NEWS : [];
      const fullList = [...dbData, ...staticNews];
      const featured = fullList.slice(0, 3);

      container.innerHTML = featured
        .map((n) => {
          const image = n.image || "";
          const bgImg = image
            ? `style="background-image:url('${image}'); background-size:cover;"`
            : "";

          return `
          <a href="/news/${n.id}" style="text-decoration:none; color:inherit;">
            <article class="card">
              <div class="card-cover ${image ? "" : "cover-default"}" ${bgImg}>
                <span class="card-cat-tag">${n.category}</span>
              </div>
              <div class="card-body">
                <h3>${n.title}</h3>
                <p>${n.summary || ""}</p>
                <span class="card-link">Read story →</span>
              </div>
            </article>
          </a>
        `;
        })
        .join("");
    })
    .catch((err) => console.error("Home fetch error:", err));
})();
