// Posts remain readable without JavaScript; this only enhances math notation.
(() => {
  const body = document.getElementById("post-body");
  if (!body || typeof renderMathInElement !== "function") return;
  renderMathInElement(body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\[", right: "\\]", display: true },
      { left: "$", right: "$", display: false },
      { left: "\\(", right: "\\)", display: false },
    ],
  });
})();
