import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.naive_bayes import GaussianNB
from skopt import BayesSearchCV


def train_and_evaluate_model(X, y, cv):
    """
    Train and evaluate a Naive Bayes model using cross-validation
    with hyperparameter tuning.

    :param X: The features
    :param y: The labels
    :param cv: The cross-validation strategy
    :return: A dictionary containing the performance metrics.
    """

    # Initialize the classifier
    model = GaussianNB()

    # Define a set of parameters to test.  The var_smoothing values span several orders of magnitude.
    param_grid = {
        'var_smoothing': np.logspace(0, -9, num=100)
    }

    # Initialize BayesSearchCV.  Using BayesSearchCV to find the best var_smoothing value according to cross-validated
    # accuracy.
    bayes = BayesSearchCV(model,
                          search_spaces=param_grid,
                          n_iter=20,
                          cv=5)

    # Fit BayesSearchCV
    bayes.fit(X, y)

    # Get the best model
    best_model = bayes.best_estimator_

    # Use cross_val_score to get scores for each fold
    accuracy_scores = cross_val_score(best_model, X, y, cv=cv, scoring='accuracy')
    f1_scores = cross_val_score(best_model, X, y, cv=cv, scoring='f1_macro')

    # Get predictions for each fold of CV
    predictions = cross_val_predict(best_model, X, y, cv=cv)

    # Performance metrics
    performance = {
        'accuracy': accuracy_scores.tolist(),
        'f1_score': f1_scores.tolist()
    }

    # Calculate cumulative confusion matrix
    cum_conf_matrix = confusion_matrix(y, predictions)

    # return performance, grid_search.best_params_
    return performance, bayes.best_params_, cum_conf_matrix
