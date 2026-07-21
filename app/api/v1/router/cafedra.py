from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.utils.language import get_language
from app.core.auth_dependency import require_admin
from app.models.admin.admin_user import AdminUser
from app.api.v1.schema.cafedra import (
    CreateCafedra,
    UpdateCafedra,
    LaboratoryItem,
    UpdateLaboratory,
    Worker,
    UpdateWorker,
    DeputyDirector,
    UpdateDeputyDirector,
    ScientificCouncilMember,
    UpdateCouncilMember,
    RichTextSectionItem,
    UpdateRichTextSectionItem,
    ProjectGrantItem,
    UpdateProjectGrantItem,
    PartnerCompanyItem,
    UpdatePartnerCompanyItem,
    PublicationItem,
    UpdatePublicationItem,
    PatentItem,
    UpdatePatentItem,
    UpdateScientificIntros,
    ReorderRequest,
)
from app.services.cafedra import (
    create_cafedra,
    delete_cafedra,
    get_cafedra,
    get_cafedras,
    update_cafedra,
    upload_cafedra_director_image,
    upload_cafedra_deputy_director_image,
    upload_cafedra_worker_image,
    create_laboratory,
    get_all_laboratories,
    get_laboratory,
    get_cafedra_laboratories,
    upload_laboratory_image,
    upload_laboratory_gallery_image,
    delete_laboratory_gallery_image,
    create_worker,
    update_worker,
    delete_worker,
    create_deputy_director,
    update_deputy_director,
    delete_deputy_director,
    create_council_member,
    update_council_member,
    delete_council_member,
    update_laboratory,
    delete_laboratory,
    get_cafedra_scientific_activity,
    update_scientific_intros,
    create_research_area,
    update_research_area,
    delete_research_area,
    create_project,
    update_project,
    delete_project,
    create_partner_company,
    update_partner_company,
    delete_partner_company,
    upload_partner_company_logo,
    create_publication,
    create_patent,
    update_publication,
    update_patent,
    delete_publication,
    delete_patent,
    reorder_publications,
    reorder_patents,
)

router = APIRouter()


