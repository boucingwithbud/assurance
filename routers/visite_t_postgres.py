from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.routing import APIRouter
import app.schemas as schemas, app.models as models
from datetime import datetime


router = APIRouter(prefix= "/Visite_technique_formulaire", tags= ["formulaire visite technique"])
@router.post('/bdd_visite_tech')
def create_visite_info(request: schemas.VisiteInfo, db: Session= Depends(get_db)):

    if request.mise_en_circulation > datetime.now().date():
        raise HTTPException(status_code=400, detail="La date de mise en circulation ne peut pas être dans le futur.")
    visite_info = models.VisiteInfo(**request.dict())
    db.add(visite_info)
    db.commit()
    db.refresh(visite_info)
    return visite_info

