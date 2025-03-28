from Enum import Coins, Aretes

# ################## Les six mouvements élémentaires pour le cubie cube #####################

# Up-move
cpU = [Coins.UBR, Coins.URF, Coins.UFL, Coins.ULB, Coins.DFR, Coins.DLF, Coins.DBL, Coins.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Aretes.RU, Aretes.FD, Aretes.LU, Aretes.BD, Aretes.FU, Aretes.LD, Aretes.BU, Aretes.RD, Aretes.FR, Aretes.FL, Aretes.BL, Aretes.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Right-move
cpR = [Coins.DFR, Coins.UFL, Coins.ULB, Coins.URF, Coins.DRB, Coins.DLF, Coins.DBL, Coins.UBR]  # permutation of the Coinsrners
coR = [2, 0, 0, 1, 1, 0, 0, 2]  # changes of the orientations of the Coinsrners
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
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Aretes.FU, Aretes.FD, Aretes.BU, Aretes.BD, Aretes.BL, Aretes.FL, Aretes.RU, Aretes.RD, Aretes.FR, Aretes.LU, Aretes.LD, Aretes.BR]
eoL = [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0]

# Back-move
cpB = [Coins.URF, Coins.UFL, Coins.UBR, Coins.DRB, Coins.DFR, Coins.DLF, Coins.ULB, Coins.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Aretes.FU, Aretes.FD, Aretes.BR, Aretes.BL, Aretes.LU, Aretes.LD, Aretes.RU, Aretes.RD, Aretes.FR, Aretes.FL, Aretes.BU, Aretes.BD]
eoB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
########################################################################################################################

# ################## Les symétries possibles du cubieCube #####################

# 120° clockwise rotation around the long diagonal URF-DBL
cpROT_URF3 = [Coins.URF, Coins.DFR, Coins.DFL, Coins.UFL, Coins.UBR, Coins.DRB, Coins.DBL, Coins.ULB]
coROT_URF3 = [1, 2, 1, 2, 2, 1, 2, 1]
epROT_URF3 = [Aretes.FD, Aretes.FR, Aretes.LD, Aretes.FL, Aretes.BD, Aretes.BR, Aretes.BD, Aretes.BL, Aretes.FU, Aretes.LU, Aretes.RU, Aretes.BU]
eoROT_URF3 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]

# 180° rotation around the axis through the F and B centers
cpROT_F2 = [Coins.DFL, Coins.DFR, Coins.DRB, Coins.DBL, Coins.UFL, Coins.URF, Coins.UBR, Coins.ULB]
coROT_F2 = [0, 0, 0, 0, 0, 0, 0, 0]
epROT_F2 = [Aretes.RU, Aretes.LD, Aretes.LU, Aretes.BD, Aretes.BU, Aretes.FD, Aretes.FU, Aretes.BD, Aretes.FL, Aretes.FR, Aretes.BR, Aretes.BL]
eoROT_F2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 90° clockwise rotation around the axis through the U and D centers
cpROT_U4 = [Coins.UBR, Coins.URF, Coins.UFL, Coins.ULB, Coins.DRB, Coins.DFR, Coins.DFL, Coins.DBL]
coROT_U4 = [0, 0, 0, 0, 0, 0, 0, 0]
epROT_U4 = [Aretes.BD, Aretes.FU, Aretes.FD, Aretes.BU, Aretes.BD, Aretes.LU, Aretes.LD, Aretes.RU, Aretes.BR, Aretes.FR, Aretes.FL, Aretes.BL]
eoROT_U4 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]

# reflection at the plane through the U, D, F, B centers
cpMIRR_LR2 = [Coins.UFL, Coins.URF, Coins.UBR, Coins.ULB, Coins.DFL, Coins.DFR, Coins.DRB, Coins.DBL]
coMIRR_LR2 = [3, 3, 3, 3, 3, 3, 3, 3]
epMIRR_LR2 = [Aretes.BU, Aretes.FD, Aretes.FU, Aretes.BD, Aretes.RU, Aretes.LD, Aretes.LU, Aretes.BD, Aretes.FL, Aretes.FR, Aretes.BR, Aretes.BL]
eoMIRR_LR2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
