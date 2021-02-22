#python 3
# For Ehrenfest calculation
# To calculate the distance ratio for a O-H-O in the system

import argparse
import numpy as np
import matplotlib.pyplot as plt

def g2f(gfloat):
    '''
    Change the number into scientific notation
    '''
    return float(gfloat.replace('D','E'))

def dist(pos1, pos2):
    '''
    Calculate the distance between 2 positions
    '''
    dist = np.linalg.norm(pos1-pos2)
    return dist

def projection(p1, p2, p3):
    '''
    Calculate the ratio of O-H projection on O-O
    '''
    proj = np.dot(p2-p1,p3-p1)/np.square(np.linalg.norm(p3-p1))
    return proj

def ehrenfest_geo(fn, restart, a):
    '''
    Obtain geometry data from log file                  
    '''

    logf = open(fn)
 
    time_n = [] # Ehrenfest
    Geo = []
    T_rc = restart # start trajectory or not
    N_rc = False # record each Ehrenfest calculation
    C_rc = False # record geometry or not
    for i in logf:
        if not T_rc:
            if 'Start new trajectory calculation' in i:
                T_rc = True
        elif not N_rc:
            if 'Trajectory Number     1    Step Number' in i and i.split()[-1]=='0':
                N_rc = True
        elif 'Time (fs)' in i:
            if eval(i.split()[-1]) not in time_n:
                time_n.append(eval(i.split()[-1]))
        elif not C_rc:
            if 'Cartesian coordinates: (bohr)' in i:
                C_rc = True
        elif 'X' in i and 'Y' in i and 'Z' in i:
            if i.split()[1]==str(a[0]):
                pos1 = []
                for k in [3,5,7]:
                    pos1.append(g2f(i.split()[k]))
            if i.split()[1]==str(a[1]):
                pos2 = []
                for k in [3,5,7]:
                    pos2.append(g2f(i.split()[k]))    
            if i.split()[1]==str(a[2]):
                pos3 = []
                for k in [3,5,7]:
                    pos3.append(g2f(i.split()[k]))
        elif 'MW cartesian velocity' in i:
            C_rc = False
#            Geo.append(dist(np.array(pos1),np.array(pos2))/dist(np.array(pos2),np.array(pos3)))
            Geo.append(projection(np.array(pos1),np.array(pos2),np.array(pos3)))
            N_rc = False

    return (time_n, Geo)

def plot_dist(time_n, Geo, fn, a):
    '''
    Plot distance VS Time (Ehrenfest step)
    '''

    plt.figure()
    time_n = time_n[:len(Geo)]
    plt.plot(time_n, Geo)#,label='%d'%(i))
#    plt.legend(loc='lower left',prop={'size': 10})
    plt.title('Dist VS Time')
    plt.xlabel('Time(fs)')
    plt.ylabel('Distance(bohr)')
#    plt.ylim((-1,1))
    plt.savefig('Dist_%s_%d_%d.png'%(fn[16:-4],a[0][0], a[0][1]))
    plt.show()

def plot_all(total_time, total_dist, fn, a):
    '''
    Plot dist VS Time and ratio VS Time (Ehrenfest step)
    '''

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for i in range(len(a)):
#        ax1.plot(total_time[0], total_dist[i], label='O[D%d] - H - O[A%d]'%((i+1),(i+1)))
        ax1.plot(total_time[0], total_dist[i], label='%d'%(i+1))
    plt.axhline(y=0.5, color='k', linestyle='dotted')
#    plt.legend(loc='upper center',prop={'size': 7})
    plt.xlabel('Time (fs)',fontsize=11)
    plt.ylabel('ratio',fontsize=11)
    plt.xlim((0,70))
#    ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
#    ax2.plot(total_time[-1], total_dist[-1], color='r', label='%d-%d/%d-%d'%(a[0][0], a[0][1], a[0][1], a[1][1]))
#    ax2.yaxis.tick_right()
#    ax2.yaxis.set_label_position("right")
#    plt.ylabel('ratio')
    plt.legend(loc='lower right',prop={'size': 7})
    plt.savefig('ratio_%s.png'%fn[16:-4])
#    plt.show()


#main():
plt.style.use(['science','no-latex','ieee','high-vis'])
parser = argparse.ArgumentParser(description = 'Input filename')
parser.add_argument('-f', type = str, nargs='+', help = 'filename of the input file as a string')
parser.add_argument('-d', type = int, nargs='+', help = 'the number of the 2 atoms')
args = parser.parse_args()
fn = args.f
a = []
for i in range(len(args.d)//3):
    a.append(args.d[i*3:i*3+3])

total_time = []
total_dist = []
for alist in a:    
    time, distance = ehrenfest_geo(fn[0], False, alist)
    if len(fn) > 1:
        for i in range(1, len(fn)):
            re_time, re_dist = ehrenfest_geo(fn[i], True, alist)
            time = time+re_time
            distance = distance+re_dist
    total_time.append(time)
    total_dist.append(distance)
plot_all(total_time, total_dist, fn[0], a)


