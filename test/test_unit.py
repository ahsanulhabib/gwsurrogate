""" tests all relevant data generated by tutorial notebooks and stored
    in npz files."""

from __future__ import division
import nose
import numpy as np
import gwsurrogate as gws
import os

# try importing data. If it doesn't exist, download it
try:
  reg_data = np.load('test/data_notebook_basics_lesson1.npz')
except:
  print "Downloading regression data..."
  os.system('wget --directory-prefix=test https://www.dropbox.com/s/07t84cpmmqjya69/gws_regression_data.tar.gz')
  os.system('tar -xf test/gws_regression_data.tar.gz -C test/')

path_to_surrogate = \
'tutorial/TutorialSurrogate/EOB_q1_2_NoSpin_Mode22/l2_m2_len12239M_SurID19poly/'
EOBNRv2_sur = gws.EvaluateSingleModeSurrogate(path_to_surrogate)


def test_notebook_basics_lesson1():
  """ regression test data from notebook example.
      data created on 5/30/2015 with
np.savez('data_notebook_basics_lesson1.npz',t=t,hp=hp,hc=hc,
          amp=amp,phase=phase,phi_m=phi_m,h_adj=h_adj)"""

  t, hp, hc  = EOBNRv2_sur(q=1.7, M=80.0, dist=1.0, phi_ref = 0.0, f_low = 10.0)
  amp, phase = EOBNRv2_sur.amp_phase(hp + 1j*hc)

  phi_m = EOBNRv2_sur.phi_merger(hp + 1j*hc)
  h_adj = EOBNRv2_sur.adjust_merger_phase(hp + 1j*hc,2.0)

  # load regression data
  reg_data = np.load('test/data_notebook_basics_lesson1.npz')

  np.testing.assert_array_almost_equal_nulp(t,reg_data['t'])
  np.testing.assert_array_almost_equal_nulp(hp,reg_data['hp'])
  np.testing.assert_array_almost_equal_nulp(hc,reg_data['hc'])
  np.testing.assert_array_almost_equal_nulp(amp,reg_data['amp'])
  np.testing.assert_array_almost_equal_nulp(phase,reg_data['phase'])
  np.testing.assert_array_almost_equal_nulp(phi_m,reg_data['phi_m'])
  np.testing.assert_array_almost_equal_nulp(h_adj,reg_data['h_adj'])


def test_notebook_basics_lesson2():
  """ regression test data from notebook example.
      data created on 5/30/2015 with
np.savez('data_notebook_basics_lesson2.npz',t_resamp=t_resamp,
          hp_resamp=hp_resamp,hc_resamp=hc_resamp)"""

  #t, hp, hc = EOBNRv2_sur(q=1.2)
  t_resamp, hp_resamp, hc_resamp = \
    EOBNRv2_sur(1.2,samples=np.linspace(EOBNRv2_sur.tmin-1000,EOBNRv2_sur.tmax+1000,num=3000))

  # load regression data
  reg_data = np.load('test/data_notebook_basics_lesson2.npz')

  np.testing.assert_array_almost_equal_nulp(t_resamp,reg_data['t_resamp'])
  np.testing.assert_array_almost_equal_nulp(hp_resamp,reg_data['hp_resamp'])
  np.testing.assert_array_almost_equal_nulp(hc_resamp,reg_data['hc_resamp'])


def test_notebook_basics_lesson3():
  """ regression test data from notebook example.
      data created on 5/30/2015 with
np.savez('data_notebook_basics_lesson3.npz',eim_pts=eim_pts, T_eim=T_eim,
          greedy_pts=greedy_pts,tmin=EOBNRv2_sur.tmin,tmax=EOBNRv2_sur.tmax,
          dt=EOBNRv2_sur.dt,tunits=EOBNRv2_sur.t_units)"""

  t, hp, hc = EOBNRv2_sur(1.7,80.0,1.0)
  eim_pts    = EOBNRv2_sur.eim_indices
  T_eim      = t[eim_pts]
  greedy_pts = EOBNRv2_sur.greedy_points

  tunits = EOBNRv2_sur.t_units
  dt = EOBNRv2_sur.dt
  tmax = EOBNRv2_sur.tmax
  tmin = EOBNRv2_sur.tmin

  # load regression data
  reg_data = np.load('test/data_notebook_basics_lesson3.npz')

  np.testing.assert_array_almost_equal_nulp(eim_pts,reg_data['eim_pts'])
  np.testing.assert_array_almost_equal_nulp(T_eim,reg_data['T_eim'])
  np.testing.assert_array_almost_equal_nulp(greedy_pts,reg_data['greedy_pts'])
  np.testing.assert_array_almost_equal_nulp(dt,reg_data['dt'])
  np.testing.assert_array_almost_equal_nulp(tmax,reg_data['tmax'])
  np.testing.assert_array_almost_equal_nulp(tmin,reg_data['tmin'])

  assert(tunits == str(reg_data['tunits']))


def test_notebook_basics_lesson4():
  """ regression test data from notebook example.
      data created on 5/30/2015 with
np.savez('data_notebook_basics_lesson4.npz',times=times,b_5=b_5,
          e_5=e_5,h_5=h_5,h_5_surr=h_5_surr)"""


  b_5   = EOBNRv2_sur.basis(4,'cardinal')
  e_5   = EOBNRv2_sur.basis(4,'orthogonal')
  h_5   = EOBNRv2_sur.basis(4,'waveform')
  junk, hp_5_surr, hc_5_surr = EOBNRv2_sur(EOBNRv2_sur.greedy_points[4])
  nrm_5 = EOBNRv2_sur.norm_eval(EOBNRv2_sur.greedy_points[4])
  hp_5_surr = hp_5_surr / nrm_5 
  hc_5_surr = hc_5_surr / nrm_5
  h_5_surr = hp_5_surr + 1j*hc_5_surr

  # load regression data
  reg_data = np.load('test/data_notebook_basics_lesson4.npz')

  np.testing.assert_array_almost_equal_nulp(b_5,reg_data['b_5'])
  np.testing.assert_array_almost_equal_nulp(e_5,reg_data['e_5'])
  np.testing.assert_array_almost_equal_nulp(h_5,reg_data['h_5'])
  np.testing.assert_array_almost_equal_nulp(h_5_surr,reg_data['h_5_surr'])

  # basis orthogonality
  dt  = 1.0/2048.0 # found from surrogate *.dat file
  e_6 = EOBNRv2_sur.basis(5,'orthogonal')
  nose.tools.assert_almost_equal(np.sum(e_5*np.conj(e_6)) * dt,0.0,places=14)
  nose.tools.assert_almost_equal(np.sum(e_5*np.conj(e_5)) * dt,1.0,places=14)

def test_notebook_basics_lesson5():

  assert(False) #TODO: code me (download surrogates need to be rebuilt)
 
