import pandas as pd
import yfinance as yf

def last_close_price (ticker):
    """
    Returns the last closing price in Yahoo Finance
    """
    x = yf.Ticker(ticker)
    return x.info ["regularMarketPreviousClose"]

def last_close_df (dataframe):
    """
    Returns the last closing price in Yahoo Finance, but applied to a whole dataframe
    """
    dataframe.loc [dataframe["code_stockexc"] == "OMK", "ticker_stockexc"] = dataframe["ticker"] + ".CO"
    dataframe.loc [dataframe["code_stockexc"] == "EAM", "ticker_stockexc"] = dataframe["ticker"] + ".AS"
    dataframe.loc [dataframe["code_stockexc"] == "ELI", "ticker_stockexc"] = dataframe["ticker"] + ".LS"
    dataframe.loc [dataframe["code_stockexc"] == "MIL", "ticker_stockexc"] = dataframe["ticker"] + ".MI"
    dataframe.loc [dataframe["code_stockexc"] == "NDQ", "ticker_stockexc"] = dataframe["ticker"]
    dataframe.loc [dataframe["code_stockexc"] == "NSY", "ticker_stockexc"] = dataframe["ticker"]
    dataframe.loc [dataframe["code_stockexc"] == "TDG", "ticker_stockexc"] = dataframe["ticker"] + ".DE"
    dataframe.loc [dataframe["code_stockexc"] == "XET", "ticker_stockexc"] = dataframe["ticker"] + ".DE"
    dataframe.loc [dataframe["code_stockexc"] == "FWB", "ticker_stockexc"] = dataframe["ticker"] + ".F"
    
    dataframe.loc [dataframe["product_id"] == 6, "ticker_stockexc"] = "BTC-EUR"
    
    for i in range (len(dataframe)):
        dataframe.loc [i,"current_closing_price"] = (yf.Ticker(dataframe.loc [i,"ticker_stockexc"])).info ["regularMarketPreviousClose"]

    return dataframe

def orders_csv_treatment (dataframe):
    # Fill the NULL values in the comissions, taxes, and cambio rates
    dataframe ["cambio_rate"] = dataframe["cambio_rate"].fillna(1)
    dataframe [["comissions", "taxes"]] = dataframe[["comissions", "taxes"]].fillna(0)

    # Calculates the total spent in comissions and taxes
    dataframe ["total_comissions_taxes"] = dataframe["comissions"] + dataframe["taxes"]

    # Anxiliary columns that show the total net and gross value of each transaction
    dataframe ["total_invested"] = 0.0
    dataframe.loc [dataframe["transaction_type"] == "BUY", "total_invested"] = (dataframe ["quantity"] * dataframe ["price_unit"]) / dataframe ["cambio_rate"]
    dataframe ["transaction_value_gross"] = 0.0
    dataframe.loc [dataframe["transaction_type"] == "BUY", "transaction_value_gross"] = dataframe ["quantity"] * dataframe ["price_unit"] / dataframe ["cambio_rate"]
    dataframe.loc [dataframe["transaction_type"] == "SELL", "transaction_value_gross"] = (-1) * (dataframe ["quantity"] * dataframe ["price_unit"] / dataframe ["cambio_rate"])
    dataframe.loc [dataframe["transaction_type"] == "Dividend", "transaction_value_gross"] = (-1) * dataframe ["quantity"] * dataframe ["price_unit"] / dataframe ["cambio_rate"]
    dataframe ["transaction_value_net"] = 0.0
    dataframe.loc [dataframe["transaction_type"] == "BUY", "transaction_value_net"] = dataframe ["quantity"] * dataframe ["price_unit"] / dataframe ["cambio_rate"] - dataframe ["total_comissions_taxes"]
    dataframe.loc [dataframe["transaction_type"] == "SELL", "transaction_value_net"] = (-1) * (dataframe ["quantity"] * dataframe ["price_unit"] / dataframe ["cambio_rate"]) - dataframe ["total_comissions_taxes"]
    dataframe.loc [dataframe["transaction_type"] == "Dividend", "transaction_value_net"] = (-1) * dataframe ["quantity"] * dataframe ["price_unit"] / dataframe ["cambio_rate"] - dataframe ["total_comissions_taxes"]

    # Column status
    dataframe.loc [dataframe["open_position"] == False, "status"] = "Closed"
    dataframe.loc [dataframe["open_position"] == True, "status"] = "Open"

    return dataframe

