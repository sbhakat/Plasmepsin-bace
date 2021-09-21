## Remember to create the folowing folders before you run the script: data & centers_masses : As the from fast.msm_gen import save_states as ss is hard-coded so that means it can only ## save the outputs in the correctly named folders
## Also name the folder trajectories where you save the *.xtc , name atom_indices.dat for the file which carries atom-indices and name prot_masses.pdb for the topology
##

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

def load_trjs(filenames, **kwargs):
    partial_load = partial(md.load, **kwargs)
    pool = Pool(processes=48)
    trjs = pool.map(partial_load, filenames)
    pool.terminate()
    return trjs


def entry_point():

    if True:
        # filenames
        filenames = np.sort(
            [
                os.path.abspath(pathname)
                for pathname in glob.glob("./trajectories/*.xtc")])
       
        print("obtained filenames!")

        # load atom indices
        pdb = md.load("prot_masses.pdb")
        iis=pdb.topology.select("backbone and resid 72 to 87")
       # iis = np.loadtxt("./atom-indices-bb.dat", dtype=int)

        # topology filename
        prot_masses = "./prot_masses.pdb"
        prot_masses = md.load(prot_masses)

        # load trjs
        print("about to load!!")
        centers = prot_masses.atom_slice(iis)
        trj_lengths, xyzs = load_as_concatenated(
            filenames=filenames, atom_indices=iis,
            processes=48, top=prot_masses)
        trjs_sub = md.Trajectory(xyz=xyzs, topology=centers.top)
        del xyzs

    if True:
        # get subset

        n_clusters = 10000
        #n_clusters = None
        dist_cutoff = 0.01
        clusterer = cluster.KCenters(metric=md.rmsd, cluster_radius=dist_cutoff, n_clusters=n_clusters)
        #clusterer = cluster.KHybrid(metric=md.rmsd, cluster_radius=dist_cutoff, n_clusters=n_clusters, kmedoids_updates=2)
        clusterer.fit(trjs_sub)
        center_indices, distances, assignments, centers = \
            clusterer.result_.partition(trj_lengths)
        ra.save("./data/assignments.h5", assignments)
        ra.save("./data/distances.h5", distances)
        trjs_sub[clusterer.center_indices_].save_xtc("./data/centers.xtc")
        np.save("./data/center_indices.npy", clusterer.center_indices_)
        
        print("Done clustering!") 

    if True:
        lag_time = 10 # 20ps * 200 = 4 ns
        #lag_time = 1 # 20ps * 200 = 4 ns
        assignments = ra.load("./data/assignments.h5")
        unique_states = np.unique(np.concatenate(assignments))
        b = partial(builders.normalize, prior_counts=1/unique_states.shape[0])
        msm_obj = MSM(lag_time=lag_time, method=b)
        msm_obj.fit(assignments)
        np.save("./data/tcounts.npy", msm_obj.tcounts_)
        np.save("./data/tprobs.npy", msm_obj.tprobs_)
        np.save("./data/populations.npy", msm_obj.eq_probs_)
        
        print("Done MSM!")

if __name__=='__main__':
    entry_point()
