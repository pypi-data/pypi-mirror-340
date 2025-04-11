import importlib
from . import pomp_class
importlib.reload(pomp_class)
from .pomp_class import Pomp
from .internal_functions import _pfilter_internal


def pfilter(pomp_object=None, J=50, rinit=None, rprocess=None, dmeasure=None, theta=None, 
            ys=None, covars=None, thresh=100, key=None):
    """
    An outside function for particle filtering algorithm. It receives two kinds of input - pomp
    class object or required arguments of 'pfilter_internal' function, and executes on the 
    object or calls 'pfilter_internal' directly.

    Args:
        pomp_object (Pomp, optional): An instance of the POMP class. If provided, the function 
                                      will execute on this object to conduct the particle 
                                      filtering algorithm. Defaults to None.
        J (int, optional): The number of particles. Defaults to 50.
        rinit (function, optional): Simulator for the initial-state distribution. 
                                    Defaults to None.
        rprocess (function, optional): Simulator for the process model. Defaults to None.
        dmeasure (function, optional): Density evaluation for the measurement model. 
                                       Defaults to None.
        theta (array-like, optional): Parameters involved in the POMP model. Defaults to None.
        ys (array-like, optional): The measurement array. Defaults to None.
        covars (array-like, optional): Covariates or None if not applicable. Defaults to None.
        thresh (float, optional):Threshold value to determine whether to resample particles. 
                                 Defaults to 100.
        key (jax.random.PRNGKey, optional): The random key. Defaults to None.

    Raises:
        ValueError: Missing the pomp class object and required arguments for calling 
        'pfilter_internal' directly

    Returns:
        float: Negative log-likelihood value
    """
    if pomp_object is not None:
        return pomp_object.pfilter(J, thresh, key)
    elif rinit is not None and rprocess is not None and dmeasure is not None and theta \
        is not None and ys is not None:
        return _pfilter_internal(theta, ys, J, rinit, rprocess, dmeasure, covars, thresh, key)
    else:
        raise ValueError("Invalid Arguments Input")
