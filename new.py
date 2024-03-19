import pandas as pd

def merge_posts(df):
    # Grouping posts by their parent IDs
    grouped = df.groupby('post_parent')

    # Merging post content for each parent post
    def merge_content(x):
        content = ' '.join(x.dropna().astype(str))
        return content if content else None

    merged_content = grouped['post_content'].apply(merge_content).reset_index()

    # Merging with the original DataFrame to update post content
    df = df.merge(merged_content, how='left', left_on='ID', right_on='post_parent', suffixes=('', '_merged'))
    df['post_content'] = df.apply(lambda row: row['post_content_merged'] if pd.notnull(row['post_content_merged']) else row['post_content'], axis=1)

    # Dropping unnecessary columns
    columns_to_drop = ["post_author", "post_modified", "pinged", "to_ping", "post_password", "comment_status",
                       "ping_status", "post_excerpt", "post_modified_gmt", "post_content_filtered",
                       "guid", "menu_order", "post_type", "post_mime_type", "comment_count", "post_parent", "post_content_merged"]
    df.drop(columns=columns_to_drop, inplace=True)

    # Dropping rows with certain conditions
    df = df[(df['post_status'] != 'draft') & (df['post_status'] != 'auto_draft') & (df['post_content'] != '')]

    # Resetting index
    df.reset_index(drop=True, inplace=True)
    return df

# Reading data from CSV
df = pd.read_csv('wp_posts.csv', encoding='utf-8')

# Merging posts
output = merge_posts(df)

# Writing to CSV
output.to_csv('output.csv', index=False)
