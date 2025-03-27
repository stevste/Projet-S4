from Enum import Coins, Aretes

# ################## Les six mouvements élémentaires pour le cubie cube #####################

# Up-move
cpU = [Coins.UBR, Coins.URF, Coins.UFL, Coins.ULB, Coins.DFR, Coins.DLF, Coins.DBL, Coins.DRB]
CoU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Aretes.RU, Aretes.FD, Aretes.LU, Aretes.BD, Aretes.FU, Aretes.LD, Aretes.BU, Aretes.RD, Aretes.FR, Aretes.FL, Aretes.BL, Aretes.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Right-move
cpR = [Coins.DFR, Coins.UFL, Coins.ULB, Coins.URF, Coins.DRB, Coins.DLF, Coins.DBL, Coins.UBR]  # permutation of the Coinsrners
CoinsR = [2, 0, 0, 1, 1, 0, 0, 2]  # changes of the orientations of the Coinsrners
epR = [Aretes.FU, Aretes.FD, Aretes.BU, Aretes.BD, Aretes.LU, Aretes.LD, Aretes.FR, Aretes.BR, Aretes.RD, Aretes.FL, Aretes.BL, Aretes.RU]  # permutation of the Aretesges
eoR = [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1]  # changes of the permutations of the Aretesges

# Front-move
cpF = [Coins.UFL, Coins.DLF, Coins.ULB, Coins.UBR, Coins.URF, Coins.DFR, Coins.DBL, Coins.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Aretes.FL, Aretes.FR, Aretes.BU, Aretes.BD, Aretes.LU, Aretes.LD, Aretes.RU, Aretes.RD, Aretes.FU, Aretes.FD, Aretes.BL, Aretes.BR]
eoF = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Down-move
cpD = [Coins.URF, Coins.UFL, Coins.ULB, Coins.UBR, Coins.DLF, Coins.DBL, Coins.DRB, Coins.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Aretes.FU, Aretes.LD, Aretes.BU, Aretes.RD, Aretes.LU, Aretes.BD, Aretes.RU, Aretes.FD, Aretes.FR, Aretes.FL, Aretes.BL, Aretes.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Left-move
cpL = [Coins.URF, Coins.ULB, Coins.DBL, Coins.UBR, Coins.DFR, Coins.UFL, Coins.DLF, Coins.DRB]
coD = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Aretes.FU, Aretes.FD, Aretes.BU, Aretes.BD, Aretes.BL, Aretes.FL, Aretes.RU, Aretes.RD, Aretes.FR, Aretes.LU, Aretes.LD, Aretes.BR]
eoL = [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0]

# Back-move
cpB = [Coins.URF, Coins.UFL, Coins.UBR, Coins.DRB, Coins.DFR, Coins.DLF, Coins.ULB, Coins.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Aretes.FU, Aretes.FD, Aretes.BR, Aretes.BL, Aretes.LU, Aretes.LD, Aretes.RU, Aretes.RD, Aretes.FR, Aretes.FL, Aretes.BU, Aretes.BD]
eoB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
########################################################################################################################

# ################## Les symétries possibles du cubieCube pour le cubie cube #####################