"""Build ES documents from SQLAlchemy rows.

Each `build_*_doc(row, translation, lang)` returns either a dict or `None`
when the translation for that language is missing.
"""

from html.parser import HTMLParser


class _StripTags(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def strip_html(value: str | None, max_chars: int = 600) -> str:
    if not value:
        return ""
    parser = _StripTags()
    try:
        parser.feed(value)
    except Exception:
        return value[:max_chars]
    text = " ".join(p.strip() for p in parser.parts if p and p.strip())
    if max_chars and len(text) > max_chars:
        text = text[: max_chars - 1].rstrip() + "…"
    return text


def _iso(dt) -> str | None:
    return dt.isoformat() if dt else None


def build_news_doc(news, tr, lang: str) -> dict | None:
    if not tr:
        return None
    return {
        "id": news.news_id,
        "type": "news",
        "lang": lang,
        "title": tr.title,
        "snippet": strip_html(tr.html_content),
        "url": f"/{lang}/news/{news.news_id}",
        "category_id": news.category_id,
        "created_at": _iso(news.created_at),
        "updated_at": _iso(news.updated_at),
    }


def build_announcement_doc(ann, tr, lang: str) -> dict | None:
    if not tr:
        return None
    return {
        "id": ann.announcement_id,
        "type": "announcement",
        "lang": lang,
        "title": tr.title,
        "snippet": strip_html(tr.html_content),
        "url": f"/{lang}/announcements/{ann.announcement_id}",
        "image": ann.image,
        "created_at": _iso(ann.created_at),
        "updated_at": _iso(ann.updated_at),
    }


def build_project_doc(proj, tr, lang: str) -> dict | None:
    if not tr:
        return None
    return {
        "id": proj.project_id,
        "type": "project",
        "lang": lang,
        "title": tr.title,
        "snippet": strip_html(tr.description) or strip_html(getattr(tr, "html_content", None)),
        "url": f"/{lang}/projects/{proj.project_id}",
        "image": proj.bg_image,
        "created_at": _iso(proj.created_at),
        "updated_at": _iso(proj.updated_at),
    }


def build_collaboration_doc(coll, tr, lang: str) -> dict | None:
    if not tr:
        return None
    return {
        "id": coll.collaboration_id,
        "type": "collaboration",
        "lang": lang,
        "title": tr.name,
        "snippet": coll.website_url or "",
        "url": f"/{lang}/collaborations/{coll.collaboration_id}",
        "image": coll.logo,
        "created_at": _iso(coll.created_at),
        "updated_at": _iso(coll.updated_at),
    }


def build_faculty_doc(faculty, tr, lang: str) -> dict | None:
    if not tr:
        return None
    return {
        "id": faculty.faculty_code,
        "type": "faculty",
        "lang": lang,
        "title": tr.faculty_name,
        "snippet": strip_html(tr.about_text),
        "url": f"/{lang}/faculties/{faculty.faculty_code}",
        "created_at": _iso(faculty.created_at),
        "updated_at": _iso(faculty.updated_at),
    }


def build_cafedra_doc(cafedra, tr, lang: str) -> dict | None:
    if not tr:
        return None
    return {
        "id": cafedra.cafedra_code,
        "type": "cafedra",
        "lang": lang,
        "title": tr.cafedra_name,
        "snippet": strip_html(tr.about_text),
        "url": f"/{lang}/cafedras/{cafedra.cafedra_code}",
        "created_at": _iso(cafedra.created_at),
        "updated_at": _iso(cafedra.updated_at),
    }


def build_department_doc(department, tr, lang: str) -> dict | None:
    if not tr:
        return None
    return {
        "id": department.department_code,
        "type": "department",
        "lang": lang,
        "title": tr.department_name,
        "snippet": strip_html(tr.about_html),
        "url": f"/{lang}/departments/{department.department_code}",
        "created_at": _iso(department.created_at),
        "updated_at": _iso(department.updated_at),
    }


def build_employee_doc(employee, tr, lang: str) -> dict | None:
    if not tr:
        return None
    title = tr.full_name or " ".join(filter(None, [tr.first_name, tr.last_name])).strip()
    if not title:
        return None
    snippet_parts = [
        tr.position,
        tr.academic_degree,
        tr.academic_title,
        strip_html(tr.scientific_interests, max_chars=200),
        strip_html(tr.biography, max_chars=300),
    ]
    snippet = " · ".join(p for p in snippet_parts if p)
    return {
        "id": employee.employee_code,
        "type": "employee",
        "lang": lang,
        "title": title,
        "snippet": snippet,
        "url": f"/{lang}/employees/{employee.employee_code}",
        "image": employee.profile_image,
        "created_at": _iso(employee.created_at),
        "updated_at": _iso(employee.updated_at),
    }


def build_research_institute_doc(institute, tr, lang: str) -> dict | None:
    if not tr:
        return None
    snippet = strip_html(tr.about_html) or strip_html(getattr(tr, "mission_html", None))
    return {
        "id": institute.institute_code,
        "type": "research_institute",
        "lang": lang,
        "title": tr.name,
        "snippet": snippet,
        "url": f"/{lang}/research-institutes/{institute.institute_code}",
        "image": institute.image,
        "created_at": _iso(institute.created_at),
        "updated_at": _iso(institute.updated_at),
    }
