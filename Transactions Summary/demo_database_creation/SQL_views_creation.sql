CREATE VIEW list_orders AS
(SELECT order_id, buy_id, open_position, orders.product_id, products.product_name, products.ticker, stockexcs.code_stockexc, "date", "hour", transaction_type, quantity, currency, price_unit, cambio_rate, comissions, taxes FROM investments.orders
INNER JOIN investments.products ON investments.products.product_id = investments.orders.product_id
INNER JOIN investments.currencies ON investments.currencies.currency_id = investments.orders.currency_id
INNER JOIN investments.stockexcs ON products.stockexc_id = stockexcs.stockexc_id
ORDER BY order_id)

CREATE VIEW table_for_geographies AS
(SELECT order_id, buy_id, open_position, orders.product_id, products.product_name, products.ticker, stockexcs.code_stockexc, transaction_type, quantity, currency, price_unit, geographies.* FROM orders
INNER JOIN investments.products ON products.product_id = orders.product_id
INNER JOIN investments.geographies ON products.geography_id = geographies.geography_id
INNER JOIN investments.currencies ON currencies.currency_id = orders.currency_id
INNER JOIN investments.stockexcs ON products.stockexc_id = stockexcs.stockexc_id
WHERE transaction_type != 'Dividend'
ORDER BY order_id)

CREATE VIEW table_for_alocations AS
(SELECT order_id, buy_id, open_position, orders.product_id, products.product_name, products.ticker, stockexcs.code_stockexc, transaction_type, quantity, currency, price_unit, alocations.* FROM orders
INNER JOIN investments.products ON products.product_id = orders.product_id
INNER JOIN investments.alocations ON products.alocation_id = alocations.alocation_id
INNER JOIN investments.currencies ON currencies.currency_id = orders.currency_id
INNER JOIN investments.stockexcs ON products.stockexc_id = stockexcs.stockexc_id
WHERE transaction_type != 'Dividend'
ORDER BY order_id)
