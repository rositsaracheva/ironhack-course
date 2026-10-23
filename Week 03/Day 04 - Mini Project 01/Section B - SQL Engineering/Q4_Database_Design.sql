-- =====================================================================
-- SECTION B: SQL ENGINEERING
-- Q4. Database Design (3NF Normalized Schemas)
-- Platform: QuickCart E-Commerce & Logistics
-- Database: quickcart.db
-- =====================================================================

-- =====================================================================
-- 1. SHIPMENT TRACKING SCHEMA
-- =====================================================================
-- Design: Decoupled into `shipments` (core shipment record) and 
-- `shipment_events` (audit log of checkpoint locations & milestones).

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    carrier_name VARCHAR(50) NOT NULL,                    -- e.g., 'DHL Express', 'FedEx'
    tracking_number VARCHAR(100) NOT NULL UNIQUE,          -- Unique tracking code
    shipment_status VARCHAR(30) NOT NULL CHECK(
        shipment_status IN ('Pending', 'In_Transit', 'Out_For_Delivery', 'Delivered', 'Returned', 'Failed')
    ),
    shipping_address TEXT NOT NULL,
    shipped_at TIMESTAMP,
    estimated_delivery DATE,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS shipment_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER NOT NULL,
    event_description VARCHAR(255) NOT NULL,               -- e.g., 'Package scanned at hub'
    facility_location VARCHAR(100) NOT NULL,               -- e.g., 'Madrid Central Hub'
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id) ON DELETE CASCADE
);

-- Indexing Recommendations for Shipments:
CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON shipments(order_id);
CREATE INDEX IF NOT EXISTS idx_shipments_status_delivery ON shipments(shipment_status, estimated_delivery);
CREATE INDEX IF NOT EXISTS idx_shipment_events_shipment_time ON shipment_events(shipment_id, event_timestamp);

/*
=== SAMPLE QUERY & OUTPUT: SHIPMENTS & TRACKING MILESTONES ===
SELECT 
    s.shipment_id, 
    s.order_id, 
    s.carrier_name, 
    s.tracking_number, 
    s.shipment_status, 
    s.estimated_delivery,
    e.event_description,
    e.facility_location,
    e.event_timestamp
FROM shipments s
JOIN shipment_events e ON s.shipment_id = e.shipment_id;

OUTPUT:
shipment_id | order_id | carrier_name | tracking_number  | shipment_status | estimated_delivery | event_description               | facility_location  | event_timestamp
------------+----------+--------------+------------------+-----------------+--------------------+---------------------------------+--------------------+-------------------
1           | 1001     | DHL Express  | TRK-2025-QC-8921 | In_Transit      | 2028-04-02         | Package scanned and sorted hub  | Madrid Central Hub | 2028-03-30 14:22:00
*/


-- =====================================================================
-- 2. PRODUCT INVENTORY SCHEMA
-- =====================================================================
-- Design: Decoupled into `warehouses` (locations) and `product_inventory` 
-- (stock per product per warehouse) to eliminate transitive dependencies.

CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS product_inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    quantity_on_hand INTEGER NOT NULL DEFAULT 0 CHECK(quantity_on_hand >= 0),
    quantity_reserved INTEGER NOT NULL DEFAULT 0 CHECK(quantity_reserved >= 0),
    reorder_threshold INTEGER NOT NULL DEFAULT 10 CHECK(reorder_threshold >= 0),
    last_restocked_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE RESTRICT,
    UNIQUE(product_id, warehouse_id)                       -- Prevents duplicate entries per warehouse
);

-- Indexing Recommendations for Inventory:
CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON product_inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_low_stock ON product_inventory(quantity_on_hand, reorder_threshold);

/*
=== SAMPLE QUERY & OUTPUT: WAREHOUSE STOCK LEVEL ===
SELECT 
    w.warehouse_name, 
    w.city, 
    p.product_name, 
    p.category,
    i.quantity_on_hand, 
    i.quantity_reserved, 
    i.reorder_threshold,
    (i.quantity_on_hand - i.quantity_reserved) AS available_to_sell
FROM product_inventory i 
JOIN warehouses w ON i.warehouse_id = w.warehouse_id 
JOIN products p ON i.product_id = p.product_id;

OUTPUT:
warehouse_name       | city   | product_name   | category    | on_hand | reserved | threshold | available_to_sell
---------------------+--------+----------------+-------------+---------+----------+-----------+------------------
QuickCart Madrid Hub | Madrid | Wireless Mouse | Electronics | 150     | 15       | 25        | 135
*/


-- =====================================================================
-- 3. CUSTOMER SUPPORT TICKETS SCHEMA
-- =====================================================================
-- Design: Normalized into `support_tickets` (ticket lifecycle) and 
-- `ticket_messages` (thread of messages between customer & support agent).

CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_id INTEGER,                                      -- Optional: ticket may be general or order-specific
    issue_category VARCHAR(50) NOT NULL CHECK(
        issue_category IN ('Delivery_Delay', 'Damaged_Product', 'Refund_Request', 'Account_Issue', 'General_Inquiry')
    ),
    priority_level VARCHAR(20) NOT NULL DEFAULT 'Medium' CHECK(
        priority_level IN ('Low', 'Medium', 'High', 'Urgent')
    ),
    ticket_status VARCHAR(20) NOT NULL DEFAULT 'Open' CHECK(
        ticket_status IN ('Open', 'In_Progress', 'Resolved', 'Closed')
    ),
    subject VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ticket_messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    sender_type VARCHAR(20) NOT NULL CHECK(
        sender_type IN ('Customer', 'Agent', 'System')
    ),
    message_body TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES support_tickets(ticket_id) ON DELETE CASCADE
);

-- Indexing Recommendations for Support Tickets:
CREATE INDEX IF NOT EXISTS idx_tickets_customer_id ON support_tickets(customer_id);
CREATE INDEX IF NOT EXISTS idx_tickets_order_id ON support_tickets(order_id);
CREATE INDEX IF NOT EXISTS idx_tickets_queue ON support_tickets(ticket_status, priority_level, created_at);
CREATE INDEX IF NOT EXISTS idx_ticket_messages_ticket ON ticket_messages(ticket_id, sent_at);

/*
=== SAMPLE QUERY & OUTPUT: SUPPORT TICKET & MESSAGE THREAD ===
SELECT 
    t.ticket_id, 
    c.customer_name, 
    t.issue_category, 
    t.priority_level, 
    t.ticket_status, 
    m.sender_type, 
    m.message_body,
    m.sent_at
FROM support_tickets t
JOIN customers c ON t.customer_id = c.customer_id
JOIN ticket_messages m ON t.ticket_id = m.ticket_id;

OUTPUT:
ticket_id | customer_name      | issue_category | priority | status      | sender   | message_body                                            | sent_at
----------+--------------------+----------------+----------+-------------+----------+---------------------------------------------------------+-------------------
1         | Miss Olivia Taylor | Delivery_Delay | High     | In_Progress | Customer | Hello, my order tracking has not updated since yesterday | 2026-10-22 16:34:00
*/
