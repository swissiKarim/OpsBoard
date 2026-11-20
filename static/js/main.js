/* OpsBoard – main.js */

/* ── Theme ────────────────────────────────────────────────── */
(function () {
  const stored = localStorage.getItem("opsboard-theme");
  if (stored === "dark" || stored === "light") {
    document.documentElement.setAttribute("data-theme", stored);
  }
})();

function toggleTheme() {
  const root = document.documentElement;
  const current = root.getAttribute("data-theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  let next;
  if (current === "dark") {
    next = "light";
  } else if (current === "light") {
    next = "dark";
  } else {
    next = prefersDark ? "light" : "dark";
  }
  root.setAttribute("data-theme", next);
  localStorage.setItem("opsboard-theme", next);
}

/* ── Sidebar ──────────────────────────────────────────────── */
function toggleSidebar() {
  const sidebar = document.querySelector(".sidebar");
  if (!sidebar) return;
  const isWide = window.innerWidth >= 1024;
  if (isWide) {
    sidebar.classList.toggle("collapsed");
  } else {
    sidebar.classList.toggle("mobile-open");
  }
}

/* Mark active nav link */
(function () {
  const links = document.querySelectorAll(".sidebar__link");
  links.forEach(function (link) {
    if (link.getAttribute("href") === window.location.pathname) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });
})();

/* ── Toast ────────────────────────────────────────────────── */
function showToast(message, duration) {
  duration = duration || 3000;
  var container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  var toast = document.createElement("div");
  toast.className = "toast";
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "polite");
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(function () {
    toast.remove();
  }, duration);
}

/* ── Dialog helpers ───────────────────────────────────────── */
function openDialog(id) {
  var dialog = document.getElementById(id);
  if (!dialog) return;
  dialog.setAttribute("open", "");
  dialog.setAttribute("aria-modal", "true");
  // Trap focus
  var focusable = dialog.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  if (focusable.length) focusable[0].focus();
  document.addEventListener("keydown", function handleEsc(e) {
    if (e.key === "Escape") {
      closeDialog(id);
      document.removeEventListener("keydown", handleEsc);
    }
  });
}

function closeDialog(id) {
  var dialog = document.getElementById(id);
  if (!dialog) return;
  dialog.removeAttribute("open");
}