def profit_per_produtct (dataframe):
    dataframe = dataframe.reset_index()

    # Filtering the columns that manner, and then the open positions only
    dataframe = dataframe [ ["open_position", "product_id", "product_name", "total_invested", "transaction_value_gross", "transaction_value_net", "total_comissions_taxes"] ]
    dataframe = dataframe [dataframe ["open_position"] == False]

    # Treatments
    dataframe ["total_invested_with_taxas"] = dataframe ["total_invested"] + dataframe ["total_comissions_taxes"]
    dataframe ["transaction_value_gross"] = dataframe ["transaction_value_gross"] * (-1)
    dataframe ["transaction_value_net"] = dataframe ["transaction_value_gross"] - dataframe ["total_comissions_taxes"]

    # Grouping by product
    dataframe = dataframe.groupby (["product_id", "product_name"]) [["total_invested", "total_invested_with_taxas", "transaction_value_gross", "transaction_value_net"]].sum().reset_index()
    # Calculate yield
    dataframe ["return"] = dataframe ["transaction_value_net"] / dataframe ["total_invested_with_taxas"]
    # Round values
    dataframe[["total_invested", "total_invested_with_taxas", "transaction_value_gross", "transaction_value_net", "return"]] = dataframe[["total_invested", "total_invested_with_taxas", "transaction_value_gross", "transaction_value_net", "return"]].round(3)

    return dataframe

def open_positions (dataframe):
    dataframe = dataframe.reset_index()

    # Filtering the columns that manner, and then the open positions only
    dataframe = dataframe [ ["buy_id", "open_position", "product_id", "product_name", "ticker", "code_stockexc", "transaction_type", "currency", "quantity", "price_unit"] ]
    dataframe = dataframe [dataframe ["open_position"] == True]

    # Treatments before grouping: 1) remove the rows related with dividends (mess up the next calculation); 2) make the "quantity" of the "SELLs" negative, and its unit_price = 0
    dataframe = dataframe [dataframe ["transaction_type"] != "Dividend"]
    dataframe.loc [dataframe["transaction_type"] == "SELL", "quantity"] = dataframe ["quantity"] * (-1)
    dataframe.loc [dataframe["transaction_type"] == "SELL", "price_unit"] = 0

    # Grouping by buy_id. Note that the unit price can be used in this sum because I classified it as 0 when we have a SELL
    dataframe = dataframe.groupby (["buy_id", "product_id", "product_name", "ticker", "code_stockexc", "currency"]) [["quantity", "price_unit"]].sum()
    dataframe = dataframe.reset_index()

    # Determine equilibrium prices by product
    dataframe ["invested_value"] = dataframe ["quantity"] * dataframe ["price_unit"]
    dataframe = dataframe.groupby (["product_id", "product_name", "ticker", "code_stockexc", "currency"]) [["quantity", "invested_value"]].sum()
    dataframe ["equilibrium_price"] = dataframe ["invested_value"] / dataframe ["quantity"]
    dataframe = dataframe.reset_index()

    # Obtain current prices
    dataframe = last_close_df (dataframe)
    dataframe ["current_value"] = dataframe ["quantity"] * dataframe ["current_closing_price"]
    dataframe ["current_gross_profit"] = dataframe ["current_value"] - dataframe ["invested_value"]

    # Round floats
    dataframe[["quantity", "equilibrium_price", "current_closing_price", "invested_value", "current_value", "current_gross_profit"]] = dataframe[["quantity", "equilibrium_price", "current_closing_price", "invested_value", "current_value", "current_gross_profit"]].round(3)

    # Filtering the columns that manner
    dataframe = dataframe [ ["product_name", "quantity", "equilibrium_price", "current_closing_price", "invested_value", "current_value", "current_gross_profit", "currency"] ]

    return dataframe

