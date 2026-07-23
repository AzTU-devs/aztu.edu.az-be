"""Permission catalogue — the enforcement source of truth.

Code is authoritative: `permissions` rows are seeded from this catalogue on boot so
that `role_permissions` has an FK target and the admin UI can render labels in one
query. A key that is not here cannot be granted and cannot be referenced by
`app/core/permission_map.py` (the boot verifier rejects it).

Key grammar (contract C1): ``domain[.subresource].action`` — lowercase snake.
`domain` is everything before the first dot, `action` is everything after it.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

SUPER_ADMIN_CODE = "super_admin"


@dataclass(frozen=True)
class PermissionDef:
    key: str
    domain: str
    action: str
    label_az: str
    label_en: str


def _p(key: str, label_az: str, label_en: str) -> PermissionDef:
    domain, _, action = key.partition(".")
    if not action:
        raise ValueError(f"Permission key must be 'domain.action': {key!r}")
    return PermissionDef(key=key, domain=domain, action=action, label_az=label_az, label_en=label_en)


DOMAIN_LABELS: Dict[str, Tuple[str, str]] = {
    "news": ("Xəbərlər", "News"),
    "news_categories": ("Xəbər kateqoriyaları", "News categories"),
    "announcements": ("Elanlar", "Announcements"),
    "hero": ("Ana səhifə videosu", "Hero"),
    "projects": ("Layihələr", "Projects"),
    "collaborations": ("Əməkdaşlıqlar", "Collaborations"),
    "employees": ("Əməkdaşlar", "Employees"),
    "faculties": ("Fakültələr", "Faculties"),
    "cafedras": ("Kafedralar", "Cafedras"),
    "departments": ("Şöbələr", "Departments"),
    "research_institutes": ("Elmi tədqiqat institutları", "Research institutes"),
    "research_projects": ("Tədqiqat layihələri", "Research projects"),
    "about": ("Haqqımızda", "About"),
    "menu": ("Menyu və altlıq", "Menu and footer"),
    "menu_header": ("Başlıq menyusu", "Header menu"),
    "chatbot_knowledge": ("Çatbot bilik bazası", "Chatbot knowledge base"),
    "chat": ("Çat monitorinqi", "Chat monitoring"),
    "search": ("Axtarış", "Search"),
    "roles": ("Rollar", "Roles"),
    "admin_users": ("Admin istifadəçilər", "Admin users"),
    "activity": ("Fəaliyyət jurnalı", "Activity log"),
}

DOMAIN_ORDER: Tuple[str, ...] = tuple(DOMAIN_LABELS.keys())


PERMISSION_CATALOGUE: Tuple[PermissionDef, ...] = (
    # ── news ────────────────────────────────────────────────────────────────
    _p("news.create", "Xəbər yaratmaq", "Create news"),
    _p("news.update", "Xəbəri redaktə etmək", "Edit news"),
    _p("news.delete", "Xəbəri silmək", "Delete news"),
    _p("news.activate", "Xəbəri dərc etmək", "Publish news"),
    _p("news.deactivate", "Xəbəri dərcdən çıxarmaq", "Unpublish news"),
    _p("news.reorder", "Xəbərləri sıralamaq", "Reorder news"),
    # ── news_categories ─────────────────────────────────────────────────────
    _p("news_categories.create", "Xəbər kateqoriyası yaratmaq", "Create news category"),
    _p("news_categories.update", "Xəbər kateqoriyasını redaktə etmək", "Edit news category"),
    _p("news_categories.delete", "Xəbər kateqoriyasını silmək", "Delete news category"),
    # ── announcements ───────────────────────────────────────────────────────
    _p("announcements.create", "Elan yaratmaq", "Create announcement"),
    _p("announcements.update", "Elanı redaktə etmək", "Edit announcement"),
    _p("announcements.delete", "Elanı silmək", "Delete announcement"),
    _p("announcements.activate", "Elanı dərc etmək", "Publish announcement"),
    _p("announcements.deactivate", "Elanı dərcdən çıxarmaq", "Unpublish announcement"),
    _p("announcements.reorder", "Elanları sıralamaq", "Reorder announcements"),
    _p("announcements.upload_file", "Elana fayl yükləmək", "Upload announcement file"),
    # ── hero ────────────────────────────────────────────────────────────────
    _p("hero.create", "Hero videosu yaratmaq", "Create hero"),
    _p("hero.update", "Hero videosunu redaktə etmək", "Edit hero"),
    _p("hero.delete", "Hero videosunu silmək", "Delete hero"),
    _p("hero.activate", "Hero videosunu aktivləşdirmək", "Activate hero"),
    _p("hero.deactivate", "Hero videosunu deaktiv etmək", "Deactivate hero"),
    # ── projects ────────────────────────────────────────────────────────────
    _p("projects.create", "Layihə yaratmaq", "Create project"),
    _p("projects.delete", "Layihəni silmək", "Delete project"),
    _p("projects.reorder", "Layihələri sıralamaq", "Reorder projects"),
    # ── collaborations ──────────────────────────────────────────────────────
    _p("collaborations.create", "Əməkdaşlıq yaratmaq", "Create collaboration"),
    _p("collaborations.update", "Əməkdaşlığı redaktə etmək", "Edit collaboration"),
    _p("collaborations.delete", "Əməkdaşlığı silmək", "Delete collaboration"),
    _p("collaborations.reorder", "Əməkdaşlıqları sıralamaq", "Reorder collaborations"),
    # ── employees ───────────────────────────────────────────────────────────
    _p("employees.create", "Əməkdaş yaratmaq", "Create employee"),
    _p("employees.update", "Əməkdaşı redaktə etmək", "Edit employee"),
    _p("employees.delete", "Əməkdaşı silmək", "Delete employee"),
    # ── faculties ───────────────────────────────────────────────────────────
    _p("faculties.create", "Fakültə yaratmaq", "Create faculty"),
    _p("faculties.update", "Fakültəni redaktə etmək", "Edit faculty"),
    _p("faculties.delete", "Fakültəni silmək", "Delete faculty"),
    _p("faculties.director.upload_image", "Fakültə dekanının şəklini yükləmək", "Upload faculty director image"),
    _p("faculties.worker.create", "Fakültəyə əməkdaş əlavə etmək", "Add faculty staff member"),
    _p("faculties.worker.update", "Fakültə əməkdaşını redaktə etmək", "Edit faculty staff member"),
    _p("faculties.worker.delete", "Fakültə əməkdaşını silmək", "Delete faculty staff member"),
    _p("faculties.worker.upload_image", "Fakültə əməkdaşının şəklini yükləmək", "Upload faculty staff image"),
    _p("faculties.deputy_dean.create", "Dekan müavini əlavə etmək", "Add deputy dean"),
    _p("faculties.deputy_dean.update", "Dekan müavinini redaktə etmək", "Edit deputy dean"),
    _p("faculties.deputy_dean.delete", "Dekan müavinini silmək", "Delete deputy dean"),
    _p("faculties.deputy_dean.upload_image", "Dekan müavininin şəklini yükləmək", "Upload deputy dean image"),
    _p("faculties.scientific_council.create", "Fakültə elmi şurasına üzv əlavə etmək", "Add faculty scientific council member"),
    _p("faculties.scientific_council.update", "Fakültə elmi şura üzvünü redaktə etmək", "Edit faculty scientific council member"),
    _p("faculties.scientific_council.delete", "Fakültə elmi şura üzvünü silmək", "Delete faculty scientific council member"),
    _p("faculties.direction_of_action.create", "Fəaliyyət istiqaməti əlavə etmək", "Add direction of action"),
    _p("faculties.direction_of_action.update", "Fəaliyyət istiqamətini redaktə etmək", "Edit direction of action"),
    _p("faculties.direction_of_action.delete", "Fəaliyyət istiqamətini silmək", "Delete direction of action"),
    # ── cafedras ────────────────────────────────────────────────────────────
    _p("cafedras.create", "Kafedra yaratmaq", "Create cafedra"),
    _p("cafedras.update", "Kafedranı redaktə etmək", "Edit cafedra"),
    _p("cafedras.delete", "Kafedranı silmək", "Delete cafedra"),
    _p("cafedras.director.upload_image", "Kafedra müdirinin şəklini yükləmək", "Upload cafedra director image"),
    _p("cafedras.scientific_activity.update_intros", "Elmi fəaliyyət mətnlərini redaktə etmək", "Edit scientific activity intros"),
    _p("cafedras.research_area.create", "Tədqiqat sahəsi əlavə etmək", "Add research area"),
    _p("cafedras.research_area.update", "Tədqiqat sahəsini redaktə etmək", "Edit research area"),
    _p("cafedras.research_area.delete", "Tədqiqat sahəsini silmək", "Delete research area"),
    _p("cafedras.project.create", "Kafedra layihəsi əlavə etmək", "Add cafedra project"),
    _p("cafedras.project.update", "Kafedra layihəsini redaktə etmək", "Edit cafedra project"),
    _p("cafedras.project.delete", "Kafedra layihəsini silmək", "Delete cafedra project"),
    _p("cafedras.partner_company.create", "Tərəfdaş şirkət əlavə etmək", "Add partner company"),
    _p("cafedras.partner_company.update", "Tərəfdaş şirkəti redaktə etmək", "Edit partner company"),
    _p("cafedras.partner_company.delete", "Tərəfdaş şirkəti silmək", "Delete partner company"),
    _p("cafedras.partner_company.upload_logo", "Tərəfdaş şirkətin loqosunu yükləmək", "Upload partner company logo"),
    _p("cafedras.publication.create", "Nəşr əlavə etmək", "Add publication"),
    _p("cafedras.publication.update", "Nəşri redaktə etmək", "Edit publication"),
    _p("cafedras.publication.delete", "Nəşri silmək", "Delete publication"),
    _p("cafedras.publication.reorder", "Nəşrləri sıralamaq", "Reorder publications"),
    _p("cafedras.patent.create", "Patent əlavə etmək", "Add patent"),
    _p("cafedras.patent.update", "Patenti redaktə etmək", "Edit patent"),
    _p("cafedras.patent.delete", "Patenti silmək", "Delete patent"),
    _p("cafedras.patent.reorder", "Patentləri sıralamaq", "Reorder patents"),
    _p("cafedras.laboratory.create", "Laboratoriya əlavə etmək", "Add laboratory"),
    _p("cafedras.laboratory.update", "Laboratoriyanı redaktə etmək", "Edit laboratory"),
    _p("cafedras.laboratory.delete", "Laboratoriyanı silmək", "Delete laboratory"),
    _p("cafedras.laboratory.upload_image", "Laboratoriyanın şəklini yükləmək", "Upload laboratory image"),
    _p("cafedras.laboratory.gallery.create", "Laboratoriya qalereyasına şəkil əlavə etmək", "Add laboratory gallery image"),
    _p("cafedras.laboratory.gallery.delete", "Laboratoriya qalereyasından şəkil silmək", "Delete laboratory gallery image"),
    _p("cafedras.worker.create", "Kafedraya əməkdaş əlavə etmək", "Add cafedra staff member"),
    _p("cafedras.worker.update", "Kafedra əməkdaşını redaktə etmək", "Edit cafedra staff member"),
    _p("cafedras.worker.delete", "Kafedra əməkdaşını silmək", "Delete cafedra staff member"),
    _p("cafedras.worker.upload_image", "Kafedra əməkdaşının şəklini yükləmək", "Upload cafedra staff image"),
    _p("cafedras.deputy_director.create", "Kafedra müdiri müavini əlavə etmək", "Add deputy director"),
    _p("cafedras.deputy_director.update", "Kafedra müdiri müavinini redaktə etmək", "Edit deputy director"),
    _p("cafedras.deputy_director.delete", "Kafedra müdiri müavinini silmək", "Delete deputy director"),
    _p("cafedras.deputy_director.upload_image", "Kafedra müdiri müavininin şəklini yükləmək", "Upload deputy director image"),
    _p("cafedras.scientific_council.create", "Kafedra elmi şurasına üzv əlavə etmək", "Add cafedra scientific council member"),
    _p("cafedras.scientific_council.update", "Kafedra elmi şura üzvünü redaktə etmək", "Edit cafedra scientific council member"),
    _p("cafedras.scientific_council.delete", "Kafedra elmi şura üzvünü silmək", "Delete cafedra scientific council member"),
    # ── departments ─────────────────────────────────────────────────────────
    _p("departments.create", "Şöbə yaratmaq", "Create department"),
    _p("departments.update", "Şöbəni redaktə etmək", "Edit department"),
    _p("departments.delete", "Şöbəni silmək", "Delete department"),
    _p("departments.director.upload_image", "Şöbə rəhbərinin şəklini yükləmək", "Upload department director image"),
    _p("departments.worker.create", "Şöbəyə əməkdaş əlavə etmək", "Add department staff member"),
    _p("departments.worker.update", "Şöbə əməkdaşını redaktə etmək", "Edit department staff member"),
    _p("departments.worker.delete", "Şöbə əməkdaşını silmək", "Delete department staff member"),
    _p("departments.worker.upload_image", "Şöbə əməkdaşının şəklini yükləmək", "Upload department staff image"),
    # ── research_institutes ─────────────────────────────────────────────────
    _p("research_institutes.create", "Elmi tədqiqat institutu yaratmaq", "Create research institute"),
    _p("research_institutes.update", "Elmi tədqiqat institutunu redaktə etmək", "Edit research institute"),
    _p("research_institutes.delete", "Elmi tədqiqat institutunu silmək", "Delete research institute"),
    _p("research_institutes.upload_image", "İnstitutun şəklini yükləmək", "Upload research institute image"),
    _p("research_institutes.director.upload_image", "İnstitut direktorunun şəklini yükləmək", "Upload research institute director image"),
    _p("research_institutes.staff.upload_image", "İnstitut əməkdaşının şəklini yükləmək", "Upload research institute staff image"),
    # ── research_projects ───────────────────────────────────────────────────
    _p("research_projects.create", "Tədqiqat layihəsi yaratmaq", "Create research project"),
    _p("research_projects.update", "Tədqiqat layihəsini redaktə etmək", "Edit research project"),
    _p("research_projects.delete", "Tədqiqat layihəsini silmək", "Delete research project"),
    _p("research_projects.upload_image", "Layihənin şəklini yükləmək", "Upload research project image"),
    # ── about ───────────────────────────────────────────────────────────────
    _p("about.update", "Haqqımızda səhifəsini redaktə etmək", "Edit about page"),
    _p("about.activate", "Haqqımızda səhifəsini dərc etmək", "Publish about page"),
    # ── menu ────────────────────────────────────────────────────────────────
    _p("menu.footer_column.create", "Altlıq sütunu yaratmaq", "Create footer column"),
    _p("menu.footer_column.update", "Altlıq sütununu redaktə etmək", "Edit footer column"),
    _p("menu.footer_column.delete", "Altlıq sütununu silmək", "Delete footer column"),
    _p("menu.footer_link.create", "Altlıq linki yaratmaq", "Create footer link"),
    _p("menu.footer_link.update", "Altlıq linkini redaktə etmək", "Edit footer link"),
    _p("menu.footer_link.delete", "Altlıq linkini silmək", "Delete footer link"),
    _p("menu.partner_logo.create", "Tərəfdaş loqosu əlavə etmək", "Add partner logo"),
    _p("menu.partner_logo.update", "Tərəfdaş loqosunu redaktə etmək", "Edit partner logo"),
    _p("menu.partner_logo.delete", "Tərəfdaş loqosunu silmək", "Delete partner logo"),
    _p("menu.quick_icon.create", "Sürətli keçid ikonu yaratmaq", "Create quick icon"),
    _p("menu.quick_icon.update", "Sürətli keçid ikonunu redaktə etmək", "Edit quick icon"),
    _p("menu.quick_icon.delete", "Sürətli keçid ikonunu silmək", "Delete quick icon"),
    _p("menu.social_link.create", "Sosial şəbəkə linki yaratmaq", "Create social link"),
    _p("menu.social_link.update", "Sosial şəbəkə linkini redaktə etmək", "Edit social link"),
    _p("menu.social_link.delete", "Sosial şəbəkə linkini silmək", "Delete social link"),
    _p("menu.contact.create", "Əlaqə məlumatı əlavə etmək", "Add contact detail"),
    _p("menu.contact.update", "Əlaqə məlumatını redaktə etmək", "Edit contact detail"),
    _p("menu.contact.delete", "Əlaqə məlumatını silmək", "Delete contact detail"),
    _p("menu.quick_left_item.create", "Sürətli menyu elementi yaratmaq", "Create quick menu item"),
    _p("menu.quick_left_item.update", "Sürətli menyu elementini redaktə etmək", "Edit quick menu item"),
    _p("menu.quick_left_item.delete", "Sürətli menyu elementini silmək", "Delete quick menu item"),
    _p("menu.quick_section.create", "Sürətli menyu bölməsi yaratmaq", "Create quick menu section"),
    _p("menu.quick_section.update", "Sürətli menyu bölməsini redaktə etmək", "Edit quick menu section"),
    _p("menu.quick_section.delete", "Sürətli menyu bölməsini silmək", "Delete quick menu section"),
    _p("menu.quick_section_item.create", "Sürətli menyu bölmə elementi yaratmaq", "Create quick section item"),
    _p("menu.quick_section_item.update", "Sürətli menyu bölmə elementini redaktə etmək", "Edit quick section item"),
    _p("menu.quick_section_item.delete", "Sürətli menyu bölmə elementini silmək", "Delete quick section item"),
    # ── menu_header ─────────────────────────────────────────────────────────
    _p("menu_header.create", "Başlıq menyusu yaratmaq", "Create header menu"),
    _p("menu_header.update", "Başlıq menyusunu redaktə etmək", "Edit header menu"),
    _p("menu_header.delete", "Başlıq menyusunu silmək", "Delete header menu"),
    _p("menu_header.item.create", "Başlıq menyu elementi yaratmaq", "Create header menu item"),
    _p("menu_header.item.update", "Başlıq menyu elementini redaktə etmək", "Edit header menu item"),
    _p("menu_header.item.delete", "Başlıq menyu elementini silmək", "Delete header menu item"),
    _p("menu_header.sub_item.create", "Başlıq alt-elementi yaratmaq", "Create header sub item"),
    _p("menu_header.sub_item.update", "Başlıq alt-elementini redaktə etmək", "Edit header sub item"),
    _p("menu_header.sub_item.delete", "Başlıq alt-elementini silmək", "Delete header sub item"),
    # ── chatbot_knowledge ───────────────────────────────────────────────────
    _p("chatbot_knowledge.read", "Bilik bazasına baxmaq", "View knowledge base"),
    _p("chatbot_knowledge.source.create", "Bilik mənbəyi əlavə etmək", "Add knowledge source"),
    _p("chatbot_knowledge.source.delete", "Bilik mənbəyini silmək", "Delete knowledge source"),
    _p("chatbot_knowledge.source.scrape", "Bilik mənbəyini yeniləmək", "Scrape knowledge source"),
    _p("chatbot_knowledge.scrape_all", "Bütün bilik mənbələrini yeniləmək", "Scrape all knowledge sources"),
    # ── chat ────────────────────────────────────────────────────────────────
    # Grants sight of visitor IP addresses. Kept out of every system role below:
    # only super_admin holds it implicitly, and it is assigned per role by hand.
    _p("chat.read", "Çat söhbətlərinə və statistikasına baxmaq", "View chat conversations and stats"),
    _p("chat.delete", "Çat söhbətini silmək", "Delete a chat conversation"),
    # ── search ──────────────────────────────────────────────────────────────
    _p("search.admin.read", "Admin axtarışından istifadə etmək", "Use admin search"),
    # ── roles ───────────────────────────────────────────────────────────────
    _p("roles.read", "Rollara baxmaq", "View roles"),
    _p("roles.create", "Rol yaratmaq", "Create role"),
    _p("roles.update", "Rolu redaktə etmək", "Edit role"),
    _p("roles.update_permissions", "Rolun icazələrini dəyişmək", "Edit role permissions"),
    _p("roles.delete", "Rolu silmək", "Delete role"),
    # ── admin_users ─────────────────────────────────────────────────────────
    _p("admin_users.read", "Admin istifadəçilərə baxmaq", "View admin users"),
    _p("admin_users.create", "Admin istifadəçi yaratmaq", "Create admin user"),
    _p("admin_users.update", "Admin istifadəçini redaktə etmək", "Edit admin user"),
    _p("admin_users.delete", "Admin istifadəçini silmək", "Delete admin user"),
    _p("admin_users.activate", "Admin istifadəçini aktivləşdirmək", "Activate admin user"),
    _p("admin_users.deactivate", "Admin istifadəçini deaktiv etmək", "Deactivate admin user"),
    _p("admin_users.reset_password", "Admin istifadəçinin şifrəsini dəyişmək", "Reset admin user password"),
    _p("admin_users.assign_role", "Admin istifadəçiyə rol təyin etmək", "Assign role to admin user"),
    # ── activity ────────────────────────────────────────────────────────────
    _p("activity.read", "Fəaliyyət jurnalına baxmaq", "View activity log"),
)


PERMISSION_KEYS = frozenset(p.key for p in PERMISSION_CATALOGUE)

PERMISSIONS_BY_KEY: Dict[str, PermissionDef] = {p.key: p for p in PERMISSION_CATALOGUE}

if len(PERMISSIONS_BY_KEY) != len(PERMISSION_CATALOGUE):
    raise RuntimeError("Duplicate key in PERMISSION_CATALOGUE")

_unlabelled = sorted({p.domain for p in PERMISSION_CATALOGUE} - set(DOMAIN_LABELS))
if _unlabelled:
    raise RuntimeError(f"Domains missing from DOMAIN_LABELS: {_unlabelled}")


def keys_for_domains(*domains: str) -> Tuple[str, ...]:
    wanted = set(domains)
    return tuple(p.key for p in PERMISSION_CATALOGUE if p.domain in wanted)


def _without(keys: Tuple[str, ...], *suffixes: str) -> Tuple[str, ...]:
    return tuple(k for k in keys if not any(k.endswith("." + s) for s in suffixes))


@dataclass(frozen=True)
class SystemRoleDef:
    code: str
    name_az: str
    name_en: str
    description_az: str
    permissions: Tuple[str, ...]      # () for super_admin — implicit all, zero grant rows
    implicit_all: bool = False


SYSTEM_ROLES: Tuple[SystemRoleDef, ...] = (
    SystemRoleDef(
        code=SUPER_ADMIN_CODE,
        name_az="Super admin",
        name_en="Super admin",
        description_az="Bütün icazələr. Redaktə və silinmə mümkün deyil.",
        permissions=(),
        implicit_all=True,
    ),
    SystemRoleDef(
        code="content_editor",
        name_az="Məzmun redaktoru",
        name_en="Content editor",
        description_az="Xəbər, elan, hero, layihə və əməkdaşlıqları idarə edir. Silmək icazəsi yoxdur.",
        permissions=_without(
            keys_for_domains("news", "news_categories", "announcements", "hero", "projects", "collaborations", "about"),
            "delete",
        ),
    ),
    SystemRoleDef(
        code="academic_editor",
        name_az="Akademik redaktor",
        name_en="Academic editor",
        description_az="Fakültə, kafedra, şöbə, elmi tədqiqat institutu və əməkdaş məlumatlarını tam idarə edir.",
        permissions=keys_for_domains(
            "faculties", "cafedras", "departments", "research_institutes", "employees",
        ),
    ),
    SystemRoleDef(
        code="viewer",
        name_az="Müşahidəçi",
        name_en="Viewer",
        description_az="Yalnız baxış: admin axtarışı və fəaliyyət jurnalı.",
        permissions=("search.admin.read", "activity.read"),
    ),
    # Chat transcripts expose visitor IPs, so this is deliberately its own role
    # rather than something bundled into viewer or content_editor — granting chat
    # access should be a decision, not a side effect of another role.
    SystemRoleDef(
        code="chat_moderator",
        name_az="Çat operatoru",
        name_en="Chat moderator",
        description_az="Çat söhbətlərinə, statistikasına və istifadəçi IP ünvanlarına baxır, sui-istifadə hallarını silir.",
        permissions=("chat.read", "chat.delete"),
    ),
)

SYSTEM_ROLES_BY_CODE: Dict[str, SystemRoleDef] = {r.code: r for r in SYSTEM_ROLES}

for _role in SYSTEM_ROLES:
    _bad = sorted(set(_role.permissions) - PERMISSION_KEYS)
    if _bad:
        raise RuntimeError(f"System role {_role.code!r} references unknown permissions: {_bad}")
