# -*- coding: utf-8 -*-

from __future__ import print_function

import tempfile
import numpy as np
import mdtraj
import pkg_resources


def get_top():
    return pkg_resources.resource_filename(__name__, 'data/test.pdb')


def create_traj(top=None, format='.xtc', dir=None, length=1000, start=0):
    trajfile = tempfile.mktemp(suffix=format, dir=dir)
    xyz = np.arange(start * 3 * 3, (start + length) * 3 * 3)
    xyz = xyz.reshape((-1, 3, 3))
    if top is None:
        top = get_top()

    t = mdtraj.load(top)
    t.xyz = xyz
    t.unitcell_vectors = np.array(length * [[0, 0, 1], [0, 1, 0], [1, 0, 0]]).reshape(length, 3, 3)
    t.time = np.arange(length)
    t.save(trajfile)

    return trajfile, xyz, length


def create_trajectory_csv(dirname, data):
    fname = tempfile.mktemp(suffix='.csv.dat', dir=dirname)
    np.savetxt(fname, data)
    return fname


def create_trajectory_numpy(dirname, data):
    fname = tempfile.mktemp(suffix='.npy', dir=dirname)
    np.save(fname, data)
    return fname


def create_dummy_pdb(dirname, dims):
    dummy_pdb = tempfile.mktemp('.pdb', dir=dirname)
    with open(dummy_pdb, 'w') as f:
        for i in range(dims):
            print('ATOM  %5d C    ACE A   1      28.490  31.600  33.379  0.00  1.00' % i, file=f)
    return dummy_pdb


def create_trajectory_xtc(dims, dirname, data):
    from mdtraj.core.trajectory import XTCTrajectoryFile
    fname = tempfile.mktemp(suffix='.xtc', dir=dirname)

    shaped = data.reshape(-1, dims, 3)
    with XTCTrajectoryFile(fname, 'w') as f:
        f.write(shaped)

    return fname
