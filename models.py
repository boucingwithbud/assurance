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
    date_naissance = Column(Date, nullable=True)
    lieu_de_naissance = Column(String, nullable=True)
    sexe = Column(String, nullable=True)
    taille = Column(Float, nullable=True)
    date_expiration = Column(Date, nullable=True)
    numero_de_cni = Column(String, nullable=True)
    nationalite = Column(String, nullable=True)
    nni = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    date_emission = Column(Date, nullable=True)
    autorite_emission = Column(String, nullable=True)


class PermisConduireRectoVerso(Base):
    __tablename__ = "permis_conduire"

    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # INFORMATIONS PERSONNELLES
    # =========================
    nom = Column(String, nullable=True)
    prenom = Column(String, nullable=True)
    date_naissance = Column(Date, nullable=True)
    addresse = Column(String, nullable=True)
    lieu_naissance = Column(String, nullable=True)

    # =========================
    # INFORMATIONS PERMIS
    # =========================
    date_delivrance = Column(Date, nullable=True)
    lieu_delivrance = Column(String, nullable=True)
    numero_permis = Column(String, nullable=True)

    # =========================
    # VALIDITE PAR CATEGORIE
    # =========================
    cat_a_validite = Column(Date, nullable=True)
    cat_b_validite = Column(Date, nullable=True)
    cat_c_validite = Column(Date, nullable=True)
    cat_d_validite = Column(Date, nullable=True)
    cat_e_validite = Column(Date, nullable=True)

    # =========================
    # EXPIRATION PAR CATEGORIE
    # =========================
    cat_a_expiration = Column(Date, nullable=True)
    cat_b_expiration = Column(Date, nullable=True)
    cat_c_expiration = Column(Date, nullable=True)
    cat_d_expiration = Column(Date, nullable=True)
    cat_e_expiration = Column(Date, nullable=True)

    # =========================
    # AUTRES INFOS
    # =========================
    groupe_sanguin = Column(String, nullable=True)
    document_identite = Column(String, nullable=True)

class CarteGriseRectoVerso(Base):
    __tablename__ = "carte_grise"

    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # IDENTIFICATION
    # =========================
    numero_immatriculation = Column(String, nullable=True)
    numero_carte_grise = Column(String, nullable=True)

    # =========================
    # DATES
    # =========================
    date_mise_circulation = Column(Date, nullable=True)
    date_edition_carte_grise = Column(Date, nullable=True)

    # =========================
    # TITULAIRE
    # =========================
    identite_titulaire = Column(String, nullable=True)

    # =========================
    # CARACTERISTIQUES VEHICULE
    # =========================
    marque = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    type_commercial = Column(String, nullable=True)
    couleur = Column(String, nullable=True)
    carrosserie = Column(String, nullable=True)
    energie = Column(String, nullable=True)
    usage_vehicule = Column(String, nullable=True)

    # =========================
    # SPECIFICATIONS TECHNIQUES
    # =========================
    nombre_essieux = Column(Integer, nullable=True)
    places_assises = Column(Integer, nullable=True)
    puissance_fiscale = Column(Integer, nullable=True)
    cylindree_cc = Column(String, nullable=True)

    masse_vehicule = Column(Integer, nullable=True)
    pv = Column(Integer, nullable=True)
    cu = Column(Integer, nullable=True)

    numero_vin_chassis = Column(String, nullable=True)
    numero_moteur = Column(String, nullable=True)
    type_technique = Column(String, nullable=True)

    # =========================
    # INFORMATIONS COMPLEMENTAIRES
    # =========================
    societe_credit = Column(String, nullable=True)
    numero_immatriculation_precedent = Column(String, nullable=True)


class BulletinAdhesion:
    __tablename__ = "bulletin_adhesion"
    
    id = Column(Integer, primary_key=True, index=True)

    nom = Column(String, nullable=True)
    societe_adherente = Column(String, nullable=True)
    adresse = Column(String, nullable=True)
    numero_telephone = Column(String, nullable=True)


from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base



class BulletinAdhesion(Base):
    __tablename__ = "bulletin_adhesion"

    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # INFORMATIONS GENERALES
    # =========================
    nom = Column(String, nullable=True)
    societe_adherente = Column(String, nullable=True)
    adresse = Column(String, nullable=True)
    numero_telephone = Column(String, nullable=True)

    assure_date_entree_entreprise = Column(String, nullable=True)

    # =========================
    # ASSURE
    # =========================
    assure_date_naissance = Column(Date, nullable=True)
    assure_lieu_naissance = Column(String, nullable=True)
    assure_profession = Column(String, nullable=True)
    assure_sport = Column(String, nullable=True)
    assure_poids = Column(Integer, nullable=True)
    assure_taille = Column(Integer, nullable=True)
    assure_maladies = Column(JSON, nullable=True)

    # =========================
    # CONJOINT
    # =========================
    conjoint_date_naissance = Column(Date, nullable=True)
    conjoint_profession = Column(String, nullable=True)
    conjoint_sport = Column(String, nullable=True)
    conjoint_poids = Column(Integer, nullable=True)
    conjoint_taille = Column(Integer, nullable=True)
    conjoint_maladies = Column(JSON, nullable=True)

    # =========================
    # ENFANT 1
    # =========================
    premier_enfant_profession = Column(String, nullable=True)
    premier_enfant_sport = Column(String, nullable=True)
    premier_enfant_poids = Column(Integer, nullable=True)
    premier_enfant_taille = Column(Integer, nullable=True)
    premier_enfant_maladies = Column(JSON, nullable=True)

    # =========================
    # ENFANT 2
    # =========================
    second_enfant_profession = Column(String, nullable=True)
    second_enfant_sport = Column(String, nullable=True)
    second_enfant_poids = Column(Integer, nullable=True)
    second_enfant_taille = Column(Integer, nullable=True)
    second_enfant_maladies = Column(JSON, nullable=True)

    # =========================
    # ENFANT 3
    # =========================
    troisieme_enfant_profession = Column(String, nullable=True)
    troisieme_enfant_sport = Column(String, nullable=True)
    troisieme_enfant_poids = Column(Integer, nullable=True)
    troisieme_enfant_taille = Column(Integer, nullable=True)
    troisieme_enfant_maladies = Column(JSON, nullable=True)

    # =========================
    # ENFANT 4
    # =========================
    quatrieme_enfant_profession = Column(String, nullable=True)
    quatrieme_enfant_sport = Column(String, nullable=True)
    quatrieme_enfant_poids = Column(Integer, nullable=True)
    quatrieme_enfant_taille = Column(Integer, nullable=True)
    quatrieme_enfant_maladies = Column(JSON, nullable=True)

    # =========================
    # ENFANT 5
    # =========================
    cinquieme_enfant_profession = Column(String, nullable=True)
    cinquieme_enfant_sport = Column(String, nullable=True)
    cinquieme_enfant_poids = Column(Integer, nullable=True)
    cinquieme_enfant_taille = Column(Integer, nullable=True)
    cinquieme_enfant_maladies = Column(JSON, nullable=True)