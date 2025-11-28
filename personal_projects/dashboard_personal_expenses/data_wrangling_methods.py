import pandas as pd
from datetime import date

def raw_in_out_inputs (dataframe):
    dataframe["date"] = pd.to_datetime (dataframe["date"], format= "%d/%m/%Y")
    return dataframe

def income (dataframe):
    dataframe = dataframe [dataframe ["main_category"] == "Income"] 
    return dataframe

def expenses(dataframe, list_essencials):
    dataframe = dataframe [dataframe ["main_category"] != "Income"] 
    dataframe.loc [dataframe["main_category"].isin(list_essencials), "essential"] = "Essentials"
    dataframe.loc [~dataframe["main_category"].isin(list_essencials), "essential"] = "Non-Essentials"
    return dataframe

def annual_avg(dataframe, grouping_column: str, neg_files=False):
    dataframe["year"] = dataframe["date"].dt.dataframe("Y").astype(str)
    if neg_files == True:
        dataframe ["value"] = dataframe ["value"] * (-1)
    dataframe =  dataframe.groupby (["year", grouping_column]) ["value"].sum().reset_index()
    dataframe =  dataframe.groupby ([grouping_column]) ["value"].mean().reset_index()
    dataframe["value"] = round (dataframe["value"], 2) 
    return dataframe

def evolution (dataframe):
    dataframe = dataframe.sort_values("date")
    # determine all unique account numbers
    list_accounts = dataframe["account_number"].drop_duplicates().tolist()
    # add evolution per account number
    list_column_titles = []
    for i in list_accounts:
        column_title = "balance_account_" + i
        dataframe [column_title] = (dataframe [dataframe ["account_number"] == i]) ["value"].cumsum()
        list_column_titles.append (column_title)
    # fill the NaN
    dataframe [list_column_titles] = dataframe[list_column_titles].ffill().fillna(0)   
    # calculate total balance
    for i in list_column_titles:
        dataframe ["total_balance"] = dataframe ["total_balance"] + dataframe [i]
    return dataframe

def evolution_plot (dataframe):
    # determine all unique account numbers
    list_accounts = dataframe["account_number"].drop_duplicates().tolist()
    # make a list of the balances of each account in each timeframe
    list_dataframes = []
    for i in list_accounts:
        column_title = "balance_account_" + i
        temporary_df = dataframe [["date", column_title]].rename (columns = {column_title: "balance"})
        temporary_df ["account"] = i
    outcome_dataframe = pd.concat( list_dataframes , ignore_index = True)
    return outcome_dataframe

def evolution_timeframe (dataframe, timeframe: str):
    """for the timeframe, select D for Daily, ME for Month-End, or YE for Year-End"""
    # determine all unique account numbers
    list_accounts = dataframe["account_number"].drop_duplicates().tolist()
    # add get list of column titles
    list_column_titles_with_date = ["date"]
    list_column_titles_without_date = []
    for i in list_accounts:
        column_title = "balance_account_" + i
        list_column_titles_with_date.append (column_title)
        list_column_titles_without_date.append (column_title)
    list_column_titles_with_date.append("total_balance")
    list_column_titles_without_date.append("total_balance")
    # group by date, and then resample considering the dimeframe
    dataframe = dataframe [list_column_titles_with_date].groupby ("date") [list_column_titles_without_date].last()
    dataframe = dataframe.resample(timeframe).last().reset_index()
    return dataframe
