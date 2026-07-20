"""Human-readable rendering of activity-log rows.

Nothing here is ever persisted. ``GET /api/activity`` renders ``message_az`` /
``message_en`` per row at read time, so wording and translations can be corrected
later with zero backfill, and an unknown ``action_key`` degrades to the raw key
rather than blanking the row.

``ACTION_LABELS`` is generated from ``RESOURCE_NOUNS`` x ``ACTION_TEMPLATES``
rather than hand-typed 157 times: a new permission key of the shape
``domain[.subresource].action`` gets a correct bilingual label for free, and the
irregular cases live in ``ACTION_OVERRIDES`` where they can be read at a glance.

Azerbaijani needs the noun in a different case per verb (accusative for
edit/delete, genitive for the upload/order phrasings), so each noun carries its
declined forms. Missing forms fall back to the nominative.
"""

import re
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.core.permissions import DOMAIN_LABELS

logger = get_logger("aztu.audit")


@dataclass(frozen=True)
class Noun:
    az: str                       # nominative        — "xəbər"
    en: str                       # singular          — "news item"
    acc: Optional[str] = None     # accusative        — "xəbəri"
    gen: Optional[str] = None     # genitive singular — "xəbərin"
    plgen: Optional[str] = None   # genitive plural   — "xəbərlərin"
    en_pl: Optional[str] = None   # english plural    — "news"

    @property
    def az_acc(self) -> str:
        return self.acc or self.az

    @property
    def az_gen(self) -> str:
        return self.gen or self.az

    @property
    def az_plgen(self) -> str:
        return self.plgen or self.az_gen

    @property
    def en_plural(self) -> str:
        return self.en_pl or f"{self.en}s"


