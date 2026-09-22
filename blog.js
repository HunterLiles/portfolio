(() => {
  "use strict";

  function escapeHtml(value) {
    return String(value).replace(
      /[&<>"']/g,
      (ch) =>
        ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
          ch
        ],
    );
  }

  const dateFormatter = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  });
  async function fetchFile(url, type = "json") {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
    return response[type]();
  }

  function renderMeta(post) {
    return `<time datetime="${escapeHtml(post.date)}">${dateFormatter.format(new Date(`${post.date}T00:00:00Z`))}</time>${
      post.readTime
        ? `<span class="dot" aria-hidden="true">·</span><span>${escapeHtml(post.readTime)}</span>`
        : ""
    }`;
  }

  // blog.html: render the post list from posts.json.
  async function initIndex(list) {
    const status = document.getElementById("writing-status");
    try {
      const posts = await fetchFile("blog/posts.json");
      if (!posts.length) {
        status.textContent = "Nothing published yet. Check back soon.";
        return;
      }
      posts.sort((a, b) => b.date.localeCompare(a.date));
      const cards = posts.map((post) => {
        const article = document.createElement("article");
        article.className = "writing-card";
        article.innerHTML = `
          <p class="writing-meta">${renderMeta(post)}</p>
          <h3><a href="blog/post.html?slug=${encodeURIComponent(post.slug)}">${escapeHtml(post.title)}</a></h3>
          <p class="writing-excerpt">${escapeHtml(post.excerpt || "")}</p>
          ${post.tech ? `<p class="technologies">${escapeHtml(post.tech)}</p>` : ""}
        `;
        return article;
      });
      list.replaceChildren(...cards);
      status.textContent = "";
    } catch (err) {
      console.error("Could not load blog/posts.json", err);
      status.textContent = "Could not load the posts. Please try again later.";
    } finally {
      list.setAttribute("aria-busy", "false");
    }
  }

  // blog/post.html: render one post from its Markdown file + posts.json metadata.
  async function initPost(body) {
    const slug = new URLSearchParams(location.search).get("slug");
    function showError(title, message) {
      document.title = `${title} — Hunter Liles`;
      document.getElementById("post-title").textContent = title;
      document.getElementById("post-meta").textContent = "";
      body.textContent = message;
      body.dataset.state = "error";
    }
    try {
      if (!slug) {
        showError("Post not found", "Choose a post from the blog to continue.");
        return;
      }
      const posts = await fetchFile("posts.json");
      const meta = posts.find((p) => p.slug === slug);
      if (!meta) {
        showError("Post not found", "This post is not listed in the blog.");
        return;
      }
      const markdown = await fetchFile(`posts/${encodeURIComponent(slug)}.md`, "text");
      // Markdown is authored in this repository and may contain trusted HTML.
      body.innerHTML = marked.parse(markdown);
      document.title = `${meta.title} — Hunter Liles`;
      document.getElementById("post-title").textContent = meta.title;
      document.getElementById("post-meta").innerHTML = renderMeta(meta);
      document.querySelector('meta[name="description"]').content =
        meta.excerpt || meta.title;
      body.dataset.state = "ready";
    } catch (err) {
      console.error("Could not load post", err);
      showError("Post unavailable", "Could not load this post. Please try again later.");
    } finally {
      body.setAttribute("aria-busy", "false");
    }
  }

  const list = document.getElementById("writing-list");
  const body = document.getElementById("post-body");
  if (list) initIndex(list);
  if (body) initPost(body);
})();
