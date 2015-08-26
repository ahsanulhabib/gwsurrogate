""" Surrogate download tool """

from __future__ import division

__copyright__ = "Copyright (C) 2014 Scott Field and Chad Galley"
__email__     = "sfield@astro.cornell.edu, crgalley@tapir.caltech.edu"
__status__    = "testing"
__author__    = "Scott Field, Chad Galley"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
from collections import namedtuple

### Naming convention: dictionary KEY should match file name KEY.tar.gz ###
surrogate_info = namedtuple('surrogate_info', ['url', 'desc'])

### dictionary of all known surrogates ###
_surrogate_world = {}

_surrogate_world['EOBNRv2'] = \
  surrogate_info('https://www.dropbox.com/s/uyliuy37uczu3ug/EOBNRv2.tar.gz',\
                 '''(WARNING: older surrogate may not evaluate with 
most recent version of gwsurrogate) Collection of single mode surrogates 
from mass ratios 1 to 10, as long as 190000M and modes (2,1), (2,2), (3,3), 
(4,4), (5,5). This is not a true multi-mode surrogate, and relative time/phase
information between the modes have not been preseved. For more information see 
http://journals.aps.org/prx/abstract/10.1103/PhysRevX.4.031006''')

_surrogate_world['SpEC_q1_10_NoSpin'] = \
  surrogate_info('https://www.black-holes.org/surrogates/data/SpEC_q1_10_NoSpin_nu5thDegPoly_exclude_2_0.h5',\
                 '''A multimode surrogate model built from numerical relativity
simulations performed with SpEC. The surrogate covers mass ratios from 1 to 10,
durations corresponding to about 15 orbits before merger, and many harmonic
modes. For more information see https://www.black-holes.org/surrogates/ or
http://arxiv.org/abs/1502.07758''')

def download_path():
  '''return the default path for downloaded surrogates'''

  import gwsurrogate
  import os
  gws_path = os.path.dirname(gwsurrogate.__file__)
  return gws_path+'/../surrogate_downloads/'

def list():
  '''show all known surrogates available for download'''

  for surr_key in _surrogate_world.keys():
    print surr_key+'...'
    print '  url: '+_surrogate_world[surr_key].url
    print "  Description: "+_surrogate_world[surr_key].desc+'\n\n'

def _unzip(surr_name,sdir=download_path()):
  '''unzip a tar.gz surrogate and remove the tar.gz file'''

  os.chdir(sdir)
  os.system('tar -xvzf '+surr_name)
  os.remove(surr_name)

  return sdir+surr_name.split('.')[0]

def get(surr_name,sdir=download_path()):
  '''pass a valid surr_name from the repo list and download location sdir. 
     The default path is used if no location supplied. tar.gz surrogates
     are automatically unziped. The new surrogate path is returned.'''

  if _surrogate_world.has_key(surr_name):
    surr_url = _surrogate_world[surr_name].url
    os.system('wget --directory-prefix='+sdir+' '+surr_url)
  else:
    raise ValueError("No surrogate package exits")

  # deduce the surrogte file name and extension type
  # one can directly load a surrogate frmo surr_path
  file_name = surr_url.split('/')[-1]
  if file_name.split('.')[1] == 'tar': # assumed to be *.h5 or *.tar.gz
    surr_path = _unzip(file_name,sdir)
  else:
    surr_path = sdir+file_name

  return surr_path

