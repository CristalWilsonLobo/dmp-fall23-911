import numpy as np
import pandas as pd
from ast import literal_eval

# Methods used to format, aggregatem and present the output of the feature selection scripts

def getPCAFeatures(file_path, show=False):
    """
    This method takes in a file path to the results of the feature selection script for the PCA
    feature selection approach and prints out a summary of the results. It takes the best model from
    the PCA models with 30 or less components (since we are aiming to select a low number of features)
    and then reports the features included in this model.

    :param file_path: The path to the results text file
    :param show: if true, prints out results
    :return: A dictionary with the rank of the feature as keys and the feature name as the value
    """

    pca_df = pd.read_csv(file_path, sep='\t', converters={'Best Features': literal_eval})

    # Select the top 30 rows
    top_30_rows = pca_df.nsmallest(30, 'Rank')

    # Sort by 'Test Score'
    sorted_top_30 = top_30_rows.sort_values(by='Test Score', ascending=False)
    top_row = sorted_top_30.nlargest(1, 'Test Score').iloc[0]

    if show == True:
    # Print model run with best train score from the models with principal components of 30 or less
        print("PCA Feature Selection Results\n")
        print("Model with best test score from models with 30 or fewer principal components included")
        # Print the rank, Test Score, and all features for the top row
        print(f"Rank: {top_row['Rank']}")
        print(f"Test Score: {top_row['Test Score']}")
        print(f"Features that contributed most strongly to each component from best model (in order of inclusion):\n")

    # Create a dictionary to store rank as key and feature as value
    features_dict = {}
    for idx, feature in enumerate(top_row['Best Features']):
        features_dict[feature] = idx

    # Strip categorical outcomes from the feature names
    strippedDict = strip_cat_keys(features_dict)

   # Print model run with best train score from the models with principal components of 30 or less
    if show == True:
        print("Univariate Feature Selection with F Statistic Results\n")
        print("Top 30 features ranked using the F statistic")
        for i in strippedDict.keys():
            print(strippedDict[i], "          ", i)

    print('\n')
    return strippedDict



def getLassoRegFeatures(file_path, show=False):
    """
    This method takes in a file path to the results of the feature selection script for the lasso OLS
    feature selection approach and prints out a summary of the results. It takes the model with the best
    test score from the models that include 30 or less features and reports the weight used to generate 
    the model, the test score, and the features included

    :param file_path: The path to the results text file
    :param show: if true, prints out results
    :return: A dictionary with the rank of the feature as keys and the feature name as the value
    """

    lasso_df = pd.read_csv(file_path, sep='|', converters={' Features with Non-Zero Coefficients': literal_eval})
    lasso_df.columns = lasso_df.columns.str.strip()
    lasso_df = lasso_df.rename(columns={'Features with Non-Zero Coefficients': 'Features Included', 'Rank': 'Penalty Weight'})

    # Select the rows with less than 30 features included
    filtered_rows = lasso_df[lasso_df['Features Included'].apply(len) < 30]

    if not filtered_rows.empty:
        # Select the row with the largest Test Score among the filtered rows
        selected_row = filtered_rows.nlargest(1, "Test Score").iloc[0]

        if show == True:
            # Print model run with best train score from the models with the # of features included of 30 or less
            print("Lasso OLS Feature Selection Results\n")
            print("Model with best test score from lasso analysis using OLS that includes 30 or less features")
            # Print the rank, Test Score, and all features for the top row
            print(f"Weight placed on penalty term: {selected_row['Penalty Weight']}")
            print(f"Test Score: {selected_row['Test Score']}")
            print(f"Features included in best model:")

        # Create a dictionary to store rank as key and feature as value
        features_dict = {}
        for idx, feature in enumerate(np.array(selected_row['Features Included'])):
            features_dict[feature] = idx

        # Strip categorical outcomes from the feature names
        strippedDict = strip_cat_keys(features_dict)
        sorted_entries = sorted(strippedDict.items(), key=lambda x: x[1])
        result_dict = {name: i + 1 for i, (name, _) in enumerate(sorted_entries)}

        if show == True:
            for i in result_dict.keys():
                print(result_dict[i], "          ", i)
            
            print('\n')
        return result_dict
    
    else:
        print("No row satisfies the condition that the number of features selected is less than 30")
        return {}



