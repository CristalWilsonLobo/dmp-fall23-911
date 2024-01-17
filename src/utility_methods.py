import numpy as np
import pandas as pd
import zipfile
import seaborn as sns

from matplotlib import pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from feature_selection.process_selected_features import getModelAverageFeatures, getModelPCAFeatures, \
    getmodelUniFeatures, getmodelLassoFeatures
from models.naive_bayes import train_and_evaluate_model as train_naive_bayes
from models.random_forest import train_and_evaluate_model as train_random_forest
from models.xgboost import train_and_evaluate_model as train_xgboost


def extract_specific_file_from_zip_archive(zip_file_path, csv_file_name):
    """
    This method takes in a file path to the zip archive and the name of a CSV file that is contained in the archive.
    It then extracts the CSV file from the archive and returns it as a dataframe.

    :param zip_file_path: The path to the archive
    :param csv_file_name: The file you want extracted from the archive
    :return: A dataframe from the CSV file that is extracted from the archive

    """
    # Using the zipfile module to read the specific CSV file from the ZIP
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        with z.open(csv_file_name) as f:
            df = pd.read_csv(f)

    return df


def load_data(filename="cleaned_Data.csv"):
    """
    This method loads the data from the CSV file and returns it as a dataframe.

    :return: A dataframe containing the data
    """
    print(f"Loading data from " + filename + "...")

    # Read the dataset
    data = pd.read_csv("data/" + filename, low_memory=False)

    print(f"Data load complete\n")

    return data


def get_all_sme_features():
    """
    This method returns a list of the features that were selected by subject-matter experts.

    :return: A list of the features that were selected by subject-matter experts
    """
    data_list = ['cat__eArrest_01', 'cat__eArrest_02', 'cat__eArrest_04', 'cat__eArrest_05',
                 'cat__eArrest_07', 'cat__eArrest_11', 'cat__ePatient_13', 'cat__ePatient_14',
                 'cat__eResponse_10', 'cat__eResponse_11', 'cat__eResponse_15', 'num__eVitals_10', 'num__eVitals_16',
                 'cat__eVitals_26', 'cat__Urbanicity', 'cat__eArrest_16', 'cat__USCensusDivision',
                 'num__EMSSystemResponseTimeMin', 'num__EMSTransportTimeMin', 'num__ageinyear', 'num__EMSSceneTimeMin',
                 'cat__Outcome']

    # Converting list to a NumPy array
    return np.array(data_list)


def pick_feature_selection_method(method, outcome_sample):
    """
    Selects and applies a feature selection method to the provided 'outcome_sample' dataframe and returns the
    categorical features, continuous features, combined features, and a subset of 'outcome_sample'.

    This function chooses the appropriate feature selection method based on the 'method' parameter. It then splits
    the feature names into categorical, continuous, and combined feature sets. The combined features are used to
    filter the 'outcome_sample' dataframe, returning its subset.

    Parameters:
    - method (str): The feature selection method to be used. The available options are:
      - 'sme': Uses get_all_sme_features()
      - 'avg': Uses getModelAverageFeatures()
      - 'pca': Uses getModelPCAFeatures()
      - 'uni': Uses getmodelUniFeatures()
      - 'lasso': Uses getmodelLassoFeatures()
    - outcome_sample (DataFrame): The dataframe to which the feature selection is applied.

    Returns:
    - tuple: A tuple containing:
      - cat_features (list): The list of categorical features.
      - cont_features (list): The list of continuous features.
      - combined_features (list): The list of combined features.
      - DataFrame: A subset of the 'outcome_sample' dataframe based on combined features.

    Raises:
    - ValueError: If an invalid method is passed as the 'method' parameter.

    Example:
    >>> cat_features, cont_features, combined_features, selected_data = pick_feature_selection_method('pca', outcome_sample)
    >>> print(selected_data.head())

    Note:
    Ensure that the feature selection functions (get_all_sme_features, getModelAverageFeatures, getModelPCAFeatures,
    getmodelUniFeatures, getmodelLassoFeatures) and the split_feature_names function are correctly defined and imported.
    """
    # Choose the appropriate feature selection method
    if method == 'sme':
        cat_features, cont_features, combined_features = split_feature_names(get_all_sme_features())
    elif method == 'avg':
        cat_features, cont_features, combined_features = split_feature_names(getModelAverageFeatures())
    elif method == 'pca':
        cat_features, cont_features, combined_features = split_feature_names(getModelPCAFeatures())
    elif method == 'uni':
        cat_features, cont_features, combined_features = split_feature_names(getmodelUniFeatures())
    elif method == 'lasso':
        cat_features, cont_features, combined_features = split_feature_names(getmodelLassoFeatures())
    else:
        raise ValueError("Invalid method selected")

    # Assuming outcome_sample is a predefined dataframe in your context
    return cat_features, cont_features, combined_features, outcome_sample[combined_features]


def split_feature_names(feature_names):
    """
    Splits feature names into categorical and continuous based on their prefixes.

    Parameters:
    feature_names (list of str): The array of feature names.

    Returns:
    tuple of lists: A tuple containing three lists:
                     - List of categorical feature names (excluding 'cat__Outcome')
                     - List of continuous feature names
                     - Combined list of all feature names including 'cat__Outcome'
    """
    # Splitting the feature names
    categorical_features = [name for name in feature_names if name.startswith('cat__') and name != 'cat__Outcome']
    continuous_features = [name for name in feature_names if name.startswith('num__')]

    # Combined list with the label
    combined_features = categorical_features + continuous_features + ['cat__Outcome']

    return categorical_features, continuous_features, combined_features


