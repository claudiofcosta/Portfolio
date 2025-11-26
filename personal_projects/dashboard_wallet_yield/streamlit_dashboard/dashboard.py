import streamlit as st
import pandas as pd

################################################################################################################################################################################################

#### These functions apply date filters in the dataframe of the monthly evolution

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

################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################

st.set_page_config(layout="wide")

################################################################################################################################################################################################
################################################################################################################################################################################################

st.subheader ("Monthly Wallet Evolution")

df_evolution_month = pd.read_csv("exported_dataframes/df_evolution_month.csv", index_col=0)
df_aux = pd.read_csv("exported_dataframes/df_evolution_month.csv", index_col=0)

#region Dataframe Monthly Evolution

df_evolution_month["month"] = pd.to_datetime (df_evolution_month["date"], utc=True)
df_evolution_month["month"] = df_evolution_month["month"].dt.to_period("M")
first_date = df_evolution_month.loc [0, "month"]
last_date = df_evolution_month.loc [len(df_evolution_month)-1, "month"]

# Filters by date
col1, col2 = st.columns (2, width=500)
with col1:
    first_month = st.multiselect("Introduce the first month:", options=sorted(df_evolution_month["month"].unique().tolist()), max_selections=1, default=first_date)
with col2:
    last_month = st.multiselect("Introduce the last month:", options=sorted(df_evolution_month["month"].unique().tolist()), max_selections=1, default=last_date)

try:
    df_evolution_month = filter (str(first_month[0]),str(last_month[0]),df_evolution_month)
except IndexError:
    df_evolution_month = df_evolution_month

columns_value_100 = ["vusa_value_of_100eur","vwce_value_of_100eur","wallet_value_of_100eur"]
columns_variations = ["vusa_rel_variation", "vwce_rel_variation", "wallet_rel_variation"]
df_evolution_month = redefine_beginning (df_evolution_month, columns_value_100, columns_variations)

# Filter columns that matter
df_evolution_month = df_evolution_month [["date", "vusa_rel_variation", "vusa_value_of_100eur", "vwce_rel_variation", "vwce_value_of_100eur", "wallet_rel_variation", "wallet_value_of_100eur"]]
df_evolution_month = df_evolution_month.sort_values("date", ascending = False)

st.dataframe (df_evolution_month, hide_index= True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                                    "vusa_rel_variation": st.column_config.NumberColumn ("Variation S&P 500 (%)", format="percent"),
                                                                    "vusa_value_of_100eur": st.column_config.NumberColumn ("S&P500: Value of 100 €", format="euro"),
                                                                    "vwce_rel_variation": st.column_config.NumberColumn ("Variation MSCI All-World (%)", format="percent"),
                                                                    "vwce_value_of_100eur": st.column_config.NumberColumn ("MSCI All-World: Value of 100 €", format="euro"),
                                                                    "wallet_rel_variation": st.column_config.NumberColumn ("Variation Wallet (%)", format="percent"),
                                                                    "wallet_value_of_100eur": st.column_config.NumberColumn ("Wallet: Value of 100 €", format="euro")})

#endregion

################################################################################################################################################################################################
    
#region Line Plot Monthly Evolution

df_evolution_month_plot = df_evolution_month.copy()
df_evolution_month_plot["date"] = pd.to_datetime (df_evolution_month_plot["date"], utc=True)

df_evolution_month_plot = df_evolution_month_plot [["date", "vusa_value_of_100eur", "vwce_value_of_100eur", "wallet_value_of_100eur"]]

df_evolution_month_plot.rename(columns={'date': "Date",
                                        'vusa_value_of_100eur': '  S&P 500 (standard)',
                                        "vwce_value_of_100eur": "  MSCI All-World (standard)",
                                        'wallet_value_of_100eur': 'Wallet'
                                        }, inplace=True)

# Define standards
filt_soma = ["Date", "Wallet"]
filt = st.multiselect("Choose standards to display:", options=sorted(["  S&P 500 (standard)", "  MSCI All-World (standard)"]), default=["  S&P 500 (standard)"], width=500)
filt_soma += filt
df_evolution_month_plot = df_evolution_month_plot[filt_soma]

df_evolution_month_plot = df_evolution_month_plot.set_index("Date")

# Define line plot
st.line_chart (df_evolution_month_plot, x_label = "Time", y_label  = "Value of 100€", height=700)

st.caption("This line plot indicates the value of an investment of 100€ across the indicated period. The first point is always fixated as 100€ to facilitate visualizations")

#endregion

################################################################################################################################################################################################

st.write("---") 

#region Annual comparison

st.subheader ("Yearly Variation (%)")

dataframe_yearly = pd.read_csv("exported_dataframes/dataframe_yearly.csv")

dataframe_yearly_bar = dataframe_yearly.loc [:,["date", "vwce_value_of_100eur", "vusa_value_of_100eur", "wallet_value_of_100eur"]]

