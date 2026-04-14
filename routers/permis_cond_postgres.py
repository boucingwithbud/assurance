from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.routing import APIRouter
import app.schemas as schemas, app.models as models

router = APIRouter(prefix= "/Permis_conduire_formulaire", tags= ["formulaire permis de conduire"])
@router.post('/bdd_permis_conduire')
def create_permis_conduire_info(request: schemas.PermisConduireRectoVerso, db: Session= Depends(get_db)):
    if request.date_naissance > datetime.now().date():
        raise HTTPException(status_code=400, detail="La date de naissance ne peut pas être dans le futur.")
    if (request.cat_a_expiration or request.cat_b_expiration or request.cat_c_expiration or request.cat_d_expiration or request.cat_e_expiration) < datetime.now().date():
        raise HTTPException(status_code=400, detail="Le permis est expiré.")
    permis_conduire_info = models.PermisConduireInfo(**request.dict())
    db.add(permis_conduire_info)
    db.commit()
    db.refresh(permis_conduire_info)
    return permis_conduire_info