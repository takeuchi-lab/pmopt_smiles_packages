import pandas as pd
from sklearn.model_selection import KFold
import os
import argparse

def split_and_save_csv(file_name, n_splits, output_path):
    # import csv file
    data = pd.read_csv(file_name)
    
    # Separate explanatory and objective variables
    X = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    
    # setting KFold
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # setting output path
    output_dir = output_path
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Split and Save
    for fold, (train_index, test_index) in enumerate(kf.split(X), 1):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        # Create DataFrame for training and test data
        train_data = pd.concat([y_train, X_train], axis=1)
        test_data = pd.concat([y_test, X_test], axis=1)
        
        # generate filename
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        train_file_name = os.path.join(output_dir, f"{base_name}_{fold}_train.csv")
        test_file_name = os.path.join(output_dir, f"{base_name}_{fold}_test.csv")
        
        # save as csv
        train_data.to_csv(train_file_name, index=False)
        test_data.to_csv(test_file_name, index=False)
        print(f"Fold {fold}:")
        print(f"  Train data saved to {train_file_name}")
        print(f"  Test data saved to {test_file_name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split and save CSV file to K-Fold')
    parser.add_argument('file_name', type=str, help='CSV file name')
    parser.add_argument('n_splits', type=int, help='k-fold')
    parser.add_argument('output_path', type=str, help='output path')

    args = parser.parse_args()
    
    split_and_save_csv(args.file_name, args.n_splits, args.output_path)
