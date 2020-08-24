module load GCC/7.3.0-2.30
module load OpenMPI/3.1.1
module load GROMACS/2018.1-PLUMED

gmx_mpi trjcat -f traj_comp.part000*.xtc -o trajall.xtc
echo 1 | gmx_mpi trjconv -f trajall.xtc -pbc nojump -o trajnoj.xtc -s md.tpr
echo 3 1 | gmx_mpi trjconv -s md.tpr -f trajnoj.xtc -fit rot+trans -o trajfit.xtc
#echo 1 | gmx_mpi trjconv -s md.tpr -f trajfit.xtc -dump 0 -o prot0.gro
#echo 3 3 | gmx_mpi rms -s md.tpr -f trajfit.xtc -o rmsd.xvg -xvg none
#gmx_mpi trjcat -f trajfit.xtc -dt 100 -o tfit_100.xtc
rm trajall.xtc
rm trajnoj.xtc
#rm trajfit.xtc
