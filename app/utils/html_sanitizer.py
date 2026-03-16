import bleach

# Tags permitted in user-supplied HTML content (CMS rich text)
ALLOWED_TAGS = [
    "p", "br", "strong", "em", "b", "i", "u", "s",
    "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "blockquote", "code", "pre", "hr",
    "a", "img",
    "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    "span", "div", "section", "article",
    "figure", "figcaption",
]

ALLOWED_ATTRS: dict = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "width", "height", "loading"],
    "th": ["colspan", "rowspan", "scope"],
    "td": ["colspan", "rowspan"],
    "*": ["class", "id", "style"],
}

# Styles that are safe to allow inline (limit to presentation-only)
ALLOWED_STYLES = [
    "color", "background-color", "font-size", "font-weight", "font-style",
    "text-align", "text-decoration", "margin", "padding",
    "width", "height", "max-width",
]


def sanitize_html(raw_html: str | None) -> str:
    """
    Sanitize user-supplied HTML to prevent XSS.
    Strips disallowed tags and dangerous attributes while preserving rich formatting.
    """
    if not raw_html:
        return ""
    return bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
        strip_comments=True,
    )
