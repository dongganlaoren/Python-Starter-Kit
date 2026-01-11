// /app/static/js/common.js

(function () {
  "use strict";

  const toggleBtn = document.getElementById("sidebarCollapse");
  const sidebar = document.getElementById("sidebar");

  if (!toggleBtn || !sidebar) return;

  toggleBtn.addEventListener("click", function () {
    const active = sidebar.classList.toggle("active");
    toggleBtn.setAttribute("aria-expanded", String(active));
  });
})();

