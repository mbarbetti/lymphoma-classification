import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from sklearn.metrics import precision_recall_curve

RESOLUTION = 300


def custom_predictions ( y_true   : np.ndarray ,
                         y_scores : np.ndarray ,
                         recall_score    : float = None ,
                         precision_score : float = None ,
                         show_curves : bool = False ,
                         save_figure : bool = False ,
                         fig_name : str = None ) -> tuple:
  if len(y_scores.shape) == 2:
    y_scores = y_scores[:,1]

  precision, recall, threshold = precision_recall_curve (y_true, y_scores)

  if show_curves:
    ## figure setup
    fig, ax = plt.subplots (figsize = (8,5), dpi = RESOLUTION)
    ax.set_xlabel ("Threshold", fontsize = 12)

    ax.plot (threshold, precision[:-1], color = "coral", linestyle = "--", label = "Precision")
    ax.plot (threshold, recall[:-1], color = "dodgerblue", linestyle = "-", label = "Recall")

    ax.legend (loc = "lower left", fontsize = 12)

    ## figure name default
    if fig_name is None:
      timestamp = str (datetime.now()) . split (".") [0]
      timestamp = timestamp . replace (" ","_")
      fig_name = "custom_predictions_"
      for time, unit in zip ( timestamp.split(":"), ["h","m","s"] ):
        fig_name += time + unit   # YYYY-MM-DD_HHhMMmSSs
    filename = f"docs/img/{fig_name}.png"

    plt.tight_layout()
    if save_figure: plt.savefig ( filename, format = "png", dpi = RESOLUTION )

    plt.show()
    plt.close()

  ## compute custom threshold for RECALL
  if (recall is not None ) and (precision_score is None):
    if (recall_score < 0) or (recall_score > 1):
      raise ValueError ("The recall score should be less than 1.")
    custom_threshold = threshold [np.argmin (recall >= recall_score) - 1]
    return (y_scores >= custom_threshold), custom_threshold

  ## compute custom threshold for PRECISION
  elif (precision is not None) and (recall_score is None):
    if (precision_score < 0) or (precision_score > 1):
      raise ValueError ("The precision score should be less than 1.")
    custom_threshold = threshold [np.argmax (precision >= precision_score)]
    return (y_scores >= custom_threshold), custom_threshold

  ## compute custom threshold for RECALL > PRECISION
  elif (precision_score is None) and (recall_score is None):
    custom_threshold = threshold [np.argmin (recall > precision)]
    return (y_scores >= custom_threshold), custom_threshold

  else:
    raise ValueError ("Only one target score should be passed: recall or precision.")
