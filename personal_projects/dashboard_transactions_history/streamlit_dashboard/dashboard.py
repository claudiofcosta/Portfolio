import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

import data_wrangling_methods as dw

################################################################################################################################################################################################

st.set_page_config(layout="wide")

col1, col2 = st.columns ([0.3,0.7], gap="large")
with col1:
    st.link_button ("SQL script for database creation", "https://github.com/claudiofcosta/Portfolio/blob/d94a968eadf1332db486612720c459326b4951c1/personal_projects/dashboard_transactions_history/SQL_database_creation_template.sql")
    st.link_button ("Template Excel file", "https://github.com/claudiofcosta/Portfolio/blob/d94a968eadf1332db486612720c459326b4951c1/personal_projects/dashboard_transactions_history/transactions_history_data_template.xlsx")
    #st.download_button ("Download a template Excel file", data=df_template, file_name="transactions_history_data_template.xlsx")

with col2:
    col11, col12, col13 = st.columns (3)
    with col11:
        uploaded_file_1 = st.file_uploader("Upload your CSV file with the list_orders view", type=["csv"])
    with col12:
        uploaded_file_2 = st.file_uploader("Upload your CSV file with the table_for_geographies view", type=["csv"])
    with col13:
        uploaded_file_3 = st.file_uploader("Upload your CSV file with the table_for_alocations view", type=["csv"])

st.space ()
st.write ("-------")
st.space ()

################################################################################################################################################################################################

df_orders = pd.read_csv("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_transactions_history/demo_database_creation/exported_views/investments.list_orders.csv", index_col="order_id", parse_dates=["date"])
df_orders_aux = pd.read_csv("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_transactions_history/demo_database_creation/exported_views/investments.list_orders.csv", index_col="order_id")
df_geographies = pd.read_csv ("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_transactions_history/demo_database_creation/exported_views/investments.table_for_geographies.csv", index_col=0)
df_aloc_type = pd.read_csv ("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_transactions_history/demo_database_creation/exported_views/investments.table_for_alocations.csv", index_col=0)

if uploaded_file_1 is not None:
    df_orders = pd.read_csv (uploaded_file_1, index_col="order_id", parse_dates=["date"])
    df_orders_aux = pd.read_csv (uploaded_file_1, index_col="order_id")
if uploaded_file_2 is not None:
    df_geographies = pd.read_csv (uploaded_file_2, index_col=0)
if uploaded_file_3 is not None:
    df_aloc_type = pd.read_csv (uploaded_file_3, index_col=0)


################################################################################################################################################################################################

df_orders = dw.orders_csv_treatment(df_orders)
df_orders_aux = dw.orders_csv_treatment(df_orders_aux)

df_prod_profit = dw.profit_per_produtct (df_orders)
df_open_positions = dw.open_positions (df_orders)
df_weights = dw.alocation_by_product(df_open_positions)
df_geographies = dw.alocation_by_geo(df_geographies)
df_aloc_type = dw.alocation_by_type(df_aloc_type)

################################################################################################################################################################################################

#region --------- Profit per product

st.subheader ("Profit per Product")

df_prod_profit = df_prod_profit.sort_values ("transaction_value_net", ascending = False)

# Define filter button
prods = st.multiselect("Filter per product: ",options=sorted(df_prod_profit["product_name"].unique().tolist()))
df_prod_profit_filtered = (df_prod_profit[df_prod_profit["product_name"].isin(prods)] if (len(prods) !=0) else df_prod_profit)

# Describe the dataframe
st.dataframe(df_prod_profit_filtered, hide_index=True,
            column_config={"product_id": st.column_config.NumberColumn("Product ID", pinned = True),
                           "product_name": st.column_config.Column ("Product Name", pinned = True),
                            "total_invested": st.column_config.NumberColumn ("Total Invested (EUR)", format = "euro"),
                            "total_invested_with_taxas": st.column_config.NumberColumn ("Total Invested (incl. Taxes) (EUR)", format = "euro"),
                            "transaction_value_gross": st.column_config.NumberColumn ("Profit (Gross) (EUR)", format = "euro"),
                            "transaction_value_net": st.column_config.NumberColumn ("Profit (Net) (EUR)", format = "euro"),
                            "return": st.column_config.NumberColumn ("Net Return (%)", format = "percent")
                            })

st.caption("This dataset indicates the profit and yield for each product. Only closed positions were considered to generate this dataset")

#endregion

################################################################################################################################################################################################

st.write("---")

#region Open Positions

st.subheader ("Open Positions")

