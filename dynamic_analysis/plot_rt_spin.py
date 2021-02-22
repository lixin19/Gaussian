#python 3
# For realtime calculation
# To plot "Spin densities vs Time"

import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

def realtime_spin(fn,restart=False):
    '''
    Obtain data from log file
    '''

    logf = open(fn)

    time = [] # real time
    record_c = False
    Charge = [] # at each step
    for line in logf:
        if 'Step:' in line and int(line.split()[-1])%100 == 0:
            time.append(eval(next(logf).split()[-2]))
        elif 'Mulliken charges and spin densities with hydrogens summed into heavy atoms' in line:
            record_c = True
            Charge.append([])
        elif record_c:
            if len(line.split()) == 4:
                Charge[-1].append(eval(line.split()[-1]))
            elif len(line.split()) > 4:
                record_c = False
    return (time, Charge)

def plot_spin(time, Charge, fn):
    '''
    plot spin densities VS time
    '''
    plt.figure()
    time = time[:len(Charge)]
    Charge = np.asarray(Charge).T
#    for i in [2,11,13,23]:
    for i in range(len(Charge)):
#        if Charge[i][0] > 0.05:
        if max(Charge[i]) > 0.05:
            plt.plot(time, Charge[i],label='%d'%(i+1))

#    plt.title('Spin density_%s VS Time'%fn[9:-4])
    plt.legend(loc='upper right',frameon=False,prop={'size': 7})
    plt.xlabel('Time(fs)',fontsize=11)
    plt.ylabel('Hole density',fontsize=11)
#    plt.xlim((0,30))
    plt.ylim((0,1))
    plt.savefig('rt_spin_%s.png'%fn[9:-4])
#    plt.show()
    

#main()
plt.style.use(['science','no-latex','ieee','high-vis'])
parser = argparse.ArgumentParser(description = 'Input filename')
parser.add_argument('-f', type = str, nargs='+', help = 'filename of the input file as a string')
args = parser.parse_args()
fn = args.f

total_time, total_spin = realtime_spin(fn[0])
if len(fn) > 1:
    for i in range(1,len(fn)):
        re_time, re_spin = realtime_spin(fn[i], True)
        total_time = total_time+re_time
        total_spin = total_spin+re_spin
total_spin=total_spin[:len(total_time)]
plot_spin(total_time, total_spin,fn[0])





