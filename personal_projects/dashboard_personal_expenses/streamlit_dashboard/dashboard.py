import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import date

import data_wrangling_methods

st.set_page_config(layout="wide")

#initial_dataset = pd.read_csv("demo_raw_data_personal_expenses.csv", delimiter=";")
initial_dataset = pd.read_csv ("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_personal_expenses/demo_raw_data_personal_expenses.csv?raw=1", delimiter=";")

col1, col2, col3 = st.columns (3, width=1500)
with col1:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
with col2:
    delimitador = st.text_input("Introduce the data delimiter", value = ";")
with col3:
    df_template = pd.read_csv ("https://raw.githubusercontent.com/claudiofcosta/Portfolio/main/personal_projects/dashboard_personal_expenses/personal_expenses_csv_template.csv?raw=1", delimiter=";")
    df_template = df_template.to_csv().encode("utf-8")
    st.download_button ("Download a template CSV file", data=df_template, file_name="personal_expenses_csv_template.csv")

if uploaded_file == True:
    uploaded_file_df = pd.read_csv (uploaded_file, delimiter=delimitador)
    initial_dataset = uploaded_file_df
else:
    initial_dataset = initial_dataset

st.space ()
st.write ("-------")
st.space ()

################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################

df_data = data_wrangling_methods.raw_in_out_inputs(initial_dataset)

df_evolution = data_wrangling_methods.evolution (df_data.copy())

df_income = data_wrangling_methods.income(df_data.copy())

list_essential_expenses = ["Car", "Groceries", "Health", "Home Expenses", "Public Transports", "Taxes", "Telecom"]
df_expenses = data_wrangling_methods.expenses(df_data.copy(), list_essential_expenses)


################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################

lado_esq, lado_dir = st.tabs(["Evolution of the Assets", "Record of Income and Expenses"])

################################################################################################################################################################################################
################################################################################################################################################################################################

