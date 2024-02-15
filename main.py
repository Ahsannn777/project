"""
Main script for processing ideal, training, and test data,
mapping test points to best-fit ideal functions,
generating visualizations, and storing results in an SQL database.
"""
import numpy as np
from sqlalchemy import create_engine
from plotting import Plotter
from classes import SQLDataset, IdealFunctionFinder

IdealData = "ideal.csv"
trainlData = "train.csv"
testlData = "test.csv"

# Create instances of SQLDataset for ideal, train, and test datasets
ideal_dataset = SQLDataset(csv_path=IdealData, title="ideal")
train_dataset = SQLDataset(csv_path=trainlData, title="train")
test_dataset = SQLDataset(csv_path=testlData, title="test")

# Create SQLite engine
engine = create_engine('sqlite:///ahsan.db')


# Create IdealFunctionFinder
ideal_functions_finder = IdealFunctionFinder(train_dataset.csv_data, ideal_dataset.csv_data)
ideal_function_mapper = ideal_functions_finder.find_best_fit_ideal_functions()

# Get best-fit ideal functions
best_fit_ideal_functions = ideal_function_mapper.best_fit_ideal_functions

# Add columns to test data for ideal function and deviation
test_dataset.add_columns('ideal_function', 'deviation')
test_data = test_dataset.csv_data

# Map test points to ideal functions and calculate deviations
for i, point in test_data.iterrows():
    ideal_function, y_delta = ideal_function_mapper.map_test_point([point['x'], point['y']])
    test_data.loc[i, 'ideal_function'] = ideal_function
    test_data.loc[i, 'deviation'] = y_delta

# Store test data with mappings in SQL table
test_data.to_sql('test_data', con=engine, if_exists='replace', index=False)
ideal_dataset.csv_data.to_sql('ideal', con=engine, if_exists='replace', index=False)
train_dataset.csv_data.to_sql('train', con=engine, if_exists='replace', index=False)

plotter = Plotter(train_dataset.csv_data, best_fit_ideal_functions, test_data)
plotter.plot_ideal_functions()
plotter.plot_training_data_and_ideal()
plotter.plot_test_points_and_ideal()


