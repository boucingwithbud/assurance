from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from PIL import Image
from datetime import date
import requests
from transformers import CLIPProcessor, CLIPModel
import numpy as np
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import Optional

# LangChain imports
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

# ✅ Imports internes absolus
from app.img_to_b64 import encode_image_to_base64
from app.transcrire import (
    TranscrireVisite,
    TranscrireFacture,
    TranscrireCNIRecto,
    TranscrireCNIVerso,
    TranscrirePermisConduire,
    TranscrireCarteGrise
)
import app.models as models
import app.schemas as schemas
from app.database import get_db

load_dotenv()

grok_api_key = os.getenv("GROQ_API_KEY")

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

router = APIRouter(tags=['Extraction de caractères'], prefix='')
@router.post('/certificat_de_visite_technique', summary= "Permet de détecter si le document chargé est un certificat de visite technique ou non et d'extraire ses informations de manière structurée")
def vt(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Fichier non supporté. Veuillez télécharger une image au format JPEG ou PNG.")
    
    img = Image.open(file.file)
    inputs = processor(text=["N'est pas un certificat de visite technique et vignette", "Certificat de visite technique et vignette"], images= img, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    classes = probs.argmax().item()
    dict = {0: False, 1: True}
    is_visite_technique = dict[classes]

    img_to_base64 = encode_image_to_base64(file.file)

    output = TranscrireVisite.transcribe_base64(img_to_base64)

    return {"is_visite_technique": dict[classes], "output": output}


@router.post('/facture_manuscrite_ou_imprime', summary= "Permet de détecter si une facture est manuscrite ou imprimée et d'extraire ses informations de manière structurée")
def facture(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Fichier non supporté. Veuillez télécharger une image au format JPEG ou PNG.")
    img = Image.open(file.file)
    inputs = processor(text=["handwritten text", "printed text", "mix of handwritten text and printed text"], images= img, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    classes = probs.argmax().item()
    dict = {0: "Document manuscrit", 1: "Document imprimé", 2: "Mélange d'écritures manuscrites et impriméees"}
    is_manuscrit = dict[classes]

    img_to_base64 = encode_image_to_base64(file.file)

    output = TranscrireFacture.transcribe_base64(img_to_base64)
    
    return {"is_manuscrit": dict[classes], "output": output}


@router.post('/cni_recto', summary= "Permet de détecter si le document chargé est une carte d'identité ou non et d'extraire les informations du recto de manière structurée")
def cni_recto(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Fichier non supporté. Veuillez télécharger une image au format JPEG ou PNG.")
    
    img = Image.open(file.file)
    inputs = processor(text=["N'est pas une carte d'identité", "est une Carte d'identité"], images= img, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    classes = probs.argmax().item()
    dict = {0: False, 1: True}
    is_visite_technique = dict[classes]

    img_to_base64 = encode_image_to_base64(file.file)

    output = TranscrireCNIRecto.transcribe_base64(img_to_base64)

    return {"is_carte_didentite": dict[classes], "output": output}



@router.post('/cni_verso', summary= "Permet de détecter si le document chargé est une carte d'identité ou non et d'extraire les informations du verso de manière structurée")
def cni_verso(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Fichier non supporté. Veuillez télécharger une image au format JPEG ou PNG.")
    
    img = Image.open(file.file)
    inputs = processor(text=["N'est pas une carte d'identité", "est une Carte d'identité"], images= img, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    classes = probs.argmax().item()
    dict = {0: False, 1: True}
    is_carte_didentite = dict[classes]

    img_to_base64 = encode_image_to_base64(file.file)

    output = TranscrireCNIVerso.transcribe_base64(img_to_base64)

    return {"is_carte_didentite": dict[classes], "output": output}

@router.post('/permis_conduire', summary= "Permet de détecter si le document chargé est un permis de conduire ou non et d'extraire les informations du permis de conduire de manière structurée")
def permis_conduire(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Fichier non supporté. Veuillez télécharger une image au format JPEG ou PNG.")
    
    img = Image.open(file.file)
    inputs = processor(text=["N'est pas un permis de conduire", "est un permis de conduire"], images= img, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    classes = probs.argmax().item()
    dict = {0: False, 1: True}
    is_permis_conduire = dict[classes]

    img_to_base64 = encode_image_to_base64(file.file)

    output = TranscrirePermisConduire.transcribe_base64(img_to_base64)

    return {"is_permis_conduire": dict[classes], "output": output}



@router.post('/carte_grise', summary= "Permet de détecter si le document chargé est une carte grise ou non et d'extraire les informations de manière structurée")
def carte_grise(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Fichier non supporté. Veuillez télécharger une image au format JPEG ou PNG.")
    
    img = Image.open(file.file)
    inputs = processor(text=["N'est pas une carte grise", "est une carte grise"], images= img, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    classes = probs.argmax().item()
    dict = {0: False, 1: True}
    is_carte_grise = dict[classes]

    img_to_base64 = encode_image_to_base64(file.file)

    output = TranscrireCarteGrise.transcribe_base64(img_to_base64)

    return {"is_carte_grise": dict[classes], "output": output}
    