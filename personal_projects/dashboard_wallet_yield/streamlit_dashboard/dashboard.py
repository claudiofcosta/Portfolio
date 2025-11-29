import streamlit as st
import pandas as pd
import yfinance as yf

import data_wrangling_methods as dw

st.set_page_config(layout="wide")


initial_dataset = pd.read_csv("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_wallet_yield/demo_raw_dataframe.csv?raw=1", delimiter=";", parse_dates=True)

col1, col2 = st.columns (2, width=1500, gap="large")
with col1:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    delimitador = st.text_input("Introduce the data delimiter", value = ";")
    df_template = pd.read_csv ("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_wallet_yield/wallet_return_csv_template.csv?raw=1", delimiter=";")
    df_template = df_template.to_csv().encode("utf-8")
    st.download_button ("Download a template CSV file", data=df_template, file_name="wallet_return_csv_template.csv")

if uploaded_file is not None:
    uploaded_file_df = pd.read_csv (uploaded_file, delimiter=delimitador, parse_dates=True)
    initial_dataset = uploaded_file_df
else:
    initial_dataset = initial_dataset

st.space ()
st.write ("-------")
st.space ()
################################################################################################################################################################################################

#### These functions apply date filters in the dataframe of the monthly evolution
    
df_wallet = dw.process_monthly (initial_dataset.copy(), "wallet")
df_vwce = dw.retrieve_process_yf("VWCE", ".DE", (df_wallet["date"].min()[:10]))
df_vusa = dw.retrieve_process_yf("VUSA", ".AS", (df_wallet["date"].min()[:10]))
df_evolution_month = dw.merge_dataframes (df_vusa, df_vwce, df_wallet)
df_aux = df_evolution_month.copy()

################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################

st.subheader ("Monthly Wallet Evolution")

#region Dataframe Monthly Evolution

df_evolution_month["month"] = pd.to_datetime (df_evolution_month["date"], utc=True)
df_evolution_month["month"] = df_evolution_month["month"].dt.to_period("M")
first_date, last_date = df_evolution_month.loc [0, "month"], df_evolution_month.loc [len(df_evolution_month)-1, "month"]

# Filters by date
col1, col2 = st.columns (2, width=500)
with col1:
    first_month = st.multiselect("Introduce the first month:", options=sorted(df_evolution_month["month"].unique().tolist()), max_selections=1, default=first_date)
with col2:
    last_month = st.multiselect("Introduce the last month:", options=sorted(df_evolution_month["month"].unique().tolist()), max_selections=1, default=last_date)

try:
    df_evolution_month = dw.filter (str(first_month[0]),str(last_month[0]),df_evolution_month)
except IndexError:
    df_evolution_month = df_evolution_month

columns_value_100 = [i for i in df_evolution_month.columns if "value_of_100eur" in i]
columns_variations =  [i for i in df_evolution_month.columns if "rel_variation" in i]
df_evolution_month = dw.redefine_beginning (df_evolution_month, columns_value_100, columns_variations)

# Filter columns that matter
df_evolution_month_ordered = df_evolution_month [["date"]]
for i in range (len(columns_value_100)):
    df_evolution_month_ordered [columns_variations[i]] = df_evolution_month [columns_variations[i]]
    df_evolution_month_ordered [columns_value_100[i]] = df_evolution_month [columns_value_100[i]]
df_evolution_month = df_evolution_month.sort_values("date", ascending = False)

st.dataframe (df_evolution_month_ordered, hide_index= True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                                    "VUSA_rel_variation": st.column_config.NumberColumn ("Variation S&P 500 (%)", format="percent"),
                                                                    "VUSA_value_of_100eur": st.column_config.NumberColumn ("S&P500: Value of 100 €", format="euro"),
                                                                    "VWCE_rel_variation": st.column_config.NumberColumn ("Variation MSCI All-World (%)", format="percent"),
                                                                    "VWCE_value_of_100eur": st.column_config.NumberColumn ("MSCI All-World: Value of 100 €", format="euro"),
                                                                    "wallet_rel_variation": st.column_config.NumberColumn ("Variation Wallet (%)", format="percent"),
                                                                    "wallet_value_of_100eur": st.column_config.NumberColumn ("Wallet: Value of 100 €", format="euro")})

