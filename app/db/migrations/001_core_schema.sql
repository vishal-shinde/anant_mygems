CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(role_id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(50) UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    line_id VARCHAR(100),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    designation VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS account_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    type_id INTEGER NOT NULL REFERENCES account_types(type_id),
    short_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(200),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(type_id, short_name)
);

CREATE TABLE IF NOT EXISTS inventory_lots (
    lot_id SERIAL PRIMARY KEY,
    lot_no VARCHAR(80) NOT NULL UNIQUE,
    item_type VARCHAR(30) NOT NULL CHECK (item_type IN ('gold', 'silver', 'stone', 'diamond')),
    metal_category VARCHAR(40),
    weight NUMERIC(18,3) NOT NULL DEFAULT 0,
    unit_price NUMERIC(18,2) NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'reserved', 'sold', 'returned', 'scrap')),
    supplier_account_id INTEGER REFERENCES accounts(account_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS purchases (
    purchase_id SERIAL PRIMARY KEY,
    purchase_no VARCHAR(80) NOT NULL UNIQUE,
    supplier_account_id INTEGER REFERENCES accounts(account_id),
    purchase_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'posted', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS purchase_items (
    purchase_item_id SERIAL PRIMARY KEY,
    purchase_id INTEGER NOT NULL REFERENCES purchases(purchase_id) ON DELETE CASCADE,
    lot_id INTEGER REFERENCES inventory_lots(lot_id),
    item_type VARCHAR(30) NOT NULL,
    description VARCHAR(200),
    quantity NUMERIC(18,3) NOT NULL DEFAULT 0,
    unit_price NUMERIC(18,2) NOT NULL DEFAULT 0,
    amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sales_orders (
    sales_order_id SERIAL PRIMARY KEY,
    order_no VARCHAR(80) NOT NULL UNIQUE,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    total_paid NUMERIC(18,2) NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'confirmed', 'completed', 'cancelled', 'returned')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sales_order_items (
    sales_order_item_id SERIAL PRIMARY KEY,
    sales_order_id INTEGER NOT NULL REFERENCES sales_orders(sales_order_id) ON DELETE CASCADE,
    lot_id INTEGER REFERENCES inventory_lots(lot_id),
    item_type VARCHAR(30) NOT NULL,
    description VARCHAR(200),
    sold_weight NUMERIC(18,3) NOT NULL DEFAULT 0,
    sold_price NUMERIC(18,2) NOT NULL DEFAULT 0,
    paid_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    balance_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    item_status VARCHAR(30) NOT NULL DEFAULT 'pending_stock' CHECK (item_status IN ('pending_stock', 'pending_send', 'sold', 'returned', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    sales_order_id INTEGER REFERENCES sales_orders(sales_order_id),
    sales_order_item_id INTEGER REFERENCES sales_order_items(sales_order_item_id),
    payment_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payment_mode VARCHAR(30) NOT NULL CHECK (payment_mode IN ('cash', 'bank', 'advance', 'pending', 'installment')),
    account_id INTEGER REFERENCES accounts(account_id),
    amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS expenses (
    expense_id SERIAL PRIMARY KEY,
    expense_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    account_id INTEGER REFERENCES accounts(account_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(80) NOT NULL,
    record_id INTEGER,
    action VARCHAR(20) NOT NULL CHECK (action IN ('insert', 'update', 'delete')),
    changed_by INTEGER REFERENCES users(user_id),
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO roles (role_name, description)
VALUES ('admin', 'System administrator')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO users (username, password_hash, role_id, is_active)
SELECT 'admin', '$2b$12$qMiqGrzbErYDxq1GnTri6.4rP7U5ZwW2EPVPaRvh.oIePfq5hMjhe', role_id, TRUE
FROM roles
WHERE role_name = 'admin'
ON CONFLICT (username) DO NOTHING;
