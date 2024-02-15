import unittest
import pandas as pd
from classes import SQLDataset, IdealFunction, IdealFunctionMapper, IdealFunctionFinder, locate_y

class TestSQLDataset(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        test_data = {'x': [17.5, 0.3, -8.7], 'y': [34.16104, 1.2151024, -16.843908]}
        self.df_test = pd.DataFrame(test_data)
        train_data = {'x': [-20.0, -19.9, -19.8, -19.7], 'y1': [39.778572, 39.604813, 40.09907, 40.1511],
                      'y2': [-40.07859, -39.784, -40.018845, -39.518402], 'y3': [-20.214268, -20.07095, -19.906782, -19.389118],
                      'y4': [-0.32491425, -0.058819864, -0.4518296, -0.6120442]}
        self.df_train = pd.DataFrame(train_data)
        ideal_data = {'x': [-20.0], 'y1': [-0.9129453], 'y2': [0.40808207], 'y3': [9.087055], 'y4': [5.408082],
                      'y5': [-9.087055], 'y6': [0.9129453], 'y7': [-0.8390715], 'y8': [-0.85091937], 'y9': [0.81616414],
                      'y10': [18.258905], 'y11': [-20.0], 'y12': [-58.0], 'y13': [-45.0], 'y14': [20.0], 'y15': [13.0],
                      'y16': [400.0], 'y17': [-400.0], 'y18': [800.0], 'y19': [410.0], 'y20': [289.0], 'y21': [-8000.0],
                      'y22': [8000.0], 'y23': [8000.0], 'y24': [-16000.0], 'y25': [-23995.0], 'y26': [-5832.0],
                      'y27': [10648.0], 'y28': [-8020.0], 'y29': [-7600.0], 'y30': [-8795.0], 'y31': [20.0],
                      'y32': [4.472136], 'y33': [20.12461], 'y34': [-0.7464143], 'y35': [10.0], 'y36': [100.0],
                      'y37': [-20.0], 'y38': [-1.3210273], 'y39': [399.08707], 'y40': [899.5919], 'y41': [-40.456474],
                      'y42': [40.20404], 'y43': [2.9957323], 'y44': [-0.008333334], 'y45': [12.995732], 'y46': [5.2983174],
                      'y47': [-5.2983174], 'y48': [-0.18627828], 'y49': [0.9129453], 'y50': [0.3968496]}
        self.df_ideal = pd.DataFrame(ideal_data)

        self.sql_dataset_test = SQLDataset(csv_path='test.csv', title='test')
        self.sql_dataset_train = SQLDataset(csv_path='train.csv', title='train')
        self.sql_dataset_ideal = SQLDataset(csv_path='ideal.csv', title='ideal')

        self.sql_dataset_test.csv_data = self.df_test
        self.sql_dataset_train.csv_data = self.df_train
        self.sql_dataset_ideal.csv_data = self.df_ideal

    def test_add_columns(self):
        # Test if columns are added correctly
        self.sql_dataset_test.add_columns('new_column')
        self.assertIn('new_column', self.sql_dataset_test.csv_data.columns)

    def test_to_sql(self):
        # Test if the DataFrames are exported to SQL correctly
        table_name_test = 'test_table_test'
        table_name_train = 'test_table_train'
        table_name_ideal = 'test_table_ideal'
        self.sql_dataset_test.to_sql(table_name=table_name_test, if_exists_table='replace', index=False)
        self.sql_dataset_train.to_sql(table_name=table_name_train, if_exists_table='replace', index=False)
        self.sql_dataset_ideal.to_sql(table_name=table_name_ideal, if_exists_table='replace', index=False)
        # Assuming you have a database connection, you can query the tables and check if they exist
        # Assert statements for checking database content can be added here

# Add similar tests for other classes (IdealFunction, IdealFunctionMapper, IdealFunctionFinder) using the provided data.

if __name__ == '__main__':
    unittest.main()