#endregion

################################################################################################################################################################################################
    
#region Line Plot Monthly Evolution

df_evolution_month_plot = df_evolution_month_ordered.copy()
df_evolution_month_plot["date"] = pd.to_datetime (df_evolution_month_plot["date"], utc=True)

df_evolution_month_plot = df_evolution_month_plot [["date", "VUSA_value_of_100eur", "VWCE_value_of_100eur", "wallet_value_of_100eur"]]

df_evolution_month_plot.rename(columns={'date': "Date",
                                        'VUSA_value_of_100eur': '  S&P 500 (standard)',
                                        "VWCE_value_of_100eur": "  MSCI All-World (standard)",
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

dataframe_yearly = dw.annual_processing (df_aux).reset_index()

temp_list = ["date", 'VUSA_value_of_100eur', 'VWCE_value_of_100eur', "wallet_value_of_100eur"]
dataframe_yearly_bar = dataframe_yearly.loc [:,temp_list]

# Treatments
dataframe_yearly_bar["year"] = pd.to_datetime (dataframe_yearly_bar["date"], utc=True)
dataframe_yearly_bar["year"] = dataframe_yearly_bar["year"].dt.to_period("Y")
dataframe_yearly_bar["year"] = dataframe_yearly_bar["year"].astype(str)
dataframe_yearly_bar [[i for i in dataframe_yearly.columns if "value_of_100eur" in i]] = dataframe_yearly_bar [[i for i in dataframe_yearly.columns if "value_of_100eur" in i]] - 100
dataframe_yearly_bar.rename(columns={'VUSA_value_of_100eur': '  S&P 500 (standard)', 'VWCE_value_of_100eur': '  MSCI All-World (standard)', "wallet_value_of_100eur": 'Wallet'}, inplace=True)

list_of_dicts = [{"year": 'ALWAYS', "  S&P 500 (standard)": df_aux.loc [len(df_aux)-1, "VUSA_value_of_100eur"], "  MSCI All-World (standard)": df_aux.loc [len(df_aux)-1, "VWCE_value_of_100eur"], "Wallet": df_aux.loc [len(df_aux)-1, "wallet_value_of_100eur"]}]
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

    st.dataframe(df_vusa, hide_index=True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                        "VUSA_close": st.column_config.NumberColumn ("Closing Value (EUR)", format="euro"),
                                                        "VUSA_value_of_100eur": st.column_config.NumberColumn ("Value of 100€ (EUR)", format="euro"),
                                                        "VUSA_absol_variation": st.column_config.NumberColumn ("Monthly Absolute Variation (EUR)", format="euro"),
                                                        "VUSA_rel_variation": st.column_config.NumberColumn ("Monthly Relative Variation (%)", format="percent") })

with col2:

    st.subheader ("MSCI All-World (standard)")

    st.dataframe(df_vwce, hide_index=True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                        "VWCE_close": st.column_config.NumberColumn ("Closing Value (EUR)", format="euro"),
                                                        "VWCE_value_of_100eur": st.column_config.NumberColumn ("Value of 100€ (EUR)", format="euro"),
                                                        "VWCE_absol_variation": st.column_config.NumberColumn ("Monthly Absolute Variation (EUR)", format="euro"),
                                                        "VWCE_rel_variation": st.column_config.NumberColumn ("Monthly Relative Variation (%)", format="percent") })

with col3:

    st.subheader ("Wallet")

    st.dataframe(df_wallet, hide_index=True, column_config={"date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                                                            "wallet_net_invested": st.column_config.NumberColumn ("Net Invested (EUR)", format="euro"),
                                                            "wallet_close": st.column_config.NumberColumn ("Closing Value (EUR)", format="euro"),
                                                            "wallet_value_of_100eur": st.column_config.NumberColumn ("Value of 100€ (EUR)", format="euro"),
                                                            "wallet_absol_variation": st.column_config.NumberColumn ("Monthly Absolute Variation (EUR)", format="euro"),
                                                            "wallet_rel_variation": st.column_config.NumberColumn ("Monthly Relative Variation (%)", format="percent") })

st.caption("These datasets contain the raw data used in the dashboard")

#endregion