def encode_categorical_and_continuous_features(categorical, continuous, X):
    """
    Transforms a dataframe by encoding categorical features and scaling continuous features.

    This function preprocesses the provided dataframe by applying one-hot encoding to categorical features and
    standard scaling to continuous features. It is designed for preparing data for machine learning models that
    require numerical input.

    The function utilizes OneHotEncoder for categorical features and StandardScaler for continuous features,
    encapsulated in a ColumnTransformer for simultaneous processing.

    :param X: The dataframe containing all features.
    :param categorical: A list containing only categorical features
    :param continuous: A list containing only continuous features
    :return: A dataframe containing only categorical features that have been encoded and a dataframe containing only
    continuous features that have been scaled
    """

    # Convert column names in 'categorical' and 'continuous' lists to standard Python strings
    categorical = [str(name) for name in categorical]
    continuous = [str(name) for name in continuous]

    # Then, proceed with your ColumnTransformer setup
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical),
            ('cont', StandardScaler(), continuous)
        ])

    # Now fit and transform the data
    return preprocessor.fit_transform(X)


def get_sample_data(df, balance=True):
    # Remove rows with 'Unknown' outcome
    df = df.drop(df[df['cat__Outcome'] == 'Unknown'].index)

    # Filter rows based on 'Alive' and 'Dead' outcomes
    alive_df = df[df['cat__Outcome'] == 'Alive']
    dead_df = df[df['cat__Outcome'] == 'Dead']

    if balance:
        # Count the number of 'Alive' rows
        num_alive = alive_df.shape[0]

        # Sample from 'Alive' rows
        sample_alive = alive_df.sample(n=num_alive, random_state=42)

        # Determine the number of samples for 'Dead' rows
        num_samples_dead = min(num_alive, dead_df.shape[0])

        # Sample from 'Dead' rows
        sample_dead = dead_df.sample(n=num_samples_dead, random_state=42)

    else:
        # Use all 'Dead' rows
        sample_dead = dead_df

        # Determine the number of 'Alive' rows to use
        num_alive = min(sample_dead.shape[0], alive_df.shape[0])

        # Sample from 'Alive' rows
        sample_alive = alive_df.sample(n=num_alive, random_state=42)

    # Print the counts
    print(f"Number of 'Alive' rows: {num_alive}")
    print(f"Number of 'Dead' rows: {sample_dead.shape[0]}")

    # Concatenate the samples into one DataFrame
    outcome_sample = pd.concat([sample_alive, sample_dead])

    return outcome_sample


def run_selected_models(model_names, X, y, cv):
    """
    This method runs the selected models and returns the results and best hyperparameters for each model.

    :param model_names: The names of the models to run. This is formatted as a list of strings.  Valid values are
        'NB', 'RF', and 'XG'. These stand for Naive Bayes, Random Forest, and XGBoost, respectively.
    :param X: The features as a dataframe
    :param y: The labels as a dataframe
    :param cv: The cross-validation strategy
    :return: A tuple containing the results and best hyperparameters for each model.
    """
    results = {}
    best_hyperparams = {}
    confusion_matrix = {}

    if 'NB' in model_names:
        print(f"Running Naive Bayes model...")
        naive_bayes_results = train_naive_bayes(X, y, cv=cv)
        results['Naive Bayes'], best_hyperparams['Naive Bayes'], confusion_matrix['Naive Bayes'] = naive_bayes_results
        print(f"Naive Bayes model processing complete\n")

    if 'RF' in model_names:
        print(f"Running Random Forest model (this will take a little time)...")
        random_forest_results = train_random_forest(X, y, cv=cv)
        results['Random Forest'], best_hyperparams['Random Forest'], confusion_matrix[
            'Random Forest'] = random_forest_results
        print(f"Random Forest model processing complete\n")

    if 'XG' in model_names:
        print(f"Running XGBoost model...")
        xgboost_results = train_xgboost(X, y, cv=cv)
        results['XGBoost'], best_hyperparams['XGBoost'], confusion_matrix['XGBoost'] = xgboost_results
        print(f"XGBoost model processing complete\n")

    return results, best_hyperparams, confusion_matrix


def plot_confusion_matrix(cm, model_name, fs_type, labels=['Alive', 'Dead'], cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix as a heatmap.

    :param fs_type: This is the type of feature selection used.  It is used in the title of the plot.
    :param labels: Labels for the confusion matrix.
    :param cm: Confusion Matrix to be plotted.
    :param model_name: Name of the model.
    :param cmap: Color map of the heatmap.
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, xticklabels=labels, yticklabels=labels)
    plt.title(f'Confusion Matrix for {model_name}, Feature Selection: {fs_type}')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(f'figs/{model_name}_{fs_type}_confusion_matrix.png')
    plt.show()


def pretty_print_conf_matrix(cm, labels=['Alive', 'Dead']):
    """
    Pretty prints the confusion matrix with correct label order.

    :param cm: Confusion matrix
    :param labels: Labels for the classes
    """
    row_format = "{:>8}" * (len(labels) + 1)
    print(row_format.format("", *labels))
    for label, row in zip(labels, cm):
        print(row_format.format(label, *row))
