# Documentation — `platform_assurance_back`

> **Repo :** [github.com/paulcoffi/assurance](https://github.com/paulcoffi/assurance)  
> **Langage :** Python 100%  
> **Stack principal :** FastAPI · SQLAlchemy · PostgreSQL · LangChain · CLIP (OpenAI)

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)  
2. [Architecture du projet](#2-architecture-du-projet)  
3. [Installation et configuration](#3-installation-et-configuration)  
4. [Base de données](#4-base-de-données)  
5. [Modèles de données](#5-modèles-de-données)  
6. [Schémas Pydantic](#6-schémas-pydantic)  
7. [Module de transcription IA (`transcrire.py`)](#7-module-de-transcription-ia-transcrirepy)  
8. [API — Endpoints](#8-api--endpoints)  
9. [Routers secondaires (persistance BDD)](#9-routers-secondaires-persistance-bdd)  
10. [Utilitaires](#10-utilitaires)  
11. [Dépendances](#11-dépendances)  
12. [Notes et points d'amélioration](#12-notes-et-points-damélioration)

---

## 1. Vue d'ensemble

`platform_assurance_back` est un **backend d'extraction intelligente de documents d'assurance**. Il expose une API REST (FastAPI) capable de :

1. **Classifier** automatiquement le type d'un document (carte grise, CNI, permis de conduire, facture, certificat de visite technique, formulaire d'adhésion) à l'aide du modèle CLIP d'OpenAI.
2. **Extraire** de manière structurée les informations contenues dans le document via un agent LLM (LangChain + Groq / Llama 4 Scout).
3. **Persister** les données extraites dans une base PostgreSQL via SQLAlchemy.

---

## 2. Architecture du projet

```
assurance/
│
├── main.py                     # Point d'entrée FastAPI, déclaration de l'app et des middlewares
├── database.py                 # Connexion PostgreSQL, session, Base SQLAlchemy
├── models.py                   # Modèles ORM (tables BDD)
├── schemas.py                  # Schémas Pydantic (validation entrée/sortie)
├── transcrire.py               # Agents IA LangChain pour la transcription de documents
├── img_to_b64.py               # Utilitaire de conversion image → base64
├── requirements.txt            # Dépendances Python
├── __init__.py
│
└── routers/
    ├── __init__.py
    ├── main_route.py           # Routes principales : classification + extraction (CLIP + LLM)
    ├── visite_t_postgres.py    # Route CRUD : visite technique → BDD
    ├── facture_postgres.py     # Route CRUD : facture → BDD
    ├── cni_recto_postgres.py   # Route CRUD : CNI → BDD
    ├── permis_cond_postgres.py # Route CRUD : permis de conduire → BDD
    └── carte_grise_postgres.py # Route CRUD : carte grise → BDD
```

---

## 3. Installation et configuration

### Prérequis

- Python 3.10+
- PostgreSQL (base `assurance_db`)
- Clé API Groq

### Installation

```bash
git clone https://github.com/paulcoffi/assurance.git
cd assurance
pip install -r requirements.txt
```

### Variables d'environnement

Créer un fichier `.env` à la racine :

```env
GROQ_API_KEY=votre_clé_groq
```

### Lancement

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur `http://localhost:8000`. La documentation Swagger est accessible à `http://localhost:8000/docs`.

### CORS autorisés (par défaut)

- `http://localhost`
- `http://localhost:5173` (frontend Vite/Vue/React)

---

## 4. Base de données

**Fichier :** `database.py`

```
URL : postgresql://kaydan:kaydan@localhost:5432/assurance_db
```

| Élément | Détail |
|---|---|
| `engine` | Connexion SQLAlchemy via `create_engine` |
| `SessionLocal` | Factory de sessions (`autoflush=False`) |
| `Base` | Classe de base déclarative pour les modèles ORM |
| `get_db()` | Générateur de dépendance FastAPI — ouvre et ferme la session automatiquement |

---

## 5. Modèles de données

**Fichier :** `models.py`

Les modèles ORM représentent les tables PostgreSQL créées automatiquement au démarrage via `Base.metadata.create_all(engine)`.

### `VisiteInfo` — Table `visite_info`

Certificat de visite technique et vignette.

| Champ | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Identifiant auto-incrémenté |
| `centre` | String | Centre de visite |
| `mtt` | Integer | Montant taxe technique |
| `cat` | String | Catégorie du véhicule |
| `kms` | String | Kilométrage |
| `stat` | String | Statut de la visite |
| `ville` | String | Ville |
| `immatriculation` | String | Numéro de plaque |
| `expiration` | Date | Date d'expiration |
| `marque` | String | Marque du véhicule |
| `type` | String | Type de véhicule |
| `numero_serie` | String | Numéro de série |
| `puis_fis_cv` | Integer | Puissance fiscale (CV) |
| `mise_en_circulation` | Date | Date de mise en circulation |
| `observations` | String | Observations |
| `quotite` | Integer | Quotité |
| `numero_vignette` | String | Numéro de vignette |
| `ncc` | String | NCC |
| `responsable` | String | Responsable |

---

### `FactureInfo` — Table `facture_info`

Facture commerciale (manuscrite ou imprimée).

**Émetteur :** `vendeur_nom`, `vendeur_adresse`, `vendeur_telephone`, `vendeur_email`, `vendeur_rccm`, `vendeur_compte_contribuable`

**Client :** `client_nom`, `client_adresse`, `client_telephone`, `client_email`, `client_code`

**Identifiants :** `numero_facture`, `date_facture`, `date_echeance`, `numero_bon_commande`, `numero_bon_livraison`, `objet`

**Lignes (colonnes JSON) :** `lignes_descriptions`, `lignes_references`, `lignes_quantites`, `lignes_unites`, `lignes_prix_unitaires`, `lignes_taux_tva`, `lignes_montants_ht`, `lignes_montants_ttc`

**Totaux :** `total_ht`, `remise`, `total_ht_apres_remise`, `montant_tva`, `taux_tva_global`, `total_ttc`, `acompte`, `reste_a_payer`, `devise`

**Paiement :** `mode_paiement`, `banque`, `iban_rib`, `numero_cheque`

**Divers :** `mentions_legales`, `notes`, `cachet_signature`

---

### `CniInfoRectoVerso` — Table `cni_info_recto`

Carte Nationale d'Identité.

| Champ | Type |
|---|---|
| `nom`, `prenom` | String |
| `date_naissance`, `date_expiration`, `date_emission` | Date |
| `lieu_de_naissance` | String |
| `sexe` | String (M/F) |
| `taille` | Float (cm) |
| `numero_de_cni` | String |
| `nationalite` | String |
| `nni` | String (Numéro National d'Identification) |
| `profession` | String |
| `autorite_emission` | String |

---

### `PermisConduireRectoVerso` — Table `permis_conduire`

| Champ | Type |
|---|---|
| `nom`, `prenom`, `addresse`, `lieu_naissance` | String |
| `date_naissance`, `date_delivrance` | Date |
| `lieu_delivrance`, `numero_permis` | String |
| `cat_a/b/c/d/e_validite` | Date (validité par catégorie) |
| `cat_a/b/c/d/e_expiration` | Date (expiration par catégorie) |
| `groupe_sanguin` | String |
| `document_identite` | String |

---

### `CarteGriseRectoVerso` — Table `carte_grise`

| Champ | Type |
|---|---|
| `numero_immatriculation`, `numero_carte_grise` | String |
| `date_mise_circulation`, `date_edition_carte_grise` | Date |
| `identite_titulaire` | String |
| `marque`, `genre`, `type_commercial`, `couleur`, `carrosserie`, `energie`, `usage_vehicule` | String |
| `nombre_essieux`, `places_assises`, `puissance_fiscale` | Integer |
| `cylindree_cc` | String |
| `masse_vehicule`, `pv`, `cu` | Integer |
| `numero_vin_chassis`, `numero_moteur`, `type_technique` | String |
| `societe_credit`, `numero_immatriculation_precedent` | String |

---

### `BulletinAdhesion` — Table `bulletin_adhesion`

Formulaire d'adhésion à une assurance couvrant l'assuré principal, le conjoint et jusqu'à 5 enfants.

Champs par membre de famille : `profession`, `sport`, `poids` (int, kg), `taille` (int, cm), `maladies` (JSON, liste de chaînes).

Champs spécifiques assuré : `date_naissance`, `lieu_naissance`, `date_entree_entreprise`.

---

## 6. Schémas Pydantic

**Fichier :** `schemas.py`

Les schémas Pydantic (`BaseModel`) miroir les modèles ORM et servent à la validation des données en entrée des routes de persistance. Chaque champ est `Optional` avec une `description` détaillée indiquant son emplacement sur le document physique, ce qui sert aussi de contexte pour l'agent IA.

Schémas disponibles : `VisiteInfo`, `FactureInfo`, `CniInfoRectoVerso`, `PermisConduireRectoVerso`, `CarteGriseRectoVerso`, `BulletinAdhesion`.

---

## 7. Module de transcription IA (`transcrire.py`)

**Fichier :** `transcrire.py`

Ce module est le cœur de l'intelligence artificielle. Il instancie des agents LangChain utilisant :

- **LLM :** `ChatGroq` avec le modèle `meta-llama/llama-4-scout-17b-16e-instruct` (température 0)
- **Pattern :** `create_agent` + `ToolStrategy` pour forcer une sortie JSON structurée (Pydantic)
- **Entrée :** image encodée en base64 + prompt texte

### Agents et classes disponibles

| Classe | Document traité | Champs extraits |
|---|---|---|
| `TranscrireVisite` | Certificat de visite technique | Voir `VisiteInfo` |
| `TranscrireFacture` | Facture (manuscrite ou imprimée) | Voir `FactureInfo` |
| `TranscrireCNIRecto` | Recto CNI | nom, prénom, naissance, sexe, taille, expiration, numéro, nationalité |
| `TranscrireCNIVerso` | Verso CNI | nni, profession, date_emission, autorite_emission |
| `TranscrirePermisConduireRecto` | Recto permis | nom, prénom, naissance, adresse, lieu, délivrance, numéro |
| `TranscrirePermisConduireVerso` | Verso permis | validité/expiration catégories A/B/C/D/E, groupe sanguin, doc identité |
| `TranscrireCarteGriseRecto` | Recto carte grise | immatriculation, titulaire, marque, genre, couleur, énergie… |
| `TranscrireCarteGriseVerso` | Verso carte grise | VIN/châssis, moteur, type technique, société crédit |
| `TranscrireCarteGrise` | Carte grise complète (recto+verso) | Ensemble des champs |
| `TranscrireBulletinAdhesion` | Formulaire d'adhésion assurance | Voir `BulletinAdhesion` |

### Méthode commune

Toutes les classes exposent une méthode statique :

```python
TranscrireXxx.transcribe_base64(img_base64: str) -> PydanticModel
```

**Flux d'exécution :**

```
Image (fichier) ──► encode_image_to_base64() ──► base64 string
                                                        │
                                                        ▼
                                         agent.invoke({messages: [
                                           {role: user, content: [
                                             {type: text, text: prompt},
                                             {type: image, base64: ..., mime_type: image/png}
                                           ]}
                                         ]})
                                                        │
                                                        ▼
                                         result["structured_response"]  ← Pydantic model
```

---

## 8. API — Endpoints

**Fichier :** `routers/main_route.py`  
**Préfixe :** `/`  
**Tag Swagger :** `Extraction de caractères`

Chaque endpoint :
1. Valide le type MIME (JPEG ou PNG uniquement)
2. Classe l'image via **CLIP** (`openai/clip-vit-base-patch32`)
3. Encode l'image en base64
4. Appelle l'agent IA pour extraire les données
5. Retourne `{"is_<type>": bool/str, "output": <données structurées>}`

---

### `POST /certificat_de_visite_technique`

Détecte si l'image est un certificat de visite technique et extrait ses informations.

**Entrée :** fichier image (JPEG/PNG)

**Réponse :**
```json
{
  "is_visite_technique": true,
  "output": {
    "centre": "...",
    "immatriculation": "...",
    "expiration": "2025-12-31",
    ...
  }
}
```

---

### `POST /facture_manuscrite_ou_imprime`

Détecte si la facture est manuscrite, imprimée ou mixte, et extrait ses informations.

**Réponse :**
```json
{
  "is_manuscrit": "Document imprimé",
  "output": {
    "vendeur_nom": "...",
    "total_ttc": 118000.0,
    ...
  }
}
```

Valeurs possibles de `is_manuscrit` : `"Document manuscrit"`, `"Document imprimé"`, `"Mélange d'écritures manuscrites et imprimées"`.

---

### `POST /cni_recto`

Classification CNI + extraction du **recto**.

**Réponse :**
```json
{
  "is_carte_didentite": true,
  "output": {
    "nom": "DUPONT",
    "prenom": "Marie",
    "date_de_naissance": "1990-05-14",
    ...
  }
}
```

---

### `POST /cni_verso`

Classification CNI + extraction du **verso** (NNI, profession, autorité d'émission).

---

### `POST /permis_conduire_recto`

Classification permis de conduire + extraction du **recto** (identité, numéro, lieu de délivrance).

---

### `POST /permis_conduire_verso`

Classification permis de conduire + extraction du **verso** (catégories, validités, groupe sanguin).

---

### `POST /carte_grise_recto`

Classification carte grise + extraction du **recto** (véhicule, titulaire, caractéristiques).

---

### `POST /carte_grise_verso`

Classification carte grise + extraction du **verso** (VIN, moteur, immatriculation précédente).

---

### `POST /formulaire_adhesion`

Classification formulaire d'adhésion + extraction des données assuré/conjoint/enfants.

---

## 9. Routers secondaires (persistance BDD)

Ces routers permettent de **sauvegarder** les données extraites (ou saisies manuellement) dans PostgreSQL.

### `POST /Visite_technique_formulaire/bdd_visite_tech`

**Fichier :** `routers/visite_t_postgres.py`

Persiste un objet `VisiteInfo` en base. Valide que la date de mise en circulation n'est pas dans le futur.

**Corps :** `schemas.VisiteInfo`

---

### Autres routers (même pattern)

| Fichier | Préfixe | Endpoint |
|---|---|---|
| `facture_postgres.py` | `/Facture_formulaire` | `POST /bdd_facture` |
| `cni_recto_postgres.py` | `/CNI_formulaire` | `POST /bdd_cni` |
| `permis_cond_postgres.py` | `/Permis_formulaire` | `POST /bdd_permis` |
| `carte_grise_postgres.py` | `/CarteGrise_formulaire` | `POST /bdd_carte_grise` |

---

## 10. Utilitaires

### `img_to_b64.py` — Conversion image → base64

```python
encode_image_to_base64(file_object) -> str
```

Encode un fichier image en chaîne base64, prête à être envoyée au LLM multimodal.

---

## 11. Dépendances

Principales dépendances du projet (`requirements.txt`) :

| Package | Rôle |
|---|---|
| `fastapi` | Framework API REST |
| `uvicorn` | Serveur ASGI |
| `sqlalchemy` | ORM Python |
| `psycopg2` | Driver PostgreSQL |
| `pydantic` | Validation des données |
| `langchain` | Orchestration des agents IA |
| `langchain-groq` | Connecteur LLM Groq |
| `langgraph` | Graphes d'agents |
| `transformers` | Modèles HuggingFace (CLIP) |
| `torch` | Backend deep learning |
| `Pillow` | Traitement d'images |
| `python-dotenv` | Variables d'environnement |
| `python-multipart` | Upload de fichiers |

---

## 12. Notes et points d'amélioration

### Points d'attention

- La chaîne de connexion BDD (`database.py`) contient des credentials en dur : `postgresql://kaydan:kaydan@localhost:5432/assurance_db`. Il est recommandé de les déplacer dans le fichier `.env`.
- `models.py` contient deux définitions de la classe `BulletinAdhesion` — la première (incomplète, sans hériter de `Base`) est à supprimer.
- Le module `transcrire.py` instancie tous les agents au démarrage du serveur, ce qui peut allonger le temps de démarrage.
- Les routes de classification CLIP et les routes de persistance BDD sont indépendantes : il n'y a pas de sauvegarde automatique après une extraction. Ce couplage reste à implémenter côté client ou en ajoutant une étape dans les routes.

### Améliorations suggérées

- Ajouter l'authentification (JWT / OAuth2) sur les endpoints.
- Ajouter des routes `GET` pour récupérer les données persistées.
- Centraliser la logique de classification CLIP dans un service dédié.
- Ajouter un support PDF (conversion vers image avant traitement).
- Mettre en place des tests unitaires et d'intégration.
