### **Dashboard Transactions History**

This small app is a dashboard that allows user to have an overview of his/her investment wallet

#### **App Overview**

- **Profit per product** is a dataframe that contains the gross and net profits per product, considering only positions that have been closed.

- **Open Positions** is a dataframe that contains currently open positions. The last closing price is obtained from Yahoo Finance.

- **Alocation by Product/Geography/Type of Asset** are pie charts/dataframes that represent the weight of each product, geography or type of asset in the wallet, allowing user to understand how diversified is his/her portfolio.

- **Dataframe of All Orders** is a dataframe with all the orders.

- Technical note: to determine which positions are closed after a SELL order, the method 'First-In First-Out' was used.


#### **App Building**

- This app is designed to obtain data from an SQL database. Its underlying schema is accessible ![here](https://github.com/claudiofcosta/Portfolio/blob/52815c9440b6016439431c97d9da4e985b6766c7/personal_projects/dashboard_transactions_history/demo_database_creation/SQL_schema.png).

- For demonstration, a demo database was used. The raw data and the SQL scripts used for its creation can be found in the **demo_database_creation** folder.

- The environmental variables used to access Supabase through SQLalchemy package are under .gitignore. To allow access to the data, all relevant SQL views were exported into csv files, that were stored in the **demo_database_creation/exported_views** folder.

- The **data treatment** folder contains the data manipulation script applied previous to the generation of the dashboard. The dataframes were stored in csv files in the **data treatment/exported_dataframes** folder, and they constitute the basis of the datasets present in the dashboard.

- The `dashboard.py` file in **streamlit_dashboard** folder contains the script used to mount the dashboard on Streamlit. Plots were built using the matplotlib package. Additionally, an automatic launcher executable file was generated using the pyinstaller package: `dashboard_launch_app.exe` , present in the main folder.

________________

#### **Contacts**

🔸 **Email**: claudiofcosta@live.com.pt

🔹 **LinkedIn**: [linkedin.com/claudiofcosta](https://www.linkedin.com/in/claudiofcosta/)
