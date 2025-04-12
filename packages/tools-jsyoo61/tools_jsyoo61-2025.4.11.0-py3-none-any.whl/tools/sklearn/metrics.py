import numpy as np
from sklearn.metrics import r2_score as r2_score_sklearn

def squared_error(y_true, y_pred):
    return (y_true-y_pred)**2

def absolute_error(y_true, y_pred):
    '''MAE without mean'''
    return np.abs(y_true-y_pred)

def r2_score(y_true, y_pred, axis=None, multioutput='raw_values'):
    """
    R^2 score for multidimensional predictions.
    collapses all axes except the specified axis.

    Parameters
    ----------
    y_true : np.ndarray
    y_pred : np.ndarray
    axis: int, default=None
        Axis to collapse.
        It must be specified if y_true and y_pred dimensions are > 2
    multioutput : Reference to `sklearn.metrics.r2_score`
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
    
    Returns
    -------
    z : np.ndarray
        if axis is specified, returns an array of shape (y_true.shape[axis],)
    """
    if axis is not None:
        y_true = np.moveaxis(y_true, axis, -1).reshape(-1, y_true.shape[axis]) # Move axis to the end, and flatten the rest
        y_pred = np.moveaxis(y_pred, axis, -1).reshape(-1, y_pred.shape[axis])
    else:
        assert (y_true.ndim <= 2) and (y_pred.ndim <= 2), "If axis is None, y_true and y_pred must be smaller than 2D"
    
    return r2_score_sklearn(y_true, y_pred, multioutput=multioutput)