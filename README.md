# Portfolio
My personal portfolio/cv website. This is where I show off my projects and talk about myself. It is a one page layout for all major information. It features a 3D wireframe renderer written in JS from a video by Tsoding.

The languages used are just HTML, CSS, and JavaScript.

## Blog

`blog.html` lists short technical write-ups; `blog/post.html` renders one.
Posts are plain Markdown files, rendered client-side ([marked.js](https://github.com/markedjs/marked) via CDN) — no conversion or build step.

To add a post:

1. Write it as `blog/posts/your-slug.md`. Start directly with body content — no top-level `# Title`, since the post page takes its title from `posts.json`. See `blog/posts/_example.md` for the supported syntax (headings, code fences, lists, blockquotes, tables).
2. Add an entry to `blog/posts.json`:
   ```json
   { "slug": "your-slug", "title": "...", "date": "YYYY-MM-DD", "readTime": "5 min read", "excerpt": "...", "tech": "C++ / OpenGL" }
   ```
   `slug`, `title`, and a valid `date` are required; `readTime`, `excerpt`, and `tech` are optional. Slugs must be unique lowercase words or numbers separated by hyphens and match the Markdown filename.

Only posts listed in `posts.json` are rendered by the post page. Unlisted files are still publicly accessible on the static host, so keep private drafts outside the published directory. Markdown may include raw HTML; only publish content you trust. Image and link paths resolve relative to `blog/post.html` (for example, `../assets/images/example.webp`).

The blog requires JavaScript. Post titles and descriptions are set after loading, so social preview crawlers that do not run JavaScript will see generic metadata. Use generated static post pages if per-post social previews become a requirement.

Both pages fetch `posts.json` and the post's `.md` file at load time, so they need to be served over `http(s)://`, not opened as a `file://` URL — browsers block `fetch()` on local files. Run `python3 -m http.server` (or any static server) in the project root to preview locally; it works as-is once deployed to any static host.
