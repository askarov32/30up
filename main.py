import pandas as pd
import csv

dicts = []
with open('wp_posts.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dict_row = dict(row)
        dicts.append(dict_row)

df = pd.DataFrame(dicts)


def merge_posts(dff):
    indices_to_drop = []
    for index, row in dff.iterrows():
        post_id = row['ID']
        inherits = []
        for i, r in dff.iterrows():
            if r['post_parent'] == post_id:
                row['post_content'] += (r['post_content'] + ' NEW POST ')
                indices_to_drop.append(i)
                inherits.append(i)
        row['post_inherits'] = inherits

    for index, row in dff.iterrows():
        if row['post_status'] == 'draft' or row['post_status'] == 'auto_draft':
            indices_to_drop.append(index)
        if row['post_content'] == '':
            indices_to_drop.append(index)
    dff.drop(indices_to_drop, inplace=True)
    dff.reset_index(drop=True, inplace=True)
    return dff


output = merge_posts(df)
output.to_csv('output.csv', index=False)
