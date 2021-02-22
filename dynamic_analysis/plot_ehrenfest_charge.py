#python 3
# For Ehrenfest calculation
# To plot "mulliken charges (hydrogens summed into heavy atoms) vs Time"

import argparse
import numpy as np
import matplotlib.pyplot as plt

def ehrenfest_spin(fn,restart=False):
    '''
    Obtain data from log file                  
    '''

    logf = open(fn)

    time_n = [] # Ehrenfest
    Charge = [] # Ehrenfest Step
    T_rc = restart # start trajectory or not
    N_rc = False # record each Ehrenfest calculation
    C_rc = False # record charge density or not
    for i in logf:
        if not T_rc:
            if 'Start new trajectory calculation' in i:
                T_rc = True
        elif 'Electronic Dynamics for Ehrenfest Step' in i:
            time_n.append(eval(i.split()[-2]))
        if not C_rc:
            if 'Mulliken charges and spin densities with hydrogens summed into heavy atoms:' in i:
                C_rc = True
                Charge.append([])
        elif len(i.split()) == 4:
            Charge[-1].append(eval(i.split()[-2]))
        elif len(i.split()) > 4:
            C_rc = False
    return (time_n, Charge)

def plot_all(time_n, Charge,fn):
    '''
    Plot Charge VS Time (Ehrenfest step)
    '''

    plt.figure()
    time_n = time_n[:len(Charge)]
    Charge = np.asarray(Charge).T
#    if n_mo:
#        mo_list = []
#        for item in n_mo:
#            if item not in mo_list:
#                mo_list.append(item)
#    else:
#        mo_list = range(1,len(Charge)+1)
#    for i in mo_list:
#        plt.plot(time_n, Charge[i-1],label='%d'%(i))
    for i in range(1,len(Charge)+1):
        if max(Charge[i-1])>0.2 or min(Charge[i-1])<(-0.3):
            plt.plot(time_n, Charge[i-1],label='%d'%(i))
    plt.legend(loc='lower left',prop={'size': 10})
    plt.title('Mulliken charges_%s VS Time'%fn[16:-4])
    plt.xlabel('Time(fs)')
    plt.ylabel('Mulliken charges')
    plt.ylim((-1,1))
    plt.savefig('Charge_%s.png'%fn[16:-4])
#    plt.show()


#main():
parser = argparse.ArgumentParser(description = 'Input filename')
parser.add_argument('-f', type = str, nargs='+', help = 'filename of the input file as a string')
args = parser.parse_args()
fn = args.f

total_time, total_spin = ehrenfest_spin(fn[0])
if len(fn) > 1:
    for i in range(1,len(fn)):
        re_time, re_spin = ehrenfest_spin(fn[i], True)
        total_time = total_time+re_time
        total_spin = total_spin+re_spin
total_spin=total_spin[:len(total_time)]
plot_all(total_time, total_spin, fn[0])

####### to find out the localization of the charge
charge=total_spin
maxmo=[]
for i in range(len(charge)):
    temp=np.argmax(charge[i])
    if not maxmo:
        maxmo.append(temp+1)
    elif temp+1==maxmo[-1]:
        continue
    else:
        maxmo.append(temp+1)
#print(maxmo)
#plot_all(total_time, total_spin, maxmo, fn[0])

