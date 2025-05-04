import re


def test_run_q1(monkeypatch, capsys):
    from project.src.q1_classement import run_q1

    run_q1("2012/2013", "Premier League (Angleterre)")
    output = capsys.readouterr().out

    lignes = output.splitlines()

    # On filtre les lignes pour ne garder que celles qui contiennent des résultats
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
