"""
Usage: soparse.py <overlap log> <pop analysis log>
"""

import numpy as np


def g2f(gfloat):
    return float(gfloat.replace('D','E'))


def parse_overlap(fname):
    """
    Parses a file for the overlap matrix.
    Assumes overlap is printed as a triangular matrix
    """

    S = None
    fin = open(fname)
    nb = 0

    for line in fin:
        if 'basis functions' in line and 'primitive gaussians' in line:
            nb = int(line.split()[0])
            S = np.zeros((nb,nb))
        if '*** Overlap ***' in line:

            while True:

                line = next(fin)

                if '*** Kinetic Energy ***' in line:
                    break

                if 'D' not in line:
                    cols = [int(c) - 1 for c in line.split()]
                    continue

                lsp = line.split()
                row = int(lsp[0]) - 1
                vals = np.array([g2f(v) for v in lsp[1:]])

                S[row, cols[0]:(min(row, cols[-1])+1)] = vals[...]

            break

    S += np.tril(S, -1).T
    return S


def get_LUMO_c(fname, nb):
    """
    Gets the C vector for the LUMO and the atomic breakpoints
    """

    fin = open(fname)
    checks = [False, False]

    cvec = []
    breaks = []

    for line in fin:

        # Select the LUMO
        if 'Beta Molecular' in line:
            checks[0] = True
        if checks[0] and 'O         V' in line:
            checks[1] = True
            line = next(fin)

        # If lumo, do mulliken analysis
        if all(checks):
            for iDummy in range(nb):
                line = next(fin)
                lsp = line.split()
                if len(lsp) == 9:
                    breaks.append((iDummy, lsp[2] == 'H'))
                cvec.append(float(lsp[-1]))
            return np.array(cvec), breaks


def parse_LUMO(fname, overlap, incH=True):
    """
    Parses a file for the MO coefficents of the LUMO, returning the mulliken
    atomic contributions.

    Parameters
    ----------
    fname : str
      Filename
    overlap : numpy.array<float>
      AO overlap matrix
    incH : bool
      Whether to sum hydrogens into heavy elements. Default true

    Returns
    -------
    numpy.array<float>
      Array of atomic contributions
    """

    c, breaks = get_LUMO_c(fname, overlap.shape[0])
    gop = overlap.dot(c)

    acont = []

    for i,atom in enumerate(breaks):
        if atom == breaks[-1]:
            break
        localcont = c[atom[0]:breaks[i+1][0]].dot(gop[atom[0]:breaks[i+1][0]])
        if incH and atom[1]:
            acont[-1] += localcont
        else:
            acont.append(localcont)

    return np.array(acont)


def print_error():
    print('Usage: soparse.py <overlap log> <pop analysis log>')
    raise RuntimeError()


# Script functionality
if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print_error()
    
    try:

        ovp = parse_overlap(sys.argv[1])
        cont = parse_LUMO(sys.argv[2], ovp)
        if np.argmax(cont) == 0:
            print('T')
        else:
            print('F')

    except:
        print_error()
