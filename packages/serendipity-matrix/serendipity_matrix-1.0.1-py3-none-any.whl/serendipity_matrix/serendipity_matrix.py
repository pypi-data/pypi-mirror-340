import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def class_indep_matrix(y_true, y_score, abs_tolerance=1e-8):
    """
    Calculate the serendipity matrix.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,). 
        Ground truth (correct) labels.

    y_score : array-like of shape (n_samples, n_classes).
        Probabilities of predicted labels, as returned by a classifier. The sum of 
        these probabilities must sum up to 1.0 over classes.

        The order of the class scores must correspond to the numerical or
        lexicographical order of the labels in y_true.

    abs_tolerance : absolute tolerance threshold for checking whether probabilities
        sum up to 1.0. Default = 1e-8.

    Returns
    ----------
    serendipityM : pandas DataFrame.
        Returns the values of the serendipity matrix.
    """
    if y_true.shape[0] != y_score.shape[0]:
        raise ValueError("'y_true' and 'y_score' have different number of samples.")
    
    if len(np.unique(y_true)) != y_score.shape[1]:
        raise ValueError("'y_true' and 'y_score' have different number of classes.")
    
    if not np.allclose(1, y_score.sum(axis=1), rtol=0, atol=abs_tolerance):
        raise ValueError(
            "Target scores need to be probabilities and they should sum up to 1.0 over classes."
        )
    
    certTypes = ["Reliability","Overconfidence","Underconfidence","Serendipity"]

    # Checks y_true data type
    if not isinstance(y_true, np.ndarray):
        y_true = y_true.to_numpy()

    # Classes and size of the test
    classes = np.unique(y_true)
    tam = y_true.shape[0]

    # Transforms y_test into a proper ground truth matrix
    groundTruthM = _groundTruthMatrix(y_true, classes)

    # Decomposes the y_score probabilistic matrix into certainty and uncertainty
    certM, uncertM = _decompositionProbConfMatrix(y_score, groundTruthM)

    # Computes the serendipity matrix
    serendipityM = pd.DataFrame([_serendipityMatrix(certM, uncertM)/tam], columns=certTypes)

    return serendipityM

def class_spec_matrix(y_true, y_score, abs_tolerance=1e-8):
    """
    Calculate the serendipity matrix by class.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,). 
        Ground truth (correct) labels.

    y_score : array-like of shape (n_samples, n_classes).
        Probabilities of predicted labels, as returned by a classifier. The sum of 
        these probabilities must sum up to 1.0 over classes.

        The order of the class scores must correspond to the numerical or
        lexicographical order of the labels in y_true.

    abs_tolerance : absolute tolerance threshold for checking whether probabilities
        sum up to 1.0. Default = 1e-8.

    Returns
    ----------
    serendipityM : pandas DataFrame.
        Returns the values of the serendipity matrix by class.
    """
    if y_true.shape[0] != y_score.shape[0]:
        raise ValueError("'y_true' and 'y_score' have different number of samples.")
    
    if len(np.unique(y_true)) != y_score.shape[1]:
        raise ValueError("'y_true' and 'y_score' have different number of classes.")
    
    if not np.allclose(1, y_score.sum(axis=1), rtol=0, atol=abs_tolerance):
        raise ValueError(
            "Target scores need to be probabilities and they should sum up to 1.0 over classes."
        )
    
    certTypes = ["Reliability","Overconfidence","Underconfidence","Serendipity"]

    # Checks y_true data type
    if not isinstance(y_true, np.ndarray):
        y_true = y_true.to_numpy()
    
    # Classes of the test
    classes = np.unique(y_true)

    # Transforms y_test into a proper ground truth matrix
    groundTruthM = _groundTruthMatrix(y_true, classes)

    # Decomposes the y_score probabilistic matrix into certainty and uncertainty
    certM, uncertM = _decompositionProbConfMatrix(y_score, groundTruthM)
     
    serendipityM = pd.DataFrame(np.zeros((certM.shape[0], len(certTypes))),
                                columns=certTypes)

    # Computes the serendipity matrix by class
    for i in range(certM.shape[0]):
        sum = np.sum(certM[:,i], axis=0) + np.sum(uncertM[:,i], axis=0)
        
        if sum != 0:
            serendipityM["Reliability"][i] += certM[i][i]/sum
            serendipityM["Overconfidence"][i] += (np.sum(certM[:,i], axis=0) - certM[i][i])/sum
            serendipityM["Serendipity"][i] += uncertM[i][i]/sum
            serendipityM["Underconfidence"][i] += (np.sum(uncertM[:,i], axis=0) - uncertM[i][i])/sum

    # Sorts the serendipity matrix
    serendipityM["CLASS_NAME"] = np.array(classes)
    serendipityM = serendipityM[[serendipityM.columns[-1]] + serendipityM.columns.tolist()[:-1]]

    return serendipityM


