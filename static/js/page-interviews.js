document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("podcastsList");
  if (!container) return;

  // Helper: Fixes standard YT links to Embed links automatically
  function getEmbedUrl(url) {
    if (!url) return null;
    let videoId = "";
    if (url.includes("v=")) videoId = url.split("v=")[1].split("&")[0];
    else if (url.includes("youtu.be/"))
      videoId = url.split("youtu.be/")[1].split("?")[0];
    else if (url.includes("shorts/"))
      videoId = url.split("shorts/")[1].split("?")[0];
    else if (url.includes("embed/")) return url;
    return videoId ? `https://www.youtube.com/embed/${videoId}` : url;
  }

  fetch("/api/content?type=interview&t=" + Date.now())
    .then((r) => r.json())
    .then((data) => {
      if (data.length === 0) {
        container.innerHTML = `<p style="text-align:center; color:var(--muted); padding:40px;">No interviews recorded yet.</p>`;
        return;
      }

      container.innerHTML = data
        .map((n) => {
          const embedUrl = getEmbedUrl(n.video_url);
          const image = n.image || "/static/img/bg.jpg";

          return `
        <div class="podcast-row" style="margin-bottom: 32px; border-bottom: 1px solid var(--line); padding-bottom: 32px;">
          <div style="display: grid; grid-template-columns: 280px 1fr; gap: 30px; align-items: center;">

            <!-- Video/Image Section -->
            <a href="/news/${n.id}" style="display:block; position:relative; border-radius:12px; overflow:hidden; aspect-ratio:16/9; background-image:url('${image}'); background-size:cover; background-position:center;">
               <div style="position:absolute; inset:0; background:rgba(0,0,0,0.2); display:flex; align-items:center; justify-content:center;">
                  <div style="width:50px; height:50px; background:var(--blue); color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:var(--shadow);">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
               </div>
            </a>

            <!-- Info Section -->
            <div class="podcast-info">
              <span class="eyebrow" style="font-size:10px;">Episode ${n.id}</span>
              <h2 style="margin: 8px 0 12px; font-size: 26px;">${n.title}</h2>
              <p style="color: var(--muted); margin-bottom: 16px; line-height: 1.6;">${n.summary}</p>
              <div style="display:flex; align-items:center; gap:12px; font-size:12px; font-weight:700; color:var(--muted); text-transform:uppercase;">
                <span>${n.date}</span>
                <span style="width:4px; height:4px; background:var(--line); border-radius:50%;"></span>
                <a href="/news/${n.id}" style="color:var(--blue);">Watch Interview →</a>
              </div>
            </div>

          </div>
        </div>
        `;
        })
        .join("");
    })
    .catch((err) => console.error("Podcast Fetch Error:", err));
});