def getLassoLogFeatures(file_path, show=False):
    """
    This method takes in a file path to the results of the feature selection script for the lasso logistic
    feature selection approach and prints out a summary of the results. It takes the model with the best
    test score from the models that include 30 or less features and reports the weight used to generate 
    the model, the test score, and the features included

    :param file_path: The path to the results text file
    :param show: if true, prints out results
    :return: A dictionary with the rank of the feature as keys and the feature name as the value
    """

    lasso_df = pd.read_csv(file_path, sep='|', converters={' Features with Non-Zero Coefficients': literal_eval})
    lasso_df.columns = lasso_df.columns.str.strip()
    lasso_df = lasso_df.rename(columns={'Features with Non-Zero Coefficients': 'Features Included', 'Rank': 'Penalty Weight'})

    filtered_rows = lasso_df[lasso_df['Features Included'].apply(len) < 40]

    if not filtered_rows.empty:
        # Select the row with the largest Test Score among the filtered rows
        selected_row = filtered_rows.nlargest(1, "Test Score").iloc[0]

        if show == True:
            # Print model run with best train score from the models with the # of features included of 30 or less
            print("Lasso Logistic Feature Selection Results\n")
            print("Model with best test score from lasso analysis using a logostic model that includes 30 or less features")
            # Print the rank, Test Score, and all features for the top row
            print(f"Weight placed on penalty term: {selected_row['Penalty Weight']}")
            print(f"Test Score: {selected_row['Test Score']}")
            print(f"Features included in best model:")

        # Create a dictionary to store rank as key and feature as value
        features_dict = {}
        for idx, feature in enumerate(np.array(selected_row['Features Included'])):
            features_dict[feature] = idx

        # Strip categorical outcomes from the feature names
        strippedDict = strip_cat_keys(features_dict)
        sorted_entries = sorted(strippedDict.items(), key=lambda x: x[1])
        result_dict = {name: i + 1 for i, (name, _) in enumerate(sorted_entries)}

        if show == True:
            for i in result_dict.keys():
                print(result_dict[i], "          ", i)
            
            print('\n')

        return result_dict
    
    else:
        print("No row satisfies the condition that the number of features selected is less than 50")
        return {}




def getUniFFeatures(file_path, show=False):
    """
    This method takes in a file path to the results of the feature selection script for the univariate
    feature selection approach using the F statistic and prints out a summary of the results.

    :param file_path: The path to the results text file
    :param show: if true, prints out results
    :return: A dictionary with the rank of the feature as keys and the feature name as the value
    """
    uni_df = pd.read_csv(file_path, sep='\t')

    # Select the top 30 rows sorted by the score
    top_30_rows = uni_df.nlargest(30, '{scoringMetric}')

    # Create a dictionary to store rank as key and feature as value
    features_dict = {}
    for idx, feature in enumerate(top_30_rows['Feature']):
            features_dict[feature] = idx

    # Strip categorical outcomes from the feature names
    strippedDict = strip_cat_keys(features_dict)

    if show == True:
    # Print model run with best train score from the models with principal components of 30 or less
        print("Univariate Feature Selection with F Statistic Results\n")
        print("Top 30 features ranked using the F statistic")
        for i in strippedDict.keys():
            print(strippedDict[i], "          ", i)

    return strippedDict




def getUniMIFeatures(file_path, show=False):
    """
    This method takes in a file path to the results of the feature selection script for the univariate
    feature selection approach using mutual information scoring and prints out a summary of the results.

    :param file_path: The path to the results text file
    :param show: if true, prints out results
    :return: A dictionary with the rank of the feature as keys and the feature name as the value
    """
    uni_df = pd.read_csv(file_path, sep='\t')

    # Select the top 30 rows sorted by the score
    top_30_rows = uni_df.nlargest(30, '{scoringMetric}')

    # Create a dictionary to store rank as key and feature as value
    features_dict = {}
    for idx, feature in enumerate(top_30_rows['Feature']):
            features_dict[feature] = idx

    # Strip categorical outcomes from the feature names
    strippedDict = strip_cat_keys(features_dict)
    sorted_entries = sorted(strippedDict.items(), key=lambda x: x[1])
    result_dict = {name: i + 1 for i, (name, _) in enumerate(sorted_entries)}

    if show == True:
        # Print model run with best train score from the models with principal components of 30 or less
        print("Univariate Feature Selection with Mutual Information Scoring Results\n")
        print("Top 30 features ranked using mutual information for scoring")
        for i in result_dict.keys():
            print(result_dict[i], "          ", i)

    return result_dict



def strip_cat_keys(dictionary):
    """
    This method strips the categorical column labels from the variable names

    :param file_path: a dictionary that has feature names as keys and the rank of the features as values
    :return: A dictionary with the rank of the feature as keys and the feature name as the value, with cat labels stripped from feature names
    """
    modified_dict = {}

    for key, value in dictionary.items():
        if key.startswith("cat_"):
            # Find the last instance of "_" in the key
            last_underscore_index = key.rfind("_")

            # Modify the key by removing characters after the last "_"
            modified_key = key[:last_underscore_index] if last_underscore_index != -1 else key

            # Add the modified key and its corresponding value to the new dictionary if not already there
            if modified_key not in modified_dict.keys():
                modified_dict[modified_key] = value
        else:
            # If the key doesn't start with "cat_", keep it unchanged
            modified_dict[key] = value

    return modified_dict



