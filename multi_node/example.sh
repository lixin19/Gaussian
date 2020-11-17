#!/bin/bash
#SBATCH --job-name=example
#SBATCH --nodes=3
#SBATCH --cpus-per-task=28
#SBATCH --time=220:00:00
#SBATCH --mem=0

#SBATCH --partition=chem
#SBATCH --account=chem

# load Gaussian environment
module load contrib/g16.b01
export inputfile='example.gjf'


# debugging information
echo "**** Job Debugging Information ****"
echo "This job will run on $SLURM_JOB_NODELIST"
echo ""
echo "ENVIRONMENT VARIABLES"
set
echo "**********************************************" 

# scrubbed scratch
export scrDir='/gscratch/scrubbed/rbeck4/'
mkdir -p $scrDir
export GAUSS_SCRDIR=$scrDir


## Memory
gbmem=`expr $SLURM_MEM_PER_NODE / 1000`
gbmem=`expr $gbmem - 10`
echo "Parsed memory: $gbmem"
sed -i "/mem/s/.*/%mem=${gbmem}GB/" $inputfile


## Set number of threads
export num_threads=$(echo $SLURM_JOB_CPUS_PER_NODE| cut -f1 -d"(" )
sed -i "/nproc/s/.*/%nprocshared=${num_threads}/" $inputfile


# add linda nodes
nodes=()
nodes+=(`scontrol show hostnames $SLURM_JOB_NODELIST `)
for ((i=0; i<${#nodes[*]}-1; i++));
do
	string+=${nodes[$i]}
	string+=","
done 
string+=${nodes[$SLURM_NNODES-1]}
sed -i -e "s/\%LindaWorker.*/\%LindaWorker=$string/gI" "$inputfile"

# check that the Linda nodes are correct
lindaline=(`grep -i 'lindaworker' $inputfile`)
if [[ $lindaline == *$string ]]
then
	echo "Using the correct nodes for Linda"
else
	echo "Using the wrong nodes for Linda"
	echo "Nodes assigned by scheduler = $string"
	echo "Line in Gaussian input file = $lindaline"
	exit 1
fi 

# run Gaussian
g16 $inputfile

exit 0 
