"""
Usage: soparse.py <overlap log> <pop analysis log>
"""

import numpy as np


def g2f(gfloat):
    '''
    Change the number into scientific notation
    '''
    return float(gfloat.replace('D','E'))

def get_num_basis(fname):
    '''
    get the number of basis functions
    '''
    fin = open(fname)
    for line in fin:
        if 'basis functions' in line and 'primitive gaussians' in line:
            nb = int(line.split()[0])
            break
    return nb

def parse_overlap(fname,nb):
    """
    Parses a file for the overlap matrix.
    Assumes overlap is printed as a triangular matrix
    """

    S = np.zeros((nb,nb))
    fin = open(fname)

    for line in fin:
        if '*** Overlap ***' in line:

            while True:
                line = next(fin) #loop over all the lines in the file
                if '*** Kinetic Energy ***' in line:  #the end of the overlap matrix
                    break

                if 'D' not in line:
                    cols = [int(c) - 1 for c in line.split()] #indices for the column in S
                    continue

                lsp = line.split()
                row = int(lsp[0]) - 1
                vals = np.array([g2f(v) for v in lsp[1:]])

                S[row, cols[0]:(min(row, cols[-1])+1)] = vals[...]

            break

    S += np.tril(S, -1).T
    return S


def get_MO_coeff(fname, nb):
    """
    Gets the MO coefficients in C[u,i] (u-atomic orbital; i-molecular orbital)
    """

    fin = open(fname)
    check = False
    record = False

    MO = []
    for i in range(nb):
        MO.append([])

    for line in fin:
        if not check:
#            if 'Molecular Orbital Coefficients' in line: # for closed shell hf calculation
           if 'Alpha Molecular' in line:  
#            if 'Beta Molecular' in line: # for tddft calculation
                check = True
                continue
        elif 'Beta Molecular' in line:
#        elif 'Density Matrix:' in line:
            check = False
            break
        elif not record:
            if 'Eigenvalues --' in line:
                record = True
                n_col = len(line.split()[2:])
                continue
        else:
            li = line.split()
            for i in range(-(n_col),0):
                MO[int(li[0])-1].append(eval(li[i]))
            if int(li[0]) == nb:
                record = False
    
    MO = np.matrix(MO)
    return MO
            

def print_error():
    print('Usage: orb_mlk_pop.py <overlap log> <pop analysis log>')
    raise RuntimeError()


def orb_mlk(fn,nm):
    '''
    Orbital based mulliken population analysis
    '''
    nb = get_num_basis(fn)
    S = parse_overlap(fn,nb)
    MO = get_MO_coeff(fn,nb)
    MO_H = MO.H

    mlk = [] #a list of mulliken population for all the molecules
    theta = np.dot(S,MO)
    for i in range(int(nb/nm)):
        mlk.append([])
        for j in range(nb):
            #pop = 0 #mulliken population on each molecule
            pop = np.dot(MO_H[j,i*nm:(i+1)*nm],theta[i*nm:(i+1)*nm,j])
            #for u in range(0,nb):
            #for v in range(i*nm,(i+1)*nm):
                #pop += MO_H[j,v]*S[v,u]*MO[u,j]
                #pop += MO_H[j,v]*theta[v,j]
            mlk[-1].append(pop)
    mlk = np.asarray(mlk)

    #check if each MO sum to one
    fw = open('mlk_alpha'+fn,'w')
    size = mlk.shape
    fw.write(' '*3)
    for j in range(size[0]):
        fw.write('%8d'%(j+1))
    for i in range(size[1]):
        fw.write('\n%3d'%(i+1))
        for j in range(size[0]):
            fw.write('%8.4f'%mlk[j,i])
    fw.close()
    #check if each MO sum to one
    fw1 = open('record.txt','a+')
    for i in range(size[1]):
        add = np.sum(mlk[:,i])
        if abs(add-1) < 0.0005:
            fw1.write('%d\n'%(i+1))
        else:
            fw1.write('error:%8.4f\n'%add)
    fw1.write('---------------------------')
    fw1.close() 


if __name__ == '__main__':

#    import argparse

#    parser = argparse.ArgumentParser(description = 'Input filename')
#    parser.add_argument('-f', type = str, help = 'filename of the input file as a string')
#    args = parser.parse_args()

#    fn = args.f
#    nm = 36 #the number of basis functions within each molecule (H2O) for 6-311g++(d,p)
    nm = 25 #for 6-31G(d,p)
    try:
        for i in [0,14,25,50,70]:
            fn = 't%d.log'%(i)
            orb_mlk(fn,nm)
            print('Job %d Done.'%(i))

    except:
        print_error()