def average_two_ranks(dict1, dict2, show=False):
    """
    This method averages the ranking of features between two dictionaries that contain feature rankings

    :param dicts1, dict2: two dictionary that has feature names as keys and the rank of the features as values
    :return: A dictionary with the rank of the feature as keys and the feature name as the value, where the rankings are the average of the two parameter rankings
    """
    # Combine all unique feature names from the dictionaries
    all_features = set(dict1.keys()) | set(dict2.keys())

    # Initialize an empty dictionary to store the averaged ranks
    averaged_ranks = {}

    # Iterate through each feature name
    for feature in all_features:
        # Get the rank for each dictionary or assume rank 30 if the feature is not present
        rank1 = dict1.get(feature, 30)
        rank2 = dict2.get(feature, 30)

        # Calculate the average rank
        avg_rank = (rank1 + rank2) / 2.0

        # Store the average rank in the result dictionary
        averaged_ranks[feature] = avg_rank

    bestFeatures = get_top_n_lowest_ranks(averaged_ranks, 30)
    
    if show == True:
        print("Averaged Rankings:\n")
        for i in bestFeatures.keys():
            print(bestFeatures[i], "          ", i)

    return bestFeatures



def average_feature_ranks(dict1, dict2, dict3, show=False):
    """
    This method averages the ranking of features between three dictionaries that contain feature rankings

    :param dict1, dict2, dict3:three dictionary that has feature names as keys and the rank of the features as values
    :return: A dictionary with the rank of the feature as keys and the feature name as the value, where the rankings are the average of the three parameter rankings
    """
    # Combine all unique feature names from the dictionaries
    all_features = set(dict1.keys()) | set(dict2.keys()) | set(dict3.keys())

    # Initialize an empty dictionary to store the averaged ranks
    averaged_ranks = {}

    # Iterate through each feature name
    for feature in all_features:
        # Get the rank for each dictionary or assume rank 40 if the feature is not present - this is done to put extra weight
        # features selected by multiple methods
        rank1 = dict1.get(feature, 40)
        rank2 = dict2.get(feature, 40)
        rank3 = dict3.get(feature, 40)

        # Calculate the average rank
        avg_rank = (rank1 + rank2 + rank3) / 3.0

        # Store the average rank in the result dictionary
        averaged_ranks[feature] = avg_rank
    
    bestFeatures = get_top_n_lowest_ranks(averaged_ranks, 20)

    if show == True:
        print("Aggregate Selected Features (Averaged Across PCA, Lasso, and Univariate):\n")
        for i in bestFeatures.keys():
            print(bestFeatures[i], "          ", i)
        
    return bestFeatures


def get_top_n_lowest_ranks(input_dict, n):
    """
    This method selects the n elements of the inputed dictionary of features that have the lowest rankings

    :param n: an integer value
    :param input_dict: a dictionary that has feature names as keys and the rank of the features as values
    :return: A dictionary with the rank of the feature as keys and the feature name as the value, where the rankings are the average of the two parameter rankings
    """
    # Sort the dictionary by values (ranks)
    sorted_entries = sorted(input_dict.items(), key=lambda x: x[1])

    # Take the top n entries with the lowest ranks
    top_n_entries = sorted_entries[:n]

    # Create a new dictionary with revalued ranks
    result_dict = {name: i + 1 for i, (name, _) in enumerate(top_n_entries)}

    return result_dict




