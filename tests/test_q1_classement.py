import re


def test20122013_run_q1(monkeypatch, capsys):
    from project.src.q1_classement import run_q1

    run_q1("2012/2013", "Premier League (Angleterre)")
    output = capsys.readouterr().out

    lignes = output.splitlines()

    # On filtre les lignes pour ne garder que celles qui contiennent des
    # résultats
    lignes_resultats = [
        ligne
        for ligne in lignes
        if ligne
        and not ligne.startswith("=")
        and "Classement de" not in ligne
        and "Équipe" not in ligne
    ]

    classement_obtenu = []
    for ligne in lignes_resultats:
        # Expression régulière : capture nom + 3 nombres (DB peut être négatif)
        match = re.match(r"^(.*\S)\s+(\d+)\s+(-?\d+)\s+(\d+)$", ligne.strip())
        if not match:
            raise ValueError(f"Ligne mal formatée : {ligne}")
        nom, pts, db, bm = match.groups()
        classement_obtenu.append((nom, int(pts), int(db), int(bm)))

    # Classement officiel trié par : Pts, Diff de buts (DB), Buts marqués (BM)
    classement_attendu = [
        ("Manchester United", 89, 43, 86),
        ("Manchester City", 78, 32, 66),
        ("Chelsea", 75, 36, 75),
        ("Arsenal", 73, 35, 72),
        ("Tottenham Hotspur", 72, 20, 66),
        ("Everton", 63, 15, 55),
        ("Liverpool", 61, 28, 71),
        ("West Bromwich Albion", 49, -4, 53),
        ("Swansea City", 46, -4, 47),
        ("West Ham United", 46, -8, 45),
        ("Norwich City", 44, -17, 41),
        ("Fulham", 43, -10, 50),
        ("Stoke City", 42, -11, 34),
        ("Southampton", 41, -11, 49),
        ("Aston Villa", 41, -22, 47),
        ("Newcastle United", 41, -23, 45),
        ("Sunderland", 39, -13, 41),
        ("Wigan Athletic", 36, -26, 47),
        ("Reading", 28, -30, 43),
        ("Queens Park Rangers", 25, -30, 30),
    ]

    assert (
        classement_obtenu == classement_attendu
    ), f"Classement incorrect :\n{classement_obtenu}"


def test20152016_run_q1(monkeypatch, capsys):
    from project.src.q1_classement import run_q1

    run_q1("2015/2016", "Premier League (Angleterre)")
    output = capsys.readouterr().out

    lignes = output.splitlines()

    # On filtre les lignes pour ne garder que celles qui contiennent des
    # résultats
    lignes_resultats = [
        ligne
        for ligne in lignes
        if ligne
        and not ligne.startswith("=")
        and "Classement de" not in ligne
        and "Équipe" not in ligne
    ]

    classement_obtenu = []
    for ligne in lignes_resultats:
        # Expression régulière : capture nom + 3 nombres (DB peut être négatif)
        match = re.match(r"^(.*\S)\s+(\d+)\s+(-?\d+)\s+(\d+)$", ligne.strip())
        if not match:
            raise ValueError(f"Ligne mal formatée : {ligne}")
        nom, pts, db, bm = match.groups()
        classement_obtenu.append((nom, int(pts), int(db), int(bm)))

    # Classement officiel trié par : Pts, Diff de buts (DB), Buts marqués (BM)
    classement_attendu = [
        ("Leicester City", 81, 32, 68),
        ("Arsenal", 71, 29, 65),
        ("Tottenham Hotspur", 70, 34, 69),
        ("Manchester City", 66, 30, 71),
        ("Manchester United", 66, 14, 49),
        ("Southampton", 63, 18, 59),
        ("West Ham United", 62, 14, 65),
        ("Liverpool", 60, 13, 63),
        ("Stoke City", 51, -14, 41),
        ("Chelsea", 50, 6, 59),
        ("Everton", 47, 4, 59),
        ("Swansea City", 47, -10, 42),
        ("Watford", 45, -10, 40),
        ("West Bromwich Albion", 43, -14, 34),
        ("Crystal Palace", 42, -12, 39),
        ("Bournemouth", 42, -22, 45),
        ("Sunderland", 39, -14, 48),
        ("Newcastle United", 37, -21, 44),
        ("Norwich City", 34, -28, 39),
        ("Aston Villa", 17, -49, 27),
    ]

    assert (
        classement_obtenu == classement_attendu
    ), f"Classement incorrect :\n{classement_obtenu}"