# Describe the dataframe
st.dataframe(df_open_positions, hide_index=True, column_config={
                                            "product_name": st.column_config.Column ("Product Name", pinned = True),
                                            "quantity": st.column_config.NumberColumn ("Quantity"),
                                            "equilibrium_price": st.column_config.NumberColumn ("Equilibrium Price"),
                                            "current_closing_price": st.column_config.NumberColumn ("Last Closing Price"),
                                            "invested_value": st.column_config.NumberColumn ("Invested Value"),
                                            "current_value": st.column_config.NumberColumn ("Current Value"),
                                            "current_gross_profit": st.column_config.NumberColumn ("Current Gross Profit"),
                                            "currency": st.column_config.Column ("Currency")
                                            })

st.caption("This dataset indicates the open positions")

#endregion

################################################################################################################################################################################################

st.write("---") 

col10, col11, col12 = st.columns(3)

with col10:
    
    #region Weight by Product

    st.subheader ("Alocation by Product")

    tab1, tab2 = st.tabs(["Pie Chart", "Data"])

    with tab1:

        # Describe the pie-chart

        df_weights = df_weights.sort_values ("product_name", ascending = True) 

        # Change names of some products (relevant for visualization)
        df_weights.loc [df_weights["product_name"] == "Vanguard FTSE All-World UCITS ETF USD Acc", "product_name"] = "Vanguard All-World ETF"
        df_weights.loc [df_weights["product_name"] == "Deutsche Boerse Commodities Xetra-Gold ETC", "product_name"] = "Xetra Gold ETC"
        df_weights.loc [df_weights["product_name"] == "Goldman Sachs Access China Government Bond UCITS ETF USD (Dist)", "product_name"] = "Goldman Sachs China Gov Bonds"

        pie = alt.Chart(df_weights).mark_arc(outerRadius=200).encode(
                                                                        theta=alt.Theta("current_value:Q", stack=True),
                                                                        color=alt.Color("product_name:N", title="Products")
                                                                        ).properties(height=600, width=600)
        
        # calculate angles
        text_layer = (alt.Chart(df_weights).transform_window(cumulative='sum(current_value)', sort=[{'field': 'product_name'}]).transform_calculate(mid_angle="datum.cumulative - datum.current_value/2"))
                            
        text = text_layer.mark_text(size=20, color="black", align='center', baseline='middle').encode(
            theta=alt.Theta("mid_angle:Q"),
            radius=alt.value(150),
            text=alt.Text("weight_in_wallet:Q", format=".1%") )

        chart = pie + text

        st.altair_chart(chart)
    
    with tab2:
        
        # Describe the dataframe
        
        st.dataframe(df_weights, hide_index = True, column_config={
                                            "product_name": st.column_config.Column ("Product Name", pinned = True),
                                            "current_value": st.column_config.NumberColumn ("Current Value (EUR)", format = "euro"),
                                            "weight_in_wallet": st.column_config.NumberColumn ("Weight in Wallet (%)", format = "percent"),
                                            })
    
    st.caption("This pie chart and correspondent dataset indicate the weight of each open position in the wallet")

    #endregion

with col11:
    
    #region Weight by Geography

    st.subheader ("Alocation by Geography")

    tab3, tab4 = st.tabs(["Pie Chart", "Data"])

    with tab3:

        # Renaming of geographies
        df_geographies ["geo"] = ["North America", "Latin America", "Europe", "MENA", "East and SE Asia", "Oceania", "Other"]

        # Describe the pie-chart
        
        pie = alt.Chart(df_geographies).mark_arc(outerRadius=200).encode(
                                                                        theta=alt.Theta("weight:Q", stack=True),
                                                                        color=alt.Color("geo:N", title="Geography")
                                                                        ).properties(height=600, width=600)
        
        # calculate angles
        text_layer = (alt.Chart(df_geographies).transform_window(cumulative='sum(weight)', sort=[{'field': 'geo'}]).transform_calculate(mid_angle="datum.cumulative - datum.weight/2"))
                            
        text = text_layer.mark_text(size=20, color="black", align='center', baseline='middle').encode(
            theta=alt.Theta("mid_angle:Q"),
            radius=alt.value(150),
            text=alt.Text("weight:Q", format=".1%") )

        chart = pie + text

        st.altair_chart(chart)
    
    with tab4:
        
        # Describe the dataframe

        st.dataframe(df_geographies, hide_index=True, column_config={
                                                                    "geo": st.column_config.Column ("Geography"),
                                                                    "weight": st.column_config.NumberColumn ("Weight in Wallet (%)", format = "percent")
                                                                    }) 

    st.caption("This pie chart and correspondent dataset indicate the relative geographical distribution of the investments.")

    #endregion