def print_aggregate_selected_featurs(show=False):
    """
    This method runs all of the above methods to print out the results of all the feature selection algorithms and then aggregate them into one ranking

    :param show: a boolean value that if true, prints out the results
    :return: the averaged dictionary of selected features across all feature selection approaches used
    """
    # Paths to files where output of feature selection scripts are stored
    pca_file_path = 'output/feature_select_PCA.txt'
    lasso_reg_filepath = 'output/feature_select_lasso_reg.txt'
    lasso_log_filepath = 'output/feature_select_lasso_log.txt'
    uni_file_path_f = 'output/feature_select_uni_f.txt'
    uni_file_path_MI = 'output/feature_select_uni_MI.txt'

    # Saves top ranked features from PCA
    pca = getPCAFeatures(pca_file_path, show)

    # # Saves top ranked features from Univariate selection using the F stat and MI scoring metrics
    uniF = getUniFFeatures(uni_file_path_f, show)
    uniMI = getUniMIFeatures(uni_file_path_MI, show)
    # Average the two ways of doing univariate selection into one dictionary of ranked features
    print("Average Rabkings of Features from Two Univariate Methods")
    uni =average_two_ranks(uniF, uniMI, show)

    # Saves top ranked features from lasso using OLS and logistic regression
    lassoReg = getLassoRegFeatures(lasso_reg_filepath, show)
    lassoLog = getLassoLogFeatures(lasso_log_filepath, show)
    # Average the two ways of doing lasso selection into one dictionary of ranked features
    print("Average Rabkings of Features from Two Lasso Methods")
    lasso = average_two_ranks(lassoReg, lassoLog, show)

    # Average the three feature selection results into one aggregate ranking of features
    print("\n")
    aggregate = average_feature_ranks(pca, uni, lasso, show)

    print("Feature selection script finished")

    return aggregate


#### The below methods return selected features as arrays for the models to use ###

def getmodelLassoFeatures():
    """
    Generates the list of the best lasso features as an array

    :return: an array of the  best features selected by the lasso methods
    """
    # Paths to files where output of feature selection scripts are stored
    lasso_reg_filepath = 'output/feature_select_lasso_reg.txt'
    lasso_log_filepath = 'output/feature_select_lasso_log.txt'

    # Average top ranked features from lasso using OLS and logistic regression
    lassoReg = getLassoRegFeatures(lasso_reg_filepath)
    lassoLog = getLassoLogFeatures(lasso_log_filepath)
    # Average the two ways of doing lasso selection into one dictionary of ranked features
    lasso = average_two_ranks(lassoReg, lassoLog)

    return np.array(list(lasso.keys()))


def getmodelUniFeatures():
    """
    Generates the list of the best univariate features as an array

    :return: an array of the  best features selected by the univariate methods
    """
    # Paths to files where output of feature selection scripts are stored
    uni_file_path_f = 'output/feature_select_uni_f.txt'
    uni_file_path_MI = 'output/feature_select_uni_MI.txt'

    # # Saves top ranked features from Univariate selection using the F stat and MI scoring metrics
    uniF = getUniFFeatures(uni_file_path_f)
    uniMI = getUniMIFeatures(uni_file_path_MI)
    # Average the two ways of doing univariate selection into one dictionary of ranked features
    print("Average Rabkings of Features from Two Univariate Methods")
    uni =average_two_ranks(uniF, uniMI)

    return np.array(list(uni.keys()))


def getModelPCAFeatures():
    """
    Generates the list of the best PCA features as an array

    :return: an array of the  best features selected by the PCA methods
    """
    # Paths to files where output of feature selection scripts are stored
    pca_file_path = 'output/feature_select_PCA.txt'

    # Saves top ranked features from PCA
    pca = getPCAFeatures(pca_file_path)

    return np.array(list(pca.keys()))



def getModelAverageFeatures():
    """
    This method runs all of the above methods to print out the results of all the feature selection algorithms and then aggregate them into one ranking

    :return: an array of the average best features across all methods employeed for feature selection
    """
    # Paths to files where output of feature selection scripts are stored
    pca_file_path = 'output/feature_select_PCA.txt'
    lasso_reg_filepath = 'output/feature_select_lasso_reg.txt'
    lasso_log_filepath = 'output/feature_select_lasso_log.txt'
    uni_file_path_f = 'output/feature_select_uni_f.txt'
    uni_file_path_MI = 'output/feature_select_uni_MI.txt'

    # Saves top ranked features from PCA
    pca = getPCAFeatures(pca_file_path)

    # # Saves top ranked features from Univariate selection using the F stat and MI scoring metrics
    uniF = getUniFFeatures(uni_file_path_f)
    uniMI = getUniMIFeatures(uni_file_path_MI)
    # Average the two ways of doing univariate selection into one dictionary of ranked features
    uni =average_two_ranks(uniF, uniMI)

    # Saves top ranked features from lasso using OLS and logistic regression
    #lassoReg = getLassoRegFeatures(lasso_reg_filepath)
    lassoLog = getLassoLogFeatures(lasso_log_filepath)
    # Average the two ways of doing lasso selection into one dictionary of ranked features
    #lasso = average_two_ranks(lassoReg, lassoLog)

    # Average the three feature selection results into one aggregate ranking of features
    print("\n")
    aggregate = average_feature_ranks(pca, uni, lassoLog)

    return np.array(list(aggregate.keys()))



#print(getModelAverageFeatures())
# print(getModelPCAFeatures())
# print(getmodelUniFeatures())
# print(getmodelLassoFeatures())