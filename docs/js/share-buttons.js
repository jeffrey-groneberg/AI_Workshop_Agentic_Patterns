document.addEventListener("DOMContentLoaded", function () {
  var repoUrl = "https://github.com/jeffreygroneberg/AI_Workshop_Agentic_Patterns";
  var title = document.title || "Agentic AI Design Patterns Workshop";
  var text = "Check out this hands-on workshop on Agentic AI Design Patterns — pure Python, no frameworks!";

  var linkedinHref =
    "https://www.linkedin.com/sharing/share-offsite/?url=" +
    encodeURIComponent(repoUrl);
  var xHref =
    "https://x.com/intent/tweet?text=" +
    encodeURIComponent(text) +
    "&url=" +
    encodeURIComponent(repoUrl);
  var substackHref =
    "https://substack.com/share?url=" +
    encodeURIComponent(repoUrl) +
    "&title=" +
    encodeURIComponent(title);

  var linkedinSvg =
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>';
  var xSvg =
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>';
  var substackSvg =
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24l9.6-5.244 9.6 5.244V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/></svg>';

  var bar = document.createElement("div");
  bar.className = "share-bar";
  bar.innerHTML =
    '<span class="share-bar__label">Share</span>' +
    '<a class="share-bar__btn share-bar__btn--linkedin" href="' + linkedinHref + '" target="_blank" rel="noopener" title="Share on LinkedIn">' + linkedinSvg + "</a>" +
    '<a class="share-bar__btn share-bar__btn--x" href="' + xHref + '" target="_blank" rel="noopener" title="Share on X">' + xSvg + "</a>" +
    '<a class="share-bar__btn share-bar__btn--substack" href="' + substackHref + '" target="_blank" rel="noopener" title="Share on Substack">' + substackSvg + "</a>";

  var content = document.querySelector(".md-content__inner");
  if (content) {
    content.appendChild(bar);
  }
});
