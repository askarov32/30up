import pandas as pd
import csv

dicts = []
with open('revision_table.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dict_row = dict(row)
        dicts2.append(dict_row)
def addRevision(df1, df2):
    for index, row in df.iterrows():
        post_id = row
        






