from json import loads
import pandas as pd

def get_nationality_dfs(movie_df):
    country_df = movie_df.copy()
    # Convert the strings in movie_df (currently on the format ['A', 'B']) to lists with json.loads. Json.loads requires double quotation marks, so we first replace to fix this.
    #country_df['countries'] = movie_df['countries'].apply(lambda row: row.replace("'", '"')).apply(loads)
    print(f"Number of rows, including those with multiple nationalities: {len(country_df)}")

    # The column 'countries' contains a list of countries for each row. We explode the df on this list, so that we get a single row for each actor/country pair
    # If a movie is from multiple countries, we will count the Oscar nominations for all those countries.
    exploded_df = country_df.explode(column='countries').rename(columns={'countries':'country'}).reset_index()

    # All rows with Oscar nominations
    nominated_df = exploded_df[exploded_df['oscar_nominated'] == True]

    return nominated_df, exploded_df


def get_adjusted_nominations(exploded_df, nominated_df):
    # Look at the nominations when we adjust for the number of movies from each country in our dataset
    countries_total_movies = {'country': [], 'value':[]}

    # For every country in our dataset
    for country in exploded_df['country'].unique():

        # If the country has any nominations
        if country in nominated_df['country'].unique():

            # We add the country and its nomination count to the dictionary
            value = exploded_df[exploded_df['country'] == country]['title'].count()
            countries_total_movies['country'].append(country)
            countries_total_movies['value'].append(value)

    # Create a dataframe from the dictionary
    countries_total_movies_df = pd.DataFrame(countries_total_movies)
    # Sort the dataframes, get the nominated movies on a usable format for adjustment
    countries_total_movies_df = countries_total_movies_df.sort_values(by='country')
    countries_nominated_movies = nominated_df.sort_values(by='country').groupby('country').count()['index']
    # Adjust the nomination numbers
    countries_nominated_movies_adjusted = countries_nominated_movies / list(countries_total_movies_df['value'])
    return countries_nominated_movies_adjusted