import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# File documents the methods used in the PCA feature selection script

# Sets the pipeline for the PCA logistic model using a given number of components to use for PCA 
def PCALogisticFixedRank(X, y, rank):

    model = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=rank)),
        ('classifier', LogisticRegression(solver='saga', max_iter=600)),
    ])
    return model.fit(X, y)


# Runs the PCA logistic model for each number of components listed in the n_components array and stores the output into the outputFile
def PCALogisticAllRanks(X, y, n_components, features, outputFile):

    # Splits the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    train_scores = []
    test_scores = []
    ranks = []
    bestFeatures = []

    # Runs the PCA model for each number of components in the n_components array
    for n in n_components:
        print(n)
        # Runs PCA pipeline with n components
        results = PCALogisticFixedRank(X_train, y_train, n)
        
        # Stores train and test scores
        train_scores.append(results.score(X_train, y_train))
        test_scores.append(results.score(X_test, y_test))
        ranks.append(n)

        # Finds the features that contribute the most to each component, then stores them
        most_important = [np.abs(results.named_steps['pca'].components_[i]).argmax() for i in range(n)]
        most_important_features = [features[most_important[i]] for i in range(n)]
        bestFeatures.append(most_important_features)
        #print(n)
        #print(bestFeatures[n-1])

    # Plot scores
    plt.title("Training & test scores using Principal-Component Regression")
    plt.plot(ranks, train_scores, label='training score')
    plt.plot(ranks, test_scores, label='test score')
    plt.xlabel('n_components')
    plt.legend()
    plt.savefig('figs/PCRLogScores.png')

    # Save output
    with open(outputFile, 'w') as file:
        file.write("Rank\tTrain Score\tTest Score\tBest Features\n")
        for i in range(len(ranks)):
            file.write(f"{ranks[i]}\t{train_scores[i]}\t{test_scores[i]}\t{bestFeatures[i]}\n")

    return bestFeatures 
