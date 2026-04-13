import langchain
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image
from langchain.agents import create_agent
from typing import Optional, List
from pydantic import Field, BaseModel
from datetime import date
from langchain.agents.structured_output import ToolStrategy
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#print(GROQ_API_KEY)

model = ChatGroq(model = "meta-llama/llama-4-scout-17b-16e-instruct", temperature = 0, api_key = GROQ_API_KEY)

#model = ChatOllama(model="qwen3-vl:4b",temperature=0)

print(model)

#model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key= "AIzaSyAk6t0AqJuqreVolR_wBjDXGhBM5xLAbvA")

#llm = HuggingFaceEndpoint(
#    repo_id="Qwen/Qwen3-VL-4B-Instruct",
#    task="text-generation",
#    max_new_tokens=512,
#    do_sample=False,
#    repetition_penalty=1.03,
#    provider="auto",  # let Hugging Face choose the best provider for you
#)

#model = ChatHuggingFace(llm=llm)

class VisiteInfo(BaseModel):
    centre: Optional[str] = Field(default=None, description="à droite de CENTRE dans le document")
    mtt: Optional[float] = Field(default=None, description="à droite de MTT dans le document")
    cat: Optional[str] = Field(default=None, description="à droite CAT dans le document")
    kms: Optional[str] = Field(default=None, description="à droite de KMS dans le document")
    stat: Optional[str] = Field(default=None, description="à droite de STAT dans le document")
    ville: Optional[str] = Field(default=None, description="Le nom de la ville")
    immatriculation: Optional[str] = Field(default=None, description="Juste en dessous de Immatriculation")
    expiration: Optional[date] = Field(default=None, description="date d'expiration juste en dessous de Expiration")
    marque: Optional[str] = Field(default=None, description="à droite de MARQUE")
    type: Optional[str] = Field(default=None, description="à droite de TYPE")
    numero_serie: Optional[str] = Field(default=None, description="à droite de N° SERIE")
    puis_fis_cv: Optional[int] = Field(default=None, description="à droite de PUIS.FIS.(CV) juste au dessus de MISE EN CIRC.")
    mise_en_circulation: Optional[date] = Field(default=None, description="la date à droite de MISE EN CIRC")
    observations: Optional[str] = Field(default=None, description="à droite de OBSERVATIONS")
    quotite: Optional[float] = Field(default=None, description="Juste en dessous de QUOTITE")
    numero_vignette: Optional[str] = Field(default=None, description="Juste en dessous de N° VIGNETTE")
    ncc: Optional[str] = Field(default=None, description="Juste en dessous de NCC (peut être vide)")
    responsable: Optional[str] = Field(default=None, description="Juste en dessous de RESPONSABLE")

agent_visite_technique = create_agent(model = model, system_prompt= "Tu es un assistant qui transcris les informations essentielles d'un certificat de visite technique et de vignette en json, les dates sont au format DD-MM-YYYY," \
"je veux que tu les retourne en YYYY-DD-MM. Lorsque des champs mtt, et quotite sont extraites, considère les comme" \
"des valeurs numériques et enlève l'unité(F)" 
                     ,response_format= ToolStrategy(VisiteInfo))

class TranscrireVisite:

    def transcribe_base64(img_base64):

        result = agent_visite_technique.invoke({"messages": [{"role": "user", "content": [{"type": "text", "text": "Extrait les informations relatives au certificat de visite technique et de vignette à partir de cette image"},{"type": "image", "base64": img_base64, "mime_type": "image/png"}]}]})

        return result["structured_response"]

