from pydantic import BaseModel


class ReOrderHero(BaseModel):
    hero_id: int
    new_order: int
