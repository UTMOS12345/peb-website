document.addEventListener("DOMContentLoaded", function () {
  const grid = document.getElementById("staffGrid");
  if (!grid) return;

  // Added Cache-busting to ensure new positions show up immediately
  fetch("/api/staff?t=" + Date.now())
    .then((res) => res.json())
    .then((data) => {
      grid.innerHTML = data
        .map((m) => {
          // 1. Get the position from the database (default to 'center' if empty)
          // 2. We use background-position to "point" the crop
          const position = m.image_position || "center";

          const photoHtml = m.image
            ? `<div class="staff-photo" style="background-image: url('${m.image}'); background-size: cover; background-position: ${position} center;"></div>`
            : `<div class="staff-photo staff-photo--placeholder">${m.initial}</div>`;

          return `
                <div class="staff-card">
                    ${photoHtml}
                    <div class="staff-info">
                        <span class="eyebrow" style="font-size: 9px; margin-bottom: 5px;">${m.dept}</span>
                        <h3 class="staff-name">${m.name}</h3>
                        <p class="staff-role">${m.role}</p>
                    </div>
                </div>
                `;
        })
        .join("");
    })
    .catch((err) => console.error("Error loading staff:", err));
});
