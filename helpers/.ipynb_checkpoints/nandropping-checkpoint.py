import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

from scipy import stats

def display_cleaning_shift_plot(clean_df, unclean_df, column, display_values = None, display_only_given = False, optional_mappings = None, savefile = None, rotation = 90):
    """Displays the distribution of a given column in terms of nominated rows and not nominated rows for both clean and unclean data

    Args:
        clean_df: Pandas dataframe of cleaned data
        unclean_df: Pandas dataframe of uncleaned data
        column: String indicating the column the analysis is done on
        display_values: List of column values that the plot will feature
        display_only_given: boolean, if True only to plot the values given in display_values, if False, plot others gathered under "Other"
        optional_mappings: dictionary, maps values in display_values to another string if there is a need to plot another word
        rotation: int, rotation of the xlabels on the plot

    Returns:
        None
    """
    
    #Get the nominated rows from the data
    nominated_df = clean_df[clean_df['oscar_nominated'] == True]
    nominated_unclean_df = unclean_df[unclean_df['oscar_nominated'] == True]

    #Get only the relevant attribute and map the values needed
    #If no wanted values were given take all
    if (display_values == None):
        display_values = unclean_df[column].unique()


    nominated_col = nominated_df[column].apply(lambda item: item if item in display_values else 'Other')
    nominated_col_unclean = nominated_unclean_df[column].apply(lambda item: item if item in display_values else 'Other')
    
    all_movies_col = clean_df[column].apply(lambda item: item if item in display_values else 'Other')
    all_movies_col_unclean = unclean_df[column].apply(lambda item: item if item in display_values else 'Other')

    #If only need to display the ones given remove "other" from all series
    if display_only_given:
        nominated_col = nominated_col[nominated_col != 'Other']
        nominated_col_unclean = nominated_col_unclean[nominated_col_unclean != 'Other']
        all_movies_col = all_movies_col[all_movies_col != 'Other']
        all_movies_col_unclean = all_movies_col_unclean[all_movies_col_unclean != 'Other']

    #Get the counts
    nominated_df_counts = nominated_col.value_counts()
    nominated_unclean_df_counts = nominated_col_unclean.value_counts()
    
    all_movies_counts = all_movies_col.value_counts()
    all_movies_counts_unclean = all_movies_col_unclean.value_counts()

    #Merge the values before and after cleaning, sort
    merged_nominated = pd.concat([nominated_unclean_df_counts, nominated_df_counts], axis=1).fillna(0)
    merged_nominated.columns = ["unclean_count", "clean_count"]
    merged_nominated = merged_nominated.sort_index()
    
    merged_all = pd.concat([all_movies_counts_unclean, all_movies_counts], axis=1).fillna(0)
    merged_all.columns = ["unclean_count", "clean_count"]
    merged_all = merged_all.sort_index()

    #If given any value mappings for clearer display apply them
    if optional_mappings != None:
        merged_nominated = merged_nominated.rename(index=optional_mappings)
        merged_all = merged_all.rename(index=optional_mappings)

    
    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(15,5))
    plt.subplots_adjust(wspace=0.15)
    fig.suptitle(column.replace("_", " "), fontsize="xx-large")
    
    merged_all.plot(kind="bar", color=["blue", "orange"], ax = axs[0])
    axs[0].set_title("For all actors")
    axs[0].tick_params(axis="x", rotation=rotation)
    axs[0].set_yscale("log")
    axs[0].set_ylabel("Log Scale Count", fontsize="x-large")
    
    merged_nominated.plot(kind="bar", color=["blue", "orange"], ax = axs[1])
    axs[1].set_title("For nominated actors")
    axs[1].tick_params(axis="x", rotation=rotation)
    axs[1].set_yscale("log")
    #axs[1].set_ylabel("Log Scale Count")

    if savefile is not None:
        plt.savefig(savefile, bbox_inches="tight")
    
    plt.show()
    
    
def display_cleaning_shift_plot_cont(clean_df, unclean_df, column, is_character, bins_all, bins_nominated, savefile=None):
    """ Displays the distribution of a given column in terms of nominated rows and not nominated rows for both clean and unclean data. Also calculates
        the Kolmogorov-Smirnov comparing the distributions before and after cleaning

    Args:
        clean_df: Pandas dataframe of cleaned data
        unclean_df: Pandas dataframe of uncleaned data
        column: String indicating the column the analysis is done on
        is_character: String, should be either "characters" or "movies" based on what the data is grouped by
    Returns:
        None
    """

    #Get the nominated rows from the data
    nominated_df = clean_df[clean_df['oscar_nominated'] == True]
    nominated_unclean_df = unclean_df[unclean_df['oscar_nominated'] == True]
    
    nominated_df_vals = nominated_df[[column]]
    nominated_unclean_df_vals = nominated_unclean_df[[column]].dropna()
    
    all_df_vals = clean_df[[column]]
    all_unclean_df_vals = unclean_df[[column]].dropna()
    
    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(15,5))
    plt.subplots_adjust(wspace=0.15)
    fig.suptitle(column.replace("_", " "), fontsize="xx-large")
    
    axs[0].hist(all_unclean_df_vals[column], bins=bins_all, alpha= 0.7, label='unclean_data', color='blue')
    axs[0].hist(all_df_vals[column], bins=bins_all, alpha= 0.7, label='cleaned_data', color='orange')
    axs[0].set_title("For all " + is_character)
    axs[0].set_ylabel("Frequency", fontsize="x-large")
    axs[0].set_xlabel(column)
    axs[0].legend()
    
    axs[1].hist(nominated_unclean_df_vals[column], bins=bins_nominated, alpha= 0.7, label='unclean_data', color='blue')
    axs[1].hist(nominated_df_vals[column], bins=bins_nominated, alpha= 0.7, label='cleaned_data', color='orange')
    axs[1].set_title("For nominated " + is_character)
    #axs[1].set_ylabel("Frequency")
    axs[1].set_xlabel(column)
    axs[1].legend()

    if savefile is not None:
        plt.savefig(savefile, bbox_inches="tight")
    
    plt.show()
    
    #Aditionally, do the kolmogorov smirnoff test for the distributions before and after 
    stat, p_value = stats.kstest(all_df_vals[column].values, all_unclean_df_vals[column].values)
    print(f"Kolmogorov-Smirnov test for the {column} distributions before and after data cleaning for all data")
    print(f"Statistic: {stat} ; p-value: {p_value}")
    print()
    stat, p_value = stats.kstest(nominated_df_vals[column].values, nominated_unclean_df_vals[column].values)
    print(f"Kolmogorov-Smirnov test for the {column} distributions before and after data cleaning for nominated data")
    print(f"Statistic: {stat} ; p-value: {p_value}")