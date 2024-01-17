from sklearn.metrics import confusion_matrix

import xgboost as xgb
from sklearn.model_selection import cross_val_score, cross_val_predict
from skopt import BayesSearchCV


def train_and_evaluate_model(X, y, cv):
    """
    Train and evaluate a XGBoost model using cross-validation with hyperparameter tuning.

    :param X: The features
    :param y: The labels
    :param cv: The cross-validation strategy
    :return: A tuple containing the performance metrics and the best hyperparameters.
    """
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)

    # Define a parameter grid to search over. These parameters were chosen because they are the most important ones to
    # tune.  We can add more parameters to this grid if needed.
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
    }

    # Set up the Bayes search with cross-validation
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

    # Return performance metrics and best hyperparameters
    return performance, bayes.best_params_, cum_conf_matrix
