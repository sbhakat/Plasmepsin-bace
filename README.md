# Flap dynamics in pepsin-like aspartic proteases: a computational perspective using Plasmepsin-II and BACE-1 as model systems
This repo provides all details to repertory and validate the paper Flap dynamics in pepsin-like aspartic proteases: a computational perspective using Plasmepsin-II and BACE-1 as model systems (doi: https://doi.org/10.1101/2020.04.27.062539)

1. Prep folder contains topology, .mdp and .gro file to generate .tpr files to perform simulation with TIP4P-Ew water model
2. TIP3P-MD1 and MD2 contains plumed.dat files to monitor and .tpr files to run MD simulations. MD1 and MD2 denotes MD simulations starting with different initial starting velocities.
3. Torsion TIP3P and TIP4P contains plumed.dat file which uses torsion angles as CVs (as described in the paper) to perform metadynamics simulations.
4. PCA-TIP3P contains plumed.dat file which uses PC1 and PC2 as CVs to perform metadynamics simulations (see the paper for analyses and plots)



