from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.routing import APIRouter
import app.schemas as schemas, app.models as models
from datetime import datetime

router = APIRouter(prefix= "/carte_grise_formulaire", tags= ["formulaire carte grise"])
@router.post('/bdd_carte_grise')
def create_carte_grise_info(request: schemas.CarteGriseRectoVerso, db: Session= Depends(get_db)):

    if request.date_edition_carte_grise > datetime.now().date():
        raise HTTPException(status_code=400, detail="La date d'édition de la carte grise ne peut pas être dans le futur.")
    if request.date_mise_circulation > datetime.now().date():
        raise HTTPException(status_code=400, detail="La date de mise en circulation ne peut pas être dans le futur.")
    if request.date_edition_carte_grise < request.date_mise_circulation:
        raise HTTPException(status_code=400, detail="La date d'édition de la carte grise ne peut pas être antérieure à la date de mise en circulation.")
    carte_grise_info = models.CarteGriseRectoVerso(**request.dict())
    db.add(carte_grise_info)
    db.commit()
    db.refresh(carte_grise_info)
    return carte_grise_info