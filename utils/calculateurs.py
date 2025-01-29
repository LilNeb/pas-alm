def calculer_mni(revenus_interets, depenses_interets, actifs_productifs_moyens):
    """
    Calcule la Marge Nette d'Intérêt
    """
    mni_absolute = revenus_interets - depenses_interets
    mni_percentage = (mni_absolute / actifs_productifs_moyens) * 100
    return mni_absolute, mni_percentage

def calculer_lcr(actifs_liquides, sorties_nettes):
    """
    Calcule le Liquidity Coverage Ratio
    Args:
        actifs_liquides (float): Total des actifs hautement liquides
        sorties_nettes (float): Sorties nettes de trésorerie sur 30 jours
    Returns:
        float: LCR en pourcentage
    """
    return (actifs_liquides / sorties_nettes) * 100

def calculer_nsfr(financement_stable_disponible, financement_stable_requis):
    """
    Calcule le Net Stable Funding Ratio
    Args:
        financement_stable_disponible (dict): Montants des sources de financement stable
        financement_stable_requis (dict): Montants des besoins de financement stable
    Returns:
        float: NSFR en pourcentage
    """
    total_disponible = sum(financement_stable_disponible.values())
    total_requis = sum(financement_stable_requis.values())
    return (total_disponible / total_requis) * 100 