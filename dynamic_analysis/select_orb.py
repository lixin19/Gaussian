#python3
#To select the most delocalized orbital from the orbital based mulliken analysis

#import os
import numpy as np

#CurrentPath = os.getcwd()
def delocal_orb(fn):
    '''
    Read in orbbital based mulliken analysis file and select the most delocalized orbital
    '''
    f = open(fn,'r')
    mlk = f.readlines()
    f.close()
    orb = []
    start = [1,109]
    for a in range(len(start)):
        sq = [] #a list of sqaured deviation
        for i in range(start[a],136): #skip the first line
            num = mlk[i].split()
            orb_w = []
            for j in range(1,len(num)):
                orb_w.append(float(num[j]))
            sq.append(np.std(np.asarray(orb_w)))
        orb.append(np.argmin(np.asarray(sq))+start[a]) #find the orbital index
    
    fw = open('orb_'+fn,'w')
    fw.write(mlk[0])
    for a in range(len(orb)):
        fw.write(mlk[orb[a]])
    fw.close()

    return orb

def localized_MO(fn,m):
    '''
    Read in orbital based mulliken analysis file and find the MOs which are mainly localized on a specific H2O molecule.
    '''
    f = open(fn,'r')
    mlk = f.readlines()
    f.close()
    orb = []
    for i in range(1,675):
        num=mlk[i].split()
        orb.append(float(num[m-1]))
        

def gen_cub(fn,orb):
    '''
    generate the cube file for a specific orbital from the chk file
    '''
    import os

    CurrentPath = os.getcwd()

    f = open('cub_'+fn+'.sh','w')
    f.write('#!/bin/bash\n')
    f.write('#SBATCH --job-name=gen_cub\n')
    f.write('#SBATCH --nodes=1\n')
    f.write('#SBATCH --ntasks-per-node=28\n')
    f.write('#SBATCH --time=24:00:00\n')
    f.write('#SBATCH --mem=110G\n')
    f.write('#SBATCH --chdir=%s\n'%CurrentPath)
    f.write('#SBATCH --partition=chem\n')
    f.write('#SBATCH --account=chem\n\n')
    f.write('# load Gaussian environment\n')
    f.write('module load contrib/gdv.i13p\n\n')
    f.write('# debugging information\necho "**** Job Debugging Information ****"\necho "This job will run on $SLURM_JOB_NODELIST"\necho ""\necho "ENVIRONMENT VARIABLES"\nset\necho "**********************************************"\n\n')
    f.write('formchk %s.chk\n'%fn)
    f.write('cubegen 1 MO=%d %s.fchk %s_%d.cub\n'%(orb,fn,fn,orb))
    f.write('\nexit 0\n')
    f.close()

    os.system('sbatch cub_%s.sh'%fn)



#main()
for i in [0,14,25,50,70]:
    f = 'mlk/mlk_t%d.log'%(i)
    fw = open('orb_sum.log','a+')
    fw.write('%5d'%(i+1))
    orb = delocal_orb(f)
    fn = 'cub_t%d'%(i)
#    gen_cub(fn,orb[1])
    fw.write('%5d\t%5d\n'%(orb[0],orb[1]))
    fw.close()
    


