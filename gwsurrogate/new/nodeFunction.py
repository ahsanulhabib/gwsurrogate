"""Classes for parameter space fits or interpolants"""

from __future__ import division

__copyright__ = "Copyright (C) 2014 Scott Field and Chad Galley"
__email__     = "sfield@astro.cornell.edu, crgalley@tapir.caltech.edu"
__status__    = "testing"
__author__    = "Jonathan Blackman"

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

from saveH5Object import SimpleH5Object

from gwsurrogate import parametric_funcs
import numpy as np
import gwtools

class DummyNodeFunction(SimpleH5Object):
    """Used for testing, returns the input or a constant."""

    def __init__(self, return_value=None):
        super(DummyNodeFunction, self).__init__()
        self.val = return_value

    def __call__(self, x):
        if self.val is None:
            return np.mean(x)
        else:
            return self.val


class Polyfit1D(SimpleH5Object):
    """Wrapper class to make use of the old parametric_funcs module"""

    def __init__(self, function_name=None, coefs=None):
        """
        function_name: A key from parametric_funcs.function_dict
        coefs: The fit coefficients to be used when called
        """
        super(Polyfit1D, self).__init__()
        self.function_name=function_name
        self.coefs = coefs

    def __call__(self, x):
        func = parametric_funcs.function_dict[self.function_name]
        return func(self.coefs, x[0])


class MappedPolyFit1D_q10_q_to_nu(Polyfit1D):
    """
    Transforms the input before evaluating the fit. Used for the SpEC q 1 to 10
    non-spinning surrogate. This could be generalized later.
    """

    def __call__(self, x):
        mapped_x = 4*gwtools.q_to_nu(x)
        return super(MappedPolyFit1D_q10_q_to_nu, self).__call__(mapped_x)


NODE_CLASSES = {
    "Dummy": DummyNodeFunction,
    "Polyfit1D": Polyfit1D,
    "SpEC_q10_non_spinning": MappedPolyFit1D_q10_q_to_nu,
        }


class NodeFunction(SimpleH5Object):
    """
    A holder class for any node function (for example a parametric fit or
    tensor-spline). This is essentially only to let us know what class to
    initialize when loading from an h5 file.
    """

    def __init__(self, name='', node_function=None):
        """
        name: A name for this node
        node_function: An instance of one of the values in NODE_CLASSES
        """
        super(NodeFunction, self).__init__(sub_keys=['node_function'])
        self.name = name
        self.node_function = node_function
        self.node_class = None
        if node_function is not None:
            for k, v in NODE_CLASSES.iteritems():
                if node_function.__class__.__name__ == v.__name__:
                    self.node_class = k
            if self.node_class is None:
                raise Exception("node_function must be in NODE_CLASSES!")

    def __call__(self, x):
        return self.node_function(x)

    def h5_prepare_subs(self):
        self.node_function = NODE_CLASSES[self.node_class]()