"""Route → permission map. One file, one entry per route.

Keyed on ``(method, route.path)`` — the *template* resolved by the router, not the
handler function name (handler names collide across faculty/cafedra/department).
Because the key is the resolved path, routes gated by a router-level
``dependencies=[Depends(require_admin)]`` need no special handling.

Rules of the road:
  * Every mutating route (anything not GET/HEAD/OPTIONS) MUST have an entry.
    ``verify_permission_map(app)`` refuses to boot otherwise, so drift is impossible.
  * Absence is never "public". A deliberately open route is an explicit ``PUBLIC``
    line, which is reviewable; an omission is a boot failure.
  * GET routes are optional here. Map one only when it needs a permission
    (`chatbot_knowledge.read`, `search.admin.read`) or an actor (`AUTHENTICATED`).
  * ``label_fields`` names *form* fields only. The request body is never read
    (see plan §4.4), so JSON-body routes carry no label fields — their labels come
    from the tier-2 target resolvers instead.
"""

import logging
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

try:  # py3.8+
    from typing import Literal
except ImportError:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore

from app.core.permissions import PERMISSION_KEYS

logger = logging.getLogger(__name__)

_SKIP_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
_SKIP_PATHS = frozenset({
    "/", "/health", "/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc",
})


@dataclass(frozen=True)
class RouteRule:
    key: Optional[str] = None
    public: bool = False
    authenticated_only: bool = False
    target_type: Optional[str] = None
    target_param: Optional[str] = None
    target_source: Literal["path", "query"] = "path"
    label_fields: Tuple[str, ...] = ()
    audit_key: Optional[str] = None       # audit action_key when there is no permission key
    no_audit: bool = False                # excluded from the activity log entirely

    @property
    def action_key(self) -> Optional[str]:
        return self.key or self.audit_key

    @property
    def domain(self) -> Optional[str]:
        action_key = self.action_key
        return action_key.partition(".")[0] if action_key else None


PUBLIC = RouteRule(None, public=True)
AUTHENTICATED = RouteRule(None, authenticated_only=True)