with lado_esq:

    #region daily evolution

    st.subheader ("Daily Evolution")

    df_evolution_daily = data_wrangling_methods.evolution_timeframe (df_evolution.copy(), "D")

    df_evolution_daily_plot = data_wrangling_methods.evolution_plot (df_evolution_daily.copy())

    # Date filters
    try:
        start_date, end_date = st.date_input("Date interval to consider:                  ",value=[df_evolution["date"].min(), "today"])
    except ValueError:
        start_date, end_date = df_evolution["date"].min(), date.today()
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    df_evolution_daily_plot = df_evolution_daily_plot[(df_evolution_daily_plot["date"] >= start_date) & (df_evolution_daily_plot["date"] <= end_date)]
    df_evolution_daily = df_evolution_daily[(df_evolution_daily["date"] >= start_date) & (df_evolution_daily["date"] <= end_date)]

    st.space()

    tab1, tab2 = st.tabs(["Area Chart", "Dataset"])

    with tab1:

        # Plot
        df_evolution_daily_plot = df_evolution_daily_plot.pivot(index="date", columns="account", values="balance")
        st.area_chart (df_evolution_daily_plot, x_label="Date", y_label="Balance (€)", stack= True, height=700)

    with tab2:

        # Dataframe
        st.dataframe (df_evolution_daily, column_config={
                        "value": st.column_config.Column ("Value"),
                        "date": st.column_config.DateColumn ("Date", format="YYYY-MM-DD"),
                        "account": st.column_config.Column ("Account"),
                        "balance_account_1111": st.column_config.NumberColumn ("Balance Account #1111", format="euro"),
                        "balance_account_2222": st.column_config.NumberColumn ("Balance Account #2222", format="euro"),
                        "balance_account_3333": st.column_config.NumberColumn ("Balance Account #3333", format="euro"),
                        "total_balance": st.column_config.NumberColumn ("Total Balance", format="euro")})

    st.caption("This area chart and correspondent dataframe show the evolution of the assets over time.")

    #endregion

    st.write("---")
    
    #region Monthly data

    st.subheader ("Monthly Evolution")

    df_evolution_month = data_wrangling_methods.evolution_timeframe (df_evolution.copy(), "ME")

    df_evolution_month_plot = data_wrangling_methods.evolution_plot(df_evolution_month.copy())

    df_evolution_month_plot_avg = df_evolution_month_plot.pivot_table(index="account", values="balance", aggfunc="mean")
    df_evolution_month_plot_avg ["date"] = "AVERAGE"
    df_evolution_month_plot_avg = df_evolution_month_plot_avg.reset_index()
    df_evolution_month_plot_avg ["balance"] = round(df_evolution_month_plot_avg ["balance"],2)
    df_evolution_month_plot_avg = df_evolution_month_plot_avg.pivot(index="date", columns="account", values="balance")

    st.space()

    tab1, tab2 = st.tabs(["Area Chart", "Dataset"])

    with tab1:

        # Plot

        col200, col201 = st.columns ([0.8, 0.2])

        with col200:
            df_evolution_month_plot["date"] = df_evolution_month_plot["date"].astype(str).str[:7]
            df_evolution_month_plot = df_evolution_month_plot.pivot(index="date", columns="account", values="balance")

            st.bar_chart (df_evolution_month_plot, x_label="Month", y_label="Variation (€)", stack= True, height=700)
        
        with col201:        
            st.bar_chart (df_evolution_month_plot_avg, x_label="Month", y_label="Variation (€)", stack= True, height=707)
    
    with tab2:

        # Dataframe

        st.dataframe (df_evolution_month, column_config={
                        "value": st.column_config.Column ("Value"),
                        "date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                        "account": st.column_config.Column ("Account"),
                        "balance_account_1111": st.column_config.NumberColumn ("Balance Account #1111", format="euro"),
                        "balance_account_2222": st.column_config.NumberColumn ("Balance Account #2222", format="euro"),
                        "balance_account_3333": st.column_config.NumberColumn ("Balance Account #3333", format="euro"),
                        "total_balance": st.column_config.NumberColumn ("Total Balance", format="euro")})
        
    st.caption("This bar chart and correspondent dataframe show the evolution of the assets over the months. The bar plot on the right represents the monthly average.")

    #endregion

    st.write("---")
    
    #region Yearly data

    st.subheader ("Yearly Evolution")

    df_evolution_year = data_wrangling_methods.evolution_timeframe (df_evolution.copy(), "YE")

    df_evolution_year_plot = data_wrangling_methods.evolution_plot(df_evolution_year.copy())

    df_evolution_year_plot_avg = df_evolution_year_plot.pivot_table(index="account", values="balance", aggfunc="mean")
    df_evolution_year_plot_avg ["date"] = "AVERAGE"
    df_evolution_year_plot_avg = df_evolution_year_plot_avg.reset_index()
    df_evolution_year_plot_avg ["balance"] = round(df_evolution_year_plot_avg ["balance"],2)
    df_evolution_year_plot_avg = df_evolution_year_plot_avg.pivot(index="date", columns="account", values="balance")

    df_evolution_year_plot_total = df_evolution_year_plot.pivot_table(index="account", values="balance", aggfunc="sum")
    df_evolution_year_plot_total ["date"] = "ALWAYS"
    df_evolution_year_plot_total = df_evolution_year_plot_total.reset_index()
    df_evolution_year_plot_total = df_evolution_year_plot_total.pivot(index="date", columns="account", values="balance")

    st.space()

    tab1, tab2 = st.tabs(["Bar Chart", "Dataset"])

    with tab1:

        # Plot

        col23, col24, col25 = st.columns ([0.6, 0.2, 0.2])

        with col23:
            
            df_evolution_year_plot["date"] = df_evolution_year_plot["date"].astype(str).str[:4]
            df_evolution_year_plot = df_evolution_year_plot.pivot(index="date", columns="account", values="balance")

            st.bar_chart (df_evolution_year_plot, x_label="Year", y_label="Variation (€)", stack= True, height=520)
        
        with col24:
            st.bar_chart (df_evolution_year_plot_avg, y_label="Variation (€)", stack= False, height=495)
        
        with col25:
            st.bar_chart (df_evolution_year_plot_total, y_label="Variation (€)", stack= False, height=492)
    
    with tab2:

        # Dataframe

        st.dataframe (df_evolution_month, column_config={
                        "value": st.column_config.Column ("Value"),
                        "date": st.column_config.DateColumn ("Month", format="YYYY-MM"),
                        "account": st.column_config.Column ("Account"),
                        "balance_account_1111": st.column_config.NumberColumn ("Balance Account #1111", format="euro"),
                        "balance_account_2222": st.column_config.NumberColumn ("Balance Account #2222", format="euro"),
                        "balance_account_3333": st.column_config.NumberColumn ("Balance Account #3333", format="euro"),
                        "total_balance": st.column_config.NumberColumn ("Total Balance", format="euro")})
        
    st.caption("This bar chart and correspondent dataframe show the evolution of the assets over the years. The middle bar plot represents the annual average, while the one on the right indicates the change since the beginning of the records.")

    #endregion

    st.write("---")

    #region raw data

    st.subheader ("Raw Data")

    df_evo_raw = df_evolution [["id_expense", "value", "date", "account", "balance_account_1111", "balance_account_2222", "balance_account_3333", "total_balance"]]

    st.dataframe (df_evo_raw, column_config={
                    "id_expense": st.column_config.Column ("ID Expense"),
                    "value": st.column_config.Column ("Value"),
                    "date": st.column_config.DateColumn ("Date", format="YYYY-MM-DD"),
                    "account": st.column_config.Column ("Account"),
                    "balance_account_1111": st.column_config.NumberColumn ("Balance Account #1111", format="euro"),
                    "balance_account_2222": st.column_config.NumberColumn ("Balance Account #2222", format="euro"),
                    "balance_account_3333": st.column_config.NumberColumn ("Balance Account #3333", format="euro"),
                    "total_balance": st.column_config.NumberColumn ("Total Balance", format="euro")})
    
    st.caption("This dataset contains the raw data used in this tab of the app")

    #endregion


