import pandas as pd
import csv

dicts1 = []
dicts2 = []

# Reading data from wp_posts.csv
with open('wp_posts.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dict_row = dict(row)
        dicts1.append(dict_row)

# Reading data from revision_table.csv
with open('revision_table.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dict_row = dict(row)
        dicts2.append(dict_row)

df1 = pd.DataFrame(dicts1)
df2 = pd.DataFrame(dicts2)

def merge_posts(df1, df2):
    # Merging data from df2 into df1 based on conditions
    for index, row in df1.iterrows():
        post_id = row['ID']
        post_content = row['post_content']
        inherits = []
        for _, rw in df2.iterrows():
            if rw['post_parent'] == post_id and rw['post_type'] == 'revision':
                post_content += (rw['post_content'] + '\n /// \n')
                inherits.append(rw)  # Appending the entire row of df2 for reference
        row['post_content'] = post_content
        row['post_inherits'] = inherits

    # Dropping rows based on conditions
    indices_to_drop = df1[(df1['post_status'].isin(['draft', 'auto_draft'])) | (df1['post_content'] == '')].index
    df1.drop(indices_to_drop, inplace=True)
    df1.reset_index(drop=True, inplace=True)
    return df1

output = merge_posts(df1, df2)  # Pass both DataFrames to the function
output.to_csv('output.csv', index=False)