ROUTE_PERMISSIONS: Dict[Tuple[str, str], RouteRule] = {
    # ── auth — the only routes with no token, all four deliberate ───────────
    ("POST", "/api/auth/login"): RouteRule(None, public=True, audit_key="auth.login"),
    ("POST", "/api/auth/refresh"): RouteRule(None, public=True, no_audit=True),
    ("POST", "/api/auth/logout"): RouteRule(None, public=True, audit_key="auth.logout"),
    ("GET", "/api/auth/me"): AUTHENTICATED,
    # Self-service: every admin may change their OWN password, whatever their role.
    ("POST", "/api/auth/change-password"): RouteRule(
        None, authenticated_only=True, audit_key="auth.password_changed"
    ),
    ("POST", "/api/chat/message"): RouteRule(None, public=True, no_audit=True),
    # Visitor tracking fires on every public page view: no auth (the site has
    # none) and no audit row, which would otherwise drown the activity log.
    ("POST", "/api/visits/track"): RouteRule(None, public=True, no_audit=True),

    # ── news ───────────────────────────────────────────────────────────────
    ("POST", "/api/news/create"): RouteRule("news.create", target_type="news", label_fields=("az_title",)),
    ("PATCH", "/api/news/{news_id}"): RouteRule("news.update", target_type="news", target_param="news_id"),
    ("DELETE", "/api/news/{news_id}/delete"): RouteRule("news.delete", target_type="news", target_param="news_id"),
    ("POST", "/api/news/activate"): RouteRule("news.activate", target_type="news", target_param="news_id", target_source="query"),
    ("POST", "/api/news/deactivate"): RouteRule("news.deactivate", target_type="news", target_param="news_id", target_source="query"),
    ("POST", "/api/news/reorder"): RouteRule("news.reorder"),

    # ── news categories ────────────────────────────────────────────────────
    ("POST", "/api/news-category/create"): RouteRule("news_categories.create", target_type="news_category", label_fields=("az_title",)),
    ("PATCH", "/api/news-category/{category_id}"): RouteRule("news_categories.update", target_type="news_category", target_param="category_id", label_fields=("az_title",)),
    ("DELETE", "/api/news-category/{category_id}/delete"): RouteRule("news_categories.delete", target_type="news_category", target_param="category_id"),

    # ── announcements ──────────────────────────────────────────────────────
    ("POST", "/api/announcement/create"): RouteRule("announcements.create", target_type="announcement", label_fields=("az_title",)),
    ("PATCH", "/api/announcement/{announcement_id}"): RouteRule("announcements.update", target_type="announcement", target_param="announcement_id"),
    ("DELETE", "/api/announcement/{announcement_id}/delete"): RouteRule("announcements.delete", target_type="announcement", target_param="announcement_id"),
    ("POST", "/api/announcement/activate"): RouteRule("announcements.activate", target_type="announcement", target_param="announcement_id", target_source="query"),
    ("POST", "/api/announcement/deactivate"): RouteRule("announcements.deactivate", target_type="announcement", target_param="announcement_id", target_source="query"),
    ("POST", "/api/announcement/reorder"): RouteRule("announcements.reorder"),
    ("POST", "/api/announcement/upload-file"): RouteRule("announcements.upload_file"),

    # ── hero ───────────────────────────────────────────────────────────────
    ("POST", "/api/hero/create"): RouteRule("hero.create", target_type="hero"),
    ("PUT", "/api/hero/{hero_id}/update"): RouteRule("hero.update", target_type="hero", target_param="hero_id"),
    ("DELETE", "/api/hero/{hero_id}/delete"): RouteRule("hero.delete", target_type="hero", target_param="hero_id"),
    ("POST", "/api/hero/activate"): RouteRule("hero.activate", target_type="hero", target_param="hero_id", target_source="query"),
    ("POST", "/api/hero/deactivate"): RouteRule("hero.deactivate", target_type="hero", target_param="hero_id", target_source="query"),

    # ── projects ───────────────────────────────────────────────────────────
    ("POST", "/api/project/create"): RouteRule("projects.create", target_type="project", label_fields=("az_title",)),
    ("DELETE", "/api/project/{project_id}/delete"): RouteRule("projects.delete", target_type="project", target_param="project_id"),
    ("POST", "/api/project/reorder"): RouteRule("projects.reorder"),

    # ── collaborations ─────────────────────────────────────────────────────
    ("POST", "/api/collaboration/create"): RouteRule("collaborations.create", target_type="collaboration", label_fields=("az_name",)),
    ("PUT", "/api/collaboration/{collaboration_id}/update"): RouteRule("collaborations.update", target_type="collaboration", target_param="collaboration_id", label_fields=("az_name",)),
    ("DELETE", "/api/collaboration/{collaboration_id}/delete"): RouteRule("collaborations.delete", target_type="collaboration", target_param="collaboration_id"),
    ("POST", "/api/collaboration/reorder"): RouteRule("collaborations.reorder"),

    # ── employees ──────────────────────────────────────────────────────────
    ("POST", "/api/employee/create"): RouteRule("employees.create", target_type="employee", label_fields=("first_name_az", "last_name_az")),
    ("PUT", "/api/employee/{employee_code}"): RouteRule("employees.update", target_type="employee", target_param="employee_code", label_fields=("first_name_az", "last_name_az")),
    ("DELETE", "/api/employee/{employee_code}"): RouteRule("employees.delete", target_type="employee", target_param="employee_code"),

    # ── faculties ──────────────────────────────────────────────────────────
    ("POST", "/api/faculty/create"): RouteRule("faculties.create", target_type="faculty"),
    ("PATCH", "/api/faculty/{faculty_code}"): RouteRule("faculties.update", target_type="faculty", target_param="faculty_code"),
    ("DELETE", "/api/faculty/{faculty_code}"): RouteRule("faculties.delete", target_type="faculty", target_param="faculty_code"),
    ("PUT", "/api/faculty/{faculty_code}/director/image"): RouteRule("faculties.director.upload_image", target_type="faculty", target_param="faculty_code"),
    ("POST", "/api/faculty/{faculty_code}/workers"): RouteRule("faculties.worker.create", target_type="faculty", target_param="faculty_code"),
    ("PUT", "/api/faculty/workers/{worker_id}"): RouteRule("faculties.worker.update", target_type="faculty_worker", target_param="worker_id"),
    ("DELETE", "/api/faculty/workers/{worker_id}"): RouteRule("faculties.worker.delete", target_type="faculty_worker", target_param="worker_id"),
    ("PUT", "/api/faculty/workers/{worker_id}/image"): RouteRule("faculties.worker.upload_image", target_type="faculty_worker", target_param="worker_id"),
    ("POST", "/api/faculty/{faculty_code}/deputy-deans"): RouteRule("faculties.deputy_dean.create", target_type="faculty", target_param="faculty_code"),
    ("PUT", "/api/faculty/deputy-deans/{deputy_dean_id}"): RouteRule("faculties.deputy_dean.update", target_type="faculty_deputy_dean", target_param="deputy_dean_id"),
    ("DELETE", "/api/faculty/deputy-deans/{deputy_dean_id}"): RouteRule("faculties.deputy_dean.delete", target_type="faculty_deputy_dean", target_param="deputy_dean_id"),
    ("PUT", "/api/faculty/deputy-deans/{deputy_dean_id}/image"): RouteRule("faculties.deputy_dean.upload_image", target_type="faculty_deputy_dean", target_param="deputy_dean_id"),
    ("POST", "/api/faculty/{faculty_code}/scientific-council"): RouteRule("faculties.scientific_council.create", target_type="faculty", target_param="faculty_code"),
    ("PUT", "/api/faculty/scientific-council/{member_id}"): RouteRule("faculties.scientific_council.update", target_type="faculty_council_member", target_param="member_id"),
    ("DELETE", "/api/faculty/scientific-council/{member_id}"): RouteRule("faculties.scientific_council.delete", target_type="faculty_council_member", target_param="member_id"),
    ("POST", "/api/faculty/{faculty_code}/directions-of-action"): RouteRule("faculties.direction_of_action.create", target_type="faculty", target_param="faculty_code"),
    ("PUT", "/api/faculty/{faculty_code}/directions-of-action/{direction_id}"): RouteRule("faculties.direction_of_action.update", target_type="faculty_direction", target_param="direction_id"),
    ("DELETE", "/api/faculty/{faculty_code}/directions-of-action/{direction_id}"): RouteRule("faculties.direction_of_action.delete", target_type="faculty_direction", target_param="direction_id"),

    # ── cafedras ───────────────────────────────────────────────────────────
    ("POST", "/api/cafedra/create"): RouteRule("cafedras.create", target_type="cafedra"),
    ("PUT", "/api/cafedra/{cafedra_code}"): RouteRule("cafedras.update", target_type="cafedra", target_param="cafedra_code"),
    ("DELETE", "/api/cafedra/{cafedra_code}"): RouteRule("cafedras.delete", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/{cafedra_code}/director/image"): RouteRule("cafedras.director.upload_image", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/{cafedra_code}/scientific-activity/intros"): RouteRule("cafedras.scientific_activity.update_intros", target_type="cafedra", target_param="cafedra_code"),
    ("POST", "/api/cafedra/{cafedra_code}/research-areas"): RouteRule("cafedras.research_area.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/research-areas/{item_id}"): RouteRule("cafedras.research_area.update", target_type="cafedra_research_area", target_param="item_id"),
    ("DELETE", "/api/cafedra/research-areas/{item_id}"): RouteRule("cafedras.research_area.delete", target_type="cafedra_research_area", target_param="item_id"),
    ("POST", "/api/cafedra/{cafedra_code}/projects"): RouteRule("cafedras.project.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/projects/{item_id}"): RouteRule("cafedras.project.update", target_type="cafedra_project", target_param="item_id"),
    ("DELETE", "/api/cafedra/projects/{item_id}"): RouteRule("cafedras.project.delete", target_type="cafedra_project", target_param="item_id"),
    ("POST", "/api/cafedra/{cafedra_code}/partner-companies"): RouteRule("cafedras.partner_company.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/partner-companies/{item_id}"): RouteRule("cafedras.partner_company.update", target_type="cafedra_partner_company", target_param="item_id"),
    ("DELETE", "/api/cafedra/partner-companies/{item_id}"): RouteRule("cafedras.partner_company.delete", target_type="cafedra_partner_company", target_param="item_id"),
    ("PUT", "/api/cafedra/partner-companies/{item_id}/logo"): RouteRule("cafedras.partner_company.upload_logo", target_type="cafedra_partner_company", target_param="item_id"),
    ("POST", "/api/cafedra/{cafedra_code}/publications"): RouteRule("cafedras.publication.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/publications/{item_id}"): RouteRule("cafedras.publication.update", target_type="cafedra_publication", target_param="item_id"),
    ("DELETE", "/api/cafedra/publications/{item_id}"): RouteRule("cafedras.publication.delete", target_type="cafedra_publication", target_param="item_id"),
    ("PUT", "/api/cafedra/{cafedra_code}/publications/reorder"): RouteRule("cafedras.publication.reorder", target_type="cafedra", target_param="cafedra_code"),
    ("POST", "/api/cafedra/{cafedra_code}/patents"): RouteRule("cafedras.patent.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/patents/{item_id}"): RouteRule("cafedras.patent.update", target_type="cafedra_patent", target_param="item_id"),
    ("DELETE", "/api/cafedra/patents/{item_id}"): RouteRule("cafedras.patent.delete", target_type="cafedra_patent", target_param="item_id"),
    ("PUT", "/api/cafedra/{cafedra_code}/patents/reorder"): RouteRule("cafedras.patent.reorder", target_type="cafedra", target_param="cafedra_code"),
    ("POST", "/api/cafedra/{cafedra_code}/laboratories"): RouteRule("cafedras.laboratory.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/laboratories/{laboratory_id}"): RouteRule("cafedras.laboratory.update", target_type="cafedra_laboratory", target_param="laboratory_id"),
    ("DELETE", "/api/cafedra/laboratories/{laboratory_id}"): RouteRule("cafedras.laboratory.delete", target_type="cafedra_laboratory", target_param="laboratory_id"),
    ("PUT", "/api/cafedra/laboratories/{laboratory_id}/image"): RouteRule("cafedras.laboratory.upload_image", target_type="cafedra_laboratory", target_param="laboratory_id"),
    ("POST", "/api/cafedra/laboratories/{laboratory_id}/gallery"): RouteRule("cafedras.laboratory.gallery.create", target_type="cafedra_laboratory", target_param="laboratory_id"),
    ("DELETE", "/api/cafedra/laboratories/gallery/{gallery_image_id}"): RouteRule("cafedras.laboratory.gallery.delete", target_type="cafedra_laboratory_gallery", target_param="gallery_image_id"),
    ("POST", "/api/cafedra/{cafedra_code}/workers"): RouteRule("cafedras.worker.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/workers/{worker_id}"): RouteRule("cafedras.worker.update", target_type="cafedra_worker", target_param="worker_id"),
    ("DELETE", "/api/cafedra/workers/{worker_id}"): RouteRule("cafedras.worker.delete", target_type="cafedra_worker", target_param="worker_id"),
    ("PUT", "/api/cafedra/workers/{worker_id}/image"): RouteRule("cafedras.worker.upload_image", target_type="cafedra_worker", target_param="worker_id"),
    ("POST", "/api/cafedra/{cafedra_code}/deputy-directors"): RouteRule("cafedras.deputy_director.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/deputy-directors/{deputy_director_id}"): RouteRule("cafedras.deputy_director.update", target_type="cafedra_deputy_director", target_param="deputy_director_id"),
    ("DELETE", "/api/cafedra/deputy-directors/{deputy_director_id}"): RouteRule("cafedras.deputy_director.delete", target_type="cafedra_deputy_director", target_param="deputy_director_id"),
    ("PUT", "/api/cafedra/deputy-directors/{deputy_director_id}/image"): RouteRule("cafedras.deputy_director.upload_image", target_type="cafedra_deputy_director", target_param="deputy_director_id"),
    ("POST", "/api/cafedra/{cafedra_code}/scientific-council"): RouteRule("cafedras.scientific_council.create", target_type="cafedra", target_param="cafedra_code"),
    ("PUT", "/api/cafedra/scientific-council/{member_id}"): RouteRule("cafedras.scientific_council.update", target_type="cafedra_council_member", target_param="member_id"),
    ("DELETE", "/api/cafedra/scientific-council/{member_id}"): RouteRule("cafedras.scientific_council.delete", target_type="cafedra_council_member", target_param="member_id"),

    # ── departments ────────────────────────────────────────────────────────
    ("POST", "/api/department/create"): RouteRule("departments.create", target_type="department"),
    ("PUT", "/api/department/{department_code}"): RouteRule("departments.update", target_type="department", target_param="department_code"),
    ("DELETE", "/api/department/{department_code}"): RouteRule("departments.delete", target_type="department", target_param="department_code"),
    ("PUT", "/api/department/{department_code}/director/image"): RouteRule("departments.director.upload_image", target_type="department", target_param="department_code"),
    ("POST", "/api/department/{department_code}/workers"): RouteRule("departments.worker.create", target_type="department", target_param="department_code"),
    ("PUT", "/api/department/workers/{worker_id}"): RouteRule("departments.worker.update", target_type="department_worker", target_param="worker_id"),
    ("DELETE", "/api/department/workers/{worker_id}"): RouteRule("departments.worker.delete", target_type="department_worker", target_param="worker_id"),
    ("PUT", "/api/department/workers/{worker_id}/image"): RouteRule("departments.worker.upload_image", target_type="department_worker", target_param="worker_id"),

    # ── research institutes ────────────────────────────────────────────────
    ("POST", "/api/research-institute/create"): RouteRule("research_institutes.create", target_type="research_institute"),
    ("PUT", "/api/research-institute/{institute_code}"): RouteRule("research_institutes.update", target_type="research_institute", target_param="institute_code"),
    ("DELETE", "/api/research-institute/{institute_code}"): RouteRule("research_institutes.delete", target_type="research_institute", target_param="institute_code"),
    ("PUT", "/api/research-institute/{institute_code}/image"): RouteRule("research_institutes.upload_image", target_type="research_institute", target_param="institute_code"),
    ("PUT", "/api/research-institute/{institute_code}/director/image"): RouteRule("research_institutes.director.upload_image", target_type="research_institute", target_param="institute_code"),
    ("PUT", "/api/research-institute/staff/{staff_id}/image"): RouteRule("research_institutes.staff.upload_image", target_type="research_institute_staff", target_param="staff_id"),
    # ── research projects ──────────────────────────────────────────────────
    ("POST", "/api/research-project/create"): RouteRule("research_projects.create", target_type="research_project"),
    ("PUT", "/api/research-project/{project_code}"): RouteRule("research_projects.update", target_type="research_project", target_param="project_code"),
    ("DELETE", "/api/research-project/{project_code}"): RouteRule("research_projects.delete", target_type="research_project", target_param="project_code"),
    ("PUT", "/api/research-project/{project_code}/image"): RouteRule("research_projects.upload_image", target_type="research_project", target_param="project_code"),

    # ── menu / footer ──────────────────────────────────────────────────────
    ("POST", "/api/menu/footer/column"): RouteRule("menu.footer_column.create", target_type="footer_column"),
    ("PUT", "/api/menu/footer/column/{column_id}"): RouteRule("menu.footer_column.update", target_type="footer_column", target_param="column_id"),
    ("DELETE", "/api/menu/footer/column/{column_id}"): RouteRule("menu.footer_column.delete", target_type="footer_column", target_param="column_id"),
    ("POST", "/api/menu/footer/link"): RouteRule("menu.footer_link.create", target_type="footer_link"),
    ("PUT", "/api/menu/footer/link/{link_id}"): RouteRule("menu.footer_link.update", target_type="footer_link", target_param="link_id"),
    ("DELETE", "/api/menu/footer/link/{link_id}"): RouteRule("menu.footer_link.delete", target_type="footer_link", target_param="link_id"),
    ("POST", "/api/menu/footer/partner-logo"): RouteRule("menu.partner_logo.create", target_type="partner_logo"),
    ("PUT", "/api/menu/footer/partner-logo/{logo_id}"): RouteRule("menu.partner_logo.update", target_type="partner_logo", target_param="logo_id"),
    ("DELETE", "/api/menu/footer/partner-logo/{logo_id}"): RouteRule("menu.partner_logo.delete", target_type="partner_logo", target_param="logo_id"),
    ("POST", "/api/menu/footer/quick-icon"): RouteRule("menu.quick_icon.create", target_type="quick_icon"),
    ("PUT", "/api/menu/footer/quick-icon/{icon_id}"): RouteRule("menu.quick_icon.update", target_type="quick_icon", target_param="icon_id"),
    ("DELETE", "/api/menu/footer/quick-icon/{icon_id}"): RouteRule("menu.quick_icon.delete", target_type="quick_icon", target_param="icon_id"),
    ("POST", "/api/menu/social-link"): RouteRule("menu.social_link.create", target_type="social_link"),
    ("PUT", "/api/menu/social-link/{link_id}"): RouteRule("menu.social_link.update", target_type="social_link", target_param="link_id"),
    ("DELETE", "/api/menu/social-link/{link_id}"): RouteRule("menu.social_link.delete", target_type="social_link", target_param="link_id"),
    ("POST", "/api/menu/contact"): RouteRule("menu.contact.create", target_type="contact"),
    ("PUT", "/api/menu/contact/{contact_id}"): RouteRule("menu.contact.update", target_type="contact", target_param="contact_id"),
    ("DELETE", "/api/menu/contact/{contact_id}"): RouteRule("menu.contact.delete", target_type="contact", target_param="contact_id"),
    ("POST", "/api/menu/quick/left-item"): RouteRule("menu.quick_left_item.create", target_type="quick_left_item"),
    ("PUT", "/api/menu/quick/left-item/{item_id}"): RouteRule("menu.quick_left_item.update", target_type="quick_left_item", target_param="item_id"),
    ("DELETE", "/api/menu/quick/left-item/{item_id}"): RouteRule("menu.quick_left_item.delete", target_type="quick_left_item", target_param="item_id"),
    ("POST", "/api/menu/quick/section"): RouteRule("menu.quick_section.create", target_type="quick_section"),
    ("PUT", "/api/menu/quick/section/{section_id}"): RouteRule("menu.quick_section.update", target_type="quick_section", target_param="section_id"),
    ("DELETE", "/api/menu/quick/section/{section_id}"): RouteRule("menu.quick_section.delete", target_type="quick_section", target_param="section_id"),
    ("POST", "/api/menu/quick/section-item"): RouteRule("menu.quick_section_item.create", target_type="quick_section_item"),
    ("PUT", "/api/menu/quick/section-item/{item_id}"): RouteRule("menu.quick_section_item.update", target_type="quick_section_item", target_param="item_id"),
    ("DELETE", "/api/menu/quick/section-item/{item_id}"): RouteRule("menu.quick_section_item.delete", target_type="quick_section_item", target_param="item_id"),

    # ── menu header ────────────────────────────────────────────────────────
    ("POST", "/api/menu/header/"): RouteRule("menu_header.create", target_type="menu_header", label_fields=("title_az",)),
    ("PUT", "/api/menu/header/{header_id}"): RouteRule("menu_header.update", target_type="menu_header", target_param="header_id", label_fields=("title_az",)),
    ("DELETE", "/api/menu/header/{header_id}"): RouteRule("menu_header.delete", target_type="menu_header", target_param="header_id"),
    ("POST", "/api/menu/header/item"): RouteRule("menu_header.item.create", target_type="menu_header_item"),
    ("PUT", "/api/menu/header/item/{item_id}"): RouteRule("menu_header.item.update", target_type="menu_header_item", target_param="item_id"),
    ("DELETE", "/api/menu/header/item/{item_id}"): RouteRule("menu_header.item.delete", target_type="menu_header_item", target_param="item_id"),
    ("POST", "/api/menu/header/sub-item"): RouteRule("menu_header.sub_item.create", target_type="menu_header_sub_item"),
    ("PUT", "/api/menu/header/sub-item/{sub_item_id}"): RouteRule("menu_header.sub_item.update", target_type="menu_header_sub_item", target_param="sub_item_id"),
    ("DELETE", "/api/menu/header/sub-item/{sub_item_id}"): RouteRule("menu_header.sub_item.delete", target_type="menu_header_sub_item", target_param="sub_item_id"),

    # ── chatbot knowledge (whole router is admin-gated) ────────────────────
    ("GET", "/api/chatbot-knowledge/sources"): RouteRule("chatbot_knowledge.read"),
    ("POST", "/api/chatbot-knowledge/sources"): RouteRule("chatbot_knowledge.source.create", target_type="knowledge_source"),
    ("DELETE", "/api/chatbot-knowledge/sources/{source_id}"): RouteRule("chatbot_knowledge.source.delete", target_type="knowledge_source", target_param="source_id"),
    ("POST", "/api/chatbot-knowledge/sources/{source_id}/scrape"): RouteRule("chatbot_knowledge.source.scrape", target_type="knowledge_source", target_param="source_id"),
    ("POST", "/api/chatbot-knowledge/sources/scrape-all"): RouteRule("chatbot_knowledge.scrape_all"),

    # ── chat monitoring ────────────────────────────────────────────────────
    # Mapped although they are GETs: unmapped reads fall through as public, and
    # these return visitor IP addresses. The audit middleware skips GET, so no
    # visitor IP can reach the activity log from here.
    ("GET", "/api/chat/admin/sessions"): RouteRule("chat.read"),
    ("GET", "/api/chat/admin/sessions/{session_id}/messages"): RouteRule("chat.read"),
    ("GET", "/api/chat/admin/stats"): RouteRule("chat.read"),
    # The only mutating chat route, so unlike the reads above it IS audited.
    # target_param records the session id — deliberately not the IP, which must
    # not reach the activity log even though this route can see it.
    ("DELETE", "/api/chat/admin/sessions/{session_id}"): RouteRule(
        "chat.delete", target_type="chat", target_param="session_id"
    ),

    # ── dashboard ──────────────────────────────────────────────────────────
    # Aggregate counts only, and it is the admin landing page every role opens,
    # so it needs a session rather than a permission of its own.
    ("GET", "/api/stats/dashboard"): AUTHENTICATED,

    # ── search ─────────────────────────────────────────────────────────────
    ("GET", "/api/search/admin"): RouteRule("search.admin.read"),

    # ── roles & permissions (greenfield — Lane C) ──────────────────────────
    ("GET", "/api/permissions"): RouteRule("roles.read"),
    ("GET", "/api/roles"): RouteRule("roles.read"),
    ("GET", "/api/roles/{role_id}"): RouteRule("roles.read"),
    ("POST", "/api/roles"): RouteRule("roles.create", target_type="role", label_fields=("code", "name_az")),
    ("PUT", "/api/roles/{role_id}"): RouteRule("roles.update", target_type="role", target_param="role_id"),
    ("PUT", "/api/roles/{role_id}/permissions"): RouteRule("roles.update_permissions", target_type="role", target_param="role_id"),
    ("DELETE", "/api/roles/{role_id}"): RouteRule("roles.delete", target_type="role", target_param="role_id"),

    # ── admin users (greenfield — Lane C) ──────────────────────────────────
    ("GET", "/api/admin-users"): RouteRule("admin_users.read"),
    ("POST", "/api/admin-users"): RouteRule("admin_users.create", target_type="admin_user", label_fields=("username",)),
    ("PUT", "/api/admin-users/{user_id}"): RouteRule("admin_users.update", target_type="admin_user", target_param="user_id"),
    ("PUT", "/api/admin-users/{user_id}/profile-image"): RouteRule("admin_users.update", target_type="admin_user", target_param="user_id"),
    ("PUT", "/api/admin-users/{user_id}/role"): RouteRule("admin_users.assign_role", target_type="admin_user", target_param="user_id"),
    ("PUT", "/api/admin-users/{user_id}/password"): RouteRule("admin_users.reset_password", target_type="admin_user", target_param="user_id"),
    ("POST", "/api/admin-users/{user_id}/activate"): RouteRule("admin_users.activate", target_type="admin_user", target_param="user_id"),
    ("POST", "/api/admin-users/{user_id}/deactivate"): RouteRule("admin_users.deactivate", target_type="admin_user", target_param="user_id"),
    ("DELETE", "/api/admin-users/{user_id}"): RouteRule("admin_users.delete", target_type="admin_user", target_param="user_id"),

    # ── activity log (greenfield — Lane C) ─────────────────────────────────
    ("GET", "/api/activity"): RouteRule("activity.read"),
    ("GET", "/api/activity/filters"): RouteRule("activity.read"),
}