def plot_class_spec(y_true, y_score, output_fig_path = None):
    """
    Plots and shows the class-specific serendipity matrix horizontal bar chart and saves them in format .png.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,). 
        Ground truth (correct) labels.

    y_score : array-like of shape (n_samples, n_classes).
        Probabilities of predicted labels, as returned by a classifier. The sum of 
        these probabilities must sum up to 1.0 over classes.

        The order of the class scores must correspond to the numerical or
        lexicographical order of the labels in y_true.

    output_fig_path : if given, figure will be saved at this location. If no file extension is given,
        png will be used by default. Default = None.
    """
    if output_fig_path is not None:
        if type(output_fig_path) is not str:
            raise ValueError("Given path should be a string.")
    
    # Checks y_true data type
    if not isinstance(y_true, np.ndarray):
        y_true = y_true.to_numpy()

    # Classes of the test
    classes = np.unique(y_true)

    # Computes the serendipity matrix and orders the matrix by the reliability
    serendipityM = class_spec_matrix(y_true, y_score)
    serendipityM = serendipityM.sort_values(by="Reliability", ascending=False)
        
    data = serendipityM[::-1].reset_index(drop=True)

    # Variable declaration for a suitable format
    if output_fig_path == None:
        plt.figure(figsize=(12, max(4,len(classes)*0.4)))
        pos = -0.00017 * len(classes)**2 + 0.0094 * len(classes) - 0.177 # ax2 + bx + c
        height = 0.05
        pad = 10
        y_axis_p = 0.1
        y_axis_margin = 0.05
        y_lim_l = 0
        y_lim_r = 0
    else:
        plt.figure(figsize=(14, len(classes)*0.5))
        pos = -0.00078 * len(classes)**2 + 0.036 * len(classes) - 0.431 # ax2 + bx + c
        height = 0.2
        pad = 35
        y_axis_p = 0.25
        y_axis_margin = 0.15
        y_lim_l = 0
        y_lim_r = 0.05

    # Sets the size of the axis
    y_axis = np.arange(y_axis_margin, len(classes)*y_axis_p + y_axis_margin, len(classes)*y_axis_p/len(classes))
    x_axis = np.linspace(-1, 1, 21)
    ymin, ymax = plt.ylim(y_lim_l, len(classes)*y_axis_p + y_lim_r)
    plt.xlim(-1.01, 1.01)

    # Plots the data
    plt.title("Class-Specific Serendipity Matrix", fontdict={'color': 'black', 'weight': 'bold'}, pad=pad)
    plt.barh(y_axis, data["Reliability"], color="#4AB071", label="Reliability", height=height)     
    plt.barh(y_axis, -data["Overconfidence"], color='#348FA7', label='Overconfidence', height=height)
    plt.barh(y_axis, -data["Underconfidence"], left=-data["Overconfidence"], color='#DB8838', label="Underconfidence", height=height)     
    plt.barh(y_axis, data["Serendipity"], left=data["Reliability"], color='#FF4F47', label='Serendipity', height=height)
    
    # Sets the style of the chart
    plt.xticks(ticks=np.linspace(-1, 1, 21), labels=["1","0.9","0.8","0.7","0.6","0.5","0.4","0.3","0.2","0.1","0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"])
    plt.yticks(y_axis, data["CLASS_NAME"])
    plt.gca().xaxis.set_label_position("top")
    plt.gca().xaxis.set_ticks_position("top")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tick_params(axis='both', which='both', colors="#4F4F4F", length=0)

    for x in x_axis:
        plt.vlines(x=x, ymin=ymin, ymax=ymax, colors='#CDCDCD', linewidth=1)

    # Sets the legend of the chart
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, pos), ncol=4, frameon=False, fontsize=8.5)

    # Shows the chart or saves it on the gived path
    if output_fig_path == None:
        plt.tight_layout()
        plt.show()
    else:
        plt.savefig(output_fig_path, bbox_inches="tight", dpi=300)
        plt.close()