# Treatments
dataframe_yearly_bar["year"] = pd.to_datetime (dataframe_yearly_bar["date"], utc=True)
dataframe_yearly_bar["year"] = dataframe_yearly_bar["year"].dt.to_period("Y")
dataframe_yearly_bar["year"] = dataframe_yearly_bar["year"].astype(str)
dataframe_yearly_bar [["vwce_value_of_100eur", "vusa_value_of_100eur", "wallet_value_of_100eur"]] = dataframe_yearly_bar [["vwce_value_of_100eur", "vusa_value_of_100eur", "wallet_value_of_100eur"]] - 100
dataframe_yearly_bar.rename(columns={'vusa_value_of_100eur': '  S&P 500 (standard)', 'vwce_value_of_100eur': '  MSCI All-World (standard)', "wallet_value_of_100eur": 'Wallet'}, inplace=True)

list_of_dicts = [{"year": 'ALWAYS', "  S&P 500 (standard)": df_aux.loc [len(df_aux)-1, "vusa_value_of_100eur"], "  MSCI All-World (standard)": df_aux.loc [len(df_aux)-1, "vwce_value_of_100eur"], "Wallet": df_aux.loc [len(df_aux)-1, "wallet_value_of_100eur"]}]
df_always = pd.DataFrame(list_of_dicts)
df_always [["  S&P 500 (standard)", "  MSCI All-World (standard)", "Wallet"]] = df_always [["  S&P 500 (standard)", "  MSCI All-World (standard)", "Wallet"]] - 100

dataframe_yearly_avg = dataframe_yearly_bar [["  S&P 500 (standard)", "  MSCI All-World (standard)", "Wallet"]].agg(["mean","std"])
dataframe_yearly_avg ["year"] = "AVERAGE"

filter_st = st.multiselect("Select the standards to display: ", options=sorted(["  S&P 500 (standard)", "  MSCI All-World (standard)"]), default=["  S&P 500 (standard)", "  MSCI All-World (standard)"])
insts = ["year", "Wallet"]
pad_ins = filter_st + insts

dataframe_yearly_bar = dataframe_yearly_bar[pad_ins]
df_always = df_always[pad_ins]
dataframe_yearly_avg = dataframe_yearly_avg[pad_ins]

col23, col24, col25 = st.columns ([0.6, 0.2, 0.2])
with col23:
    st.bar_chart(data=dataframe_yearly_bar, x = "year", stack=False, height=400)
with col24:
    st.bar_chart(data=dataframe_yearly_avg, x = "year", x_label="", stack=False, height=390)
with col25:
    st.bar_chart(data=df_always, x = "year", x_label="", stack=False, height=385)

st.caption("This bar plot indicates the return on investments each year. The middle plot represents the annual average, while the one on the right indicates the return since the beginning of the records.")

# #endregion

st.space(size="small")

st.write("---") 

st.space(size="small")

#region Raw data

st.subheader ("Raw Data")

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader ("S&P 500 (standard)")

    df_vusa = pd.read_csv ("exported_dataframes/df_vusa.csv", index_col=0)

    st.dataframe(df_vusa, hide_index=True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                        "vusa_close": st.column_config.NumberColumn ("Closing Value (EUR)", format="euro"),
                                                        "vusa_value_of_100eur": st.column_config.NumberColumn ("Value of 100€ (EUR)", format="euro"),
                                                        "vusa_absol_variation": st.column_config.NumberColumn ("Monthly Absolute Variation (EUR)", format="euro"),
                                                        "vusa_rel_variation": st.column_config.NumberColumn ("Monthly Relative Variation (%)", format="percent") })

with col2:

    st.subheader ("MSCI All-World (standard)")

    df_vwce = pd.read_csv ("exported_dataframes/df_vwce.csv", index_col=0)

    st.dataframe(df_vwce, hide_index=True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                        "vwce_close": st.column_config.NumberColumn ("Closing Value (EUR)", format="euro"),
                                                        "vwce_value_of_100eur": st.column_config.NumberColumn ("Value of 100€ (EUR)", format="euro"),
                                                        "vwce_absol_variation": st.column_config.NumberColumn ("Monthly Absolute Variation (EUR)", format="euro"),
                                                        "vwce_rel_variation": st.column_config.NumberColumn ("Monthly Relative Variation (%)", format="percent") })

with col3:

    st.subheader ("Wallet")

    df_wallet = pd.read_csv ("exported_dataframes/df_wallet.csv", index_col=0)

    st.dataframe(df_wallet, hide_index=True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                            "wallet_net_invested": st.column_config.NumberColumn ("Net Invested (EUR)", format="euro"),
                                                            "wallet_close": st.column_config.NumberColumn ("Closing Value (EUR)", format="euro"),
                                                            "wallet_value_of_100eur": st.column_config.NumberColumn ("Value of 100€ (EUR)", format="euro"),
                                                            "wallet_absol_variation": st.column_config.NumberColumn ("Monthly Absolute Variation (EUR)", format="euro"),
                                                            "wallet_rel_variation": st.column_config.NumberColumn ("Monthly Relative Variation (%)", format="percent") })

st.caption("These datasets contain the raw data used in the dashboard")

#endregion


