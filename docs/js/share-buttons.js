document.addEventListener("DOMContentLoaded", function () {
  var repoUrl = "https://github.com/jeffreygroneberg/AI_Workshop_Agentic_Patterns";
  var title = "Agentic AI Design Patterns Workshop";
  var text = "Check out this hands-on workshop on Agentic AI Design Patterns — pure Python, no frameworks!";

  var links = [
    {
      name: "LinkedIn",
      href: "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(repoUrl),
      svg: '<svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
    },
    {
      name: "X",
      href: "https://x.com/intent/tweet?text=" + encodeURIComponent(text) + "&url=" + encodeURIComponent(repoUrl),
      svg: '<svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>'
    },
    {
      name: "Substack",
      href: "https://substack.com/share?url=" + encodeURIComponent(repoUrl) + "&title=" + encodeURIComponent(title),
      svg: '<svg viewBox="0 0 24 24"><path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24l9.6-5.244 9.6 5.244V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/></svg>'
    },
    {
      name: "Reddit",
      href: "https://www.reddit.com/submit?url=" + encodeURIComponent(repoUrl) + "&title=" + encodeURIComponent(title),
      svg: '<svg viewBox="0 0 24 24"><path d="M12 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 12 0 0012 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 01-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 01.042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 014.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 01.14-.197.35.35 0 01.238-.042l2.906.617a1.214 1.214 0 011.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 00-.231.094.33.33 0 000 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 000-.463.327.327 0 00-.462 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 00-.205-.094z"/></svg>'
    },
    {
      name: "Hacker News",
      href: "https://news.ycombinator.com/submitlink?u=" + encodeURIComponent(repoUrl) + "&t=" + encodeURIComponent(title),
      svg: '<svg viewBox="0 0 24 24"><path d="M0 24V0h24v24H0zM6.951 5.896l4.112 7.708v5.064h1.583v-4.972l4.148-7.799h-1.749l-2.457 4.875c-.372.745-.688 1.434-.688 1.434s-.297-.708-.651-1.434L8.831 5.896H6.951z"/></svg>'
    }
  ];

  var container = document.createElement("div");
  container.className = "share-header";

  links.forEach(function (link) {
    var a = document.createElement("a");
    a.className = "share-header__btn";
    a.href = link.href;
    a.target = "_blank";
    a.rel = "noopener";
    a.title = "Share on " + link.name;
    a.innerHTML = link.svg;
    container.appendChild(a);
  });

  // Insert into the header, before the repo/source link
  var header = document.querySelector(".md-header__inner");
  var source = document.querySelector(".md-header__source");
  if (header && source) {
    header.insertBefore(container, source);
  } else if (header) {
    header.appendChild(container);
  }
});
