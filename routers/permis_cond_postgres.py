from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.routing import APIRouter
import app.schemas as schemas, app.models as models

router = APIRouter(prefix= "/Permis_conduire_formulaire", tags= ["formulaire permis de conduire"])
@router.post('/bdd_permis_conduire')
def create_permis_conduire_info(request: schemas.PermisConduireInfo, db: Session= Depends(get_db)):
    permis_conduire_info = models.PermisConduireInfo(**request.dict())
    db.add(permis_conduire_info)
    db.commit()
    db.refresh(permis_conduire_info)
    return permis_conduire_info