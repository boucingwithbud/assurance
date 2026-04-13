from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.dialects.postgresql import JSON
from app.database import Base

class VisiteInfo(Base):

    __tablename__ = "visite_info"
    id = Column(Integer, primary_key=True, index=True)
    centre = Column(String, nullable=True)
    mtt = Column(Integer, nullable=True)     
    cat = Column(String, nullable=True)
    kms = Column(String, nullable=True)
    stat = Column(String, nullable=True)
    ville = Column(String, nullable=True)
    immatriculation = Column(String, nullable=True)
    expiration = Column(Date, nullable=True)
    marque = Column(String, nullable=True)
    type = Column(String, nullable=True)
    numero_serie = Column(String, nullable=True)
    puis_fis_cv = Column(Integer, nullable=True)
    mise_en_circulation = Column(Date, nullable=True)
    observations = Column(String, nullable=True)
    quotite = Column(Integer, nullable=True)
    numero_vignette = Column(String, nullable=True)
    ncc = Column(String, nullable=True)
    responsable = Column(String, nullable=True)


class FactureInfo(Base):
    __tablename__ = "facture_info"

    id = Column(Integer, primary_key=True, index=True)

    # ── Émetteur ──
    vendeur_nom = Column(String, nullable=True)
    vendeur_adresse = Column(String, nullable=True)
    vendeur_telephone = Column(String, nullable=True)
    vendeur_email = Column(String, nullable=True)
    vendeur_rccm = Column(String, nullable=True)
    vendeur_compte_contribuable = Column(String, nullable=True)

    # ── Client ──
    client_nom = Column(String, nullable=True)
    client_adresse = Column(String, nullable=True)
    client_telephone = Column(String, nullable=True)
    client_email = Column(String, nullable=True)
    client_code = Column(String, nullable=True)

    # ── Identifiants facture ──
    numero_facture = Column(String, nullable=True)
    date_facture = Column(Date, nullable=True)
    date_echeance = Column(Date, nullable=True)
    numero_bon_commande = Column(String, nullable=True)
    numero_bon_livraison = Column(String, nullable=True)
    objet = Column(String, nullable=True)

    # ── Lignes de détail (JSON) ──
    lignes_descriptions    = Column(JSON, nullable=True)
    lignes_references      = Column(JSON, nullable=True)
    lignes_quantites       = Column(JSON, nullable=True)
    lignes_unites          = Column(JSON, nullable=True)
    lignes_prix_unitaires  = Column(JSON, nullable=True)
    lignes_taux_tva        = Column(JSON, nullable=True)
    lignes_montants_ht     = Column(JSON, nullable=True)
    lignes_montants_ttc    = Column(JSON, nullable=True)

    # ── Totaux ──
    total_ht              = Column(Float, nullable=True)
    remise                = Column(Float, nullable=True)
    total_ht_apres_remise = Column(Float, nullable=True)
    montant_tva           = Column(Float, nullable=True)
    taux_tva_global       = Column(Float, nullable=True)
    total_ttc             = Column(Float, nullable=True)
    acompte               = Column(Float, nullable=True)
    reste_a_payer         = Column(Float, nullable=True)
    devise                = Column(String, nullable=True)

    # ── Paiement ──
    mode_paiement = Column(String, nullable=True)
    banque        = Column(String, nullable=True)
    iban_rib      = Column(String, nullable=True)
    numero_cheque = Column(String, nullable=True)

    # ── Divers ──
    mentions_legales = Column(String, nullable=True)
    notes            = Column(String, nullable=True)
    cachet_signature = Column(String, nullable=True)


class CniInfoRectoVerso(Base):
    __tablename__ = "cni_info_recto"

    id = Column(Integer, primary_key=True, index=True)

    nom = Column(String, nullable=True)
    prenom = Column(String, nullable=True)
    date_de_naissance = Column(Date, nullable=True)
    lieu_de_naissance = Column(String, nullable=True)
    sexe = Column(String, nullable=True)
    taille = Column(Float, nullable=True)
    date_d_expiration = Column(Date, nullable=True)
    numero_de_cni = Column(String, nullable=True)
    nationalite = Column(String, nullable=True)
    nni = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    date_d_emission = Column(Date, nullable=True)
    autorite_d_emission = Column(String, nullable=True)


class PermisConduireInfo(Base):
    __tablename__ = "permis_conduire"

    id = Column(Integer, primary_key=True, index=True)

    nom = Column(String, nullable=True)
    prenom = Column(String, nullable=True)

    date_naissance = Column(Date, nullable=True)
    lieu_naissance = Column(String, nullable=True)

    adresse = Column(String, nullable=True)

    lieu_delivrance = Column(String, nullable=True)

    date_expiration = Column(Date, nullable=True)

    numero_permis = Column(String, nullable=True)

    categories = Column(String, nullable=True)


class CarteGriseInfo(Base):
    __tablename__ = "carte_grise"

    id = Column(Integer, primary_key=True, index=True)

    # ── Identifiants ─────────────────────────────
    numero_immatriculation = Column(String, nullable=True, index=True)
    numero_carte_grise = Column(String, nullable=True, unique=True, index=True)

    # ── Dates ────────────────────────────────────
    date_premiere_mise_circulation = Column(Date, nullable=True)
    date_edition_carte_grise = Column(Date, nullable=True)

    # ── Titulaire ────────────────────────────────
    identite_titulaire = Column(String, nullable=True)

    # ── Véhicule ────────────────────────────────
    marque = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    type_commercial = Column(String, nullable=True)
    couleur = Column(String, nullable=True)
    carrosserie = Column(String, nullable=True)
    energie = Column(String, nullable=True)
    usage_vehicule = Column(String, nullable=True)

    # ── Caractéristiques techniques ─────────────
    nombre_essieux = Column(Integer, nullable=True)
    places_assises = Column(Integer, nullable=True)

    puissance_fiscale = Column(Integer, nullable=True)
    cylindree_cc = Column(Integer, nullable=True)

    masse_vehicule = Column(Integer, nullable=True)  # PTAC
    pv = Column(Integer, nullable=True)               # poids à vide
    cu = Column(Integer, nullable=True)               # charge utile