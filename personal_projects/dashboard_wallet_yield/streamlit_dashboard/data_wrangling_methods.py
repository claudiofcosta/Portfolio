import pandas as pd
import yfinance as yf

def filter (begin, end, dataframe):
    """
    begin: begin of the filter\n
    end: end of the filter\n
    dataframe: dataframe that is going to be filtered\n
    _________________________________\n
    introduce the months in the following format: "YYYY-MM" (example: "2015-08")
    """
    index_begin = dataframe.index[dataframe["month"] == begin][0]
    index_end = dataframe.index[dataframe["month"] == end][0]
    df = dataframe.loc [index_begin:index_end]
    # Reset index is mandatory to allow data treatment
    df = df.reset_index()
    return df

def redefine_beginning (dataframe, columns_value_100, columns_variations):
    """
    dataframe: dataframe that is going to be filtered\n
    columns_value_100: list of strings that indicate the name of the columns whose first value we want to be 100\n
    columns_variations: list of strings that indicate the name of the columns of the monthly variations
    """
    for i in columns_value_100:
        dataframe.loc [0,i] = 100
    for i in columns_variations:
        dataframe.loc [0,i] = None
    for column in range (len(columns_value_100)):
        for row in range (1, len(dataframe)):
            dataframe.loc [row,columns_value_100[column]] = dataframe.loc [row-1, columns_value_100[column]] * (1 + dataframe.loc [row, columns_variations[column]])
    return dataframe

def retrieve_process_yf (ticker, stock_exchange, start_date):
    """stock_exchange format example: .DE (the point is essential)"""
    # Obtain dataframe with monthly closes
    all_data = yf.Ticker(ticker+stock_exchange).history(start=start_date)
    monthly_data = all_data.resample('ME').last().reset_index()
    dataframe = monthly_data [["Date", "Close"]].rename(columns = {"Date": "date", "Close": (ticker + "_close")})
    # Calculate monthly variations of standards
    dataframe.loc [0, (ticker + "_value_of_100eur")] = 100.0
    for i in range (1, len(dataframe)):
        dataframe.loc [i, (ticker + "_absol_variation")] = dataframe.loc [i, (ticker + "_close")] - dataframe.loc [i-1, (ticker + "_close")]
        dataframe.loc [i, (ticker + "_rel_variation")] = dataframe.loc [i, (ticker + "_absol_variation")] / dataframe.loc [i-1, (ticker + "_close")]
        dataframe.loc [i, (ticker + "_value_of_100eur")] = dataframe.loc [i-1, (ticker + "_value_of_100eur")] * (1 + dataframe.loc [i, (ticker + "_rel_variation")])
    # Reorder columns
    dataframe = dataframe [["date", (ticker + "_close"), (ticker + "_absol_variation"), (ticker + "_rel_variation"), (ticker + "_value_of_100eur")]]
    return dataframe

def process_monthly (dataframe,name):
    # Calculate monthly variations of standards
    dataframe.loc [0, (name + "_value_of_100eur")] = 100.0
    dataframe = dataframe.fillna(0)
    for i in range (1, len(dataframe)):
        dataframe.loc [i, (name + "_absol_variation")] = dataframe.loc [i, (name + "_close")] - dataframe.loc [i-1, (name + "_close")] - dataframe.loc [i, (name + "_net_invested")]
        dataframe.loc [i, (name + "_rel_variation")] = dataframe.loc [i, (name + "_absol_variation")] / dataframe.loc [i-1, (name + "_close")]
        dataframe.loc [i, (name + "_value_of_100eur")] = dataframe.loc [i-1, (name + "_value_of_100eur")] * (1 + dataframe.loc [i, (name + "_rel_variation")])
    # Reorder columns
    dataframe = dataframe [["date", (name + "_net_invested"), (name + "_close"), (name + "_absol_variation"), (name + "_rel_variation"), (name + "_value_of_100eur")]]
    return dataframe

def merge_dataframes (*dataframes):
    list_df = [i for i in dataframes]
    outcome_df = list_df[0].copy()
    for i in dataframes[1:]:
        for j in i.columns:
            if j != "date":
                outcome_df [j] = i[j]
    return outcome_df

def annual_processing (dataframe):
    dataframe["date"] = pd.to_datetime (dataframe["date"], utc=True)

    list_all_indexes = [i for i in range (0,len(dataframe))]
    list_index_jans = dataframe.index[dataframe["date"].dt.month == 1].tolist()
    list_except_jans = [i for i in list_all_indexes if i not in list_index_jans]

    col_value_100 = [i for i in dataframe.columns if "value_of_100eur" in i]
    col_rel_var = [i for i in dataframe.columns if "rel_variation" in i]

    for i in col_value_100:
        for j in range (1, len(dataframe)): 
            dataframe.loc [j, (i[:-16] + "_open")] = dataframe.loc [j-1, (i[:-16] + "_value_of_100eur")]
        
    col_open = [i for i in dataframe.columns if "open" in i]
    
    filtered_df = dataframe ["date"].to_frame()
    
    for i in range (len(col_open)):
        filtered_df [col_open[i]] = dataframe [col_open[i]]
        filtered_df [col_value_100[i]] = dataframe [col_value_100[i]]
        filtered_df [col_rel_var[i]] = dataframe [col_rel_var[i]]
    
    #Define opens of Jan as 100, and then the closing values considering that new beginning
    filtered_df.loc [list_index_jans,col_open] = 100
    for i in range (len(col_open)):
        filtered_df.loc [list_index_jans,col_value_100[i]] = filtered_df.loc[list_index_jans,col_open[i]] * (1 + (filtered_df.loc[list_index_jans,col_rel_var[i]]) )

    # Apply the same filter in the remaining rows
    for i in list_except_jans[1:]:
        for j in range (len(col_open)):
            filtered_df.loc [i,col_open[j]] = filtered_df.loc [i-1,col_value_100[j]]
            filtered_df.loc [i,col_value_100[j]] = filtered_df.loc[i,col_open[j]] * (1 + (filtered_df.loc[i,col_rel_var[j]]) )

    # Filter the dataframe to include only the last month of the year
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.set_index("date")
    filtered_df = filtered_df.resample('YE').last()

    return filtered_df