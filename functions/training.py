import matplotlib

from sklearn.inspection import permutation_importance
from sklearn.utils.fixes import parse_version


def plot_permutation_importance(clf, X, y, ax):
    result = permutation_importance(clf, X, y, n_repeats=10, random_state=42, n_jobs=2)
    perm_sorted_idx = result.importances_mean.argsort()

    # `labels` argument in boxplot is deprecated in matplotlib 3.9 and has been
    # renamed to `tick_labels`. The following code handles this, but as a
    # scikit-learn user you probably can write simpler code by using `labels=...`
    # (matplotlib < 3.9) or `tick_labels=...` (matplotlib >= 3.9).
    tick_labels_parameter_name = (
        "tick_labels"
        if parse_version(matplotlib.__version__) >= parse_version("3.9")
        else "labels"
    )
    tick_labels_dict = {tick_labels_parameter_name: X.columns[perm_sorted_idx]}
    # `vert` was deprecated in matplotlib 3.11 and is replaced by `orientation`,
    # which is available since matplotlib 3.10. The following code handles this,
    # but as a scikit-learn user you probably can write simpler code by using
    # `vert=False` (matplotlib < 3.11) or `orientation="horizontal"`
    # (matplotlib >= 3.10).
    orientation_dict = (
        {"orientation": "horizontal"}
        if parse_version(matplotlib.__version__) >= parse_version("3.10")
        else {"vert": False}
    )
    ax.boxplot(
        result.importances[perm_sorted_idx].T, **orientation_dict, **tick_labels_dict
    )
    ax.axvline(x=0, color="k", linestyle="--")
    return ax