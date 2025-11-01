from sqlalchemy.orm import Session
from models.project.project import Project
from models.project.project_tr import ProjectTranslation
from app.api.v1.schema.project import ProjectCreate, ProjectReorder

async def get_all_projects(db: Session):
    return db.query(Project).order_by(Project.display_order).all()

def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.project_id == project_id).first()

def create_project(db: Session, data: ProjectCreate):
    last_project = db.query(Project).order_by(Project.display_order.desc()).first()
    next_order = (last_project.display_order + 1) if last_project else 1

    new_project_id = (db.query(Project).count() or 0) + 1

    project = Project(
        project_id=new_project_id,
        bg_image=data.bg_image,
        display_order=next_order,
        is_active=data.is_active or False,
    )
    db.add(project)
    db.flush()  

    for tr in data.translations:
        db.add(ProjectTranslation(
            project_id=new_project_id,
            lang_code=tr.lang_code,
            title=tr.title,
            desc=tr.desc
        ))

    db.commit()
    db.refresh(project)
    return project


def reorder_project(db: Session, data: ProjectReorder):
    project = db.query(Project).filter(Project.project_id == data.project_id).first()
    if not project:
        return None

    old_order = project.display_order
    new_order = data.new_order

    if old_order == new_order:
        return project

    if new_order < old_order:
        db.query(Project).filter(
            Project.display_order >= new_order,
            Project.display_order < old_order
        ).update({Project.display_order: Project.display_order + 1})

    else:
        db.query(Project).filter(
            Project.display_order <= new_order,
            Project.display_order > old_order
        ).update({Project.display_order: Project.display_order - 1})

    project.display_order = new_order
    db.commit()
    db.refresh(project)
    return project