# Keyed on the permission key minus its final action segment.
RESOURCE_NOUNS: Dict[str, Noun] = {
    "news": Noun("xəbər", "news item", "xəbəri", "xəbərin", "xəbərlərin", "news"),
    "news_categories": Noun("xəbər kateqoriyası", "news category", "xəbər kateqoriyasını", "xəbər kateqoriyasının", "xəbər kateqoriyalarının", "news categories"),
    "announcements": Noun("elan", "announcement", "elanı", "elanın", "elanların"),
    "hero": Noun("əsas video", "hero video", "əsas videonu", "əsas videonun", "əsas videoların"),
    "projects": Noun("layihə", "project", "layihəni", "layihənin", "layihələrin"),
    "collaborations": Noun("əməkdaşlıq", "collaboration", "əməkdaşlığı", "əməkdaşlığın", "əməkdaşlıqların"),
    "employees": Noun("əməkdaş", "employee", "əməkdaşı", "əməkdaşın", "əməkdaşların"),

    "faculties": Noun("fakültə", "faculty", "fakültəni", "fakültənin", "fakültələrin", "faculties"),
    "faculties.worker": Noun("fakültə əməkdaşı", "faculty staff member", "fakültə əməkdaşını", "fakültə əməkdaşının", "fakültə əməkdaşlarının", "faculty staff members"),
    "faculties.deputy_dean": Noun("dekan müavini", "deputy dean", "dekan müavinini", "dekan müavininin", "dekan müavinlərinin"),
    "faculties.director": Noun("dekan", "dean", "dekanı", "dekanın", "dekanların"),
    "faculties.direction_of_action": Noun("fəaliyyət istiqaməti", "field of activity", "fəaliyyət istiqamətini", "fəaliyyət istiqamətinin", "fəaliyyət istiqamətlərinin", "fields of activity"),
    "faculties.scientific_council": Noun("elmi şura üzvü", "scientific council member", "elmi şura üzvünü", "elmi şura üzvünün", "elmi şura üzvlərinin"),

    "cafedras": Noun("kafedra", "cafedra", "kafedranı", "kafedranın", "kafedraların"),
    "cafedras.worker": Noun("kafedra əməkdaşı", "cafedra staff member", "kafedra əməkdaşını", "kafedra əməkdaşının", "kafedra əməkdaşlarının", "cafedra staff members"),
    "cafedras.deputy_director": Noun("müdir müavini", "deputy head", "müdir müavinini", "müdir müavininin", "müdir müavinlərinin"),
    "cafedras.director": Noun("kafedra müdiri", "cafedra head", "kafedra müdirini", "kafedra müdirinin", "kafedra müdirlərinin"),
    "cafedras.laboratory": Noun("laboratoriya", "laboratory", "laboratoriyanı", "laboratoriyanın", "laboratoriyaların", "laboratories"),
    "cafedras.laboratory.gallery": Noun("laboratoriya qalereya şəkli", "laboratory gallery image", "laboratoriya qalereya şəklini", "laboratoriya qalereya şəklinin", "laboratoriya qalereya şəkillərinin"),
    "cafedras.partner_company": Noun("tərəfdaş şirkət", "partner company", "tərəfdaş şirkəti", "tərəfdaş şirkətin", "tərəfdaş şirkətlərin", "partner companies"),
    "cafedras.project": Noun("kafedra layihəsi", "cafedra project", "kafedra layihəsini", "kafedra layihəsinin", "kafedra layihələrinin"),
    "cafedras.publication": Noun("elmi nəşr", "publication", "elmi nəşri", "elmi nəşrin", "elmi nəşrlərin"),
    "cafedras.research_area": Noun("tədqiqat sahəsi", "research area", "tədqiqat sahəsini", "tədqiqat sahəsinin", "tədqiqat sahələrinin"),
    "cafedras.scientific_council": Noun("elmi şura üzvü", "scientific council member", "elmi şura üzvünü", "elmi şura üzvünün", "elmi şura üzvlərinin"),
    "cafedras.scientific_activity": Noun("elmi fəaliyyət", "scientific activity", "elmi fəaliyyəti", "elmi fəaliyyətin", "elmi fəaliyyətlərin", "scientific activities"),

    "departments": Noun("şöbə", "department", "şöbəni", "şöbənin", "şöbələrin"),
    "departments.worker": Noun("şöbə əməkdaşı", "department staff member", "şöbə əməkdaşını", "şöbə əməkdaşının", "şöbə əməkdaşlarının", "department staff members"),
    "departments.director": Noun("şöbə müdiri", "department head", "şöbə müdirini", "şöbə müdirinin", "şöbə müdirlərinin"),

    "research_institutes": Noun("elmi-tədqiqat institutu", "research institute", "elmi-tədqiqat institutunu", "elmi-tədqiqat institutunun", "elmi-tədqiqat institutlarının"),
    "research_institutes.director": Noun("institut direktoru", "institute director", "institut direktorunu", "institut direktorunun", "institut direktorlarının"),
    "research_institutes.staff": Noun("institut əməkdaşı", "institute staff member", "institut əməkdaşını", "institut əməkdaşının", "institut əməkdaşlarının", "institute staff members"),

    "menu.contact": Noun("əlaqə məlumatı", "contact detail", "əlaqə məlumatını", "əlaqə məlumatının", "əlaqə məlumatlarının"),
    "menu.footer_column": Noun("altlıq sütunu", "footer column", "altlıq sütununu", "altlıq sütununun", "altlıq sütunlarının"),
    "menu.footer_link": Noun("altlıq linki", "footer link", "altlıq linkini", "altlıq linkinin", "altlıq linklərinin"),
    "menu.partner_logo": Noun("tərəfdaş loqosu", "partner logo", "tərəfdaş loqosunu", "tərəfdaş loqosunun", "tərəfdaş loqolarının"),
    "menu.quick_icon": Noun("sürətli keçid ikonu", "quick-access icon", "sürətli keçid ikonunu", "sürətli keçid ikonunun", "sürətli keçid ikonlarının"),
    "menu.quick_left_item": Noun("sürətli keçid elementi", "quick-access item", "sürətli keçid elementini", "sürətli keçid elementinin", "sürətli keçid elementlərinin"),
    "menu.quick_section": Noun("sürətli keçid bölməsi", "quick-access section", "sürətli keçid bölməsini", "sürətli keçid bölməsinin", "sürətli keçid bölmələrinin"),
    "menu.quick_section_item": Noun("sürətli keçid bölmə elementi", "quick-access section item", "sürətli keçid bölmə elementini", "sürətli keçid bölmə elementinin", "sürətli keçid bölmə elementlərinin"),
    "menu.social_link": Noun("sosial şəbəkə linki", "social link", "sosial şəbəkə linkini", "sosial şəbəkə linkinin", "sosial şəbəkə linklərinin"),

    "menu_header": Noun("menyu başlığı", "menu header", "menyu başlığını", "menyu başlığının", "menyu başlıqlarının"),
    "menu_header.item": Noun("menyu elementi", "menu item", "menyu elementini", "menyu elementinin", "menyu elementlərinin"),
    "menu_header.sub_item": Noun("alt menyu elementi", "submenu item", "alt menyu elementini", "alt menyu elementinin", "alt menyu elementlərinin"),

    "admin_users": Noun("istifadəçi", "admin user", "istifadəçini", "istifadəçinin", "istifadəçilərin"),
    "roles": Noun("rol", "role", "rolu", "rolun", "rolların"),
    "activity": Noun("fəaliyyət jurnalı", "activity log", "fəaliyyət jurnalını", "fəaliyyət jurnalının", "fəaliyyət jurnallarının"),
    "chat": Noun("çat söhbəti", "chat conversation", "çat söhbətini", "çat söhbətinin", "çat söhbətlərinin"),
    "chatbot_knowledge": Noun("bilik bazası", "knowledge base", "bilik bazasını", "bilik bazasının", "bilik bazalarının"),
    "chatbot_knowledge.source": Noun("bilik mənbəyi", "knowledge source", "bilik mənbəyini", "bilik mənbəyinin", "bilik mənbələrinin"),
    "search.admin": Noun("axtarış", "search", "axtarışı", "axtarışın", "axtarışların", "searches"),
}