@router.get("/admin/all")
async def get_cafedras_endpoint_admin(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: str | None = Query(None),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await get_cafedras(
        start=start,
        end=end,
        faculty_code=faculty_code,
        lang=lang,
        db=db,
    )


@router.get("/public/all")
async def get_cafedras_endpoint_public(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    faculty_code: str | None = Query(None),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedras(
        start=start,
        end=end,
        faculty_code=faculty_code,
        lang=lang,
        db=db,
    )


@router.get("/laboratories/all")
async def get_all_laboratories_endpoint(
    start: int = Query(0, ge=0, description="Start index"),
    end: int = Query(10, gt=0, description="End index"),
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_laboratories(
        start=start,
        end=end,
        lang=lang,
        db=db,
    )


@router.get("/laboratories/{laboratory_id}")
async def get_laboratory_endpoint(
    laboratory_id: int,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_laboratory(
        laboratory_id=laboratory_id,
        lang=lang,
        db=db,
    )


@router.put("/research-areas/{item_id}")
async def update_research_area_endpoint(
    item_id: int,
    request: UpdateRichTextSectionItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_research_area(
        item_id=item_id,
        request=request,
        db=db,
    )


@router.delete("/research-areas/{item_id}")
async def delete_research_area_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_research_area(
        item_id=item_id,
        db=db,
    )


@router.put("/projects/{item_id}")
async def update_project_endpoint(
    item_id: int,
    request: UpdateProjectGrantItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_project(
        item_id=item_id,
        request=request,
        db=db,
    )


@router.delete("/projects/{item_id}")
async def delete_project_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_project(
        item_id=item_id,
        db=db,
    )


@router.put("/partner-companies/{item_id}/logo")
async def upload_partner_company_logo_endpoint(
    item_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_partner_company_logo(
        item_id=item_id,
        image=image,
        db=db,
    )


@router.put("/partner-companies/{item_id}")
async def update_partner_company_endpoint(
    item_id: int,
    request: UpdatePartnerCompanyItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_partner_company(
        item_id=item_id,
        request=request,
        db=db,
    )


@router.delete("/partner-companies/{item_id}")
async def delete_partner_company_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_partner_company(
        item_id=item_id,
        db=db,
    )


@router.put("/publications/{item_id}")
async def update_publication_endpoint(
    item_id: int,
    request: UpdatePublicationItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_publication(
        item_id=item_id,
        request=request,
        db=db,
    )


@router.delete("/publications/{item_id}")
async def delete_publication_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_publication(
        item_id=item_id,
        db=db,
    )


@router.get("/{cafedra_code}")
async def get_cafedra_details_endpoint(
    cafedra_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedra(
        cafedra_code=cafedra_code,
        lang_code=lang_code,
        db=db,
    )


@router.get("/{cafedra_code}/laboratories")
async def get_cafedra_laboratories_endpoint(
    cafedra_code: str,
    lang: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedra_laboratories(
        cafedra_code=cafedra_code,
        lang=lang,
        db=db,
    )


@router.get("/{cafedra_code}/scientific-activity")
async def get_cafedra_scientific_activity_endpoint(
    cafedra_code: str,
    lang_code: str = Depends(get_language),
    db: AsyncSession = Depends(get_db),
):
    return await get_cafedra_scientific_activity(
        cafedra_code=cafedra_code,
        lang_code=lang_code,
        db=db,
    )


@router.put("/{cafedra_code}/scientific-activity/intros")
async def update_scientific_intros_endpoint(
    cafedra_code: str,
    request: UpdateScientificIntros,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_scientific_intros(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.post("/{cafedra_code}/research-areas")
async def create_research_area_endpoint(
    cafedra_code: str,
    request: RichTextSectionItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_research_area(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.post("/{cafedra_code}/projects")
async def create_project_endpoint(
    cafedra_code: str,
    request: ProjectGrantItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_project(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.post("/{cafedra_code}/partner-companies")
async def create_partner_company_endpoint(
    cafedra_code: str,
    request: PartnerCompanyItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_partner_company(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.post("/{cafedra_code}/publications")
async def create_publication_endpoint(
    cafedra_code: str,
    request: PublicationItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_publication(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.put("/{cafedra_code}/publications/reorder")
async def reorder_publications_endpoint(
    cafedra_code: str,
    request: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_publications(
        cafedra_code=cafedra_code,
        ids=request.ids,
        db=db,
    )


@router.post("/create")
async def create_cafedra_endpoint(
    request: CreateCafedra,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_cafedra(
        request=request,
        db=db,
    )


@router.post("/{cafedra_code}/laboratories")
async def create_laboratory_endpoint(
    cafedra_code: str,
    request: LaboratoryItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_laboratory(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.put("/{cafedra_code}")
async def update_cafedra_endpoint(
    cafedra_code: str,
    request: UpdateCafedra,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_cafedra(
        cafedra_code=cafedra_code,
        request=request,
        db=db,
    )


@router.delete("/{cafedra_code}")
async def delete_cafedra_endpoint(
    cafedra_code: str,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_cafedra(
        cafedra_code=cafedra_code,
        db=db,
    )


@router.put("/{cafedra_code}/director/image")
async def upload_cafedra_director_image_endpoint(
    cafedra_code: str,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_cafedra_director_image(
        cafedra_code=cafedra_code,
        image=image,
        db=db,
    )


@router.put("/deputy-directors/{deputy_director_id}/image")
async def upload_cafedra_deputy_director_image_endpoint(
    deputy_director_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_cafedra_deputy_director_image(
        deputy_director_id=deputy_director_id,
        image=image,
        db=db,
    )


@router.put("/workers/{worker_id}/image")
async def upload_cafedra_worker_image_endpoint(
    worker_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_cafedra_worker_image(
        worker_id=worker_id,
        image=image,
        db=db,
    )


@router.put("/laboratories/{laboratory_id}/image")
async def upload_laboratory_image_endpoint(
    laboratory_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_laboratory_image(
        laboratory_id=laboratory_id,
        image=image,
        db=db,
    )


@router.post("/laboratories/{laboratory_id}/gallery")
async def upload_laboratory_gallery_image_endpoint(
    laboratory_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await upload_laboratory_gallery_image(
        laboratory_id=laboratory_id,
        image=image,
        db=db,
    )


@router.delete("/laboratories/gallery/{gallery_image_id}")
async def delete_laboratory_gallery_image_endpoint(
    gallery_image_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_laboratory_gallery_image(
        gallery_image_id=gallery_image_id,
        db=db,
    )


# ── Standalone personnel CRUD ────────────────────────────────────────────────────


@router.post("/{cafedra_code}/workers")
async def create_worker_endpoint(
    cafedra_code: str,
    request: Worker,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_worker(cafedra_code=cafedra_code, request=request, db=db)


@router.put("/workers/{worker_id}")
async def update_worker_endpoint(
    worker_id: int,
    request: UpdateWorker,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_worker(worker_id=worker_id, request=request, db=db)


@router.delete("/workers/{worker_id}")
async def delete_worker_endpoint(
    worker_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_worker(worker_id=worker_id, db=db)


@router.post("/{cafedra_code}/deputy-directors")
async def create_deputy_director_endpoint(
    cafedra_code: str,
    request: DeputyDirector,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_deputy_director(cafedra_code=cafedra_code, request=request, db=db)


@router.put("/deputy-directors/{deputy_director_id}")
async def update_deputy_director_endpoint(
    deputy_director_id: int,
    request: UpdateDeputyDirector,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_deputy_director(deputy_director_id=deputy_director_id, request=request, db=db)


@router.delete("/deputy-directors/{deputy_director_id}")
async def delete_deputy_director_endpoint(
    deputy_director_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_deputy_director(deputy_director_id=deputy_director_id, db=db)


@router.post("/{cafedra_code}/scientific-council")
async def create_council_member_endpoint(
    cafedra_code: str,
    request: ScientificCouncilMember,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_council_member(cafedra_code=cafedra_code, request=request, db=db)


@router.put("/scientific-council/{member_id}")
async def update_council_member_endpoint(
    member_id: int,
    request: UpdateCouncilMember,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_council_member(member_id=member_id, request=request, db=db)


@router.delete("/scientific-council/{member_id}")
async def delete_council_member_endpoint(
    member_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_council_member(member_id=member_id, db=db)


@router.put("/laboratories/{laboratory_id}")
async def update_laboratory_endpoint(
    laboratory_id: int,
    request: UpdateLaboratory,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_laboratory(laboratory_id=laboratory_id, request=request, db=db)


@router.delete("/laboratories/{laboratory_id}")
async def delete_laboratory_endpoint(
    laboratory_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_laboratory(laboratory_id=laboratory_id, db=db)


@router.put("/patents/{item_id}")
async def update_patent_endpoint(
    item_id: int,
    request: UpdatePatentItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await update_patent(item_id=item_id, request=request, db=db)


@router.delete("/patents/{item_id}")
async def delete_patent_endpoint(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await delete_patent(item_id=item_id, db=db)


@router.post("/{cafedra_code}/patents")
async def create_patent_endpoint(
    cafedra_code: str,
    request: PatentItem,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await create_patent(cafedra_code=cafedra_code, request=request, db=db)


@router.put("/{cafedra_code}/patents/reorder")
async def reorder_patents_endpoint(
    cafedra_code: str,
    request: ReorderRequest,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(require_admin),
):
    return await reorder_patents(cafedra_code=cafedra_code, ids=request.ids, db=db)
