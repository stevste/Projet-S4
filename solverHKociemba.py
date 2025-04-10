# ################### The SolverThread class solves implements the two phase algorithm #################################
import RubiksCubeTailleN as rubiks
import threading as thr
import CubieCube as cubie
import PrunningTable as prT
from Enum import *
import time


class SolverThread(thr.Thread):

    def __init__(self, cb_cube, rot, inv, ret_length, timeout, start_time, solutions, terminated, shortest_length):
        """
        :param cb_cube: The cube to be solved in CubieCube representation
        :param rot: Rotates the  cube 120° * rot along the long diagonal before applying the two-phase-algorithm
        :param inv: 0: Do not invert the cube . 1: Invert the cube before applying the two-phase-algorithm
        :param ret_length: If a solution with length <= ret_length is found the search stops.
         The most efficient way to solve a cube is to start six threads in parallel with rot = 0, 1 and 2 and 
         inv = 0, 1. The first thread which finds a solutions sets the terminated flag which signals all other threads
         to teminate. On average this solves a cube about 12 times faster than solving one cube with a single thread.
         And this despite of Pythons GlobalInterpreterLock GIL.
        :param timeout: Essentially the maximal search time in seconds. Essentially because the search does not return
         before at least one solution has been found.
        :param start_time: The time the search started.
        :param solutions: An array with the found solutions found by the six parallel threads
        :param terminated: An event shared by the six threads to signal a termination request
        :param shortest_length: The length of the shortes solutions in the solution array
        """
        thr.Thread.__init__(self)
        self.cb_cube = cb_cube  # CubieCube
        self.rot = rot
        self.inv = inv
        self.sofar_phase1 = None
        self.sofar_phase2 = None
        self.phase2_done = False
        self.lock = thr.Lock()
        self.ret_length = ret_length
        self.timeout = timeout
        self.start_time = start_time

        self.cornersave = 0

        # these variables are shared by the six threads, initialized in function solve
        self.solutions = solutions
        self.terminated = terminated
        self.shortest_length = shortest_length

    def search_phase2(self, corners, ud_edges, slice_sorted, dist, togo_phase2):
        # ##############################################################################################################
        if self.terminated.is_set() or self.phase2_done:
            return
        ################################################################################################################
        if togo_phase2 == 0 and slice_sorted == 0:
            self.lock.acquire()  # phase 2 solved, store solution
            man = self.sofar_phase1 + self.sofar_phase2
            if len(self.solutions) == 0 or (len(self.solutions[-1]) > len(man)):

                if self.inv == 1:  # we solved the inverse cube
                    man = list(reversed(man))
                    man[:] = [Moves((m // 3) * 3 + (2 - m % 3)) for m in man]  # R1->R3, R2->R2, R3->R1 etc.
                man[:] = [Moves(cubie.conjMove[prT.N_MOVE * 16 * self.rot + m]) for m in man]
                self.solutions.append(man)
                self.shortest_length[0] = len(man)

            if self.shortest_length[0] <= self.ret_length:  # we have reached the target length
                self.terminated.set()
            self.lock.release()
            self.phase2_done = True
        else:
            for m in Moves:
                if m in [Moves.R1, Moves.R3, Moves.F1, Moves.F3,
                         Moves.L1, Moves.L3, Moves.B1, Moves.B3]:
                    continue

                if len(self.sofar_phase2) > 0:
                    diff = self.sofar_phase2[-1] // 3 - m // 3
                    if diff in [0, 3]:  # successive moves: on same face or on same axis with wrong order
                        continue
                else:
                    if len(self.sofar_phase1) > 0:
                        diff = self.sofar_phase1[-1] // 3 - m // 3
                        if diff in [0, 3]:  # successive moves: on same face or on same axis with wrong order
                            continue

                corners_new = prT.corners_move[18 * corners + m]
                ud_edges_new = prT.ud_edges_move[18 * ud_edges + m]
                slice_sorted_new = prT.slice_sorted_move[18 * slice_sorted + m]

                classidx = prT.corner_classidx[corners_new]
                sym = prT.corner_sym[corners_new]
                dist_new_mod3 = prT.get_corners_ud_edges_depth3(
                    40320 * classidx + prT.ud_edges_conj[(ud_edges_new << 4) + sym])
                dist_new = prT.distance[3 * dist + dist_new_mod3]
                if max(dist_new, prT.cornslice_depth[24 * corners_new + slice_sorted_new]) >= togo_phase2:
                    continue  # impossible to reach solved cube in togo_phase2 - 1 moves

                self.sofar_phase2.append(m)
                self.search_phase2(corners_new, ud_edges_new, slice_sorted_new, dist_new, togo_phase2 - 1)
                self.sofar_phase2.pop(-1)

    def search(self, flip, twist, slice_sorted, dist, togo_phase1):
        # ##############################################################################################################
        if self.terminated.is_set():
            return
        ################################################################################################################
        if togo_phase1 == 0:  # phase 1 solved

            if time.monotonic() > self.start_time + self.timeout and len(self.solutions) > 0:
                self.terminated.set()

            # compute initial phase 2 coordinates
            if self.sofar_phase1:  # check if list is not empty
                m = self.sofar_phase1[-1]
            else:
                m = Moves.U1  # value is irrelevant here, no phase 1 moves

            if m in [Moves.R3, Moves.F3, Moves.L3, Moves.B3]:  # phase 1 solution come in pairs
                corners = prT.corners_move[18 * self.cornersave + m - 1]  # apply R2, F2, L2 ord B2 on last ph1 solution
            else:
                corners = self.cb_cube.GetCornerPermCoord()
                for m in self.sofar_phase1:  # get current corner configuration
                    corners = prT.corners_move[18 * corners + m]
                self.cornersave = corners

            # new solution must be shorter and we do not use phase 2 maneuvers with length > 11 - 1 = 10
            togo2_limit = min(self.shortest_length[0] - len(self.sofar_phase1), 11)
            if prT.cornslice_depth[24 * corners + slice_sorted] >= togo2_limit:  # precheck speeds up the computation
                return

            u_edges = self.cb_cube.GetUEdgeCoord()
            d_edges = self.cb_cube.GetDEdgeCoord()
            for m in self.sofar_phase1:
                u_edges = prT.u_edges_move[18 * u_edges + m]
                d_edges = prT.d_edges_move[18 * d_edges + m]
            ud_edges = prT.u_edges_plus_d_edges_to_ud_edges[24 * u_edges + d_edges % 24]

            dist2 = get_depth_phase2(corners, ud_edges)
            for togo2 in range(dist2, togo2_limit):  # do not use more than togo2_limit - 1 moves in phase 2
                self.sofar_phase2 = []
                self.phase2_done = False
                self.search_phase2(corners, ud_edges, slice_sorted, dist2, togo2)
                if self.phase2_done:  # solution already found
                    break

        else:
            for m in Moves:
                # dist = 0 means that we are already are in the subgroup H. If there are less than 5 moves left
                # this forces all remaining moves to be phase 2 moves. So we can forbid these at the end of phase 1
                # and generate these moves in phase 2.
                if dist == 0 and togo_phase1 < 5 and m in [Moves.U1, Moves.U2, Moves.U3, Moves.R2,
                                                           Moves.F2, Moves.D1, Moves.D2, Moves.D3,
                                                           Moves.L2, Moves.B2]:
                    continue

                if len(self.sofar_phase1) > 0:
                    diff = self.sofar_phase1[-1] // 3 - m // 3
                    if diff in [0, 3]:  # successive moves: on same face or on same axis with wrong order
                        continue

                flip_new = prT.flip_move[18 * flip + m]  # N_MOVE = 18
                twist_new = prT.twist_move[18 * twist + m]
                slice_sorted_new = prT.slice_sorted_move[18 * slice_sorted + m]

                flipslice = 2048 * (slice_sorted_new // 24) + flip_new  # N_FLIP * (slice_sorted // N_PERM_4) + flip
                classidx = prT.flipslice_classidx[flipslice]
                sym = prT.flipslice_sym[flipslice]
                dist_new_mod3 = prT.get_flipslice_twist_depth3(2187 * classidx + prT.twist_conj[(twist_new << 4) + sym])
                dist_new = prT.distance[3 * dist + dist_new_mod3]
                if dist_new >= togo_phase1:  # impossible to reach subgroup H in togo_phase1 - 1 moves
                    continue

                self.sofar_phase1.append(m)
                self.search(flip_new, twist_new, slice_sorted_new, dist_new, togo_phase1 - 1)
                self.sofar_phase1.pop(-1)

    def run(self):
        cb = None
        if self.rot == 0:  # no rotation
            cb = cubie.CubieCube(None, self.cb_cube.cornerPerm, self.cb_cube.cornerOri, self.cb_cube.edgePerm, self.cb_cube.edgeOri)
        elif self.rot == 1:  # conjugation by 120° rotation
            cb = cubie.CubieCube(None, cubie.sTable[32].cornerPerm, cubie.sTable[32].cornerOri, cubie.sTable[32].edgePerm, cubie.sTable[32].edgeOri)
            cb.Composition(self.cb_cube)
            cb.Composition(cubie.sTable[16])
        elif self.rot == 2:  # conjugation by 240° rotation
            cb = cubie.CubieCube(None, cubie.sTable[16].cornerPerm, cubie.sTable[16].cornerPerm, cubie.sTable[16].edgePerm, cubie.sTable[16].edgeOri)
            cb.Composition(self.cb_cube)
            cb.Composition(cubie.sTable[32])
        if self.inv == 1:  # invert cube
            tmp = cb.InvCube()
            cb = tmp

        dist = get_depth_phase1(self.cb_cube)
        for togo1 in range(dist, 20):  # iterative deepening, solution has at least dist moves
            self.sofar_phase1 = []
            self.search(self.cb_cube.GetCornerOriCoord(), self.cb_cube.GetEdgeOriCoord(), self.cb_cube.GetUDSliceCoord(), dist, togo1)


# ################################End class SolverThread################################################################


def solve(cube: rubiks.RubiksCube, max_length=20, timeout=3):
    """Solve a cube defined by its cube definition string.
     :param cubestring: The format of the string is given in the Facelet class defined in the file py
     :param max_length: The function will return if a maneuver of length <= max_length has been found
     :param timeout: If the function times out, the best solution found so far is returned. If there has not been found
     any solution yet the computation continues until a first solution appears.
    """
    
    cc = cubie.CubieCube(cube)

    my_threads = []
    s_time = time.monotonic()

    # these mutable variables are modidified by all six threads
    s_length = [999]
    solutions = []
    terminated = thr.Event()
    terminated.clear()
    syms = cc.GetSymetrie()
    if len(list({16, 20, 24, 28} & set(syms))) > 0:  # we have some rotational symmetry along a long diagonal
        tr = [0, 3]  # so we search only one direction and the inverse
    else:
        tr = range(6)  # This means search in 3 directions + inverse cube
    if len(list(set(range(48, 96)) & set(syms))) > 0:  # we have some antisymmetry so we do not search the inverses
        tr = list(filter(lambda x: x < 3, tr))
    for i in tr:
        th = SolverThread(cc, i % 3, i // 3, max_length, timeout, s_time, solutions, terminated, [999])
        my_threads.append(th)
        th.start()
    for t in my_threads:
        t.join()  # wait until all threads have finished
    s = ''
    if len(solutions) > 0:
        for m in solutions[-1]:  # the last solution is the shortest
            s += m.name + ' '
    print(s + '(' + str(len(s) // 3) + 'f)')
    return s + '(' + str(len(s) // 3) + 'f)'

########################################################################################################################

def get_depth_phase1(cubieCube : cubie.CubieCube):
    """
    Compute the distance to the cube subgroup H where flip=slice=twist=0
    :return: The distance to H
    """
    slice_ = cubieCube.GetUDSliceCoord() // prT.N_PERM_4
    flip = cubieCube.GetCornerOriCoord()
    twist = cubieCube.GetEdgeOriCoord()
    flipslice = prT.N_FLIP * slice_ + flip
    classidx = prT.flipslice_classidx[flipslice]
    sym = prT.flipslice_sym[flipslice]
    depth_mod3 = prT.get_flipslice_twist_depth3(prT.N_TWIST * classidx + prT.twist_conj[(twist << 4) + sym])

    depth = 0
    while flip != 0 or slice_ != 0 or twist != 0:
        if depth_mod3 == 0:
            depth_mod3 = 3
        for m in Moves:
            twist1 = prT.twist_move[prT.N_MOVE * twist + m]
            flip1 = prT.flip_move[prT.N_MOVE * flip + m]
            slice1 = prT.slice_sorted_move[prT.N_MOVE * slice_ * prT.N_PERM_4 + m] // prT.N_PERM_4
            flipslice1 = prT.N_FLIP * slice1 + flip1
            classidx1 = prT.flipslice_classidx[flipslice1]
            sym = prT.flipslice_sym[flipslice1]
            if prT.get_flipslice_twist_depth3(
                    prT.N_TWIST * classidx1 + prT.twist_conj[(twist1 << 4) + sym]) == depth_mod3 - 1:
                depth += 1
                twist = twist1
                flip = flip1
                slice_ = slice1
                depth_mod3 -= 1
                break
    return depth

def get_depth_phase2(corners, ud_edges):
    """
    Get distance to subgroup where only the UD-slice edges may be permuted in their slice (only 24/2 = 12 possible
    ways due to overall even parity). This is a lower bound for the number of moves to solve phase 2.
    :param corners: Corners coordinate
    :param ud_edges: Coordinate of the 8 edges of U and D face.
    :return:
    """
    classidx = prT.corner_classidx[corners]
    sym = prT.corner_sym[corners]
    depth_mod3 = prT.get_corners_ud_edges_depth3(prT.N_UD_EDGES * classidx + prT.ud_edges_conj[(ud_edges << 4) + sym])
    if depth_mod3 == 3:  # unfilled entry, depth >= 11
        return 11
    depth = 0
    while corners != 0 or ud_edges != 0:
        if depth_mod3 == 0:
            depth_mod3 = 3
        # only iterate phase 2 moves
        for m in (Moves.U1, Moves.U2, Moves.U3, Moves.R2, Moves.F2, Moves.D1,
                    Moves.D2, Moves.D3, Moves.L2, Moves.B2):
            corners1 = prT.corners_move[prT.N_MOVE * corners + m]
            ud_edges1 = prT.ud_edges_move[prT.N_MOVE * ud_edges + m]
            classidx1 = prT.corner_classidx[corners1]
            sym = prT.corner_sym[corners1]
            if prT.get_corners_ud_edges_depth3(
                    prT.N_UD_EDGES * classidx1 + prT.ud_edges_conj[(ud_edges1 << 4) + sym]) == depth_mod3 - 1:
                depth += 1
                corners = corners1
                ud_edges = ud_edges1
                depth_mod3 -= 1
                break
    return depth