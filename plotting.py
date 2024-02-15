from bokeh.plotting import figure, output_file, show
from bokeh.models import Band, ColumnDataSource, HoverTool
from bokeh.layouts import column, gridplot
import pandas as pd
"""
Plotter class for visualizing ideal functions, training data, and test points.

Uses Bokeh to generate interactive visualizations.
"""
class Plotter:
    """
   Initializes the Plotter with training, ideal, and test datasets.

   Args:
       train_set (pd.DataFrame): DataFrame containing training data.
       ideal_set (pd.DataFrame): DataFrame containing ideal functions.
       test_set (pd.DataFrame): DataFrame containing test points with mapped ideal functions.
   """
    def __init__(self, train_set, ideal_set, test_set):
        self.train_set = train_set
        self.ideal_set = ideal_set
        self.test_set = test_set

    """
    Generates plots of individual ideal functions.

    Creates line plots for the first 50 ideal functions and scatter plots for pairs of ideal functions.
    """
    def plot_ideal_functions(self):
        line_plots = [self.create_line_plot_ideal(i) for i in range(min(50, len(self.ideal_set.columns)))]
        scatter_plots = [self.create_scatter_plot_ideal(i, j) for i in range(1, min(50, len(self.ideal_set.columns))) for j in range(i + 1, min(50, len(self.ideal_set.columns)))]

        # Arrange the plots in a grid
        grid = gridplot(line_plots + scatter_plots, ncols=2, plot_width=400, plot_height=400)

        output_file("output/ideal_functions.html")
        show(grid)
        """
    Generates plots of training data overlaid with corresponding ideal functions.

    Creates line plots for the first 5 training data columns and their corresponding ideal functions.
    """

    def create_line_plot_ideal(self, index):
        if index >= len(self.ideal_set.columns):
            # Handle the case where the index is out of bounds
            print(f"Index {index} is out of bounds for the number of columns in ideal_set.")
            return None

        x_value = self.ideal_set['x']
        ideal_data = self.ideal_set.iloc[:, index]
        ideal_name = self.ideal_set.columns[index]

        plot = figure(title=f"Ideal Function {ideal_name} vs x", x_axis_label='x', y_axis_label='y',
                      tools="pan,box_zoom,reset,save", sizing_mode="stretch_width", plot_height=300)

        plot.line(x_value, ideal_data, legend_label=f"Ideal {ideal_name}", line_width=2, line_color='blue')

        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"

        return plot

    def create_scatter_plot_ideal(self, index1, index2):
        if index1 >= len(self.ideal_set.columns) or index2 >= len(self.ideal_set.columns):
            # Handle the case where the indices are out of bounds
            print(f"Indices {index1}, {index2} are out of bounds for the number of columns in ideal_set.")
            return None

        ideal_data_x = self.ideal_set.iloc[:, index1]
        ideal_data_y = self.ideal_set.iloc[:, index2]
        ideal_name_x = self.ideal_set.columns[index1]
        ideal_name_y = self.ideal_set.columns[index2]

        plot = figure(title=f"Ideal Function {ideal_name_x} vs {ideal_name_y}", x_axis_label=f"Ideal {ideal_name_x}",
                      y_axis_label=f"Ideal {ideal_name_y}", tools="pan,box_zoom,reset,save",
                      sizing_mode="stretch_width", plot_height=300)

        plot.scatter(ideal_data_x, ideal_data_y, fill_color="blue", size=6, marker='circle', line_color='black', alpha=0.7)

        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"

        return plot

    def plot_training_data_and_ideal(self):
        line_plots = [self.create_line_plot_training_and_ideal(i) for i in range(1, min(5, len(self.train_set.columns)))]

        # Arrange the plots in a grid
        grid = gridplot(line_plots, ncols=2, plot_width=400, plot_height=400)

        output_file("output/training_data_and_ideal.html")
        show(grid)

    def create_line_plot_training_and_ideal(self, index):
        if index >= len(self.train_set.columns):
            # Handle the case where the index is out of bounds
            print(f"Index {index} is out of bounds for the number of columns in train_set.")
            return None

        x_value = self.train_set['x']
        train_data = self.train_set.iloc[:, index]
        ideal_data = self.ideal_set.iloc[:, index]
        train_name = self.train_set.columns[index]

        plot = figure(title=f"Train {train_name} vs x with Ideal", x_axis_label='x', y_axis_label='y',
                      tools="pan,box_zoom,reset,save", sizing_mode="stretch_width", plot_height=300)

        # Plot training data
        plot.line(x_value, train_data, legend_label=f"Train {train_name}", line_width=2, line_color='red')

        # Plot corresponding ideal function
        plot.line(x_value, ideal_data, legend_label=f"Ideal {train_name}", line_width=2, line_color='blue', line_alpha=0.7)

        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"

        return plot

    def plot_test_points_and_ideal(self):
        scatter_plots = [self.create_scatter_plot_test_and_ideal(i) for i in self.test_set.itertuples(index=True, name='Pandas') if i.ideal_function]

        # Arrange the plots in a grid
        grid = gridplot(scatter_plots, ncols=2, plot_width=400, plot_height=400)

        output_file("output/test_points_and_ideal.html")
        show(grid)

    def create_scatter_plot_test_and_ideal(self, point):
        ideal_name = point.ideal_function

        plot = figure(title=f"Test Point: ({point.x},{round(point.y, 2)}) with Ideal {ideal_name}", x_axis_label='x',
                      y_axis_label='y', tools="pan,box_zoom,reset,save", sizing_mode="stretch_width", plot_height=300)

        # Plot corresponding ideal function
        plot.line(self.ideal_set.x, self.ideal_set[ideal_name], legend_label=f"Ideal {ideal_name}", line_width=2,
                  line_color='blue', line_alpha=0.7)

        # Highlight the test point
        plot.scatter([point.x], [round(point.y, 4)], fill_color="red", legend_label="Test points", size=8, marker='square')

        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"
        return plot

