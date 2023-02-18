from operator import index
from xml.dom import INDEX_SIZE_ERR
import pandas as pd
import numpy as np
from tabulate import tabulate
import os
import meetingTimer

class Data:
    def __init__(self):
        self.df = pd.DataFrame([], columns = ['Task', 'Description', 'Durations (in seconds)'])

    """Display Pandas Dataframe beatifully with tabulate module: https://pypi.org/project/tabulate/"""
    def display_table(self):
        table_headers = ['Task', 'Description', 'Durations (in seconds)']
        print(tabulate(self.df, headers=table_headers, tablefmt='fancy_grid', showindex=False))

    """Add new task to dataset"""
    def add_task(self, title, description, duration):
        self.df = self.df.append({'Task': title, 'Description': description, 'Durations (in seconds)': duration}, ignore_index=True)
    
    """Update task in dataset"""
    def update_task(self, index, title, description, duration):
        self.df.loc[index, 'Task'] = title
        self.df.loc[index, 'Description'] = description
        self.df.loc[index, 'Durations (in seconds)'] = duration

    """Removes all tasks from dataset"""
    def delete_data(self):
        self.df = pd.DataFrame([], columns = ['Task', 'Description', 'Durations (in seconds)'])

    """Export to csv file"""
    def export_data(self, dir_name):
        if dir_name[-1] != '/': dir_name += '/'
        if(os.path.isdir(dir_name)):
            self.df.to_csv(dir_name + 'config.csv', index=False, encoding='utf-8')
        else:
            print('Directory doesnt exist')

    """Import a CSV file, check if it has correct CSV form, then parse it to the DataFrame"""
    def import_data(self, filename):
        if(os.path.exists(filename)): 
            if os.path.splitext(filename)[1] == '.csv':
                data_frame = pd.read_csv(filename, index_col=False)
                tasks = []
                cols = []
                for row in data_frame:
                    cols.append(row)
                if cols == ['Task', 'Description', 'Durations (in seconds)']:
                    if not data_frame.isnull().values.any():
                        #Check if all values in duration column is integer and positive value
                        if data_frame['Durations (in seconds)'].dtype == np.dtype('int64') and not (data_frame['Durations (in seconds)'] < 0).values.any():
                            self.df = data_frame
                            for id, row in data_frame.iterrows():
                                tasks.append(meetingTimer.Task( row['Task'], row['Description'], row['Durations (in seconds)']))
                            return tasks

                        else:
                            print("All of duration values must be positive integer values")
                    else: 
                        print("There must be not be any null value in the table")
                else: 
                    print("Wrong column's name")
            else: 
                print("Not a csv file")
        else: 
            print("File doesn't exist")