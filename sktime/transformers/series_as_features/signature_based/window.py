"""
window.py
======================================
Introduces the Window module that is used when splitting the path over:
    - Global
    - Sliding
    - Expanding
    - Dyadic
window types.

Code based on window code written by Patrick Kidger.
"""
import collections as co


_Pair = co.namedtuple('Pair', ('start', 'end'))


def window_getter(string, **kwargs):
    """Gets the window method correspondent to the given string and initialises with specified parameters.

    Parameters
    ----------
    string : str
             String from ['global', 'sliding', 'expanding', 'dyadic'] used to access the window method.
    kwargs : dict
             Dictionary of key-word arguments to be passed to the window method.

    Returns
    -------
    list:
        A list of lists where the inner lists are lists of tuples that denote the start and end indexes of each window.
    """
    # Setup all available windows here
    window_dict = {
        'global': Global,
        'sliding': Sliding,
        'expanding': Expanding,
        'dyadic': Dyadic,
    }

    assert string in window_dict.keys(), "Window name must be one of: {}. Got: {}.".format(window_dict.keys(), string)

    return window_dict[string](**kwargs)


class Window:
    """Abstract base class for windows.

    Each subclass must implement a __call__ method that returns a list of lists of 2-tuples. Each 2-tuple specifies the
    start and end of each window. These windows are grouped into a list that will (usually) cover the full time series.
    These lists are grouped into another list for situations where we consider windows of multiple scales.
    """
    def num_windows(self, length):
        """Method that returns the total number of windows in the set.

        Parameters
        ----------
        length : int
                 The length of the input path.

        Returns
        -------
        int:
            The number of windows.
        """
        return sum([len(w) for w in self(length)])


class Global(Window):
    """ A single window over the full data. """
    def __call__(self, length=None):
        return [[_Pair(None, None)]]


class _ExpandingSliding(Window):
    def __init__(self, initial_length, start_step, end_step):
        """
        Parameters
        ----------
        initial_length : int
                         Initial length of the input window.
        start_step : int
                     Initial step size.
        end_step : int
                   Final step size.
        """
        super(_ExpandingSliding, self).__init__()
        self.initial_length = initial_length
        self.start_step = start_step
        self.end_step = end_step

    def __call__(self, length):
        def _call():
            start = 0
            end = self.initial_length
            while end <= length:
                yield _Pair(start, end)
                start += self.start_step
                end += self.end_step
        return [list(_call())]


class Sliding(_ExpandingSliding):
    """ A window starting at zero and going to some point that increases between windows. """
    def __init__(self, length, step):
        """
        Parameters
        ----------
        length : int
                 The length of the window.
        step : int
               The sliding step size.
        """
        super(Sliding, self).__init__(initial_length=length, start_step=step, end_step=step)


class Expanding(_ExpandingSliding):
    """ A window of fixed length, slid along the dataset. """
    def __init__(self, length, step):
        """
        Parameters
        ----------
        length : int
            The length of each window.
        step : int
            The step size.
        """
        super(Expanding, self).__init__(initial_length=length, start_step=0, end_step=step)


class Dyadic(Window):
    """Windows generated 'dyadically'.

    These are successive windows of increasing fineness. The windows are as follows:
        Depth 1: The global window over the full data.
        Depth 2: The windows of the first and second halves of the dataset.
        Depth 3: The dataset is split into quarters, and we take the windows of each quater.
        ...
        Depth n: For a dataset of length L, we generate windows [0:L/(2^n), L/(2^n):(2L)/(2^n), ..., (2^(n-1))L/2^n:L].
    Each depth also contains all previous depths.

    Note: Ensure the depth, n, is chosen such that L/(2^n) >= 1, else it will be too high for the dataset.
    """
    def __init__(self, depth):
        """
        Parameters
        ----------
        depth : int
            The depth of the dyadic window, noted in the class description.
        """
        super(Dyadic, self).__init__()
        self.depth = depth

    def __call__(self, length):
        return self.call(float(length))

    def call(self, length, _offset=0.0, _depth=0, _out=None):
        if _out is None:
            _out = [[] for _ in range(self.depth + 1)]
        _out[_depth].append(_Pair(int(_offset), int(_offset + length)))

        if _depth < self.depth:
            left = Dyadic(self.depth)
            right = Dyadic(self.depth)
            half_length = length / 2
            # The order of left then right is important, so that they add their entries to _out in the correct order.
            left.call(half_length, _offset, _depth + 1, _out)
            right.call(half_length, _offset + half_length, _depth + 1, _out)

        return _out

