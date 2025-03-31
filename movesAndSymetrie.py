from Enum import Coins, Aretes

# ################## Les six mouvements élémentaires pour le cubie cube #####################

# ################## The basic six cube moves described by permutations and changes in orientation #####################

# Up-move
cpU = [Coins.UBR, Coins.URF, Coins.UFL, Coins.ULB, Coins.DFR, Coins.DLF, Coins.DBL, Coins.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Aretes.UB, Aretes.UR, Aretes.UF, Aretes.UL, Aretes.DR, Aretes.DF, Aretes.DL, Aretes.DB, Aretes.FR, Aretes.FL, Aretes.BL, Aretes.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Right-move
cpR = [Coins.DFR, Coins.UFL, Coins.ULB, Coins.URF, Coins.DRB, Coins.DLF, Coins.DBL, Coins.UBR]  # permutation of the corners
coR = [2, 0, 0, 1, 1, 0, 0, 2]  # changes of the orientations of the corners
epR = [Aretes.FR, Aretes.UF, Aretes.UL, Aretes.UB, Aretes.BR, Aretes.DF, Aretes.DL, Aretes.DB, Aretes.DR, Aretes.FL, Aretes.BL, Aretes.UR]  # permutation of the edges
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # changes of the permutations of the edges

# Front-move
cpF = [Coins.UFL, Coins.DLF, Coins.ULB, Coins.UBR, Coins.URF, Coins.DFR, Coins.DBL, Coins.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Aretes.UR, Aretes.FL, Aretes.UL, Aretes.UB, Aretes.DR, Aretes.FR, Aretes.DL, Aretes.DB, Aretes.UF, Aretes.DF, Aretes.BL, Aretes.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# Down-move
cpD = [Coins.URF, Coins.UFL, Coins.ULB, Coins.UBR, Coins.DLF, Coins.DBL, Coins.DRB, Coins.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Aretes.UR, Aretes.UF, Aretes.UL, Aretes.UB, Aretes.DF, Aretes.DL, Aretes.DB, Aretes.DR, Aretes.FR, Aretes.FL, Aretes.BL, Aretes.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Left-move
cpL = [Coins.URF, Coins.ULB, Coins.DBL, Coins.UBR, Coins.DFR, Coins.UFL, Coins.DLF, Coins.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Aretes.UR, Aretes.UF, Aretes.BL, Aretes.UB, Aretes.DR, Aretes.DF, Aretes.FL, Aretes.DB, Aretes.FR, Aretes.UL, Aretes.DL, Aretes.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Back-move
cpB = [Coins.URF, Coins.UFL, Coins.UBR, Coins.DRB, Coins.DFR, Coins.DLF, Coins.ULB, Coins.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Aretes.UR, Aretes.UF, Aretes.UL, Aretes.BR, Aretes.DR, Aretes.DF, Aretes.DL, Aretes.BL, Aretes.FR, Aretes.FL, Aretes.UB, Aretes.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

# ################## Les symétries possibles du cubieCube #####################

# 120° clockwise rotation around the long diagonal URF-DBL
cpROT_URF3 = [Coins.URF, Coins.DFR, Coins.DLF, Coins.UFL, Coins.UBR, Coins.DRB, Coins.DBL, Coins.ULB]
coROT_URF3 = [1, 2, 1, 2, 2, 1, 2, 1]
epROT_URF3 = [Aretes.UF, Aretes.FR, Aretes.DF, Aretes.FL, Aretes.UB, Aretes.BR, Aretes.DB, Aretes.BL, Aretes.UR, Aretes.DR, Aretes.DL, Aretes.UL]
eoROT_URF3 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]

# 180° rotation around the axis through the F and B centers
cpROT_F2 = [Coins.DLF, Coins.DFR, Coins.DRB, Coins.DBL, Coins.UFL, Coins.URF, Coins.UBR, Coins.ULB]
coROT_F2 = [0, 0, 0, 0, 0, 0, 0, 0]
epROT_F2 = [Aretes.DL, Aretes.DF, Aretes.DR, Aretes.DB, Aretes.UL, Aretes.UF, Aretes.UR, Aretes.UB, Aretes.FL, Aretes.FR, Aretes.BR, Aretes.BL]
eoROT_F2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 90° clockwise rotation around the axis through the U and D centers
cpROT_U4 = [Coins.UBR, Coins.URF, Coins.UFL, Coins.ULB, Coins.DRB, Coins.DFR, Coins.DLF, Coins.DBL]
coROT_U4 = [0, 0, 0, 0, 0, 0, 0, 0]
epROT_U4 = [Aretes.UB, Aretes.UR, Aretes.UF, Aretes.UL, Aretes.DB, Aretes.DR, Aretes.DF, Aretes.DL, Aretes.BR, Aretes.FR, Aretes.FL, Aretes.BL]
eoROT_U4 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]

# reflection at the plane through the U, D, F, B centers
cpMIRR_LR2 = [Coins.UFL, Coins.URF, Coins.UBR, Coins.ULB, Coins.DLF, Coins.DFR, Coins.DRB, Coins.DBL]
coMIRR_LR2 = [3, 3, 3, 3, 3, 3, 3, 3]
epMIRR_LR2 = [Aretes.UL, Aretes.UF, Aretes.UR, Aretes.UB, Aretes.DL, Aretes.DF, Aretes.DR, Aretes.DB, Aretes.FL, Aretes.FR, Aretes.BR, Aretes.BL]
eoMIRR_LR2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]