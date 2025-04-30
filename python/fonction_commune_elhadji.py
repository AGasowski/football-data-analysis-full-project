
def fusionner_colonnes_en_listes(df, colonnes):
    """
    Fusionne les valeurs de plusieurs colonnes sélectionnées d’un DataFrame ligne par ligne.

    Paramètres:
    -----------
    df : pandas.DataFrame
        Le DataFrame contenant les données d’entrée.

    colonnes : list of str
        Liste des noms de colonnes du DataFrame à fusionner. Les colonnes doivent exister 
        dans le DataFrame. Chaque ligne des colonnes sélectionnées sera transformée en une liste.

    Retourne:
    ---------
    list of list
        Une liste de listes, où chaque sous-liste contient les valeurs d’une ligne pour les 
        colonnes spécifiées.
    """
    if not all(col in df.columns for col in colonnes):
        raise ValueError("Une ou plusieurs colonnes spécifiées n'existent pas dans le DataFrame.")
    
    return df[colonnes].apply(lambda row: list(row), axis=1).tolist()

def cle_maximale(D):
    """
    Renvoie la clé associée à la plus grande valeur dans un dictionnaire.

    Paramètres
    ----------
    D : dict
        Dictionnaire dont les valeurs sont comparables (int, float, etc.).

    Retourne
    --------
    key
        La clé correspondant à la valeur maximale dans le dictionnaire.

    Lève
    -----
    ValueError
        Si le dictionnaire est vide.
    """
    if not D:
        raise ValueError("Le dictionnaire est vide.")
    
    return max(D, key=D.get)

def cle_minimale(D):
    """
    Renvoie la clé associée à la plus petite valeur dans un dictionnaire.

    Paramètres
    ----------
    D : dict
        Dictionnaire dont les valeurs sont comparables (int, float, etc.).

    Retourne
    --------
    key
        La clé correspondant à la valeur maximale dans le dictionnaire.

    Lève
    -----
    ValueError
        Si le dictionnaire est vide.
    """
    if not D:
        raise ValueError("Le dictionnaire est vide.")
    
    return min(D, key=D.get)

def moyenne_liste(L):
    """
    Calcule la moyenne des éléments d'une liste de nombres.

    Paramètres
    ----------
    L : list of int or float
        Liste contenant des valeurs numériques.

    Retourne
    --------
    float
        La moyenne arithmétique des éléments de la liste.

    Lève
    -----
    ValueError
        Si la liste est vide.
    """
    if not L:
        raise ValueError("La liste est vide.")
    
    return sum(L) / len(L)

def appliquer_fonction_aux_valeurs(d, f):
    """
    Applique une fonction à chaque valeur d’un dictionnaire et renvoie un nouveau dictionnaire.

    Paramètres
    ----------
    d : dict
        Dictionnaire dont les valeurs seront transformées.
    
    f : callable
        Fonction à appliquer à chaque valeur du dictionnaire.

    Retourne
    --------
    dict
        Nouveau dictionnaire avec les mêmes clés et les valeurs transformées par la fonction.
    """
    return {k: f(v) for k, v in d.items()} 

def element_min_colonne(df, col_b, col_a):
    """
    Renvoie l'élément de la colonne 'col_a' où la valeur correspondante dans la colonne 'col_b' est minimale.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant les colonnes spécifiées.
        
    col_b : str
        Le nom de la colonne dans le DataFrame où la valeur minimale sera recherchée.
        
    col_a : str
        Le nom de la colonne dans le DataFrame dont l'élément sera renvoyé pour la ligne où la valeur de 'col_b' est minimale.

    Retourne
    -------
    element : type de l'élément dans 'col_a'
        L'élément de la colonne 'col_a' correspondant à la ligne où la colonne 'col_b' a la valeur minimale.
        Si plusieurs éléments ont la même valeur minimale dans 'col_b', l'élément de la première ligne est retourné.

    Exemple
    -------
    >>> df = pd.DataFrame({'A': [10, 20, 30, 40], 'B': [5, 2, 9, 1]})
    >>> element_min_colonne(df, 'B', 'A')
    40

    L'exemple ci-dessus retourne '40' car la valeur minimale de la colonne 'B' est '1',
    et l'élément correspondant de la colonne 'A' à cet index est '40'.
    """
    # Trouver l'index de la valeur minimale dans la colonne spécifiée 'col_b'
    idx_min = df[col_b].idxmin()
    # Retourner l'élément correspondant dans la colonne spécifiée 'col_a'
    return df.loc[idx_min, col_a]

def data_to_dict(df, col_a, col_b):
    """
    Crée un dictionnaire à partir de deux colonnes d'un DataFrame où chaque élément
    de la première colonne devient une clé et l'élément correspondant de la seconde
    colonne devient la valeur associée.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant les colonnes spécifiées.
        
    col_a : str
        Le nom de la colonne dont les éléments seront utilisés comme clés dans le dictionnaire.
        
    col_b : str
        Le nom de la colonne dont les éléments seront utilisés comme valeurs dans le dictionnaire.

    Retourne
    -------
    dict
        Un dictionnaire où les clés sont les éléments de la colonne `col_a` et les valeurs sont
        les éléments correspondants de la colonne `col_b`.

    Exemple
    -------
    >>> df = pd.DataFrame({'A': ['a', 'b', 'c', 'd'], 'B': [1, 2, 3, 4]})
    >>> creer_dictionnaire(df, 'A', 'B')
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    L'exemple ci-dessus retourne un dictionnaire où les éléments de la colonne 'A'
    sont utilisés comme clés et ceux de la colonne 'B' comme valeurs.
    """
    # Crée le dictionnaire à partir des colonnes A et B
    return dict(zip(df[col_a], df[col_b]))

def moyenne_par_colonne(df, col_1, col_2):
    """
    Crée un dictionnaire où chaque clé est un identifiant (col_1) et la valeur est la
    moyenne des valeurs de la colonne (col_2) associées à cet identifiant.

    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant les colonnes spécifiées.
        
    col_1 : str
        Nom de la colonne représentant les identifiants (par exemple, 'id').
        
    col_2 : str
        Nom de la colonne représentant les valeurs à agréger (par exemple, 'ratio').

    Retourne
    -------
    dict
        Un dictionnaire où chaque clé est un identifiant et chaque valeur est la moyenne des valeurs
        associées à cet identifiant dans la colonne `col_2`.
    """
    # Calcul de la moyenne des valeurs dans col_2 pour chaque identifiant dans col_1
    moyenne_values = df.groupby(col_1)[col_2].mean().to_dict()

    return moyenne_values







