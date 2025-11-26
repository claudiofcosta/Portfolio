import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

################################################################################################################################################################################################

st.set_page_config(layout="wide")

#region --------- Profit per product

st.subheader ("Profit per Product")

df_prod_profit = pd.read_csv ("data treatment/exported_dataframes/df_prod_profit.csv", index_col=0)
df_prod_profit = df_prod_profit.reset_index(drop = True)
df_prod_profit = df_prod_profit.sort_values ("transaction_value_net", ascending = False)

# Define filter button
prods = st.multiselect("Filter per product: ",options=sorted(df_prod_profit["product_name"].unique().tolist()))
df_prod_profit_filtered = (df_prod_profit[df_prod_profit["product_name"].isin(prods)] if (len(prods) !=0) else df_prod_profit)

# Describe the dataframe
st.dataframe(df_prod_profit_filtered, hide_index=True,
            column_config={"product_name": st.column_config.Column ("Product Name", pinned = True),
                            "total_invested": st.column_config.NumberColumn ("Total Invested (EUR)", format = "euro"),
                            "total_invested_with_taxas": st.column_config.NumberColumn ("Total Invested (incl. Taxes) (EUR)", format = "euro"),
                            "transaction_value_gross": st.column_config.NumberColumn ("Profit (Gross) (EUR)", format = "euro"),
                            "transaction_value_net": st.column_config.NumberColumn ("Profit (Net) (EUR)", format = "euro"),
                            "yield": st.column_config.NumberColumn ("Net Yield", format = "percent")
                            })

st.caption("This dataset indicates the profit and yield for each product. Only closed positions were considered to generate this dataset")

#endregion

################################################################################################################################################################################################

st.write("---")

#region Open Positions

st.subheader ("Open Positions")

df_open_positions = pd.read_csv ("data treatment/exported_dataframes/df_open_positions.csv")

