CREATE SCHEMA investments;

CREATE TABLE investments.currencies (
    currency_id SERIAL PRIMARY KEY,
    currency VARCHAR(3) NOT NULL
);

CREATE TABLE investments.alocations (
    alocation_id SERIAL PRIMARY KEY,
    alocation_description VARCHAR(255) NOT NULL,
    perc_stocks DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_bonds DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_gold DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_crypto DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_other_fin_instruments DECIMAL(8, 4) NOT NULL DEFAULT 0
);

CREATE TABLE investments.geographies (
    geography_id SERIAL PRIMARY KEY,
    geography_description VARCHAR(255) NOT NULL,
    perc_north_america DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_latin_america DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_europe DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_mena DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_east_se_asia DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_oceania DECIMAL(8, 4) NOT NULL DEFAULT 0,
    perc_other_geo DECIMAL(8, 4) NOT NULL DEFAULT 0
);

CREATE TABLE investments.stockexcs (
    stockexc_id SERIAL PRIMARY KEY,
    stockexc VARCHAR(50) NOT NULL,
    code_stockexc VARCHAR(4) NOT NULL
);

CREATE TABLE investments.tipologies (
    tipology_id SERIAL PRIMARY KEY,
    tipology VARCHAR(20) NOT NULL
);

CREATE TABLE investments.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    tipology_id INTEGER NOT NULL,
    ticker VARCHAR(30) NOT NULL,
    isin VARCHAR(12) NOT NULL,
    stockexc_id INTEGER NOT NULL,
    geography_id INTEGER NOT NULL DEFAULT 13,
    alocation_id INTEGER NOT NULL,
    FOREIGN KEY (tipology_id) REFERENCES investments.tipologies (tipology_id),
    FOREIGN KEY (stockexc_id) REFERENCES investments.stockexcs (stockexc_id),
    FOREIGN KEY (geography_id) REFERENCES investments.geographies (geography_id),
    FOREIGN KEY (alocation_id) REFERENCES investments.alocations (alocation_id)
);

CREATE TABLE investments.orders (
    order_id SERIAL PRIMARY KEY,
    buy_id INTEGER NOT NULL,
    open_position BOOLEAN NOT NULL,
    "date" DATE NOT NULL,
    "hour" TIME NOT NULL,
    product_id INTEGER NOT NULL,
    transaction_type VARCHAR(9) NOT NULL,
        CHECK(transaction_type IN ('BUY','SELL', 'Dividend')),
    quantity DECIMAL(10, 4) NOT NULL,
    price_unit DECIMAL(10, 4) NOT NULL,
    currency_id INTEGER NOT NULL,
    cambio_rate DECIMAL(10, 4),
    comissions DECIMAL(8, 2),
    taxes DECIMAL(8, 2),
    FOREIGN KEY (product_id) REFERENCES investments.products (product_id),
    FOREIGN KEY (currency_id) REFERENCES investments.currencies (currency_id)
);








