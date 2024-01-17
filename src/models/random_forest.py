from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, cross_val_predict
from skopt import BayesSearchCV


def train_and_evaluate_model(X, y, cv):
    """
    Train and evaluate a Random Forest model using cross-validation with hyperparameter tuning.

    :param X: The features
    :param y: The labels
    :param cv: The cross-validation strategy
    :return: A dictionary containing the performance metrics and the best hyperparameters
    """
    model = RandomForestClassifier(random_state=42)

    # Define the parameter grid to search. These parameters were chosen because they are the most important ones to
    # tune.
    param_grid = {
        'n_estimators': [100, 150, 200, 250],
        'max_depth': [1, 2, 5, 10],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    # Initialize BayesSearchCV
    bayes = BayesSearchCV(model,
                          search_spaces=param_grid,  # same space as GridSearch
                          n_iter=20,
                          cv=5,
                          n_jobs=-1)

    # Fit BayesSearchCV
    bayes.fit(X, y)

    # Get the best model
    best_model = bayes.best_estimator_

    # Use cross_val_score to get scores for each fold
    accuracy_scores = cross_val_score(best_model, X, y, cv=cv, scoring='accuracy')
    f1_scores = cross_val_score(best_model, X, y, cv=cv, scoring='f1_macro')

    # Get predictions for each fold of CV
    predictions = cross_val_predict(best_model, X, y, cv=cv)

    performance = {
        'accuracy': accuracy_scores.tolist(),
        'f1_score': f1_scores.tolist()
    }

    # Calculate cumulative confusion matrix
    cum_conf_matrix = confusion_matrix(y, predictions)

    # Return performance metrics and best hyperparameters
    return performance, bayes.best_params_, cum_conf_matrix