# {form} is substituted with the noun in the case the phrasing needs.
ACTION_TEMPLATES: Dict[str, Tuple[str, str, str]] = {
    # action: (az template, en template, noun form)
    "create":        ("yeni {n} əlavə etdi",        "added a new {n}",                  "az"),
    "update":        ("{n} redaktə etdi",           "edited a {n}",                     "acc"),
    "delete":        ("{n} sildi",                  "deleted a {n}",                    "acc"),
    "activate":      ("{n} dərc etdi",              "published a {n}",                  "acc"),
    "deactivate":    ("{n} yayımdan çıxardı",       "unpublished a {n}",                "acc"),
    "reorder":       ("{n} sırasını dəyişdi",       "changed the order of the {n}",     "plgen_en_pl"),
    "read":          ("{n} baxdı",                  "viewed the {n}",                   "acc"),
    "upload_image":  ("{n} şəklini yüklədi",        "uploaded a {n} photo",             "gen_en"),
    "upload_logo":   ("{n} loqosunu yüklədi",       "uploaded a {n} logo",              "gen_en"),
    "upload_file":   ("{n} faylını yüklədi",        "uploaded a {n} file",              "gen_en"),
}


ACTION_OVERRIDES: Dict[str, Tuple[str, str]] = {
    "auth.login":         ("sistemə daxil oldu",                    "signed in"),
    "auth.login_failed":  ("uğursuz giriş cəhdi",                   "failed sign-in attempt"),
    "auth.logout":        ("sistemdən çıxdı",                       "signed out"),
    "auth.password_changed": ("öz şifrəsini dəyişdi",               "changed their own password"),

    "admin_users.activate":       ("istifadəçini aktivləşdirdi",    "activated an admin user"),
    "admin_users.deactivate":     ("istifadəçini deaktiv etdi",     "deactivated an admin user"),
    "admin_users.assign_role":    ("istifadəçinin rolunu dəyişdi",  "changed an admin user's role"),
    "admin_users.reset_password": ("istifadəçinin şifrəsini sıfırladı", "reset an admin user's password"),

    "roles.update_permissions":   ("rolun icazələrini dəyişdi",     "changed a role's permissions"),

    "chatbot_knowledge.scrape_all":    ("bütün bilik mənbələrini yenilədi", "refreshed all knowledge sources"),
    "chatbot_knowledge.source.scrape": ("bilik mənbəyini yenilədi",  "refreshed a knowledge source"),

    "cafedras.scientific_activity.update_intros": (
        "kafedranın elmi fəaliyyət mətnlərini redaktə etdi",
        "edited the cafedra scientific-activity texts",
    ),
}


