import pandas as pd
import numpy as np
import ast
import argparse
import data_load.Data_Clean as dc
import feature_selection.Lasso_methods as Lasso
import feature_selection.Univariate_methods as Uni
import feature_selection.PCA_methods as PCR
import feature_selection.process_selected_features as process
from sklearn.model_selection import train_test_split


def run_feature_selection(algorithms, use_subset_of_date, use_balanced_subset_of_data, use_half_data):
    run_lasso = False
    run_univariate = False
    run_pca = False
    print(use_balanced_subset_of_data)

    algorithms = [ag.strip("'\"") for ag in algorithms]
    print(algorithms)


    if "lasso" in algorithms:
        print("Lasso included")
        run_lasso = True
    if "pca" in algorithms:
        print("PCA included")
        run_pca = True
    if "uni" in algorithms:
        print("Univariate included")
        run_univariate = True

    # Loads cleaned data, assumes a file named cleaned_data.csv exists in data folder
    print("Initialing feature selection script")
    df = pd.read_csv('data/cleaned_Data.csv', index_col=False, low_memory=False)
    print(df.shape)

    print('Outcome variable value counts in cleaned data')
    print(df['cat__Outcome'].value_counts())
    print('Finished loaded cleaned dataset')


    #Format data for feature selection
    print('formating data into X and y, scaling, and encoding categorical variables')

    # Drop all rows of dataframe without an Outcome variable
    df = df[df['cat__Outcome'] != 'Unknown']

    if use_balanced_subset_of_data == True:
        print('balancing dataset based on outcome variable')

        # Filtering the rows where 'cat__Outcome' is 'Alive' or 'Dead'
        alive_df = df[df['cat__Outcome'] == 'Alive']
        dead_df = df[df['cat__Outcome'] == 'Dead']

        # Random sampling 53,000 rows from each of these dataframes.  That's just about the total number of "Alive" rows.
        sample_alive = alive_df.sample(n=53000, random_state=42)
        sample_dead = dead_df.sample(n=53000, random_state=42)

        # Concatenating the samples into one dataframe
        df = pd.concat([sample_alive, sample_dead])
    
    else:
        print("Using unlanaced data")

    if use_half_data == True:
        # Split the DataFrame based on the 'Outcome' column
        train_df, test_df = train_test_split(df, test_size=0.5, random_state=42, stratify=df['cat__Outcome'])
        train_df.to_csv('data/half_data_feature_selection.csv', index=False)
        test_df.to_csv('data/half_data_models.csv', index=False)
        df = train_df
        print(df.shape)

    # Extracts X from df and drops certain columns (PCR key and columns used to make Outcome variable)
    # These variables are excluded tue to being part of the outcome deinition or the key of the datatset
    print('Dropping excluded columns from X')
    X = df.drop(columns=['cat__Outcome', 'cat__PcrKey', 'cat__eOutcome_01', 'cat__eArrest_18'])

    # These variables are dropped because we judgementally assessed them to be too closely correlated with the outcome to have predictive value 
    # (i.e. they explicitly indiciate the patient is deas/alive, meaning they cant be used to predict dead/alive)
    X = X.drop(columns=['cat__eArrest_16', 'cat__eDisposition_12', 'cat__eSituation_13', 'cat__eDisposition_19', 'cat__eDisposition_23', 'cat__eDispatch_01', 'cat__eDisposition_22', 'cat__eDisposition_21'])

    # Extracts y from df, converts it to a binary where Alive = 1, Dead = 0
    y = df['cat__Outcome'].map({'Alive': 1, 'Dead': 0})

    # Uses OneHotEncoder to format categorical variables
    print("Encoding categorical variables and scaling numeric variables")
    X = dc.oneHotEncodeCat(X)
    X = dc.scaleNum(X)

    # selects a sample of the data to use if use_subset_of_date is true
    if use_subset_of_date == True:
        # Samples certain rows of the data to make run faster
        num_rows_to_select = 1000

        # Select random rows from the DataFrame
        X = X.sample(n=num_rows_to_select, random_state=42)
        X.drop(columns= X.columns[X.nunique() == 1], inplace=True)

        # Select corresponding rows from the array
        y = y.sample(n=num_rows_to_select, random_state=42)


    # feature names
    features = X.columns

    print('Shape of X:', X.shape)
    print('Preprocessing and data formatting finished')

    # Creates a folder name doutput to put the results of the feature selection
    dc.create_output_folder('output')

    # Run Feature Selection pipelines based on which parameters are selected at the top of the file

    # Runs univariate feature selection if run_univariate = true
    if run_univariate == True:

        print('Running univariate selection  with F stat scoring')
        f = Uni.univariateSelectF(X, y, 15, features)
        Uni.saveResults(f, 'F-Score','output/feature_select_uni_f.txt')
        print('Univariate analysis with F Statistic finished')

        print('Running univariate selection with mutual information scoring')
        MI = Uni.univariateSelectMI(X, y, 15, features)
        Uni.saveResults(MI, 'MutualInfo','output/feature_select_uni_MI.txt')
        print('Univariate analysis with Mutual Information finished')

        # Print results
        uni_file_path_f = 'output/feature_select_uni_f.txt'
        uni_file_path_MI = 'output/feature_select_uni_MI.txt'
        process.getUniFFeatures(uni_file_path_f, True)
        process.getUniMIFeatures(uni_file_path_MI, True)


    # Runs PCA feature selection if run_pca = true
    if run_pca == True:
        print('Running PCA feature selection')
        n_components = np.arange(1, 100)
        logisticPCA = PCR.PCALogisticAllRanks(X,y,n_components, features, 'output/feature_select_PCA.txt')

        # Print results
        pca_file_path = 'output/feature_select_PCA.txt'
        process.getPCAFeatures(pca_file_path, True)

        print('PCA finished')

    # Runs Lasso feature selection if run_lasso = true
    if run_lasso == True:

        logisticWeights = np.arange(.0065, .0085, .0001)
        #logisticWeights = [.0005, .001, .0015, .002]

        print('Running lasso with logistic underlying model')
        log = Lasso.lassoLogisticAllWeights(X, y, logisticWeights, features, 'output/feature_select_lasso_log.txt')
        print("Logistic lasso finished")

        # Print results
        lasso_log_filepath = 'output/feature_select_lasso_log.txt'
        process.getLassoLogFeatures(lasso_log_filepath, True)

        print('Lasso analysis finished')


    print("Feature selection script finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run feature selection script with specified parameters.')
    #parser.add_argument('--balance', type=bool, default=False, help='Balance the data or not')
    parser.add_argument('--balance', type=ast.literal_eval, default=True, help='Balance the data or not')
    parser.add_argument('--feature_selection',  nargs='+', default="uni pca lasso", help='Methods of feature selection to run')

    args = parser.parse_args()

    # Other parameters: 
    # Use_subset_of_data: if true, runs script only on num_rows_to_select sampled datapoints
    # use_balanced_subset_of_data: if true, selects 53l of both alive and dead rows, to have a balanced dataset
    # use_half_data: if true, saves half the data for testing with the models and only uses half for feature selection (no cheating)
    # use_subset_of_date = False
    # use_balanced_subset_of_data = True
    # use_half_data = True
    print(args.balance)
    run_feature_selection(args.feature_selection, False, args.balance, True)