def alocation_by_product (dataframe):
    dataframe = dataframe.reset_index()

    # Transform the current values in euros
    for i in range (len(dataframe)):
        if dataframe.loc [i, "currency"] != "EUR":
            dataframe.loc [i, "current_value"] = dataframe.loc [i, "current_value"] / last_close_price("EUR" + str(dataframe.loc [i, "currency"]) + "=X")

    # Calculate the weights of each product in the wallet
    all_invest = dataframe["current_value"].sum()
    dataframe ["weight_in_wallet"] = dataframe["current_value"] / all_invest

    # Filter columns that matter
    dataframe = dataframe [ ["product_name", "current_value", "weight_in_wallet"] ]
    # Round floats
    dataframe[["current_value", "weight_in_wallet"]] = dataframe[["current_value", "weight_in_wallet"]].round(3)

    return dataframe

def alocation_by_geo (dataframe):
    # Filter relevant columns
    dataframe = dataframe [ ["order_id", "buy_id", "open_position", "product_id", "product_name", "ticker", "code_stockexc", "transaction_type", "currency", "quantity", "price_unit", "geography_id", "perc_north_america", "perc_latin_america", "perc_europe", "perc_mena", "perc_east_se_asia", "perc_oceania", "perc_other_geo"] ]
    # Filter the open positions only
    dataframe = dataframe [dataframe ["open_position"] == True]

    # Treatments before grouping: 1) remove the rows related with dividends (messes up the next calculation); 2) make the "quantity" of the "SELLs" negative, and its unit_price = 0
    dataframe = dataframe [dataframe ["transaction_type"] != "Dividend"]
    dataframe.loc [dataframe["transaction_type"] == "SELL", "quantity"] = dataframe ["quantity"] * (-1)
    dataframe.loc [dataframe["transaction_type"] == "SELL", "price_unit"] = 0

    # Grouping by order. Reminder: the unit price can be used in this sum because I classified it as 0 when we have a SELL
    dataframe = dataframe.groupby (["buy_id", "product_id", "product_name", "ticker", "code_stockexc", "currency", "geography_id", "perc_north_america", "perc_latin_america", "perc_europe", "perc_mena", "perc_east_se_asia", "perc_oceania", "perc_other_geo"]) [["quantity", "price_unit"]].sum().reset_index()

    # Determine the total invested value by product, then do the respective grouping
    dataframe ["invested_value"] = dataframe ["quantity"] * dataframe ["price_unit"]
    dataframe = dataframe.groupby (["product_id", "product_name", "ticker", "code_stockexc", "currency", "geography_id", "perc_north_america", "perc_latin_america", "perc_europe", "perc_mena", "perc_east_se_asia", "perc_oceania", "perc_other_geo"]) [["quantity", "price_unit"]].sum().reset_index()

    # Add current prices
    dataframe = last_close_df (dataframe)
    dataframe ["current_value"] = dataframe ["quantity"] * dataframe ["current_closing_price"]

    # Transform the current values in euros
    for i in range (len(dataframe)):
        if dataframe.loc [i, "currency"] != "EUR":
            dataframe.loc [i, "current_value"] = dataframe.loc [i, "current_value"] / last_close_price("EUR" + str(dataframe.loc [i, "currency"]) + "=X")

    # Calculate the weight of each geography in the wallet
    total_invest = dataframe["current_value"].sum()
    dataframe ["weight_in_wallet"] = dataframe["current_value"] / total_invest

    # Filter relevant columns
    dataframe = dataframe [["perc_north_america", "perc_latin_america", "perc_europe", "perc_mena", "perc_east_se_asia", "perc_oceania", "perc_other_geo", "weight_in_wallet"]].set_index("weight_in_wallet")

    # Treatment of the data - multiply the weight by each field in its row
    dataframe = dataframe.mul(dataframe.index, axis=0).mul(0.01, axis=0).reset_index()

    # Grouping of data
    dataframe = dataframe [["perc_north_america", "perc_latin_america", "perc_europe", "perc_mena", "perc_east_se_asia", "perc_oceania", "perc_other_geo"]].sum().reset_index().rename (columns = {"index": "geo", 0: "weight"})

    return dataframe