_DENYLIST = frozenset({
    "password", "new_password", "current_password", "confirm_password",
    "hashed_password", "token", "access_token", "refresh_token", "api_key", "secret",
})

_bad_labels = sorted(
    {f for rule in ROUTE_PERMISSIONS.values() for f in rule.label_fields} & _DENYLIST
)
if _bad_labels:
    raise RuntimeError(f"label_fields must never name a secret: {_bad_labels}")

_bad_keys = sorted({r.key for r in ROUTE_PERMISSIONS.values() if r.key} - PERMISSION_KEYS)
if _bad_keys:
    raise RuntimeError(f"ROUTE_PERMISSIONS references keys absent from the catalogue: {_bad_keys}")


def verify_permission_map(app) -> None:
    """Fail startup when a mutating route has no entry, or an entry has a bad key.

    Called from the lifespan. A developer who adds a mutating route cannot deploy
    without deciding its permission.
    """
    unmapped = []
    seen = set()

    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)
        if not path or not methods or path in _SKIP_PATHS:
            continue
        for method in sorted(set(methods)):
            seen.add((method, path))
            if method in _SKIP_METHODS:
                continue
            if (method, path) not in ROUTE_PERMISSIONS:
                unmapped.append(f"{method} {path}")

    if unmapped:
        raise RuntimeError(
            "Unmapped mutating routes — add them to app/core/permission_map.py:\n  "
            + "\n  ".join(sorted(unmapped))
        )

    stale = sorted(f"{m} {p}" for (m, p) in ROUTE_PERMISSIONS if (m, p) not in seen)
    if stale:
        logger.warning(
            "permission_map has %d entries with no matching route (routers not mounted yet?): %s",
            len(stale), ", ".join(stale),
        )

    unused = sorted(PERMISSION_KEYS - {r.key for r in ROUTE_PERMISSIONS.values() if r.key})
    if unused:
        logger.warning("Catalogue permissions not referenced by any route: %s", ", ".join(unused))

    logger.info(
        "permission_map verified: %d routes mapped, %d catalogue keys.",
        len(ROUTE_PERMISSIONS), len(PERMISSION_KEYS),
    )