def _article(text: str) -> str:
    """"a announcement" -> "an announcement". Applied only to the generated English."""
    return re.sub(r"\ba (?=[aeiou])", "an ", text)


def _build_action_labels() -> Dict[str, Dict[str, str]]:
    labels: Dict[str, Dict[str, str]] = {}
    for resource, noun in RESOURCE_NOUNS.items():
        for action, (az_tpl, en_tpl, form) in ACTION_TEMPLATES.items():
            if form == "plgen_en_pl":
                az_word, en_word = noun.az_plgen, noun.en_plural
            elif form == "gen_en":
                az_word, en_word = noun.az_gen, noun.en
            elif form == "acc":
                az_word, en_word = noun.az_acc, noun.en
            else:
                az_word, en_word = noun.az, noun.en
            labels[f"{resource}.{action}"] = {
                "az": az_tpl.format(n=az_word),
                "en": _article(en_tpl.format(n=en_word)),
            }

    for key, (az, en) in ACTION_OVERRIDES.items():
        labels[key] = {"az": az, "en": en}
    return labels


ACTION_LABELS: Dict[str, Dict[str, str]] = _build_action_labels()


def action_label(action_key: Optional[str], lang: str = "az") -> str:
    """Verb phrase for an action key; degrades to the raw key when unknown."""
    if not action_key:
        return ""
    entry = ACTION_LABELS.get(action_key)
    if entry is None:
        return action_key
    return entry.get(lang) or entry.get("az") or action_key


def domain_label(domain: Optional[str], lang: str = "az") -> str:
    labels = DOMAIN_LABELS.get(domain or "")
    if not labels:
        return domain or ""
    return labels[0] if lang == "az" else labels[1]


# ── Tier 2: naming the affected record ────────────────────────────────────────
# One cheap indexed SELECT per audited row, on the audit middleware's own session,
# after the response has already been produced. Whitelisted to the types below —
# a target_type with no entry simply yields no label. Never raises.


@dataclass(frozen=True)
class _Resolver:
    module: str
    model: str
    key_attr: str
    label_attr: str
    numeric_key: bool = False
    lang_attr: Optional[str] = "lang_code"


_RESOLVER_SPECS: Dict[str, _Resolver] = {
    "news": _Resolver("app.models.news.news_translation", "NewsTranslation", "news_id", "title", True),
    "news_category": _Resolver("app.models.news_category.news_category_translation", "NewsCategoryTranslation", "category_id", "title", True),
    "announcement": _Resolver("app.models.announcement.announcement_translation", "AnnouncementTranslation", "announcement_id", "title", True),
    "project": _Resolver("app.models.project.project_tr", "ProjectTranslation", "project_id", "title", True),
    "collaboration": _Resolver("app.models.collaboration.collaboration_tr", "CollaborationTranslation", "collaboration_id", "name", True),
    "employee": _Resolver("app.models.employee.employee_tr", "EmployeeTr", "employee_code", "full_name"),
    "faculty": _Resolver("app.models.faculties.faculties_tr", "FacultyTr", "faculty_code", "faculty_name"),
    "cafedra": _Resolver("app.models.cafedras.cafedras_tr", "CafedraTr", "cafedra_code", "cafedra_name"),
    "department": _Resolver("app.models.departments.department_tr", "DepartmentTr", "department_code", "department_name"),
    # app.models.research_institute.institute is the module the services use;
    # the parallel research_institutes package is dead weight and redefines the
    # same tables on the same MetaData.
    "research_institute": _Resolver("app.models.research_institute.institute", "ResearchInstituteTr", "institute_code", "name"),
}