# ################################################################################################################################################################################################
# ################################################################################################################################################################################################

with lado_dir:

    col1, col2 = st.columns(2, border = True)

    with col1:
        
        #region Data over income

        st.subheader ("Income")
        
        tab1, tab2 = st.tabs(["Income by Category", "Income per Year"])

        with tab1:
        
            df_income_by_cat = df_income.copy()

            try:
                start_date, end_date = st.date_input("Date interval to consider:",value=[df_income_by_cat["date"].min(), "today"])
            except ValueError:
                start_date, end_date = df_income_by_cat["date"].min(), date.today()
            start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
            df_income_by_cat = df_income_by_cat[(df_income_by_cat["date"] >= start_date) & (df_income_by_cat["date"] <= end_date)]
            
            df_income_by_cat = df_income_by_cat.groupby("secondary_category")["value"].sum().reset_index()
            df_income_by_cat = df_income_by_cat [df_income_by_cat["value"] > 0]

            tab11, tab12 = st.tabs(["Pie Chart", "Dataset"])

            with tab11:

                fig, ax = plt.subplots()
                
                wedges, label_texts, autopct_texts = ax.pie(df_income_by_cat["value"], labels=df_income_by_cat["secondary_category"], autopct='%1.1f%%', startangle=140,
                        pctdistance=0.8, textprops={'color':"k", 'fontsize': 7}, colors=['tomato', 'turquoise', 'khaki', 'springgreen', "hotpink", "orange", "ghostwhite", "limegreen"])
                for txt in label_texts:
                    txt.set_color("white")

                plt.style.use ("ggplot")
                fig.patch.set_facecolor('none')  # figure background

                st.pyplot(fig)
            
            with tab12:
                df_income_by_cat_table = df_income_by_cat.copy()
                df_income_by_cat_table ["weight"] = df_income_by_cat_table ["value"] / (df_income_by_cat_table ["value"].sum())
                df_income_by_cat_table = df_income_by_cat_table.sort_values ("value", ascending = False)
                st.dataframe(df_income_by_cat_table, hide_index=True, column_config={"value": st.column_config.NumberColumn ("Total Income (EUR)", format="euro"),
                                                                                     "secondary_category": st.column_config.Column ("Secondary Category"),
                                                                                     "weight": st.column_config.NumberColumn ("Weight (%)", format="percent")
                                                                                     })
            
            st.caption("This pie chart and correspondent dataset represent the income by category")

        with tab2:

            st.subheader ("Total Yearly Income")

            df_income_year = df_income.copy()
            df_income_year["year"] = df_income_year["date"].dt.to_period("Y").astype(str)
            df_income_year =  df_income_year.groupby (["year", "secondary_category"]) ["value"].sum().reset_index()

            df_income_year = df_income_year.rename (columns = {"year": "Year", "secondary_category": "Secondary Category", "value": "Value"})
 
            df_income_year = df_income_year.pivot(index="Year", columns="Secondary Category", values="Value")

            st.bar_chart (df_income_year, x_label="", y_label="Euros", stack= True)

            st.caption ("This bar chart represents the yearly income per category")

            st.write("---")

            st.subheader ("Yearly Average")
            
            df_income_year_avg = data_wrangling_methods.annual_avg(df_income.copy(), "secondary_category")

            df_income_year_avg = df_income_year_avg.rename (columns = {"secondary_category": "Category", "value": "Value"})

            st.bar_chart (df_income_year_avg, x= "Category", x_label="", y = "Value", y_label="Euros", sort="-Value")
        
            st.caption ("This bar chart represents the yearly average of income per category")

        #endregion

