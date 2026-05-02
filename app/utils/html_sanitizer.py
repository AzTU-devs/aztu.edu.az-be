import bleach

try:
    from bleach.css_sanitizer import CSSSanitizer
    _HAS_CSS_SANITIZER = True
except ImportError:  # bleach < 6 fallback
    CSSSanitizer = None
    _HAS_CSS_SANITIZER = False

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
    # Class is needed for CMS theming, style for inline formatting (filtered by CSSSanitizer below).
    # `id` is intentionally excluded — user-supplied IDs can clobber DOM globals
    # and enable DOM clobbering attacks.
    "*": ["class", "style"],
}

# CSS properties that survive sanitization. Anything else is stripped.
ALLOWED_CSS_PROPERTIES = [
    "color", "background-color", "font-size", "font-weight", "font-style",
    "text-align", "text-decoration", "margin", "padding",
    "width", "height", "max-width",
]

# Only allow http/https/mailto links — bleach default already blocks
# javascript:, data:, file:, etc., but we make it explicit.
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

_css_sanitizer = (
    CSSSanitizer(allowed_css_properties=ALLOWED_CSS_PROPERTIES)
    if _HAS_CSS_SANITIZER
    else None
)


def sanitize_html(raw_html: str | None) -> str:
    """
    Sanitize user-supplied HTML to prevent XSS.
    Strips disallowed tags, dangerous attributes, and unsafe CSS while
    preserving rich text formatting.
    """
    if not raw_html:
        return ""
    kwargs: dict = {
        "tags": ALLOWED_TAGS,
        "attributes": ALLOWED_ATTRS,
        "protocols": ALLOWED_PROTOCOLS,
        "strip": True,
        "strip_comments": True,
    }
    if _css_sanitizer is not None:
        kwargs["css_sanitizer"] = _css_sanitizer
    return bleach.clean(raw_html, **kwargs)
