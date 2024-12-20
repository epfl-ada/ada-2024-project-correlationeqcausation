import pandas as pd

# Load the data

def create_career_datasets(data_df):

    post_2000_df = data_df.loc[data_df['year'] > 2000]

    # Split data into data for actors who have been nominated for an Oscar before and after the nomination.
    first_oscar_nomination_year_df = post_2000_df.loc[post_2000_df['oscar_nominated'] == 1].groupby('actor_identifier').agg(
        year_of_first_oscar_nomination=('year', 'min')).reset_index()
    temp_df = post_2000_df.merge(first_oscar_nomination_year_df, on='actor_identifier')

    pre_first_oscar_nominated_df = temp_df.loc[temp_df['year'] < temp_df['year_of_first_oscar_nomination']]

    first_oscar_nomination_df = temp_df.loc[temp_df['year'] == temp_df['year_of_first_oscar_nomination']]

    post_first_oscar_nominated_df = temp_df.loc[temp_df['year'] > temp_df['year_of_first_oscar_nomination']]

    # Select the last movie for actors who have not been nominated for an Oscar
    non_nominated_df = post_2000_df.loc[post_2000_df['oscar_nominated'] == 0]
    temp_df = non_nominated_df.groupby('actor_identifier').agg(
        max_number_of_movies_starred_in=('number_of_movies_starred_in', 'max')).reset_index()
    non_nominated_df = non_nominated_df.merge(temp_df, on='actor_identifier')
    non_nominated_df = non_nominated_df.loc[non_nominated_df['number_of_movies_starred_in'] == non_nominated_df['max_number_of_movies_starred_in']]

    # Select the last movie for actors who have been nominated for an Oscar
    nominated_df = post_2000_df.loc[post_2000_df['oscar_nominated'] == 1]
    temp_df = nominated_df.groupby('actor_identifier').agg(
        max_number_of_movies_starred_in=('number_of_movies_starred_in', 'max')).reset_index()
    nominated_df = nominated_df.merge(temp_df, on='actor_identifier')
    nominated_df = nominated_df.loc[nominated_df['number_of_movies_starred_in'] == nominated_df['max_number_of_movies_starred_in']]

    return pre_first_oscar_nominated_df, first_oscar_nomination_df, post_first_oscar_nominated_df, non_nominated_df, nominated_df