class FactureInfo(BaseModel):
    # ── Émetteur ─────────────────────────────────────────────
    vendeur_nom:                 Optional[str]  = Field(default=None, description="Nom ou raison sociale du vendeur/fournisseur")
    vendeur_adresse:             Optional[str]  = Field(default=None, description="Adresse complète du vendeur/fournisseur")
    vendeur_telephone:           Optional[str]  = Field(default=None, description="Numéro de téléphone du vendeur")
    vendeur_email:               Optional[str]  = Field(default=None, description="Adresse email du vendeur")
    vendeur_rccm:                Optional[str]  = Field(default=None, description="Numéro RCCM, SIRET, NIF ou identifiant fiscal du vendeur")
    vendeur_compte_contribuable: Optional[str]  = Field(default=None, description="Compte contribuable ou numéro fiscal du vendeur")

    # ── Client ───────────────────────────────────────────────
    client_nom:                  Optional[str]  = Field(default=None, description="Nom ou raison sociale du client/acheteur")
    client_adresse:              Optional[str]  = Field(default=None, description="Adresse complète du client")
    client_telephone:            Optional[str]  = Field(default=None, description="Numéro de téléphone du client")
    client_email:                Optional[str]  = Field(default=None, description="Adresse email du client")
    client_code:                 Optional[str]  = Field(default=None, description="Code client ou référence client")

    # ── Identifiants facture ──────────────────────────────────
    numero_facture:              Optional[str]  = Field(default=None, description="Numéro de la facture, souvent après FACTURE N° ou N° FACTURE")
    date_facture:                Optional[date] = Field(default=None, description="Date d'émission de la facture au format YYYY-MM-DD")
    date_echeance:               Optional[date] = Field(default=None, description="Date limite de paiement au format YYYY-MM-DD")
    numero_bon_commande:         Optional[str]  = Field(default=None, description="Numéro de bon de commande associé")
    numero_bon_livraison:        Optional[str]  = Field(default=None, description="Numéro de bon de livraison associé")
    objet:                       Optional[str]  = Field(default=None, description="Objet ou intitulé de la facture")

    # ── Lignes de détail (aplaties) ───────────────────────────
    lignes_descriptions:         Optional[List[str]] = Field(default=None, description="Liste des descriptions/libellés de chaque ligne article ou service")
    lignes_references:           Optional[List[str]] = Field(default=None, description="Liste des références ou codes article de chaque ligne")
    lignes_quantites:            Optional[List[int]] = Field(default=None, description="Liste des quantités de chaque ligne")
    lignes_unites:               Optional[List[str]] = Field(default=None, description="Liste des unités de mesure de chaque ligne (pcs, kg, h…)")
    lignes_prix_unitaires:       Optional[List[float]] = Field(default=None, description="Liste des prix unitaires HT de chaque ligne")
    lignes_taux_tva:             Optional[List[float]] = Field(default=None, description="Liste des taux de TVA de chaque ligne (ex: 18%)")
    lignes_montants_ht:          Optional[List[float]] = Field(default=None, description="Liste des montants HT de chaque ligne")
    lignes_montants_ttc:         Optional[List[float]] = Field(default=None, description="Liste des montants TTC de chaque ligne")

    # ── Totaux ───────────────────────────────────────────────
    total_ht:                    Optional[float]  = Field(default=None, description="Total hors taxes, souvent après TOTAL HT ou MONTANT HT")
    remise:                      Optional[float]  = Field(default=None, description="Remise ou réduction globale appliquée")
    total_ht_apres_remise:       Optional[float]  = Field(default=None, description="Total HT après déduction de la remise")
    montant_tva:                 Optional[float]  = Field(default=None, description="Montant de la TVA, souvent après TVA ou MONTANT TVA")
    taux_tva_global:             Optional[float]  = Field(default=None, description="Taux de TVA global appliqué sur la facture (ex: 18%)")
    total_ttc:                   Optional[float]  = Field(default=None, description="Total toutes taxes comprises, souvent après TOTAL TTC ou NET A PAYER")
    acompte:                     Optional[float]  = Field(default=None, description="Acompte déjà versé, souvent après ACOMPTE ou AVANCE")
    reste_a_payer:               Optional[float]  = Field(default=None, description="Reste à payer après déduction de l'acompte")
    devise:                      Optional[str]  = Field(default=None, description="Devise utilisée (XOF, EUR, USD…)")

    # ── Paiement ─────────────────────────────────────────────
    mode_paiement:               Optional[str]  = Field(default=None, description="Mode de paiement indiqué (virement, chèque, espèces, mobile money…)")
    banque:                      Optional[str]  = Field(default=None, description="Nom de la banque du bénéficiaire")
    iban_rib:                    Optional[str]  = Field(default=None, description="IBAN, RIB ou numéro de compte bancaire")
    numero_cheque:               Optional[str]  = Field(default=None, description="Numéro de chèque si paiement par chèque")

    # ── Divers ───────────────────────────────────────────────
    mentions_legales:            Optional[str]  = Field(default=None, description="Mentions légales, pénalités de retard ou conditions de vente")
    notes:                       Optional[str]  = Field(default=None, description="Remarques ou informations supplémentaires en bas de facture")
    cachet_signature:            Optional[str]  = Field(default=None, description="Présence d'un cachet ou d'une signature (oui/non)")

