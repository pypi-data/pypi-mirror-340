# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
The sparse threshold strategy allows hold the logic on how ArrayLike should be change based on a density threshold.
"""
from titanq._model.array.arraybuilder import ArrayBuilder
from titanq._model.array.arraylike import ArrayLike
from titanq._model.array.arraylike.numpy_array import NumpyArray
from titanq._model.array.arraylike.scipy_coo_array import ScipyCooArray
from titanq._model.array.transform import ArrayTransformStrategy


class SparseThresholdStrategy(ArrayTransformStrategy):
    """
    This strategy bases on the sparse threshold, meaning depending on the calculated density
    it will return an ArrayLikeConvertOptions.
    """
    def __init__(self, threshold: float):
        self._threshold = threshold

    def check(self, array: ArrayBuilder) -> ArrayLike:
        if array.density() > self._threshold:
            return NumpyArray
        else:
            return ScipyCooArray