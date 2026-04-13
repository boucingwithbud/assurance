from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.routing import APIRouter
import app.schemas as schemas, app.models as models

router = APIRouter(prefix= "/carte_grise_formulaire", tags= ["formulaire carte grise"])
@router.post('/bdd_carte_grise')
def create_carte_grise_info(request: schemas.CarteGriseInfo, db: Session= Depends(get_db)):
    carte_grise_info = models.CarteGriseInfo(**request.dict())
    db.add(carte_grise_info)
    db.commit()
    db.refresh(carte_grise_info)
    return carte_grise_info