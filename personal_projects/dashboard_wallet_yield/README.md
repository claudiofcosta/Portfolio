### **Dashboard Wallet Yield**

This small app is a dashboard that allows user to have an overview of how his/her investments compare with the general market. App has been deployed [here](https://cfcosta-dashboard-wallet-yield.streamlit.app/).

Throughout the app, the user's wallet can be compared with two standards, the S&P500 and the MSCI All-World. To eliminate noise factors (for instance dollar/euro exchange rate fluctuations), the price of two ETFs were used as proxies of the value of these indexes, namely, the VUSA ETF (traded in the Euronext Amsterdam Stock Exchange) and the VWCE ETF (traded in XETRA Stock Exchange).

#### **App Overview**

- **Monthly Wallet Evolution** is a dataframe that contains the monthly returns of the investments. Besides the percentual monthly variation, also the return of 100€ invested is shown. Noteworthy, applying a date filter in this dataframe recalculates the "return of 100€" columns.

- The formula to calculate return of 100€ invested for a given month n can be found below. The usage this formula instead of simply dividing each row by the value in the first row serves to accomodate the fact that the user may make investments throughout the years. Using this formula, the additional alocated funds are considered for the calculation of the returns only after being invested, and not since timepoint 0.<br> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; return month n = return month n-1 x (1 + relative variation month n) 

- The data of this dataframe (including date filters) is then used to generate a line plot, that shows the return of 100€ invested over time.

- **Yearly Variation** is a bar plot that shows the yearly percentual returns of the investments, as well as the annual average and the return the beginning of the records

- Below **Raw Data** it is possible to find three dataframes, containing the datasets that sustain the whole app. Regarding the standards, the first two columns (months and closing values) were obtaining from Yahoo Finance using the yfinance package.

#### **App Building**

- For demonstration, a demo dataset was used. The CSV file is found in the main folder under the name `demo_raw_dataset`.

- The **data treatment** Jupyter Notebook file contains the data manipulation scripts applied previous to the generation of the dashboard. The dataframes were stored in csv files in the **exported_dataframes** folder, and they constitute the basis of the datasets present in the dashboard.

- The `dashboard.py` file in the **streamlit_dashboard** folder contains the script used to mount the dashboard on Streamlit. Additionally, an automatic launcher executable file was generated using the pyinstaller package: `dashboard_launch_app.exe` , present in the main folder. With it, the user can open the dashboard automatically without the need of a terminal or an IDE.
________________

#### **Contacts**

🔸 **Email**: claudiofcosta@live.com.pt

🔹 **LinkedIn**: [linkedin.com/claudiofcosta](https://www.linkedin.com/in/claudiofcosta/)