def _groundTruthMatrix(y_true, classes):
    """
    Returns the ground truth matrix from a given array of true values.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,). 
        Ground truth (correct) labels.

    classes : list with all the classes of the dataset.

    Returns
    ----------
    groundTruthM : numpy array(n_samples, n_classes).
        Returns the ground truth matrix.
    """
    # Size of the test
    tam = y_true.shape[0]

    # Initializes some utility arrays
    groundTruthM = np.zeros((tam, len(classes)))
    index = np.array([])

    # Makes a binary array from y_true
    for i in range(tam):
        class_y = y_true[i]
        for j in range(len(classes)):
            if(classes[j] == class_y):
                index = np.append(index, np.where(classes == classes[j])[0])

    # Turns the binary array into a binary matrix
    groundTruthM[np.arange(tam), index.astype(int)] = 1

    return groundTruthM

def _decompositionProbConfMatrix(probPredM, groundTruthM):
    """
    Decomposes the probabilistic prediction matrix into a certainty matrix and an uncertainty matrix.

    Parameters
    ----------
    probPredM :  array-like of shape (n_samples, n_classes).
        Probabilistic prediction matrix.

    groundTruthM :   array-like of shape (n_samples, n_classes).
        Ground truth matrix.

    Returns
    ----------
    certM :  array-like of shape (n_classes, n_classes).
        Certainty matrix.

    uncertM:  array-like of shape (n_classes, n_classes).
        Uncertainty matrix.
    """
    # Initializes two empty matrix and one empty array
    certM = np.zeros((probPredM.shape[0], probPredM.shape[1]))
    uncertM = np.zeros((probPredM.shape[0], probPredM.shape[1]))
    classes = np.zeros((probPredM.shape[1]))

    # Fills the empty array with a different number for each different class
    for i in range(1, probPredM.shape[1]):
        classes[i] = i

    # Saves the index for the most likely prediction from the probabilistic prediction matrix
    certIndex = np.argmax(probPredM, axis=1)

    # Saves the probabilistic predictions into the certainty and uncertainty matrix
    for i in range(probPredM.shape[0]):
        uncertIndex = np.delete(classes.astype(int), certIndex[i])
        certM[i][certIndex[i]] = np.max(probPredM[i])
        for j in range(len(uncertIndex)):
            uncertM[i][uncertIndex[j]] = probPredM[i][uncertIndex[j]]

    # Computes the certainty matrix and the uncertainty matrix
    certM = _confusionMatrix(groundTruthM, certM)
    uncertM = _confusionMatrix(groundTruthM, uncertM)

    return certM, uncertM

def _confusionMatrix(groundTruthM, predM):
    """
    Returns the confusion matrix as a result of the multiplication of the ground truth matrix and the prediction matrix.

    Parameters
    ----------
    groundTruthM : array-like of shape (n_samples, n_classes). 
        Ground truth matrix.

    predM : array-like of shape (n_samples, , n_classes). 
        Prediction matrix.

    Returns
    ----------
    confM : nnumpy array (n_classes, n_classes).
        Confusion matrix.
    """
    # Transposes the ground truth matrix and multiplies it by the prediction matrix
    confM = np.dot(np.transpose(groundTruthM), predM)

    return confM

def _serendipityMatrix(certM, uncertM):
    """
    Calculates the values of the serendipity matrix.

    Parameters
    ----------
    certM : array-like of shape (n_classes, n_classes). 
        Certainty matrix.

    uncertM : array-like of shape (n_classes, n_classes). 
        Uncertainty matrix.

    Returns
    ----------
    serendipityM : numpy array.
        Returns the serendipity matrix.
    """
    # Computes the certain and uncertain measures
    certAcc = np.trace(certM)
    certInacc = np.sum (certM) - np.trace(certM)
    uncertInacc = np.trace(uncertM)
    uncertAcc = np.sum (uncertM) - np.trace(uncertM)

    serendipityM = np.array([certAcc, certInacc, uncertAcc, uncertInacc])
    serendipityM[serendipityM < 0] = 0

    return serendipityM