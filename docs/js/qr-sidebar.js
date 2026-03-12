/* Inject QR code into the left sidebar, only on the Home page.
   Handles Material theme instant-loading (no full page reloads). */
(function () {
  var qrEl = null;
  var imgSrc = "";

  function isHomePage() {
    var p = window.location.pathname;
    // Match root, /index.html, or /AI_Workshop_Agentic_Patterns/ etc.
    return /\/(index\.html)?$/.test(p);
  }

  function ensureQR() {
    if (!isHomePage()) {
      if (qrEl && qrEl.parentNode) qrEl.parentNode.removeChild(qrEl);
      return;
    }

    var sidebar = document.querySelector(".md-sidebar--primary .md-sidebar__inner");
    if (!sidebar) return;
    var nav = sidebar.querySelector(".md-nav--primary");
    if (!nav) return;

    // Already inserted in the right place
    if (qrEl && qrEl.parentNode === nav.parentNode) return;

    if (!qrEl) {
      // Resolve image path once
      if (!imgSrc) {
        var s = document.querySelector('script[src*="qr-sidebar"]');
        imgSrc = s ? s.src.replace(/js\/qr-sidebar\.js.*$/, "") + "img/qr-code.svg" : "img/qr-code.svg";
      }
      qrEl = document.createElement("div");
      qrEl.className = "sidebar-qr";
      var img = document.createElement("img");
      img.src = imgSrc;
      img.alt = "QR Code — scan to open this workshop";
      var label = document.createElement("span");
      label.className = "sidebar-qr__label";
      label.textContent = "📱 Scan to open on mobile";
      qrEl.appendChild(img);
      qrEl.appendChild(label);
    }

    nav.parentNode.insertBefore(qrEl, nav.nextSibling);
  }

  // Initial load
  document.addEventListener("DOMContentLoaded", ensureQR);

  // Material instant-loading navigation events
  if (typeof document$ !== "undefined") {
    document$.subscribe(ensureQR);
  } else {
    // Fallback: listen for URL changes via popstate + observe for content swaps
    window.addEventListener("popstate", function () { setTimeout(ensureQR, 100); });
    new MutationObserver(function () { setTimeout(ensureQR, 50); })
      .observe(document.body, { childList: true, subtree: true });
  }
})();
