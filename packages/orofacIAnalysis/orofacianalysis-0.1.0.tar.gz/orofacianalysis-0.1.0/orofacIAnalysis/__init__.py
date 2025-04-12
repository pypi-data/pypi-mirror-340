"""orofacIAnalysis - A library for analyzing chewing patterns using computer vision."""

__version__ = "0.1.0"

# Import main classes and functions to expose at the package level
from orofacIAnalysis.cycle import Cycle
from orofacIAnalysis.chew_annotator import ChewAnnotator
from orofacIAnalysis.landmarks import Landmarks
from orofacIAnalysis.smoothing import (
    SmoothingMethods,
    SmoothingMethodsList,
    apply_smoothing
)
from orofacIAnalysis.utils import (
    euclidian_distance,
    axis_translation,
    pandas_entropy,
    butterworth_filter,
    moving_average,
    exponential_smoothing,
    spline_smoothing
)