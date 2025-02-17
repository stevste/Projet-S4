import RubiksCubeTailleN

def jouerFormule(formule: list, cube: RubiksCubeTailleN):
    for i in formule:
        cube.pivoterFace(i[0], i[1])