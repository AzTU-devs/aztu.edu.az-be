"""Seed the About-page registry and each page's section skeleton.

Usage:
    python -m app.scripts.seed_about_pages            # create what is missing
    python -m app.scripts.seed_about_pages --dry-run  # report, change nothing
    python -m app.scripts.seed_about_pages --sql      # print the equivalent SQL

Idempotent and strictly additive. A page or section that already exists is left
exactly as the editor left it — re-running this after adding a new page to
BLUEPRINT only creates the new rows.

`--sql` emits the same inserts as a standalone script for environments where the
migration is pasted into a database console rather than run from the app
container. It is generated from BLUEPRINT below, so the two cannot drift.

The blueprint mirrors, field for field, what each /about screen renders today
from the website's locale files. Seeding the *structure* (which blocks a page
has, in what order, of what type) is what lets the dashboard show the right form
per page on day one; the copy itself is then typed in by an editor.

Pages land with is_active = false, so nothing is exposed publicly until it is
explicitly published.
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.about.about_page import (
    AboutPage,
    AboutPageTr,
    AboutSection,
    AboutSectionTr,
)


def page(
    key: str,
    group: str,
    template: str,
    order: int,
    slug_az: str,
    slug_en: str,
    az: tuple[str, str, str],
    en: tuple[str, str, str],
    sections: list[tuple[str, str, str, str]],
) -> dict:
    """`az`/`en` are (eyebrow, title, breadcrumb); sections are (key, type, az, en)."""
    return {
        "page_key": key,
        "group_key": group,
        "template": template,
        "display_order": order,
        "slug_az": slug_az,
        "slug_en": slug_en,
        "az": {"eyebrow": az[0], "title": az[1], "breadcrumb": az[2]},
        "en": {"eyebrow": en[0], "title": en[1], "breadcrumb": en[2]},
        "sections": sections,
    }


RELATED = ("related", "links", "Bölmədə daha çox", "More in this section")


BLUEPRINT: list[dict] = [
    # ── Vizyon və Missiya ─────────────────────────────────────────────────
    page(
        "history", "vision_mission", "history", 1,
        "vizyon-ve-missiya/aztu-nun-tarixi", "vision-mission/history-of-aztu",
        ("Mirasımız", "AzTU-nun Tarixi", "Tarix"),
        ("Our Legacy", "History of AzTU", "History"),
        [
            ("milestones", "timeline", "Əsas Mərhələlər", "Key Milestones"),
            ("stats", "stats", "Rəqəmlərlə AzTU", "AzTU in Numbers"),
            RELATED,
        ],
    ),
    page(
        "vision", "vision_mission", "statement", 2,
        "vizyon-ve-missiya/vizyon", "vision-mission/vision",
        ("İstiqamətimiz", "Vizyon", "Vizyon"),
        ("Our Direction", "Vision", "Vision"),
        [
            ("statement", "quote", "Vizyon Bəyanatımız", "Our Vision Statement"),
            RELATED,
        ],
    ),
    page(
        "mission", "vision_mission", "statement", 3,
        "vizyon-ve-missiya/missiya", "vision-mission/mission",
        ("Məqsədimiz", "Missiya", "Missiya"),
        ("Our Purpose", "Mission", "Mission"),
        [
            ("statement", "quote", "Missiya Bəyanatımız", "Our Mission Statement"),
            RELATED,
        ],
    ),
    page(
        "strategic-plan", "vision_mission", "strategic_plan", 4,
        "vizyon-ve-missiya/strateji-plan", "vision-mission/strategic-plan",
        ("Vizyon 2030", "Strateji İnkişaf Planı", "Strateji Plan"),
        ("Vision 2030", "Strategic Development Plan", "Strategic Plan"),
        [
            # Uploaded from the dashboard, with a separate AZ and EN file.
            ("document", "documents", "Plan sənədi", "Plan document"),
            ("vision", "paragraphs", "Vizyon", "Vision"),
            ("mission", "paragraphs", "Missiya", "Mission"),
            ("pillars", "pillars", "Strateji Sütunlar", "Strategic Pillars"),
            ("values", "list", "Korporativ Dəyərlər", "Corporate Values"),
            ("targets", "list", "Əsas Performans Göstəriciləri (KPI)", "Key Performance Indicators (KPI)"),
            RELATED,
        ],
    ),
    page(
        "anniversary-film", "vision_mission", "video", 5,
        "vizyon-ve-missiya/75-illik-yubiley-filmi", "vision-mission/75th-anniversary-film",
        ("Tədbir", "75 İllik Yubiley Filmi", "Yubiley Filmi"),
        ("Event", "75th Anniversary Film", "Anniversary Film"),
        [
            ("film", "video", "Film", "Film"),
            RELATED,
        ],
    ),
    page(
        "vision-mission-goal", "vision_mission", "statement", 6,
        "vizyon-ve-missiya/vizyon-missiya-meqsed", "vision-mission/vision-mission-goal",
        ("Kimliyimiz", "Vizyon, Missiya və Məqsəd", "Vizyon, Missiya və Məqsəd"),
        ("Our Identity", "Vision, Mission & Goal", "Vision, Mission & Goal"),
        [
            ("mission", "paragraphs", "Missiya", "Mission"),
            ("vision", "paragraphs", "Vizyon", "Vision"),
            ("goal", "paragraphs", "Məqsəd", "Goal"),
            RELATED,
        ],
    ),

    # ── Rəhbərlik və İdarəetmə ────────────────────────────────────────────
    page(
        "rector", "leadership", "rector", 10,
        "rehbetlik-ve-idareetme/rektor", "leadership-and-management/rector",
        ("Rəhbərlik və İdarəetmə", "Rektor", "Rektor"),
        ("Leadership & Governance", "Rector", "Rector"),
        [
            # The rector himself: name, degree, position, e-mail and photo,
            # which the hero renders above everything else.
            ("profile", "people", "Rektor", "Rector"),
            # The two figures beside the portrait — academic degree and years
            # of experience — as label/value pairs.
            ("highlights", "facts", "Əsas göstəricilər", "At a glance"),
            # One rich-text field, not three blocks: on the site the greeting,
            # the priority list and the sign-off are a single letter, and an
            # editor needs to control the spacing between its paragraphs.
            ("message", "paragraphs", "Rektorun Müraciəti", "Message from the Rector"),
            ("about_rector", "paragraphs", "Rektor haqqında", "About the Rector"),
            ("responsibilities", "list", "Vəzifə Öhdəlikləri", "Responsibilities"),
            # Heading + rich-text lead + the list of units underneath it.
            ("departments", "list", "Rektora tabe olan strukturlar", "Units Reporting to the Rector"),
            ("gallery", "gallery", "Rektorun Qalereyası", "Rector's Gallery"),
            RELATED,
        ],
    ),
    page(
        "vice-rector", "leadership", "people", 11,
        "vice-rector", "vice-rector",
        ("Rəhbərlik və İdarəetmə", "Prorektorlar", "Prorektorlar"),
        ("Leadership & Governance", "Vice-Rectors", "Vice-Rectors"),
        [
            ("overview", "paragraphs", "Ümumi məlumat", "Overview"),
            ("vice_rectors", "people", "Prorektorlar", "Vice-Rectors"),
            # Button and heading strings the detail page renders around a person.
            ("labels", "list", "İnterfeys mətnləri", "Interface labels"),
            RELATED,
        ],
    ),
    page(
        "rectors-office", "leadership", "people", 12,
        "rectors-office", "rectors-office",
        ("Rəhbərlik və İdarəetmə", "Rektorat", "Rektorat"),
        ("Leadership & Governance", "Rector's Office", "Rectorate"),
        [
            ("staff", "people", "Rektorat heyəti", "Rectorate Staff"),
        ],
    ),
    page(
        "scientific-board", "leadership", "board", 13,
        "scientific-board", "scientific-board",
        ("Rəhbərlik və İdarəetmə", "Elmi Şura", "Elmi Şura"),
        ("Leadership & Governance", "Scientific Board", "Scientific Board"),
        [
            ("about", "paragraphs", "Şura haqqında", "About the Board"),
            ("scientific_council", "table", "Elmi Şuranın tərkibi", "Scientific Board Members"),
            ("digital_council", "table", "Rəqəmsal Şura", "Digital Council"),
            ("digital_council_secretariat", "table", "Katiblik", "Secretariat"),
            RELATED,
        ],
    ),

    # ── Bağlı Qurumlar ────────────────────────────────────────────────────
    page(
        "tau", "affiliated", "entity", 20,
        "tau", "tau",
        ("Bağlı Qurum", "Türkiyə–Azərbaycan Universiteti", "TAU"),
        ("Affiliated Entity", "Türkiye–Azerbaijan University", "TAU"),
        [
            ("about", "paragraphs", "TAU haqqında", "About TAU"),
            ("programmes", "list", "Təklif edilən proqramlar", "Programmes Offered"),
            ("facts", "facts", "Qısa məlumat", "Key Facts"),
            RELATED,
        ],
    ),
    page(
        "iit", "affiliated", "entity", 21,
        "iit", "iit",
        ("Bağlı Qurum", "İnformasiya Texnologiyaları İnstitutu", "İTİ"),
        ("Affiliated Entity", "Institute of Information Technology", "IIT"),
        [
            ("about", "paragraphs", "İnstitut haqqında", "About the Institute"),
            RELATED,
        ],
    ),
    page(
        "ics", "affiliated", "entity", 22,
        "ics", "ics",
        ("Bağlı Qurum", "İdarəetmə Sistemləri İnstitutu", "İSİ"),
        ("Affiliated Entity", "Institute of Control Systems", "ICS"),
        [
            ("about", "paragraphs", "İnstitut haqqında", "About the Institute"),
            RELATED,
        ],
    ),
    page(
        "baku-technical-colleges", "affiliated", "entity", 23,
        "baku-technical-colleges", "baku-technical-colleges",
        ("Bağlı Qurum", "Bakı Texniki Kolleci", "Bakı Texniki Kolleci"),
        ("Affiliated Entity", "Baku Technical College", "Technical College"),
        [
            ("about", "paragraphs", "Kollec haqqında", "About the College"),
            RELATED,
        ],
    ),
    page(
        "baku-state-colleges", "affiliated", "entity", 24,
        "baku-state-colleges", "baku-state-colleges",
        ("Bağlı Qurum", "Bakı Dövlət Rabitə və Nəqliyyat Kolleci", "BDRNK"),
        ("Affiliated Entity", "Baku State College of Communication and Transport", "Communication College"),
        [
            ("about", "paragraphs", "Kollec haqqında", "About the College"),
            RELATED,
        ],
    ),

    # ── Siyasətlər və Sənədlər ────────────────────────────────────────────
    page(
        "general-policies", "policies", "policy_library", 30,
        "normativ-senedler/siyaset-senedleri", "regulatory-documents/policy-documents",
        ("Normativ Sənədlər", "Ümumi Siyasətlər", "Ümumi Siyasətlər"),
        ("Regulatory Documents", "General Policies", "General Policies"),
        [
            ("categories", "list", "Kateqoriyalar", "Categories"),
            ("documents", "documents", "Siyasət sənədləri", "Policy Documents"),
        ],
    ),
    page(
        "academic-policies", "policies", "policy_pdf", 31,
        "academic-policies", "academic-policies",
        ("Siyasətlər və Sənədlər", "Akademik Siyasətlər", "Akademik Siyasətlər"),
        ("Policies & Documents", "Academic Policies", "Academic Policies"),
        [
            ("document", "documents", "Sənəd", "Document"),
        ],
    ),
    page(
        "sustainability-policies", "policies", "policy_pdf", 32,
        "sustainability-policies", "sustainability-policies",
        ("Siyasətlər və Sənədlər", "Davamlılıq Siyasətləri", "Davamlılıq Siyasətləri"),
        ("Policies & Documents", "Sustainability Policies", "Sustainability Policies"),
        [
            ("document", "documents", "Sənəd", "Document"),
        ],
    ),
    page(
        "procedure-guidelines", "policies", "policy_pdf", 33,
        "procedure-guidelines", "procedure-guidelines",
        ("Siyasətlər və Sənədlər", "Prosedurlar və Qaydalar", "Prosedurlar və Qaydalar"),
        ("Policies & Documents", "Procedures & Guidelines", "Procedures & Guidelines"),
        [
            ("document", "documents", "Sənəd", "Document"),
        ],
    ),
    page(
        "sustainability-documents", "policies", "policy_library", 34,
        "sustainability-documents", "sustainability-documents",
        ("Normativ Sənədlər", "Davamlılıq Sənədləri", "Davamlılıq Sənədləri"),
        ("Regulatory Documents", "Sustainability Documents", "Sustainability Documents"),
        [
            ("documents", "documents", "Sənədlər", "Documents"),
        ],
    ),
    page(
        "accreditation", "policies", "accreditation", 35,
        "accreditation", "accreditation",
        ("Haqqımızda", "Akkreditasiya", "Akkreditasiya"),
        ("About", "Accreditation", "Accreditation"),
        [
            ("what", "paragraphs", "Akkreditasiya nədir?", "What is accreditation?"),
            ("importance", "list", "Akkreditasiyanın əhəmiyyəti", "Why accreditation matters"),
            ("legal", "list", "Hüquqi əsaslar", "Legal basis"),
            ("institutional", "list", "İnstitusional akkreditasiya", "Institutional accreditation"),
            ("institutional_links", "links", "İnstitusional akkreditasiya sənədləri", "Institutional accreditation documents"),
            ("program", "list", "Proqram akkreditasiyası", "Program accreditation"),
            ("aqas", "list", "Beynəlxalq akkreditasiya – AQAS", "International accreditation – AQAS"),
            ("aqas_programs", "gallery", "AQAS akkreditasiyalı proqramlar", "AQAS-accredited programmes"),
            ("process", "list", "Akkreditasiya prosesi", "The accreditation process"),
            ("reports", "documents", "Proqram akkreditasiyası yekun hesabatları", "Program accreditation final reports"),
            ("certificates", "documents", "Proqram akkreditasiyası sertifikatları", "Program accreditation certificates"),
            ("iso", "list", "ISO standartları", "ISO standards"),
        ],
    ),

    # ── Reytinqlər və proqramlar ──────────────────────────────────────────
    page(
        "rankings", "other", "rankings", 40,
        "reytinqler", "rankings",
        ("Reytinqlər", "Beynəlxalq Reytinqlər", "Reytinqlər"),
        ("Rankings", "International Rankings", "Rankings"),
        [
            ("importance", "list", "Əhəmiyyəti", "Why rankings matter"),
            ("systems", "ranking_systems", "Reytinq sistemləri", "Ranking Systems"),
            ("positions", "ranking_positions", "Beynəlxalq Reytinqlərdə Mövqeyimiz", "Our Positions in International Rankings"),
            ("profile", "links", "Universitet profilləri", "University Profiles"),
        ],
    ),
    page(
        "hei", "other", "institute", 41,
        "hei", "hei",
        ("Təhsil və Proqramlar", "Yüksək Təhsil İnstitutu (YTİ)", "Yüksək Təhsil İnstitutu"),
        ("Education and Programs", "Higher Education Institute (HEI)", "Higher Education Institute"),
        [
            ("about", "paragraphs", "İnstitut haqqında", "About the Institute"),
            ("mission", "paragraphs", "Missiya və strateji istiqamətlər", "Mission and strategic direction"),
            ("strategic_directions", "list", "Strateji istiqamətlər", "Strategic directions"),
            ("academic_opportunities", "list", "Təhsil imkanları", "Academic opportunities"),
            ("academic_languages", "list", "Tədris dilləri", "Languages of instruction"),
            ("research", "list", "Elmi-tədqiqat fəaliyyəti", "Research activity"),
            ("doctoral", "paragraphs", "Doktorantura təhsili", "Doctoral studies"),
            ("doctoral_formats", "list", "Doktorantura formaları", "Doctoral study formats"),
            ("doctoral_duration", "group_list", "Təhsil müddəti", "Programme duration"),
            ("director", "people", "Direktor", "Director"),
            ("staff", "people", "Əməkdaşlar", "Staff"),
            ("contact", "contact", "Əlaqə", "Contact"),
            ("board_duties", "list", "İdarə Heyətinin vəzifələri", "Board duties"),
            ("board_rights", "list", "İdarə Heyətinin hüquqları", "Board rights"),
            ("board_composition", "list", "İdarə Heyətinin tərkibi", "Board composition"),
            ("board_requirements", "list", "İdarə Heyətinin üzvlərinə olan tələblər", "Requirements for board members"),
            ("board_chairman", "paragraphs", "İdarə Heyətinin sədri", "Chair of the Board"),
            RELATED,
        ],
    ),
    page(
        "mba", "other", "programme", 42,
        "mba", "mba",
        ("Təhsil və Proqramlar", "MBA Proqramı", "MBA"),
        ("Education and Programs", "MBA Program", "MBA"),
        [
            ("about", "paragraphs", "MBA Proqramı Haqqında", "About the MBA Program"),
            ("stats", "stats", "Proqramın Əsas Göstəriciləri", "Program at a Glance"),
            ("languages", "list", "Tədris Dilləri", "Languages of Instruction"),
            ("structure", "list", "Proqramın Strukturu", "Program Structure"),
            ("doctoral", "paragraphs", "Doktorantura İstiqamətləri", "Doctoral Pathways"),
            ("doctoral_formats", "list", "Doktorantura formaları", "Doctoral study formats"),
            ("doctoral_duration", "group_list", "Təhsil Müddəti", "Programme duration"),
            ("contact", "contact", "Əlaqə", "Contact"),
            RELATED,
        ],
    ),

    # ── İdarəetmə → Ofis və Mərkəzlər ─────────────────────────────────────
    # The header's Management dropdown has two halves. "Struktur bölmələr"
    # already reads the departments API and is edited under Departamentlər;
    # these seven screens were the static half, so they move here.
    #
    # They share one shape — about / objectives / functions / head / staff /
    # contact — with a few page-specific blocks on top, which is exactly what
    # this block model already expresses.
    page(
        "tto", "offices", "office", 50,
        "idareetme/ofis-ve-merkezler/texnaloji-transfer-ofisi-tto",
        "management/offices-and-centers/technology-transfer-office",
        ("İdarəetmə", "Texnoloji Transfer Ofisi", "Texnoloji Transfer Ofisi"),
        ("Management", "Technology Transfer Office", "Technology Transfer Office"),
        [
            ("about", "paragraphs", "Haqqında", "About"),
            ("objectives", "list", "Məqsədlər", "Objectives"),
            ("functions", "cards", "Əsas Funksiyalar", "Key Functions"),
            ("partnerships", "table", "Tərəfdaşlıq və Ekosistem", "Partnerships and Ecosystem"),
            ("international", "cards", "Beynəlxalq Əməkdaşlıq", "International Cooperation"),
            ("innovation", "table", "İnnovasiya Tərəfdaşları", "Innovation Partners"),
            ("head", "people", "Rəhbər", "Head of Office"),
            ("staff", "people", "Əməkdaşlar", "Staff"),
            ("contact", "contact", "Əlaqə", "Contact"),
        ],
    ),
    page(
        "qatim", "offices", "office", 51,
        "idareetme/ofis-ve-merkezler/qatim",
        "management/offices-and-centers/qatim",
        ("İdarəetmə", "Keyfiyyətin Təminatı və Öyrənmə-Öyrətmə Mərkəzi", "QATİM"),
        ("Management", "Quality Assurance and Teaching-Learning Centre", "QATIM"),
        [
            ("about", "paragraphs", "Haqqında", "About"),
            ("objectives", "list", "Məqsədlər", "Objectives"),
            ("functions", "cards", "Əsas Funksiyalar", "Key Functions"),
            ("head", "people", "Rəhbər", "Head of Centre"),
            ("staff", "people", "Əməkdaşlar", "Staff"),
            ("contact", "contact", "Əlaqə", "Contact"),
        ],
    ),
    page(
        "sabah-center", "offices", "office", 52,
        "idareetme/ofis-ve-merkezler/sabah-merkezi",
        "management/offices-and-centers/sabah-center",
        ("İdarəetmə", "SABAH Mərkəzi", "SABAH Mərkəzi"),
        ("Management", "SABAH Centre", "SABAH Centre"),
        [
            ("about", "paragraphs", "Haqqında", "About"),
            ("objectives", "list", "Məqsədlər", "Objectives"),
            ("functions", "cards", "Əsas Funksiyalar", "Key Functions"),
            ("head", "people", "Rəhbər", "Head of Centre"),
            ("staff", "people", "Əməkdaşlar", "Staff"),
            ("contact", "contact", "Əlaqə", "Contact"),
        ],
    ),
    page(
        "career-center", "offices", "office", 53,
        "idareetme/ofis-ve-merkezler/karyera-ve-mesgulluq-merkezi",
        "management/offices-and-centers/career-and-employment-center",
        ("İdarəetmə", "Karyera və Məşğulluq Mərkəzi", "Karyera Mərkəzi"),
        ("Management", "Career and Employment Centre", "Career Centre"),
        [
            ("about", "paragraphs", "Haqqında", "About"),
            ("objectives", "list", "Məqsədlər", "Objectives"),
            ("functions", "cards", "Əsas Funksiyalar", "Key Functions"),
            ("head", "people", "Rəhbər", "Head of Centre"),
            ("staff", "people", "Əməkdaşlar", "Staff"),
            ("statute", "documents", "Əsasnamə", "Statute"),
            ("contact", "contact", "Əlaqə", "Contact"),
        ],
    ),
    page(
        "lifelong-learning", "offices", "office", 54,
        "idareetme/ofis-ve-merkezler/omurboyu-tehsil",
        "management/offices-and-centers/lifelong-learning",
        ("İdarəetmə", "Ömürboyu Təhsil Mərkəzi", "Ömürboyu Təhsil"),
        ("Management", "Lifelong Learning Centre", "Lifelong Learning"),
        [
            ("about", "paragraphs", "Haqqında", "About"),
            ("objectives", "list", "Məqsədlər", "Objectives"),
            # Plain strings on this page, unlike the title+description cards
            # the other offices use.
            ("functions", "list", "Əsas Funksiyalar", "Key Functions"),
            ("staff", "people", "Əməkdaşlar", "Staff"),
            ("statute", "documents", "Əsasnamə", "Statute"),
            ("contact", "contact", "Əlaqə", "Contact"),
        ],
    ),
    page(
        "library", "offices", "office", 55,
        "idareetme/ofis-ve-merkezler/kitabxana-informasiya-merkezi",
        "management/offices-and-centers/library-and-information-center",
        ("İdarəetmə", "Kitabxana-İnformasiya Mərkəzi", "Kitabxana"),
        ("Management", "Library and Information Centre", "Library"),
        [
            ("about", "paragraphs", "Haqqında", "About"),
            ("departments", "list", "Şöbələr", "Departments"),
            ("technical", "list", "Texniki proseslər", "Technical processes"),
            ("dls", "list", "Elektron kitabxana xidmətləri", "Digital library services"),
            ("info_services", "list", "İnformasiya xidmətləri", "Information services"),
            ("activities", "list", "Fəaliyyətlər", "Activities"),
            ("purpose", "paragraphs", "Məqsəd", "Purpose"),
            ("report", "paragraphs", "Hesabat", "Report"),
            ("visitors", "stats", "Ziyarətçi statistikası", "Visitor statistics"),
            ("databases", "list", "Elektron bazalar", "Databases"),
            ("email_queries", "paragraphs", "Elektron sorğular", "Email queries"),
            ("head", "people", "Rəhbər", "Head of Centre"),
            ("staff", "people", "Əməkdaşlar", "Staff"),
            ("contact", "contact", "Əlaqə", "Contact"),
        ],
    ),
    page(
        "nabran", "offices", "office", 56,
        "idareetme/ofis-ve-merkezler/nabran-istirahet-merkezi",
        "management/offices-and-centers/nabran-recreation-center",
        ("İdarəetmə", "Nabran İstirahət Mərkəzi", "Nabran"),
        ("Management", "Nabran Recreation Centre", "Nabran"),
        [
            ("about", "paragraphs", "Haqqında", "About"),
            ("stats", "stats", "Mərkəz haqqında", "At a glance"),
            ("facilities", "list", "İmkanlar", "Facilities"),
            ("gallery", "gallery", "Foto Qalereya", "Photo Gallery"),
            ("contact", "contact", "Əlaqə", "Contact"),
        ],
    ),
]


async def seed(dry_run: bool = False) -> None:
    now = datetime.now(timezone.utc)
    created_pages = 0
    created_sections = 0

    async with AsyncSessionLocal() as db:
        for spec in BLUEPRINT:
            existing = (
                await db.execute(
                    select(AboutPage).where(AboutPage.page_key == spec["page_key"])
                )
            ).scalar_one_or_none()

            if existing is None:
                print(f"+ page   {spec['page_key']}")
                created_pages += 1
                if dry_run:
                    # Without the row there is no id to hang sections off, so the
                    # dry run reports them all as pending and moves on.
                    for section_key, section_type, _, _ in spec["sections"]:
                        print(f"    + section {section_key} ({section_type})")
                        created_sections += 1
                    continue

                existing = AboutPage(
                    page_key=spec["page_key"],
                    group_key=spec["group_key"],
                    template=spec["template"],
                    slug_az=spec["slug_az"],
                    slug_en=spec["slug_en"],
                    display_order=spec["display_order"],
                    is_active=False,
                    created_at=now,
                    updated_at=now,
                )
                db.add(existing)
                await db.flush()

                for lang in ("az", "en"):
                    db.add(
                        AboutPageTr(
                            page_id=existing.id,
                            lang_code=lang,
                            eyebrow=spec[lang]["eyebrow"],
                            title=spec[lang]["title"],
                            breadcrumb=spec[lang]["breadcrumb"],
                            created_at=now,
                            updated_at=now,
                        )
                    )

            present = set(
                (
                    await db.execute(
                        select(AboutSection.section_key).where(
                            AboutSection.page_id == existing.id
                        )
                    )
                )
                .scalars()
                .all()
            )

            for order, (section_key, section_type, az_title, en_title) in enumerate(
                spec["sections"], start=1
            ):
                if section_key in present:
                    continue

                print(f"    + section {spec['page_key']}/{section_key} ({section_type})")
                created_sections += 1
                if dry_run:
                    continue

                section = AboutSection(
                    page_id=existing.id,
                    section_key=section_key,
                    section_type=section_type,
                    display_order=order,
                    is_active=True,
                    created_at=now,
                    updated_at=now,
                )
                db.add(section)
                await db.flush()

                for lang, title in (("az", az_title), ("en", en_title)):
                    db.add(
                        AboutSectionTr(
                            section_id=section.id,
                            lang_code=lang,
                            title=title,
                            created_at=now,
                            updated_at=now,
                        )
                    )

        if dry_run:
            await db.rollback()
        else:
            await db.commit()

    verb = "would create" if dry_run else "created"
    print(f"\n{verb}: {created_pages} page(s), {created_sections} section(s)")


def _q(value: str | None) -> str:
    """SQL string literal, with embedded quotes doubled ("Rector's Office")."""
    if value is None:
        return "null"
    return "'" + value.replace("'", "''") + "'"


def emit_sql() -> str:
    """The blueprint as a standalone, idempotent SQL script.

    Every insert is guarded by the unique constraint the migration already
    created, so re-running it is a no-op and an editor's existing copy is never
    overwritten.
    """
    out: list[str] = [
        "-- =====================================================================",
        "-- SEED — About page registry and section skeleton",
        "--",
        "-- Generated by `python -m app.scripts.seed_about_pages --sql`.",
        "-- Do not edit by hand; change BLUEPRINT in that script and regenerate.",
        "--",
        "-- Run AFTER migrations_about_pages.sql, in one psql session. Every",
        "-- statement is idempotent: existing pages and sections are left exactly",
        "-- as an editor left them, so this is safe to re-run after new pages are",
        "-- added to the blueprint.",
        "--",
        "-- Pages land with is_active = false — nothing is public until it is",
        "-- explicitly published from the dashboard.",
        "-- =====================================================================",
        "",
    ]

    for spec in BLUEPRINT:
        key = spec["page_key"]
        out.append(f"-- ── {key} " + "─" * max(0, 60 - len(key)))
        out.append(
            "insert into about_pages "
            "(page_key, group_key, template, slug_az, slug_en, display_order, is_active)\n"
            f"values ({_q(key)}, {_q(spec['group_key'])}, {_q(spec['template'])}, "
            f"{_q(spec['slug_az'])}, {_q(spec['slug_en'])}, {spec['display_order']}, false)\n"
            "on conflict (page_key) do nothing;"
        )

        for lang in ("az", "en"):
            tr = spec[lang]
            out.append(
                "insert into about_page_tr (page_id, lang_code, eyebrow, title, breadcrumb)\n"
                f"select p.id, {_q(lang)}, {_q(tr['eyebrow'])}, {_q(tr['title'])}, {_q(tr['breadcrumb'])}\n"
                f"from about_pages p where p.page_key = {_q(key)}\n"
                "on conflict (page_id, lang_code) do nothing;"
            )

        for order, (section_key, section_type, az_title, en_title) in enumerate(
            spec["sections"], start=1
        ):
            out.append(
                "insert into about_sections "
                "(page_id, section_key, section_type, display_order, is_active)\n"
                f"select p.id, {_q(section_key)}, {_q(section_type)}, {order}, true\n"
                f"from about_pages p where p.page_key = {_q(key)}\n"
                "on conflict (page_id, section_key) do nothing;"
            )
            for lang, title in (("az", az_title), ("en", en_title)):
                out.append(
                    "insert into about_section_tr (section_id, lang_code, title)\n"
                    f"select s.id, {_q(lang)}, {_q(title)}\n"
                    "from about_sections s join about_pages p on p.id = s.page_id\n"
                    f"where p.page_key = {_q(key)} and s.section_key = {_q(section_key)}\n"
                    "on conflict (section_id, lang_code) do nothing;"
                )
        out.append("")

    total_sections = sum(len(spec["sections"]) for spec in BLUEPRINT)
    out += [
        "-- =====================================================================",
        "-- VERIFY",
        "-- =====================================================================",
        f"-- Expect {len(BLUEPRINT)} pages and {total_sections} sections.",
        "select (select count(*) from about_pages)    as pages,",
        "       (select count(*) from about_sections) as sections;",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the About-page registry.")
    parser.add_argument("--dry-run", action="store_true", help="Report only; write nothing.")
    parser.add_argument(
        "--sql", action="store_true", help="Print the equivalent SQL instead of connecting."
    )
    args = parser.parse_args()

    if args.sql:
        print(emit_sql())
        return

    asyncio.run(seed(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
