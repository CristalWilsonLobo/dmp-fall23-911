import numpy as np
from numpy.lib.npyio import load
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.feature_selection import SelectFromModel

# File documents the methods used in the lasso feature selection script

# Sets the pipeline for the lasso logistic model using a given weight 
def lassoLogisticFixedWeight(X, y, weight):
    #Set up pipeline
    pipeline = Pipeline([
    ('model', LogisticRegression(penalty='l1', solver='saga', max_iter=800, C=weight))
    ])

    return pipeline.fit(X, y)


# Runs the lasso logistic model for each weight listed in the weights array and stores the output into the outputFile
def lassoLogisticAllWeights(X, y, weights, features, outputFile):

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    train_scores = []
    test_scores = []
    featuresIncluded = []
    for n in weights:
        print(n)
        # Runs lasso logistic pipeline with n components
        results = lassoLogisticFixedWeight(X_train, y_train, n)
        
    # Use SelectFromModel after fitting the pipeline
        sfm = SelectFromModel(results.named_steps['model'])
        sfm.fit(X_train, y_train)

        # Transform the features
        selected_feature_indices = sfm.get_support(indices=True)
        features_selected = np.array(features)[selected_feature_indices].tolist()
        print(features_selected)

        # Stores train and test scores
        train_scores.append(results.score(X_train, y_train))
        test_scores.append(results.score(X_test, y_test))
        print(test_scores[len(train_scores)-1])

        featuresIncluded.append(features_selected)

    # Plot scores
    plt.title("Training & test scores using Logistic Regression with l1 penality")
    plt.plot(weights, train_scores, label='training score')
    plt.plot(weights, test_scores, label='test score')
    plt.xlabel('weights')
    plt.legend()
    plt.savefig('PCRLogScores.png')

    # Save output
    with open(outputFile, 'w') as file:
        file.write("Penalty Weight | Train Score | Test Score | Features with Non-Zero Coefficients\n")
        for i in range(len(weights)):
            file.write(f"{weights[i]} | {train_scores[i]} | {test_scores[i]} | {featuresIncluded[i]}\n")

    return (train_scores, test_scores, featuresIncluded) 


# Sets the pipeline for the lasso model using a given weight 
def lassoRegressionFixedWeight(X, y, weight):
    #Set up pipeline
    pipeline = Pipeline([
    ('model', Lasso(alpha=weight))])

    return pipeline.fit(X, y)


# Runs the lasso OSL model for each weight listed in the weights array and stores the output into the outputFile
def lassoRegressionAllWeights(X, y, weights, features, outputFile):

    # split data into train and test sections
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    train_scores = []
    test_scores = []
    featuresIncluded = []

    # runs the lasso model on all weights 
    for n in weights:
        print(n)
        # Runs lasso logistic pipeline with n components
        results = lassoRegressionFixedWeight(X_train, y_train, n)

        # Use SelectFromModel after fitting the pipeline
        sfm = SelectFromModel(results.named_steps['model'])
        sfm.fit(X_train, y_train)

        # Transform the features
        selected_feature_indices = sfm.get_support(indices=True)
        features_selected = np.array(features)[selected_feature_indices].tolist()
        print(features_selected)

        # Stores train and test scores
        train_scores.append(results.score(X_train, y_train))
        test_scores.append(results.score(X_test, y_test))
        print(test_scores[len(train_scores)-1])

        featuresIncluded.append(features_selected)

    # Plot scores of each model version against penalty weights
    plt.title("Training & test scores using Lasso Regression")
    plt.plot(weights, train_scores, label='training score')
    plt.plot(weights, test_scores, label='test score')
    plt.xlabel('weights')
    plt.legend()
    plt.savefig('lassoRegScores.png')

    # Save output
    with open(outputFile, 'w') as file:
        file.write("Penalty Weight | Train Score | Test Score | Features with Non-Zero Coefficients\n")
        for i in range(len(weights)):
            file.write(f"{weights[i]} | {train_scores[i]} | {test_scores[i]} | {featuresIncluded[i]}\n")

    return (train_scores, test_scores, featuresIncluded) 