# Describe the dataframe
st.dataframe(df_open_positions, hide_index=True, column_config={
                                            "product_name": st.column_config.Column ("Product Name", pinned = True),
                                            "quantity": st.column_config.NumberColumn ("Quantity"),
                                            "equilibrium_price": st.column_config.NumberColumn ("Equilibrium Price"),
                                            "current_closing_price": st.column_config.NumberColumn ("Last Closing Price"),
                                            "currency": st.column_config.Column ("Currency"),
                                            "invested_value": st.column_config.NumberColumn ("Invested Value"),
                                            "current_value": st.column_config.NumberColumn ("Current Value"),
                                            "current_gross_profit": st.column_config.NumberColumn ("Current Gross Profit"),
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

        df_weights = pd.read_csv ("data treatment/exported_dataframes/df_weights.csv")

        df_weights = df_weights.sort_values ("product_name", ascending = True) 

        fig, ax = plt.subplots()

        ax.pie(df_weights["weight_in_wallet"], autopct='%1.1f%%', startangle=40, pctdistance=0.8, textprops={'color':"k", 'fontsize': 7},
                colors=['gold', "hotpink", 'orange', 'springgreen', 'turquoise', "tomato", "ghostwhite", "springgreen"])
        plt.legend(df_weights["product_name"], loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor='black')

        # Graph style
        plt.style.use ("ggplot")
        fig.patch.set_facecolor('none')  # figure background
        ax.set_facecolor('none')         # axes background

        # Call figure
        st.pyplot(fig)
    
    with tab2:
        
        # Describe the dataframe
        
        st.dataframe(df_weights, hide_index = True, column_config={
                                            "product_name": st.column_config.Column ("Product Name", pinned = True),
                                            "current_value": st.column_config.NumberColumn ("Current Value (EUR)", format = "euro"),
                                            "weight_in_wallet": st.column_config.NumberColumn ("Weight in Wallet (%)", format = "percent"),
                                            })
    
    st.caption("This dataset and pie-chart indicate the weight of each open position in the wallet")

    #endregion

with col11:
    
    #region Weight by Geography

    st.subheader ("Alocation by Geography")

    tab3, tab4 = st.tabs(["Pie Chart", "Data"])

    with tab3:

        # Describe the pie-chart
        
        df_geographies = pd.read_csv ("data treatment/exported_dataframes/df_geographies.csv", index_col=0)

        fig, ax = plt.subplots()

        ax.pie(df_geographies["weight"], autopct='%1.1f%%', startangle=0, pctdistance=0.8, textprops={'color':"k", 'fontsize': 7},
                colors=['tomato', 'gold', 'turquoise', 'orange', "hotpink", "limegreen"])
        plt.legend(df_geographies["geo"], loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor='black')

        # Graph style
        plt.style.use ("ggplot")
        fig.patch.set_facecolor('none')  # figure background
        ax.set_facecolor('none')         # axes background

        # Call figure
        st.pyplot(fig)
    
    with tab4:
        
        # Describe the dataframe

        st.dataframe(df_geographies, hide_index=True, column_config={
                                                                    "geo": st.column_config.Column ("Geography"),
                                                                    "weight": st.column_config.NumberColumn ("Weight in Wallet (%)", format = "percent")
                                                                    }) 

    st.caption("This dataset and pie-chart indicate the relative geographical distribution of the investments.")

    #endregion

with col12:
    
    #region Alocation by Type of Asset

    st.subheader ("Alocation by Type of Asset")

    tab5, tab6 = st.tabs(["Pie Chart", "Data"])

    with tab5:
        
        # Describe the pie-chart
            
        df_aloc_type = pd.read_csv ("data treatment/exported_dataframes/df_aloc_type.csv", index_col=0)
        df_aloc_type = df_aloc_type[df_aloc_type["weight"] > 0]

        fig, ax = plt.subplots()

        ax.pie(df_aloc_type["weight"], autopct='%1.1f%%', startangle=0, pctdistance=0.8, textprops={'color':"k", 'fontsize': 7},
                colors=['gold', 'tomato', 'limegreen', 'turquoise', "hotpink"])
        plt.legend(df_aloc_type["aloc_type"], loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor='black')

        # Graph style
        plt.style.use ("ggplot")
        fig.patch.set_facecolor('none')  # figure background
        ax.set_facecolor('none')         # axes background

        # Call figure
        st.pyplot(fig)
    
    with tab6:

        # Describe the dataframe

        st.dataframe(df_aloc_type, hide_index=True, column_config={
                                                                    "aloc_type": st.column_config.Column ("Type of Asset"),
                                                                    "weight": st.column_config.NumberColumn ("Weight in Wallet (%)", format = "percent")
                                                                    })

    st.caption("This dataset and pie-chart indicate the weight of each type of financial instrument in the wallet")
    
    #endregion

################################################################################################################################################################################################

st.space(size="small")

st.write("---") 

st.space(size="small")

#region --------- All orders

st.subheader ("Dataframe of All Orders")

df_orders_filtered_aux = pd.read_csv("data treatment/exported_dataframes/df_orders.csv", index_col="order_id")
df_orders_filtered = pd.read_csv("data treatment/exported_dataframes/df_orders.csv", index_col="order_id", parse_dates=["date"])

# Define filter buttons
col1, col2, col3, col4 = st.columns(4)
# By product
with col1:
    movs = st.multiselect("Filter by product:", options=sorted(df_orders_filtered["product_name"].unique().tolist()))
    df_orders_filtered = (df_orders_filtered[df_orders_filtered["product_name"].isin(movs)] if (len(movs) != 0) else df_orders_filtered)
# By status (position open or closed)
with col2:
    movs2 = st.multiselect("Filter by status:", options=sorted(df_orders_filtered["status"].unique().tolist()))
    df_orders_filtered = (df_orders_filtered[df_orders_filtered["status"].isin(movs2)] if (len(movs2) != 0) else df_orders_filtered)
# By type (BUY, SELL or dividend)
with col3:
    movs3 = st.multiselect("Filter by transaction type:", options=sorted(df_orders_filtered["transaction_type"].unique().tolist()))
    df_orders_filtered = (df_orders_filtered[df_orders_filtered["transaction_type"].isin(movs3)] if (len(movs3) != 0) else df_orders_filtered)
# By date
with col4:
    try:
        start_date, end_date = st.date_input("Select the date interval:",value=[df_orders_filtered_aux["date"].min(), "today"])
    except ValueError:
        start_date = df_orders_filtered_aux["date"].min()
        end_date = "today"
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_orders_filtered = df_orders_filtered[(df_orders_filtered["date"] >= start_date) & (df_orders_filtered["date"] <= end_date)]

# Order of columns
df_orders_filtered = df_orders_filtered [["status", "product_id", "product_name", "date", "hour", "transaction_type", "quantity", "currency", "price_unit", "cambio_rate", "comissions", "taxes", "transaction_value_gross", "transaction_value_net"]]
df_orders_filtered = df_orders_filtered.rename_axis("Order ID")

# Describe the dataframe
st.dataframe(df_orders_filtered,column_config={"status": st.column_config.Column ("Status Position"),
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