TARGET_LABEL_MAX_LENGTH = 200


_MODEL_CACHE: Dict[str, object] = {}


def _model_for(spec: _Resolver):
    """Import the mapped class once, on first use.

    Deferred rather than imported at module scope: this module is pulled in by the
    permission layer, and importing every translation model here would both widen
    the import graph and, in isolation, hit mapper-configuration errors from
    relationships whose sibling class has not been registered yet.
    """
    cached = _MODEL_CACHE.get(spec.module + spec.model)
    if cached is None:
        from importlib import import_module

        cached = getattr(import_module(spec.module), spec.model)
        _MODEL_CACHE[spec.module + spec.model] = cached
    return cached


def _make_resolver(spec: _Resolver) -> Callable:
    async def resolve(db: AsyncSession, target_id: str) -> Optional[str]:
        key: object = target_id
        if spec.numeric_key:
            try:
                key = int(target_id)
            except (TypeError, ValueError):
                return None

        model = _model_for(spec)
        column = getattr(model, spec.label_attr)
        stmt = select(column).where(getattr(model, spec.key_attr) == key)
        if spec.lang_attr:
            stmt = stmt.where(getattr(model, spec.lang_attr) == "az")

        value = (await db.execute(stmt.limit(1))).scalar_one_or_none()
        if not value:
            return None
        return str(value).strip()[:TARGET_LABEL_MAX_LENGTH] or None

    return resolve


TARGET_RESOLVERS: Dict[str, Callable] = {
    target_type: _make_resolver(spec) for target_type, spec in _RESOLVER_SPECS.items()
}


async def resolve_target_label(
    db: AsyncSession, target_type: Optional[str], target_id: Optional[str]
) -> Optional[str]:
    """Best-effort name for the affected record. A miss is never an error."""
    if not target_type or not target_id:
        return None
    resolver = TARGET_RESOLVERS.get(target_type)
    if resolver is None:
        return None
    try:
        return await resolver(db, target_id)
    except Exception:
        # A label is a nicety; never let one break the audit row that carries it.
        logger.warning("Target label lookup failed for %s=%s", target_type, target_id, exc_info=True)
        return None


def label_from_fields(fields: Optional[dict]) -> Optional[str]:
    """Label for a create, assembled from the route's whitelisted form fields.

    Creates have no id — it lives in the response body, which is deliberately never
    parsed — so their name comes from what the request already carried.
    """
    if not fields:
        return None
    parts = [str(v).strip() for v in fields.values() if isinstance(v, (str, int)) and str(v).strip()]
    if not parts:
        return None
    return " ".join(parts)[:TARGET_LABEL_MAX_LENGTH]


def render_message(row, lang: str = "az") -> str:
    """``"nigar yeni xəbər əlavə etdi — "AzTU-da elmi konfrans""``.

    Reads a row object or a mapping. Never raises: an unknown action key falls back
    to the raw key, and a missing label just shortens the sentence.
    """
    get = row.get if isinstance(row, dict) else lambda name: getattr(row, name, None)

    username = get("admin_username") or ("naməlum" if lang == "az" else "unknown")
    verb = action_label(get("action_key"), lang)
    label = get("target_label")

    message = f"{username} {verb}".strip()
    if label:
        message = f'{message} — "{label}"'

    # A failed sign-in is already denied by definition — its verb says so.
    if (get("outcome") or "success") == "denied" and get("action_key") != "auth.login_failed":
        suffix = "(icazə yoxdur)" if lang == "az" else "(permission denied)"
        message = f"{message} {suffix}"
    return message
