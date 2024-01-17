import argparse

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

from utility_methods import (run_selected_models, encode_categorical_and_continuous_features, plot_confusion_matrix,
                             pretty_print_conf_matrix, get_sample_data,
                             pick_feature_selection_method, load_data)


def run_analysis(filename='', balance=True, feature_selection='sme', model_types=['NB']):
    # Strip quotes from filename and feature_selection if present
    filename = filename.strip("'\"")
    feature_selection = feature_selection.strip("'\"")

    # Process model_types to remove any extra quotes
    model_types = [mt.strip("'\"") for mt in model_types]

    # Load data
    df = load_data(filename if filename else "cleaned_Data.csv")

    print("Dropping unknown outcomes and gathering 'Alive' and 'Dead' dataset...")
    outcome_sample = get_sample_data(df, balance=balance)
    print("Processing complete\n")

    print("Pick feature selection type...")
    cat_features, cont_features, combined_features, outcome_sample_subset = pick_feature_selection_method(
        feature_selection, outcome_sample)
    print("Features selected\n")

    print(f"Shape of dataframe going to model processing: {outcome_sample_subset.shape}")

    # Separate features and label
    X = outcome_sample_subset.drop('cat__Outcome', axis=1)
    y = outcome_sample_subset['cat__Outcome']

    # Encode categorical and continuous features
    X = encode_categorical_and_continuous_features(cat_features, cont_features, X)

    # Encode labels
    y = LabelEncoder().fit_transform(y)

    # Define cross-validation strategy
    cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Run the selected models
    results, best_hyperparams, conf_matrix = run_selected_models(model_types, X, y, cv_strategy)

    # Print the results and the best hyperparameters for each model
    for model, performance in results.items():
        print(f"Model: {model}")
        for metric, scores in performance.items():
            print(f"  {metric.capitalize()}: Mean={np.mean(scores):.3f}, Std={np.std(scores):.6f}")
        print(f"Best hyperparameters: {best_hyperparams[model]}")
        print("\n")

        print("Confusion Matrix:")
        pretty_print_conf_matrix(conf_matrix[model], labels=['Alive', 'Dead'])
        print("\n")

        # Plot a heat map of the confusion matrix
        plot_confusion_matrix(conf_matrix[model], model, feature_selection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run models with specified parameters.')
    parser.add_argument('filename', nargs='?', default='', help='Filename of the CSV file')
    parser.add_argument('--balance', type=bool, default=True, help='Balance the data or not')
    parser.add_argument('--feature_selection', default='sme', help='Method of feature selection')
    parser.add_argument('--model_types', nargs='+', default=['NB'], help="List of model types to run")

    args = parser.parse_args()

    run_analysis(args.filename, args.balance, args.feature_selection, args.model_types)
