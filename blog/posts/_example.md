<!--
  Reference file, not a real post — not listed in posts.json, so blog.html
  won't show it. It exists to show the Markdown syntax that maps onto the
  .prose styling in blog.css. Copy the syntax below into a real post, not
  this file itself.

  A real post file (blog/posts/your-slug.md) should start directly with
  body content — no top-level "# Title" heading, since the post page
  renders the title from posts.json instead. Use "##" and "###" for
  in-post section headings.
-->

Open with what you were doing when you hit the thing worth writing down,
and what the payoff of reading this is.

## A section heading

Body text. Use `inline code` for identifiers, flags, and file names.

```cpp
float sdSphere(vec3 p, float r) {
  return length(p) - r;
}
```

### A subsection

- Unordered point one.
- Unordered point two.

1. Ordered step one.
2. Ordered step two.

> A quoted note, spec excerpt, or something worth setting apart.

Inline math uses `$...$` or `\(...\)`: partial fractions split
$\frac{1}{x^2 - 1}$ into $\frac{1}{2(x-1)} - \frac{1}{2(x+1)}$. Prefer
`\(...\)` over `$...$` when an expression has multiple underscores
close together (e.g. subscripts like $x_1$, $x_2$) — Markdown's own
emphasis parsing can occasionally misread a lone `$...$` pair before
KaTeX gets to it, and `\(...\)` has no such collision.

Display math uses `$$...$$` or `\[...\]`:

$$
\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

| Approach | Trade-off |
| --- | --- |
| Option A | Faster, less accurate. |
| Option B | Slower, exact. |

---

Close with what you'd do differently next time, if anything.
