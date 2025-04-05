from os import path
import array as ar

N_PERM_4 = 24
N_CHOOSE_8_4 = 70
N_MOVE = 18  # number of possible face moves

N_TWIST = 2187  # 3^7 possible corner orientations in phase 1
N_FLIP = 2048  # 2^11 possible edge orientations in phase 1
N_SLICE_SORTED = 11880  # 12*11*10*9 possible positions of the FR, FL, BL, BR edges in phase 1
N_SLICE = N_SLICE_SORTED // N_PERM_4  # we ignore the permutation of FR, FL, BL, BR in phase 1
N_FLIPSLICE_CLASS = 64430  # number of equivalence classes for combined flip+slice concerning symmetry group D4h

N_U_EDGES_PHASE2 = 1680  # number of different positions of the edges UR, UF, UL and UB in phase 2
# N_D_EDGES_PHASE2 = 1680  # number of different positions of the edges DR, DF, DL and DB in phase 2
N_CORNERS = 40320  # 8! corner permutations in phase 2
N_CORNERS_CLASS = 2768  # number of equivalence classes concerning symmetry group D4h
N_UD_EDGES = 40320  # 8! permutations of the edges in the U-face and D-face in phase 2

N_SYM = 48  # number of cube symmetries of full group Oh
N_SYM_D4h = 16  # Number of symmetries of subgroup D4h
FOLDER = "RubiksData"  # Folder name for generated tables

INVALID = 65535
uint32 = 'I' if ar.array('I').itemsize >= 4 else 'L'
TOTALP1 = N_FLIPSLICE_CLASS * N_TWIST
TOTALP2 = N_CORNERS_CLASS * N_UD_EDGES

def get_flipslice_twist_depth3(ix):
    """get_fst_depth3(ix) is *exactly* the number of moves % 3 to solve phase 1 of a cube with index ix"""
    y = flipslice_twist_depth3[ix // 16]
    y >>= (ix % 16) * 2
    return y & 3


def get_corners_ud_edges_depth3(ix):
    """corners_ud_edges_depth3(ix) is *at least* the number of moves % 3 to solve phase 2 of a cube with index ix"""
    y = corners_ud_edges_depth3[ix // 16]
    y >>= (ix % 16) * 2
    return y & 3


def set_flipslice_twist_depth3(ix, value):
    shift = (ix % 16) * 2
    base = ix >> 4
    flipslice_twist_depth3[base] &= ~(3 << shift) & 0xffffffff
    flipslice_twist_depth3[base] |= value << shift


def set_corners_ud_edges_depth3(ix, value):
    shift = (ix % 16) * 2
    base = ix >> 4
    corners_ud_edges_depth3[base] &= ~(3 << shift) & 0xffffffff
    corners_ud_edges_depth3[base] |= value << shift

fname = "conj_twist"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), 'rb')
twist_conj = ar.array('H')
twist_conj.fromfile(fh, N_TWIST * N_SYM_D4h)

fname = "conj_ud_edges"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
ud_edges_conj = ar.array('H')
ud_edges_conj.fromfile(fh, N_UD_EDGES * N_SYM_D4h)

fname1 = "fs_classidx"
fname2 = "fs_sym"
fname3 = "fs_rep"

print("loading " + "flipslice sym-tables...")

fh = open(path.join(FOLDER, fname1), 'rb')
flipslice_classidx = ar.array('H')
flipslice_classidx.fromfile(fh, N_FLIP * N_SLICE)
fh.close()
fh = open(path.join(FOLDER, fname2), 'rb')
flipslice_sym = ar.array('B')
flipslice_sym.fromfile(fh, N_FLIP * N_SLICE)
fh.close()
fh = open(path.join(FOLDER, fname3), 'rb')
flipslice_rep = ar.array(uint32)
flipslice_rep.fromfile(fh, N_FLIPSLICE_CLASS)
fh.close()

fname1 = "co_classidx"
fname2 = "co_sym"
fname3 = "co_rep"

print("loading " + "corner sym-tables...")

fh = open(path.join(FOLDER, fname1), 'rb')
corner_classidx = ar.array('H')
corner_classidx.fromfile(fh, N_CORNERS)
fh.close()
fh = open(path.join(FOLDER, fname2), 'rb')
corner_sym = ar.array('B')
corner_sym.fromfile(fh, N_CORNERS)
fh.close()
fh = open(path.join(FOLDER, fname3), 'rb')
corner_rep = ar.array('H')
corner_rep.fromfile(fh, N_CORNERS_CLASS)
fh.close()

fname = "move_twist"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
twist_move = ar.array('H')
twist_move.fromfile(fh, N_TWIST * N_MOVE)
fh.close()

fname = "move_flip"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
flip_move = ar.array('H')
flip_move.fromfile(fh, N_FLIP * N_MOVE)
fh.close()

fname = "move_slice_sorted"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
slice_sorted_move = ar.array('H')
slice_sorted_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()

fname = "move_u_edges"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
u_edges_move = ar.array('H')
u_edges_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()

fname = "move_d_edges"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
d_edges_move = ar.array('H')
d_edges_move.fromfile(fh, N_SLICE_SORTED * N_MOVE)
fh.close()

fname = "move_ud_edges"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
ud_edges_move = ar.array('H')
ud_edges_move.fromfile(fh, N_UD_EDGES * N_MOVE)
fh.close()

fname = "move_corners"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
corners_move = ar.array('H')
corners_move.fromfile(fh, N_CORNERS * N_MOVE)
fh.close()

fname = "phase1_prun"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
flipslice_twist_depth3 = ar.array(uint32)
flipslice_twist_depth3.fromfile(fh, TOTALP1 // 16 + 1)
fh.close()

fname = "phase2_prun"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
corners_ud_edges_depth3 = ar.array(uint32)
corners_ud_edges_depth3.fromfile(fh, TOTALP2 // 16)

fname = "phase2_cornsliceprun"

print("loading " + fname + " table...")
fh = open(path.join(FOLDER, fname), "rb")
cornslice_depth = ar.array('b')
cornslice_depth.fromfile(fh, N_CORNERS * N_PERM_4)