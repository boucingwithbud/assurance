from fastapi import FastAPI
from app.routers import carte_grise_postgres, main_route, visite_t_postgres, facture_postgres, cni_recto_postgres, permis_cond_postgres, carte_grise_postgres
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_route.router)
app.include_router(visite_t_postgres.router)
app.include_router(facture_postgres.router)
app.include_router(cni_recto_postgres.router)
app.include_router(permis_cond_postgres.router)
app.include_router(carte_grise_postgres.router)
