import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif, chi2
import matplotlib.pyplot as plt

# File documents the methods used in the univariate feature selection script

def univariateSelectF(X, y, numVisualize, features, k='all'):
    """
    This method takes in a file path to the results of the feature selection script for the PCA
    feature selection approach and prints out a summary of the results. It takes the best model from
    the PCA models with 30 or less components (since we are aiming to select a low number of features)
    and then reports the features included in this model.

    :param file_path: The path to the results text file
    :param show: if true, prints out results
    :return: A dictionary with the rank of the feature as keys and the feature name as the value
    """
    # use SelecKBest to identify features
    k_best = SelectKBest(score_func=f_classif, k=k)
    k_best.fit(X, y)

    # Sort features by F score
    f_scores = k_best.scores_
    p_values = k_best.pvalues_
    results = pd.DataFrame({'Feature': features, 'F-Score': f_scores, 'P-Value': p_values})
    results = results.sort_values(by='F-Score', ascending=False)

    # Visualize the scores of the k best features with labels
    plt.figure(figsize=(10, 6))
    plt.barh(results['Feature'][:numVisualize], results['F-Score'][:numVisualize])
    plt.xlabel('F-Score')
    plt.title('Top {} Features'.format(numVisualize))
    plt.savefig('figs/uniFResults.png')
    #plt.show()
    
    print(results)
    return results


# univariate feature selection using mutual info for scoring
def univariateSelectMI(X, y, numVisualize, features, k='all'):

    # use SelecKBest to identify features
    k_best = SelectKBest(score_func=mutual_info_classif, k=k)
    k_best.fit(X, y)

    # Sort features by F score
    f_scores = k_best.scores_
    p_values = k_best.pvalues_
    results = pd.DataFrame({'Feature': features, 'MutualInfo': f_scores, 'P-Value': p_values})
    results = results.sort_values(by='MutualInfo', ascending=False)

    # Visualize the scores of the k best features with labels
    plt.figure(figsize=(10, 6))
    plt.barh(results['Feature'][:numVisualize], results['MutualInfo'][:numVisualize])
    plt.xlabel('Mutual Information Score')
    plt.title('Top {} Features'.format(numVisualize))
    plt.savefig('figs/uniMIResults.png')

    print(results)
    return results

# univariate feature selection using chi^2  for scoring - doesnt work unless we scale X to have only non negative values
def univariateSelectChi(X, y, numVisualize, features, k='all'):

    # use SelecKBest to identify features
    k_best = SelectKBest(score_func=chi2, k=k)
    k_best.fit(X, y)

    # Sort features by F score
    f_scores = k_best.scores_
    p_values = k_best.pvalues_
    results = pd.DataFrame({'Feature': features, 'chi2': f_scores, 'P-Value': p_values})
    results = results.sort_values(by='chi2', ascending=False)

    # Visualize the scores of the k best features with labels
    plt.figure(figsize=(10, 6))
    plt.barh(results['Feature'][:numVisualize], results['chi2'][:numVisualize])
    plt.xlabel('Chi^2 Score')
    plt.title('Top {} Features'.format(numVisualize))
    plt.savefig('figs/uniChiResults.png')

    print(results)
    return results

def saveResults(results, scoringMetric, outputFile):
    # Save results to a text file
    with open(outputFile, 'w') as file:
        file.write("Feature\t{scoringMetric}\tP-Value\n")
        for i in range(len(results)):
            file.write(f"{results['Feature'][i]}\t{results[scoringMetric][i]}\t{results['P-Value'][i]}\n")