#     ################################################################################################################################################################################################
#     ################################################################################################################################################################################################
    
    with col2:
        
        #region Data over expenses by main category

        st.subheader ("Expenses by Main Category")

        tab21, tab22, tab23, tab24, tab25 = st.tabs(["Expense by Category", "Yearly Expenses by Category", "Define your Essential Expenses", "Aggregation by Essenciality", "Yearly Expenses by Essenciality"])
        
        with tab21:

            df_primary_exp = df_expenses.copy()

            try:
                start_date, end_date = st.date_input("Date interval to consider: ",value=[df_primary_exp["date"].min(), "today"])
            except ValueError:
                start_date, end_date = df_primary_exp["date"].min(), "today"            
            start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
            df_primary_exp = df_primary_exp[(df_primary_exp["date"] >= start_date) & (df_primary_exp["date"] <= end_date)]
            
            df_primary_exp = df_primary_exp.groupby ("main_category") ["value"].sum().reset_index()
            
            tab11, tab12 = st.tabs(["Pie Chart", "Dataset"])

            with tab11:

                df_primary_exp ["value"] = df_primary_exp ["value"] * (-1)

                fig, ax = plt.subplots()
                
                wedges, label_texts, autopct_texts = ax.pie(df_primary_exp["value"], labels=df_primary_exp["main_category"], autopct='%1.1f%%', startangle=40,
                        pctdistance=0.8, textprops={'color':"k", 'fontsize': 7}, colors=['tomato', 'turquoise', 'khaki', 'springgreen', "hotpink", "orange", "ghostwhite", "mediumorchid", "limegreen", "brown", "dodgerblue", "gold", "red", "mediumslateblue", "lawngreen", "peru"])
                for txt in label_texts:
                    txt.set_color("white")

                plt.style.use ("ggplot")
                fig.patch.set_facecolor('none')  # figure background

                st.pyplot(fig)
            
            with tab12:
                df_primary_exp_table = df_primary_exp.copy()
                df_primary_exp_table ["weight"] = df_primary_exp_table ["value"] / (df_primary_exp_table ["value"].sum())
                df_primary_exp_table = df_primary_exp_table.sort_values ("value", ascending = False)
                st.dataframe(df_primary_exp_table, hide_index=True, column_config={"value": st.column_config.NumberColumn ("Total Expense (EUR)", format="euro"),
                                                                                    "main_category": st.column_config.Column ("Main Category"),
                                                                                    "weight": st.column_config.NumberColumn ("Weight (%)", format="percent")})
            
            st.caption("This pie chart and correspondent dataset represent the expenses by main category")

        with tab22:
            st.subheader ("Total Yearly Expenses")

            df_primary_year = df_expenses.copy()
            df_primary_year["year"] = df_primary_year["date"].dt.to_period("Y").astype(str)
            df_primary_year =  df_primary_year.groupby (["year", "main_category"]) ["value"].sum().reset_index()
            df_primary_year ["value"] = df_primary_year ["value"] * (-1)

            df_primary_year = df_primary_year.pivot(index="year", columns="main_category", values="value")

            st.bar_chart (df_primary_year, x_label="", y_label="Euros", stack= True)

            st.caption ("This bar chart represents the yearly expenses per category")

            st.write("---")

            st.subheader ("Yearly Average")

            df_primary_year_avg = data_wrangling_methods.annual_avg(df_expenses.copy(), "main_category", True)

            df_primary_year_avg = df_primary_year_avg.rename (columns = {"year": "Year",
                                                                        "main_category": "Main Category",
                                                                        "value": "Value"})

            st.bar_chart (df_primary_year_avg, x= "Main Category", x_label="", y = "Value", y_label="Euros", sort="-Value")
        
            st.caption ("This bar chart represents the yearly average of expenses per category")       

        with tab23:

            ess_expenses = st.multiselect("Define the essencial expenses:", options=sorted(df_expenses["main_category"].unique().tolist()), default = list_essential_expenses)
            df_expenses.loc [df_expenses["main_category"].isin(ess_expenses), "essential"] = "Essentials"
            df_expenses.loc [~df_expenses["main_category"].isin(ess_expenses), "essential"] = "Non-Essentials"

            col1000, col1001 = st.columns(2)
            with col1000:
                st.write("Essential Expenses:")
                st.table(df_expenses["main_category"] [df_expenses["essential"] == "Essentials"].sort_values().unique())
            with col1001:
                st.write("Non-Essential Expenses:")
                st.table(df_expenses["main_category"] [df_expenses["essential"] == "Non-Essentials"].sort_values().unique())

        with tab24:

            df_primary_aggregated = df_expenses.copy()
            df_primary_aggregated ["value"] = df_primary_aggregated ["value"] * (-1)

            try:
                start_date, end_date = st.date_input("Date interval to consider:  ",value=[df_primary_aggregated["date"].min(), "today"])
            except ValueError:
                start_date, end_date = df_primary_aggregated["date"].min(), "today"            
            start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
            df_primary_aggregated = df_primary_aggregated[(df_primary_aggregated["date"] >= start_date) & (df_primary_aggregated["date"] <= end_date)]
            
            df_primary_aggregated = df_primary_aggregated.groupby ("essential") ["value"].sum().reset_index()

            tab11, tab12 = st.tabs(["Pie Chart", "Dataset"])

            with tab11:

                fig, ax = plt.subplots()
                
                wedges, label_texts, autopct_texts = ax.pie(df_primary_aggregated["value"], labels=df_primary_aggregated["essential"], autopct='%1.1f%%', startangle=40,
                        pctdistance=0.8, textprops={'color':"k", 'fontsize': 7}, colors=['tomato', 'turquoise', 'khaki', 'springgreen', "hotpink", "orange", "ghostwhite", "limegreen"])
                for txt in label_texts:
                    txt.set_color("white")
                #plt.legend(loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor='black')

                plt.style.use ("ggplot")
                fig.patch.set_facecolor('none')  # figure background
                ax.set_facecolor('none')         # axes background

                st.pyplot(fig)
            
            with tab12:
                df_primary_aggregated_table = df_primary_aggregated.copy()
                df_primary_aggregated_table ["weight"] = df_primary_aggregated_table ["value"] / (df_primary_aggregated_table ["value"].sum())
                df_primary_aggregated_table = df_primary_aggregated_table.sort_values ("value", ascending = False)
                st.dataframe(df_primary_aggregated_table, hide_index=True, column_config={"value": st.column_config.NumberColumn ("Total Expense (EUR)", format="euro"),
                                                                                           "essential": st.column_config.Column ("Type of Expense"),
                                                                                           "weight": st.column_config.NumberColumn ("Weight (%)", format="percent")})    
                        
            st.caption("This pie chart and correspondent dataset represent the expenses aggregated by its essentiality")

        with tab25:
            st.subheader ("Total Yearly Expenses")

            df_primary_aggregated_year = df_expenses.copy()

            df_primary_aggregated_year["year"] = df_primary_aggregated_year["date"].dt.to_period("Y").astype(str)
            df_primary_aggregated_year =  df_primary_aggregated_year.groupby (["year", "essential"]) ["value"].sum().reset_index()
            df_primary_aggregated_year ["value"] = df_primary_aggregated_year ["value"] * (-1)

            df_primary_aggregated_year = df_primary_aggregated_year.pivot(index="year", columns="essential", values="value")

            st.bar_chart (df_primary_aggregated_year, x_label="", y_label="Euros", stack= True)

            st.caption ("This bar chart represents the yearly expenses aggregated by its essentiality")

            st.write("---")

            st.subheader ("Yearly Average")
        
            df_primary_aggregated_year_avg = data_wrangling_methods.annual_avg(df_expenses.copy(), "essential", True)

            df_primary_aggregated_year_avg = df_primary_aggregated_year_avg.rename (columns = {"year": "Year",
                                                                                                "essential": "Type of Expense",
                                                                                                "value": "Value"})

            st.bar_chart (df_primary_aggregated_year_avg, x= "Type of Expense", x_label="", y = "Value", y_label="Euros", sort="-Value")
        
            st.caption ("This bar chart represents the yearly average of expenses aggregated by its essentiality")

        #endregion