agent_facture = create_agent(model = model, system_prompt= "Tu es un assistant qui transcris les informations essentielles d'une facture", response_format= FactureInfo)

class TranscrireFacture:

    def transcribe_base64(img_base64):

        result = agent_facture.invoke({"messages": [{"role": "user", "content": [{"type": "text", "text": "Extrais les informations relatives à une facture à partir de cette image. Les dates sont au format DD-MM-YYYY renvoie les au format YYYY-MM-DD."
        "Pour les variables qui représente des valeurs numériques comme les taux ou le montant, extrait uniquement des "
        "les valeurs numériques en sortie et ignore les autres caractères(il s'agit peut être des unités ou symbôles ou devises ou "
        "de texte)"},{"type": "image", "base64": img_base64, "mime_type": "image/png"}]}]})

        return result["structured_response"]
    

class CniInfoRecto(BaseModel):

    Nom: Optional[str] = Field(default=None, description="Nom de famille de la personne titulaire de la carte d'identité")
    Prenom: Optional[str] = Field(default=None, description="Prénom de la personne titulaire de la carte d'identité")
    Date_de_naissance: Optional[date] = Field(default=None, description="Date de naissance de la personne titulaire de la carte d'identité au format YYYY-MM-DD")
    Lieu_de_naissance: Optional[str] = Field(default=None, description="Lieu de naissance de la personne titulaire de la carte d'identité")
    Sexe: Optional[str] = Field(default=None, description="Sexe de la personne titulaire de la carte d'identité (M ou F)")
    Taille: Optional[float] = Field(default=None, description="Taille de la personne titulaire de la carte d'identité en cm")
    Date_d_expiration: Optional[str] = Field(default=None, description="Date d'expiration de la carte d'identité au format YYYY-MM-DD")
    Numero_de_cni: Optional[str] = Field(default=None, description="Numéro de la carte d'identité")
    Nationalite: Optional[str] = Field(default=None, description="Nationalité de la personne titulaire de la carte d'identité")

agent_cni_recto = create_agent(model = model, system_prompt= "Tu es un assistant qui transcris les informations essentielles d'une carte d'identité", response_format= CniInfoRecto)

class TranscrireCNIRecto:

    def transcribe_base64(img_base64):

        result = agent_cni_recto.invoke({"messages": [{"role": "user", "content": [{"type": "text", "text": "Extrais les informations relatives au recto d'une carte d'identité à partir de cette image. Les dates sont au format DD-MM-YYYY renvoie les au format YYYY-MM-DD"},{"type": "image", "base64": img_base64, "mime_type": "image/png"}]}]})

        return result["structured_response"]
    


class CniInfoVerso(BaseModel):

    NNI: str = Field(default=None, description="Numéro National d'Identification (NNI) présent au verso de la carte d'identité")
    Profession: str = Field(default=None, description="Profession de la personne titulaire de la carte d'identité, souvent indiquée au verso")
    Date_emission: str = Field(default=None, description="Date d'émission de la carte d'identité au format YYYY-MM-DD, souvent indiquée au verso")
    Autorite_emission: str = Field(default=None, description="Autorité ayant émis la carte d'identité, souvent indiquée au verso")

agent_cni_verso = create_agent(model = model, system_prompt= "Tu es un assistant qui transcris les informations essentielles d'une carte d'identité", response_format= CniInfoVerso)

class TranscrireCNIVerso:

    def transcribe_base64(img_base64):

        result = agent_cni_verso.invoke({"messages": [{"role": "user", "content": [{"type": "text", "text": "Extrais les informations relatives au recto d'une carte d'identité à partir de cette image. Les dates sont au format DD-MM-YYYY renvoie les au format YYYY-MM-DD"},{"type": "image", "base64": img_base64, "mime_type": "image/png"}]}]})

        return result["structured_response"]
    