with col12:
    
    #region Alocation by Type of Asset

    st.subheader ("Alocation by Type of Asset")

    tab5, tab6 = st.tabs(["Pie Chart", "Data"])

    with tab5:
                
        # Renaming the types
        df_aloc_type ["aloc_type"] = ['Stocks', 'Bonds', 'Gold', 'Crypto', 'Other']
        # Filtering only the existent values
        df_aloc_type = df_aloc_type[df_aloc_type["weight"] > 0]

        # Describe the pie-chart

        pie = alt.Chart(df_aloc_type).mark_arc(outerRadius=200).encode(
                                                                        theta=alt.Theta("weight:Q", stack=True),
                                                                        color=alt.Color("aloc_type:N", title="Asset Type")
                                                                        ).properties(height=600, width=600)
        
        # calculate angles
        text_layer = (alt.Chart(df_aloc_type).transform_window(cumulative='sum(weight)', sort=[{'field': 'aloc_type'}]).transform_calculate(mid_angle="datum.cumulative - datum.weight/2"))
                            
        text = text_layer.mark_text(size=20, color="black", align='center', baseline='middle').encode(
            theta=alt.Theta("mid_angle:Q"),
            radius=alt.value(150),
            text=alt.Text("weight:Q", format=".1%") )

        chart = pie + text

        st.altair_chart(chart)
    
    with tab6:

        # Describe the dataframe

        st.dataframe(df_aloc_type, hide_index=True, column_config={
                                                                    "aloc_type": st.column_config.Column ("Type of Asset"),
                                                                    "weight": st.column_config.NumberColumn ("Weight in Wallet (%)", format = "percent")
                                                                    })

    st.caption("This pie chart and correspondent dataset indicate the weight of each type of financial instrument in the wallet")
    
    #endregion

################################################################################################################################################################################################

st.space(size="small")

st.write("---") 

st.space(size="small")

#region --------- All orders

st.subheader ("Dataframe of All Orders")

# Define filter buttons
col1, col2, col3, col4 = st.columns(4)
# By product
with col1:
    movs = st.multiselect("Filter by product:", options=sorted(df_orders["product_name"].unique().tolist()))
    df_orders_filtered = (df_orders[df_orders["product_name"].isin(movs)] if (len(movs) != 0) else df_orders)
# By status (position open or closed)
with col2:
    movs2 = st.multiselect("Filter by status:", options=sorted(df_orders["status"].unique().tolist()))
    df_orders = (df_orders[df_orders["status"].isin(movs2)] if (len(movs2) != 0) else df_orders)
# By type (BUY, SELL or dividend)
with col3:
    movs3 = st.multiselect("Filter by transaction type:", options=sorted(df_orders["transaction_type"].unique().tolist()))
    df_orders = (df_orders[df_orders["transaction_type"].isin(movs3)] if (len(movs3) != 0) else df_orders)
# By date
with col4:
    try:
        start_date, end_date = st.date_input("Select the date interval:",value=[df_orders_aux["date"].min(), "today"])
    except ValueError:
        start_date = df_orders_aux["date"].min()
        end_date = "today"
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    df_orders = df_orders[(df_orders["date"] >= start_date) & (df_orders["date"] <= end_date)]

# Order of columns
df_orders = df_orders [["status", "product_id", "product_name", "date", "hour", "transaction_type", "quantity", "currency", "price_unit", "cambio_rate", "comissions", "taxes", "transaction_value_gross", "transaction_value_net"]]
df_orders = df_orders.rename_axis("Order ID")

# Describe the dataframe
st.dataframe(df_orders,column_config={"status": st.column_config.Column ("Status Position"),
                                                "product_id": st.column_config.NumberColumn ("Product ID"),
                                                "product_name": st.column_config.Column ("Product Name"),
                                                "date": st.column_config.DateColumn ("Date", format="YYYY-MM-DD"),
                                                "hour": st.column_config.TimeColumn ("Hour", format="hh:mm"),
                                                "transaction_type": st.column_config.Column ("Transaction Type"),
                                                "quantity": st.column_config.NumberColumn ("Quantity"),
                                                "currency": st.column_config.Column ("Currency"),
                                                "price_unit": st.column_config.NumberColumn ("Unit Price"),
                                                "cambio_rate": st.column_config.NumberColumn ("Cambio Rate"),
                                                "comissions": st.column_config.NumberColumn ("Comissions"),
                                                "taxes": st.column_config.NumberColumn ("Taxes"),
                                                "transaction_value_gross": st.column_config.NumberColumn ("Gross Transaction Value"),
                                                "transaction_value_net": st.column_config.NumberColumn ("Net Transaction Value")}
                                                )

st.caption("This dataset represent all individual movements in the wallet. To determine the status of one position, the method 'First-In First-Out' was used")

#endregion