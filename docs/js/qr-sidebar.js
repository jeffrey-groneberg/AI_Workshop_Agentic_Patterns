/* Inject QR code into the left sidebar, below the Home nav link */
document.addEventListener("DOMContentLoaded", function () {
  var sidebar = document.querySelector(".md-sidebar--primary .md-sidebar__inner");
  if (!sidebar) return;

  var nav = sidebar.querySelector(".md-nav--primary");
  if (!nav) return;

  // Resolve site root from the script's own src path
  var scripts = document.querySelectorAll('script[src*="qr-sidebar"]');
  var root = "";
  if (scripts.length) {
    root = scripts[0].src.replace(/js\/qr-sidebar\.js.*$/, "");
  }

  var qr = document.createElement("div");
  qr.className = "sidebar-qr";

  var img = document.createElement("img");
  img.src = root + "img/qr-code.svg";
  img.alt = "QR Code — scan to open this workshop";

  var label = document.createElement("span");
  label.className = "sidebar-qr__label";
  label.textContent = "📱 Scan to open on mobile";

  qr.appendChild(img);
  qr.appendChild(label);

  nav.parentNode.insertBefore(qr, nav.nextSibling);
});
