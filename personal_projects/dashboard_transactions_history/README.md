### **Dashboard Transactions History**

This small app is a dashboard that allows user to have an overview of his/her investment wallet. App has been deployed [here](https://cfcosta-dashboard-transactions-history.streamlit.app/).

#### **App Overview**

- The app is designed to obtain data from an SQL database (for more information, see below). Script for its creation is available by clicking the link on top.

- Also on top, it is provided a template Excel file in which each tab corresponds to a different SQL table. It can be downloaded via the download button.

- On top-right, user can upload csv files obtained from the database SQL views. To obtain those files, a template .py file with scripts is available [here](https://github.com/claudiofcosta/Portfolio/blob/ac7b337afe973dbf8fd30f90e3a8444126631ea4/personal_projects/dashboard_transactions_history/demo_database_creation/export_demo_views.py).

- **Profit per product** is a dataframe that contains the gross and net profits per product, considering only positions that have been closed.

- **Open Positions** is a dataframe that contains currently open positions. The last closing price is obtained from Yahoo Finance.

- **Alocation by Product/Geography/Type of Asset** are pie charts/dataframes that represent the weight of each product, geography or type of asset in the wallet, allowing user to understand how diversified is his/her portfolio.

- **Dataframe of All Orders** is a dataframe with all the orders.

- Technical note: to determine which positions are closed after a SELL order, the method 'First-In First-Out' was used.

#### **App Building**

- This app is designed to obtain data from an SQL database. Its underlying schema is accessible [here](https://github.com/claudiofcosta/Portfolio/blob/52815c9440b6016439431c97d9da4e985b6766c7/personal_projects/dashboard_transactions_history/demo_database_creation/SQL_schema.png).

- For demonstration, a demo database was used. The raw data and the SQL scripts used for its creation can be found in the **demo_database_creation** folder.

- The environmental variables used to access Supabase through SQLalchemy package are under .gitignore. To allow access to the data, all relevant SQL views were exported into csv files, that were stored in the **demo_database_creation/exported_views** folder.

- Basic manipulations functions are kept in an apart script (called `data_wrangling_methods.py`).

- The `dashboard.py` file in **streamlit_dashboard** folder contains the script used to mount the dashboard on Streamlit. Plots were built using the Altair package. Additionally, an automatic launcher executable file was generated using the pyinstaller package: `dashboard_launch_app.exe` , present in the main folder. With it, the user can open the dashboard automatically without the need of a terminal or an IDE.
________________

#### **Contacts**

🔸 **Email**: claudiofcosta@live.com.pt

🔹 **LinkedIn**: [linkedin.com/claudiofcosta](https://www.linkedin.com/in/claudiofcosta/)
