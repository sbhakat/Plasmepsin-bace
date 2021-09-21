import glob
import mdtraj as md
import numpy as np
import os
from fast.msm_gen import save_states as ss
from functools import partial
from multiprocessing import Pool
from enspara import cluster
from enspara.msm import MSM, builders
from enspara.util.load import load_as_concatenated
from enspara.util import array as ra

dist_cutoff = 0.01
assignments = ra.load("./data/assignments.h5")
distances = ra.load("./data/distances.h5")
ss.save_states(assignments, distances, save_routine='masses',largest_center=dist_cutoff, n_confs=1, n_procs=64)
print("Saving the states!")

prot_masses = "./prot_masses.pdb"
prot_masses = md.load(prot_masses)
pdb_names = np.sort(glob.glob("./centers_masses/*.pdb"))
trj_lengths, xyzs = load_as_concatenated(pdb_names, processes=64, top=prot_masses)
centers_full = md.Trajectory(xyz=xyzs, topology=prot_masses.top)
centers_full.save_xtc("./data/full_centers.xtc")
print("Wrote Full Cluster Centers!")
