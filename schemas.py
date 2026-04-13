from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class VisiteInfo(BaseModel):
    centre: Optional[str] = Field(default=None, description="à droite de CENTRE dans le document")
    mtt: Optional[int] = Field(default=None, description="à droite de MTT dans le document")
    cat: Optional[str] = Field(default=None, description="à droite CAT dans le document")
    kms: Optional[str] = Field(default=None, description="à droite de KMS dans le document")
    stat: Optional[str] = Field(default=None, description="à droite de STAT dans le document")
    ville: Optional[str] = Field(default=None, description="Le nom de la ville")
    immatriculation: Optional[str] = Field(default=None, description="Juste en dessous de Immatriculation")
    expiration: Optional[str] = Field(default=None, description="date d'expiration juste en dessous de Expiration")
    marque: Optional[str] = Field(default=None, description="à droite de MARQUE")
    type: Optional[str] = Field(default=None, description="à droite de TYPE")
    numero_serie: Optional[str] = Field(default=None, description="à droite de N° SERIE")
    puis_fis_cv: Optional[int] = Field(default=None, description="à droite de PUIS.FIS.(CV) juste au dessus de MISE EN CIRC.")
    mise_en_circulation: Optional[date] = Field(default=None, description="la date à droite de MISE EN CIRC")
    observations: Optional[str] = Field(default=None, description="à droite de OBSERVATIONS")
    quotite: Optional[str] = Field(default=None, description="Juste en dessous de QUOTITE")
    numero_vignette: Optional[str] = Field(default=None, description="Juste en dessous de N° VIGNETTE")
    ncc: Optional[str] = Field(default=None, description="Juste en dessous de NCC (peut être vide)")
    responsable: Optional[str] = Field(default=None, description="Juste en dessous de RESPONSABLE")





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


class CniInfoRectoVerso(BaseModel):

    nom: Optional[str] = Field(default=None, description="Nom de famille de la personne titulaire de la carte d'identité")
    prenom: Optional[str] = Field(default=None, description="Prénom de la personne titulaire de la carte d'identité")
    date_de_naissance: Optional[date] = Field(default=None, description="Date de naissance de la personne titulaire de la carte d'identité au format YYYY-MM-DD")
    lieu_de_naissance: Optional[str] = Field(default=None, description="Lieu de naissance de la personne titulaire de la carte d'identité")
    sexe: Optional[str] = Field(default=None, description="Sexe de la personne titulaire de la carte d'identité (M ou F)")
    taille: Optional[float] = Field(default=None, description="Taille de la personne titulaire de la carte d'identité en cm")
    date_d_expiration: Optional[date] = Field(default=None, description="Date d'expiration de la carte d'identité au format YYYY-MM-DD")
    numero_de_cni: Optional[str] = Field(default=None, description="Numéro de la carte d'identité")
    nationalite: Optional[str] = Field(default=None, description="Nationalité de la personne titulaire de la carte d'identité")
    nni: str = Field(default=None, description="Numéro National d'Identification (NNI) présent au verso de la carte d'identité")
    profession: str = Field(default=None, description="Profession de la personne titulaire de la carte d'identité, souvent indiquée au verso")
    date_d_emission: str = Field(default=None, description="Date d'émission de la carte d'identité au format YYYY-MM-DD, souvent indiquée au verso")
    autorite_d_emission: str = Field(default=None, description="Autorité ayant émis la carte d'identité, souvent indiquée au verso")



class PermisConduireInfo(BaseModel):

    nom: str = Field(default=None, description="Numéro National d'Identification (NNI) présent au verso de la carte d'identité")
    prenom: str = Field(default=None, description="Profession de la personne titulaire de la carte d'identité, souvent indiquée au verso")
    date_naissance: date = Field(default=None, description="Date d'émission de la carte d'identité au format YYYY-MM-DD, souvent indiquée au verso")
    adresse: str = Field(default=None, description="Autorité ayant émis la carte d'identité, souvent indiquée au verso")
    lieu_naissance: str = Field(default=None, description="Lieu de naissance de la personne titulaire du permis de conduire")
    lieu_delivrance: str = Field(default=None, description="Lieu de délivrance du permis de conduire")
    date_expiration: date = Field(default=None, description="Date d'expiration du permis de conduire au format YYYY-MM-DD")
    numero_permis: str = Field(default=None, description="Numéro du permis de conduire PC ou N° PERMIS")
    categories: str = Field(default=None, description="Catégories de véhicules autorisées par le permis de conduire")

class CarteGriseInfo(BaseModel):

    numero_immatriculation: str = Field(default=None, description="Numéro d'immatriculation du véhicule")
    numero_carte_grise: str = Field(default=None, description="Numéro de la carte grise")
    date_premiere_mise_circulation: str = Field(default=None, description="Date de première mise en circulation du véhicule au format YYYY-MM-DD")
    date_edition_carte_grise: str = Field(default=None, description="Date d'édition de la carte grise au format YYYY-MM-DD")
    identite_titulaire: str = Field(default=None, description="Identité du titulaire de la carte grise (nom et prénom)")
    marque: str = Field(default=None, description="Marque du véhicule")
    genre: str = Field(default=None, description="Genre du véhicule (VP, CTTE, Camion MOTO, etc.)")
    type_commercial: str = Field(default=None, description="Type commercial du véhicule")
    couleur: str = Field(default=None, description="Couleur du véhicule")
    carrosserie: str = Field(default=None, description="Carrosserie du véhicule")
    energie: str = Field(default=None, description="Type d'énergie du véhicule (essence, diesel, électrique, Gas-Oil etc.)")        
    usage_vehicule: str = Field(default=None, description="Usage du véhicule (particulier, professionnel, privé etc.)")
    nombre_essieux: str = Field(default=None, description="Nombre d'essieux du véhicule")
    places_assises: str = Field(default=None, description="Nombre de places assises du véhicule")
    puissance_fiscale: str = Field(default=None, description="Puissance fiscale du véhicule en CV")
    cylindree_cc: str = Field(default=None, description="Cylindrée du véhicule en centimètres cubes (CC)")
    masse_vehicule: str = Field(default=None, description=" PTAC ou poids total autorisé en charge du véhicule en kg")
    pv: str = Field(default=None, description="Poids à vide du véhicule en kg")
    cu: str = Field(default=None, description="Charge utile du véhicule en kg")