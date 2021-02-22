#python 3
# For Ehrenfest calculation
# To plot "Energy vs Time"

import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

#########################################################

#           Obtain data from log file                   #

#########################################################
parser = argparse.ArgumentParser(description = 'Input filename')
parser.add_argument('-f', type = str, help = 'filename of the input file as a string')
args = parser.parse_args()

fn = args.f
logf = open(fn, 'r')
logfline = logf.readlines()
logf.close()

time_n = [] # Ehrenfest
Energy = [] # Ehrenfest step
T_rc = False # start trajectory or not
for i in range(len(logfline)):
#    if not T_rc:
#        if 'Start new trajectory calculation' in logfline[i]:
#            T_rc = True
    if 'EKin' in logfline[i] and 'EPot' in logfline[i] and 'ETot' in logfline[i]:
        time_n.append(eval(logfline[i-1].split()[-1]))
        Energy.append(eval(logfline[i].split()[-2]))

#print(len(Energy))
#print(len(time_n))
ferror=open('error.txt','a')
ferror.write('%.6f\n'%(max(Energy)-min(Energy)))
ferror.close()


##############################################################

#        Plot Energy VS Time (electronic step)               #

##############################################################

time_n = time_n[:len(Energy)]
plt.plot(time_n,Energy)
plt.title('Energy_%s VS Time'%fn[16:-4])
plt.xlabel('Time (fs)')
plt.ylabel('Energy (Hartree)')
plt.savefig('Energy_%s.png'%fn[16:-4]) 

#plt.show()