def alocation_by_type (dataframe):
    # Filter relevant columns
    dataframe = dataframe [ ["open_position", "product_id", "product_name", "ticker", "code_stockexc", "transaction_type", "currency", "quantity", "price_unit", "alocation_id", "perc_stocks", "perc_bonds", "perc_gold", "perc_crypto", "perc_other_fin_instruments"] ]
    # Filter the open positions only
    dataframe = dataframe [dataframe ["open_position"] == True]

    # Treatments before grouping: 1) remove the rows related with dividends (mess up the next calculation); 2) make the "quantity" of the "SELLs" negative, and its unit_price = 0
    dataframe = dataframe [dataframe ["transaction_type"] != "Dividend"]
    dataframe.loc [dataframe["transaction_type"] == "SELL", "quantity"] = dataframe ["quantity"] * (-1)
    dataframe.loc [dataframe["transaction_type"] == "SELL", "price_unit"] = 0

    # Grouping by order. Reminder: the unit price can be used in this sum because I classified it as 0 when we have a SELL
    dataframe = dataframe.groupby (["product_id", "product_name", "ticker", "code_stockexc", "currency", "alocation_id", "perc_stocks", "perc_bonds", "perc_gold", "perc_crypto", "perc_other_fin_instruments"]) [["quantity", "price_unit"]].sum().reset_index()

    # Determine the total invested value by product, then do the respective grouping
    dataframe ["invested_value"] = dataframe ["quantity"] * dataframe ["price_unit"]
    dataframe = dataframe.groupby (["product_id", "product_name", "ticker", "code_stockexc", "currency", "alocation_id", "perc_stocks", "perc_bonds", "perc_gold", "perc_crypto", "perc_other_fin_instruments"]) [["quantity", "invested_value"]].sum().reset_index()

    # Add current prices
    dataframe = last_close_df (dataframe)
    dataframe ["current_value"] = dataframe ["quantity"] * dataframe ["current_closing_price"]

    # Transform the current values in euros
    for i in range (len(dataframe)):
        if dataframe.loc [i, "currency"] != "EUR":
            dataframe.loc [i, "current_value"] = dataframe.loc [i, "current_value"] / last_close_price("EUR" + str(dataframe.loc [i, "currency"]) + "=X")

    # Calculate the weight of each asset type in the wallet
    total_invest = dataframe["current_value"].sum()
    dataframe ["weight"] = dataframe["current_value"] / total_invest

    # Filter relevant columns
    dataframe = dataframe [["perc_stocks", "perc_bonds", "perc_gold", "perc_crypto", "perc_other_fin_instruments", "weight"]]
    dataframe = dataframe.set_index("weight")

    # Treatment of the data - multiply the weight by each field in its row
    dataframe = dataframe.mul(dataframe.index, axis=0).mul(0.01, axis=0).reset_index()

    # Grouping of data
    dataframe = dataframe [["perc_stocks", "perc_bonds", "perc_gold", "perc_crypto", "perc_other_fin_instruments"]].sum().reset_index().rename (columns = {"index": "aloc_type", 0: "weight"})

    return dataframe