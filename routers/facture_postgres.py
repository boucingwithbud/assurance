from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.routing import APIRouter
import app.schemas as schemas, app.models as models


router = APIRouter(prefix= "/facture_bdd", tags= ["formulaire facture"])
@router.post('/bdd_facture')
def create_facture_info(request: schemas.FactureInfo, db: Session= Depends(get_db)):
    facture_info = models.FactureInfo(**request.dict())
    db.add(facture_info)
    db.commit()
    db.refresh(facture_info)
    return facture_info