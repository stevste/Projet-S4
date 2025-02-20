import RubiksCubeTailleN

def jouerFormule(formule: list, cube: RubiksCubeTailleN):
    for i in formule:
        cube.ajouterAction(i)