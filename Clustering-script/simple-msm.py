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

lag_time = 100 # 20ps * 200 = 4 ns
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