#     ################################################################################################################################################################################################
#     ################################################################################################################################################################################################

    col101, col102 = st.columns ([2,1], border = True)

    with col101:

        #region Data over expenses by secondary category

        st.subheader ("Expenses by Secondary Category")

        df_secondary_exp_plot = df_expenses.copy()

        try:
            start_date, end_date = st.date_input("Date interval to consider:    ",value=[df_secondary_exp_plot["date"].min(), "today"])
        except ValueError:
            start_date, end_date = df_secondary_exp_plot["date"].min(), "today"            
        start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
        df_secondary_exp_plot = df_secondary_exp_plot[(df_secondary_exp_plot["date"] >= start_date) & (df_secondary_exp_plot["date"] <= end_date)]
        
        df_secondary_exp_plot = df_secondary_exp_plot.groupby (["main_category", "secondary_category", "essential"]) ["value"].sum().reset_index()

        df_secondary_exp_plot = df_secondary_exp_plot [["secondary_category", "essential", "value"]].sort_values("value")
        df_secondary_exp_plot ["value"] = df_secondary_exp_plot ["value"] * (-1)
        df_secondary_exp_plot ["Weight"] = df_secondary_exp_plot ["value"] / (df_secondary_exp_plot ["value"].sum())
        df_secondary_exp_plot = df_secondary_exp_plot.rename (columns = {"secondary_category": "Secondary Category",
                                                                         "essential": "Type of Expense",
                                                                         "value": "Value"})

        tab11, tab12 = st.tabs (["Bar Chart", "Dataset"])

        with tab11:

            max_val = int(df_secondary_exp_plot["Value"].max())

            scale = st.session_state.get("scale", max_val)

            chart = (
                    alt.Chart(df_secondary_exp_plot)
                    .mark_bar()
                    .encode(
                        y=alt.Y("Secondary Category:N", sort=None, axis=alt.Axis(title=None, labelLimit=0)),
                        x=alt.X("Value:Q", axis=alt.Axis(title="Euros (€)"), scale=alt.Scale(domain=[0, scale])),
                        color=alt.Color("Type of Expense:N"))
                    ).interactive()

            st.altair_chart(chart)
            
            scale = st.select_slider("Force the scale:", options=list(range(0, max_val+1)), value=(max_val), key="scale") # key ⬅ IMPORTANT to update session_state


        with tab12:

            st.dataframe(df_secondary_exp_plot, hide_index=True, column_config={"Value": st.column_config.NumberColumn ("Value (EUR)", format="euro"), "Weight": st.column_config.NumberColumn ("Weight (%)", format="percent")})
        
        st.caption("This bar chart and correspondent dataset represent the expenses per secondary category")

        #endregion

    with col102:

        #region Fragmenting primary categories

        st.subheader ("Fragmention of Primary Categories")

        df_exp_fragm = df_expenses.copy()

        col111, col112 = st.columns (2)

        with col111:

            try:
                start_date, end_date = st.date_input("Interval to consider:          ",value=[df_exp_fragm["date"].min(), "today"])
            except ValueError:
                start_date, end_date = df_exp_fragm["date"].min(), "today"        
            start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
                    
        with col112:
            primaries = st.multiselect("Select the primary categories:", options=sorted(df_exp_fragm["main_category"].unique().tolist()), default = ["Leisure", "Holidays"])

        df_exp_fragm = df_exp_fragm[(df_exp_fragm["date"] >= start_date) & (df_exp_fragm["date"] <= end_date)]
        df_exp_fragm = df_exp_fragm[df_exp_fragm["main_category"].isin(primaries)]    
        df_exp_fragm = df_exp_fragm.groupby (["main_category", "secondary_category"]) ["value"].sum().reset_index()
        
        df_exp_fragm_plot = df_exp_fragm [["secondary_category", "value"]].sort_values("value")
        df_exp_fragm_plot ["value"] = df_exp_fragm_plot ["value"] * (-1)
        df_exp_fragm_plot ["Weight"] = df_exp_fragm_plot ["value"] / (df_exp_fragm_plot ["value"].sum())
        df_exp_fragm_plot = df_exp_fragm_plot.rename (columns = {"secondary_category": "Secondary Category",
                                                                "value": "Value"})

        tab11, tab12 = st.tabs (["Pie Chart", "Dataset"])

        with tab11:

            fig, ax = plt.subplots()
            
            wedges, label_texts, autopct_texts = ax.pie(df_exp_fragm_plot["Value"], labels=df_exp_fragm_plot["Secondary Category"], autopct='%1.1f%%', startangle=40,
                    pctdistance=0.8, textprops={'color':"k", 'fontsize': 7}, colors=['tomato', 'turquoise', 'khaki', 'springgreen', "hotpink", "orange", "ghostwhite", "mediumorchid", "limegreen", "brown", "dodgerblue", "gold", "red", "mediumslateblue", "lawngreen", "peru"])
            for txt in label_texts:
                txt.set_color("white")
            #plt.legend(loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor='black')

            plt.style.use ("ggplot")
            fig.patch.set_facecolor('none')  # figure background
            ax.set_facecolor('none')         # axes background

            st.pyplot(fig)

        with tab12:

            st.dataframe(df_exp_fragm_plot, hide_index=True, column_config={"Value": st.column_config.NumberColumn ("Value (EUR)", format="euro"), "Weight": st.column_config.NumberColumn ("Weight (%)", format="percent")})
        
        st.caption("This pie chart and correspondent dataset represent the weight of each secondary category in the selected primary categories.")

        #endregion

    ################################################################################################################################################################################################
    ################################################################################################################################################################################################
    
    st.write("---")

    #region df raw data

    st.subheader ("Raw Data - List of All Inputs")

    # Filter buttons
    col1, col2, col3, col4 = st.columns(4)
    # By main category
    with col1:
        movs1 = st.multiselect("Filter by main category:", options=sorted(df_data["main_category"].unique().tolist()))
    df_data = df_data[df_data["main_category"].isin(movs1)] if len(movs1) != 0 else df_data
    # By secondary category
    with col2:
        movs2 = st.multiselect("Filter by secondary category:", options=sorted(df_data["secondary_category"].unique().tolist()))
    df_data = df_data[df_data["secondary_category"].isin(movs2)] if len(movs2) != 0 else df_data
    # By account
    with col3:
        movs3 = st.multiselect("Filter by account:", options=sorted(df_data["account"].unique().tolist()))
    df_data = df_data[df_data["account"].isin(movs3)] if len(movs3) != 0 else df_data
    # By date
    with col4:
        try:
            start_date, end_date = st.date_input("Select the date interval:",value=[df_data["date"].min(), "today"])
        except ValueError:
            start_date, end_date = df_data["date"].min(), date.today()
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    df_data = df_data[(df_data["date"] >= start_date) & (df_data["date"] <= end_date)]

    df_data = df_data.sort_values ("date", ascending = True) 

    # Describe dataframe
    st.dataframe(df_data, hide_index=True, column_config = {"id_expense": st.column_config.NumberColumn ("ID Expense"),
                                                            "value": st.column_config.NumberColumn ("Value", format="euro"),
                                                            "date": st.column_config.DateColumn ("Date"),
                                                            "account": st.column_config.Column ("Account"),
                                                            "category_id": st.column_config.Column ("Category ID"),
                                                            "main_category": st.column_config.Column ("Main Category"),
                                                            "secondary_category": st.column_config.Column ("Secondary Category")
                                                            })
    
    st.caption("This dataset contains the raw data used in this tab of the app")

    #endregion