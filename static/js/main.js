/* OpsBoard – main.js */

/* ── Theme ────────────────────────────────────────────────── */
/* Note: initial theme is applied in <head> of base.html to avoid FOUC */

function toggleTheme() {
  var root = document.documentElement;
  var current = root.getAttribute("data-theme");
  var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  var next;
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
  var sidebar = document.getElementById("main-sidebar");
  var overlay = document.getElementById("sidebar-overlay");
  if (!sidebar) return;
  var isWide = window.innerWidth >= 1024;
  if (isWide) {
    sidebar.classList.toggle("collapsed");
    var wrapper = document.getElementById("main-wrapper");
    if (wrapper) {
      if (sidebar.classList.contains("collapsed")) {
        wrapper.style.marginLeft = "var(--sidebar-collapsed-width)";
      } else {
        wrapper.style.marginLeft = "var(--sidebar-width)";
      }
    }
  } else {
    var isOpen = sidebar.classList.toggle("mobile-open");
    if (overlay) {
      if (isOpen) {
        overlay.classList.add("active");
      } else {
        overlay.classList.remove("active");
      }
    }
  }
}

function closeMobileSidebar() {
  var sidebar = document.getElementById("main-sidebar");
  var overlay = document.getElementById("sidebar-overlay");
  if (sidebar) sidebar.classList.remove("mobile-open");
  if (overlay) overlay.classList.remove("active");
}

/* Mark active nav link */
(function () {
  var links = document.querySelectorAll(".sidebar__link");
  links.forEach(function (link) {
    if (link.getAttribute("href") === window.location.pathname) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });
}());

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
