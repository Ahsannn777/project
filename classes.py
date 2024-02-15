import pandas as pd
from sqlalchemy import create_engine
import numpy as np

class SQLDataset:
    """
   Represents a dataset loaded from a CSV file and provides methods for interacting with it.
   Attributes:
       csv_data (pandas.DataFrame): The DataFrame containing the dataset's data.
       title (str): The title to be appended to column names when creating an SQL table.
   Methods:
       to_sql(table_name, if_exists_table="replace", index=True):
           Exports the dataset to an SQL table.
       add_columns(*column_names):
           Adds new columns to the dataset's DataFrame.
   """
    def __init__(self, csv_path, title):
        try:
            self.csv_data = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(f"Issue while reading file {csv_path}")
            raise

        self.title = title

    def to_sql(self, table_name, if_exists_table="replace", index=True):
        db_engine = create_engine(f'sqlite:///{table_name}.db', echo=False)
        csv_data = self.csv_data.copy()
        csv_data.columns = [name.capitalize() + self.title for name in csv_data.columns]
        csv_data.set_index(csv_data.columns[0], inplace=True)
        csv_data.to_sql(table_name, db_engine, if_exists=if_exists_table, index=index)
        db_engine.dispose()  # Close the database connection

    def add_columns(self, *column_names):
        for column_name in column_names:
            self.csv_data[column_name] = ''


class ParentFunction:
    """
   Abstract base class representing a function with ideal values.

   Attributes:
       ideal (pandas.Series or numpy.ndarray): The ideal values of the function.
       name (str): The name of the function.
   """
    def __init__(self, ideal, name):
        self._name = name
        self.ideal = ideal


class IdealFunction(ParentFunction):
    """
   Represents an ideal function with corresponding training data.

   Attributes:
       train_function (pandas.Series or numpy.ndarray): The training data for the function.
   """
    def __init__(self, ideal, train, name):
        self.train_function = train
        super().__init__(ideal, name)

    def calculate_largest_deviation(self):
        """
       Calculates the largest deviation between the ideal and training values.

       Returns:
           float: The largest deviation.
       """
        deviation = self.train_function - self.ideal
        return max(deviation.abs())


class IdealFunctionMapper:
    """
  Maps test points to ideal functions based on their best fit.

  Attributes:
      train_data (pandas.DataFrame): The training data used for best fit calculation.
      best_fit_ideal_functions (pandas.DataFrame): The DataFrame containing the best-fit ideal functions.

  Methods:
      map_test_point(test_point):
          Maps a test point to its best-fit ideal function and returns the mapped function's name and deviation.
  """
    def __init__(self, train_data, best_fit_ideal_functions):
        self.train_data = train_data
        self.best_fit_ideal_functions = best_fit_ideal_functions

    def map_test_point(self, test_point):
        no_of_ideal = None
        delta = 0

        for i, ideal_set in enumerate(self.best_fit_ideal_functions.columns[1:5]):
            try:
                deviation = IdealFunction(self.best_fit_ideal_functions[ideal_set], self.train_data.iloc[:, i + 1], ideal_set)
                largest_deviation = deviation.calculate_largest_deviation()
                y_location = locate_y(test_point[0], self.best_fit_ideal_functions['x'], self.best_fit_ideal_functions[ideal_set])
            except IndexError:
                print("Index Error")
                raise IndexError

            deviation = abs(y_location - test_point[1])

            if abs(deviation < largest_deviation * np.sqrt(2)):
                if (no_of_ideal is None) or (deviation < delta):
                    no_of_ideal = ideal_set
                    delta = deviation

        return no_of_ideal, delta


def locate_y(x, ideal_x, ideal_y):
    """
  Locates the y-value on an ideal function corresponding to a given x-value.

  Raises:
      IndexError: If the x-value is not found in the ideal function's x-values.
  """
    try:
        match = ideal_y[ideal_x == x]
        if not match.empty:
            return match.iloc[0]
        else:
            raise IndexError
    except IndexError:
        raise IndexError


class IdealFunctionFinder:
    """
   Finds the best-fit ideal functions for a given training dataset.

   Attributes:
       train_data (pandas.DataFrame): The training dataset.
       ideal_set (pandas.DataFrame): The set of ideal functions to compare against.

   Methods:
       find_best_fit_ideal_functions():
           Finds the best-fit ideal functions for each column in the training dataset.
   """
    def __init__(self, train_data, ideal_set):
        self.train_data = train_data
        self.ideal_set = ideal_set

    def find_best_fit_ideal_functions(self):
        chosen_functions = {}
        for train in self.train_data.columns:
            if train != 'x':
                trains = []
                for ideal in self.ideal_set.columns:
                    if ideal != 'x':
                        deviation = ((self.ideal_set[ideal] - self.train_data[train]) ** 2).sum().sum()
                        trains.append(deviation)

                chosen_functions[train] = trains.index(min(trains)) + 1

        chosen_functions['x'] = 0
        best_fit = self.ideal_set.iloc[:, list(chosen_functions.values())]

        return IdealFunctionMapper(self.train_data, best_fit)