class PermisConduireInfo(BaseModel):

    Nom: str = Field(default=None, description="Numéro National d'Identification (NNI) présent au verso de la carte d'identité")
    Prenom: str = Field(default=None, description="Profession de la personne titulaire de la carte d'identité, souvent indiquée au verso")
    Date_naissance: date = Field(default=None, description="Date d'émission de la carte d'identité au format YYYY-MM-DD, souvent indiquée au verso")
    Addresse: str = Field(default=None, description="Autorité ayant émis la carte d'identité, souvent indiquée au verso")
    Lieu_naissance: str = Field(default=None, description="Lieu de naissance de la personne titulaire du permis de conduire")
    Lieu_delivrance: str = Field(default=None, description="Lieu de délivrance du permis de conduire")
    Date_expiration: date = Field(default=None, description="Date d'expiration du permis de conduire au format YYYY-MM-DD")
    Numero_permis: str = Field(default=None, description="Numéro du permis de conduire PC ou N° PERMIS")
    Categories: str = Field(default=None, description="Catégories de véhicules autorisées par le permis de conduire")


agent_permis_conduire = create_agent(model = model, system_prompt= "Tu es un assistant qui transcris les informations essentielles d'une carte d'identité", response_format= PermisConduireInfo)

class TranscrirePermisConduire:

    def transcribe_base64(img_base64):

        result = agent_permis_conduire.invoke({"messages": [{"role": "user", "content": [{"type": "text", "text": "Extrais les informations relatives au recto d'une carte d'identité à partir de cette image. Les dates sont au format DD-MM-YYYY renvoie les au format YYYY-MM-DD"},{"type": "image", "base64": img_base64, "mime_type": "image/png"}]}]})

        return result["structured_response"]
    


class CarteGrise(BaseModel):

    Numero_immatriculation: str = Field(default=None, description="Numéro d'immatriculation du véhicule")
    Numero_carte_grise: str = Field(default=None, description="Numéro de la carte grise")
    Date_premiere_mise_circulation: str = Field(default=None, description="Date de première mise en circulation du véhicule au format YYYY-MM-DD")
    Date_edition_carte_grise: str = Field(default=None, description="Date d'édition de la carte grise au format YYYY-MM-DD")
    Identite_titulaire: str = Field(default=None, description="Identité du titulaire de la carte grise (nom et prénom)")
    Marque: str = Field(default=None, description="Marque du véhicule")
    Genre: str = Field(default=None, description="Genre du véhicule (VP, CTTE, Camion MOTO, etc.)")
    Type_commercial: str = Field(default=None, description="Type commercial du véhicule")
    Couleur: str = Field(default=None, description="Couleur du véhicule")
    Carrosserie: str = Field(default=None, description="Carrosserie du véhicule")
    Energie: str = Field(default=None, description="Type d'énergie du véhicule (essence, diesel, électrique, Gas-Oil etc.)")        
    Usage_vehicule: str = Field(default=None, description="Usage du véhicule (particulier, professionnel, privé etc.)")
    Nombre_essieux: str = Field(default=None, description="Nombre d'essieux du véhicule")
    Places_assises: str = Field(default=None, description="Nombre de places assises du véhicule")
    Puissance_fiscale: str = Field(default=None, description="Puissance fiscale du véhicule en CV")
    Cylindree_CC: str = Field(default=None, description="Cylindrée du véhicule en centimètres cubes (CC)")
    Masse_vehicule: str = Field(default=None, description=" PTAC ou poids total autorisé en charge du véhicule en kg")
    PV: str = Field(default=None, description="Poids à vide du véhicule en kg")
    CU: str = Field(default=None, description="Charge utile du véhicule en kg")

agent_carte_grise = create_agent(model = model, system_prompt= "Tu es un assistant qui transcris les informations essentielles d'une carte grise", response_format= CarteGrise)

class TranscrireCarteGrise:

    def transcribe_base64(img_base64):

        result = agent_carte_grise.invoke({"messages": [{"role": "user", "content": [{"type": "text", "text": "Extrais les informations relatives au recto d'une carte grise à partir de cette image. Les dates sont au format DD-MM-YYYY renvoie les au format YYYY-MM-DD"},{"type": "image", "base64": img_base64, "mime_type": "image/png"}]}]})

        return result["structured_response"]


