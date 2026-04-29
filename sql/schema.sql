-- ============================================================
-- Expired Product Alert System - Oracle Schema
-- ============================================================

-- Drop tables if they already exist (for clean re-runs)
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE alert_log CASCADE CONSTRAINTS';
    EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE products CASCADE CONSTRAINTS';
    EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE categories CASCADE CONSTRAINTS';
    EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE product_seq';
    EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP SEQUENCE alert_seq';
    EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- ============================================================
-- SEQUENCES
-- ============================================================

CREATE SEQUENCE product_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE SEQUENCE alert_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- ============================================================
-- CATEGORIES TABLE
-- ============================================================

CREATE TABLE categories (
    category_id   NUMBER PRIMARY KEY,
    category_name VARCHAR2(100) NOT NULL,
    alert_days    NUMBER DEFAULT 7 NOT NULL,  -- days before expiry to trigger alert
    CONSTRAINT chk_alert_days CHECK (alert_days > 0)
);

-- ============================================================
-- PRODUCTS TABLE
-- ============================================================

CREATE TABLE products (
    product_id    NUMBER DEFAULT product_seq.NEXTVAL PRIMARY KEY,
    product_name  VARCHAR2(200) NOT NULL,
    barcode       VARCHAR2(50) UNIQUE,
    category_id   NUMBER NOT NULL,
    quantity      NUMBER DEFAULT 0 NOT NULL,
    unit_price    NUMBER(10, 2) NOT NULL,
    expiry_date   DATE NOT NULL,
    location      VARCHAR2(100),  -- e.g. Aisle 3, Shelf B
    created_at    DATE DEFAULT SYSDATE,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CONSTRAINT chk_quantity CHECK (quantity >= 0),
    CONSTRAINT chk_price    CHECK (unit_price >= 0)
);

-- ============================================================
-- ALERT LOG TABLE (tracks every alert run)
-- ============================================================

CREATE TABLE alert_log (
    alert_id      NUMBER DEFAULT alert_seq.NEXTVAL PRIMARY KEY,
    product_id    NUMBER NOT NULL,
    alert_type    VARCHAR2(20) NOT NULL,  -- 'EXPIRING_SOON' or 'EXPIRED'
    days_left     NUMBER,                 -- negative = already expired
    logged_at     DATE DEFAULT SYSDATE,
    CONSTRAINT fk_alert_product FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT chk_alert_type CHECK (alert_type IN ('EXPIRING_SOON', 'EXPIRED'))
);

-- ============================================================
-- SEED DATA
-- ============================================================

INSERT INTO categories VALUES (1, 'Dairy',        3);
INSERT INTO categories VALUES (2, 'Bakery',        2);
INSERT INTO categories VALUES (3, 'Frozen Foods', 14);
INSERT INTO categories VALUES (4, 'Produce',       5);
INSERT INTO categories VALUES (5, 'Beverages',    10);

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Whole Milk 2L',        'BC001', 1, 20, 4.99,  SYSDATE + 2,  'Fridge A1');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Greek Yogurt 500g',    'BC002', 1, 15, 3.49,  SYSDATE + 1,  'Fridge A2');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Sourdough Bread',      'BC003', 2, 8,  5.99,  SYSDATE + 1,  'Bakery Shelf 1');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Croissants 6-pack',    'BC004', 2, 12, 6.49,  SYSDATE - 1,  'Bakery Shelf 2');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Frozen Pizza',         'BC005', 3, 30, 8.99,  SYSDATE + 10, 'Freezer B1');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Strawberries 500g',    'BC006', 4, 25, 4.29,  SYSDATE + 3,  'Produce D1');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Baby Spinach 200g',    'BC007', 4, 18, 3.99,  SYSDATE - 2,  'Produce D2');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Orange Juice 1L',      'BC008', 5, 40, 5.49,  SYSDATE + 7,  'Fridge C1');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Cheddar Cheese 400g',  'BC009', 1, 22, 7.99,  SYSDATE + 30, 'Fridge A3');

INSERT INTO products (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
VALUES ('Blueberry Muffins',    'BC010', 2, 6,  4.99,  SYSDATE,      'Bakery Shelf 3');

COMMIT;

-- ============================================================
-- USEFUL VIEWS
-- ============================================================

CREATE OR REPLACE VIEW v_expiry_status AS
SELECT
    p.product_id,
    p.product_name,
    p.barcode,
    c.category_name,
    p.quantity,
    p.unit_price,
    ROUND(p.quantity * p.unit_price, 2)          AS stock_value,
    p.expiry_date,
    p.location,
    TRUNC(p.expiry_date) - TRUNC(SYSDATE)        AS days_until_expiry,
    c.alert_days,
    CASE
        WHEN TRUNC(p.expiry_date) < TRUNC(SYSDATE)                            THEN 'EXPIRED'
        WHEN TRUNC(p.expiry_date) - TRUNC(SYSDATE) <= c.alert_days            THEN 'EXPIRING_SOON'
        ELSE 'OK'
    END AS status
FROM products p
JOIN categories c ON p.category_id = c.category_id;
