"""
Module : fonctions.capture

Ce module fournit des fonctions pour capturer la sortie d'une fonction sous
forme de texte et l'enregistrer dans un fichier image PNG. Il est
principalement utilisé pour sauvegarder des résultats d'exécution sous une
forme visuelle.
"""

import io
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def capture_et_enregistrer_png(
    fonction_a_executer, *args, chemin="output.png", **kwargs
):
    """
    Exécute une fonction, capture son output (print), et l'enregistre en PNG.

    Args:
        fonction_a_executer (callable): Fonction à exécuter (ex: run_q2).
        *args: Arguments positionnels pour la fonction. chemin (str): Chemin du
        fichier PNG de sortie. **kwargs: Arguments nommés pour la fonction.
    """
    buffer = io.StringIO()
    stdout_original = sys.stdout
    sys.stdout = buffer

    try:
        fonction_a_executer(*args, **kwargs)
    finally:
        sys.stdout = stdout_original

    texte = buffer.getvalue()
    buffer.close()

    print(texte)  # Affiche aussi dans le terminal
    save_print_as_png(texte, chemin)


def save_print_as_png(
    texte: str,
    chemin_sortie: str = "output.png",
    couleur_fond: str = "white",
    couleur_texte: str = "black",
    taille_police: int = 40,
    marge: int = 30,
    ligne_spacing: int = 15,
):
    """
    Sauvegarde un texte sous forme d'image PNG avec des paramètres de mise en
    forme.

    Args:
        texte (str): Le texte à enregistrer sous forme d'image. chemin_sortie
        (str): Le chemin de l'image PNG de sortie (par défaut "output.png").
        couleur_fond (str): La couleur de fond de l'image (par défaut "white").
        couleur_texte (str): La couleur du texte (par défaut "black").
        taille_police (int): La taille de la police en pixels (par défaut 40).
        marge (int): La marge autour du texte en pixels (par défaut 30).
        ligne_spacing (int): L'espacement entre les lignes en pixels (par
        défaut 15).

    Returns:
        None
    """
    # 1. Définir un chemin vers une police Unicode fiable
    police_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",  # Linux
        "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",  # macOS
        "C:\\Windows\\Fonts\\cour.ttf",  # Windows
    ]

    # 2. Sélection de la première police existante
    police_trouvee = None
    for path in police_candidates:
        if Path(path).exists():
            police_trouvee = path
            break

    if not police_trouvee:
        print(
            "Aucune police Unicode trouvée. Utilisation de la police par "
            "défaut."
        )
        police = ImageFont.load_default()
    else:
        print(f"Police utilisée : {police_trouvee}")
        police = ImageFont.truetype(police_trouvee, taille_police)

    # 3. Gérer le texte
    lignes = texte.split("\n")
    largeur = max(police.getlength(ligne) for ligne in lignes) + marge * 2
    hauteur = len(lignes) * (taille_police + ligne_spacing) + marge * 2

    image = Image.new("RGB", (int(largeur), int(hauteur)), color=couleur_fond)
    dessin = ImageDraw.Draw(image)

    y = marge
    for ligne in lignes:
        dessin.text((marge, y), ligne, fill=couleur_texte, font=police)
        y += taille_police + ligne_spacing

    image.save(chemin_sortie, dpi=(300, 300))
    print(f"Image enregistrée : {chemin_sortie}")
