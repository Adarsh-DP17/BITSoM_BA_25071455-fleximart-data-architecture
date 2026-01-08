Entity–Relationship Description

ENTITY: customers
Purpose: Stores customer details
Attributes:

customer_id (PK)

first_name

last_name

email (unique)

phone

city

registration_date

Relationships:

One customer → many orders (1:M)

ENTITY: products
Purpose: Stores product catalog
Attributes: product_id (PK), product_name, category, price, stock_quantity

ENTITY: orders
Purpose: Stores customer orders
Attributes: order_id (PK), customer_id (FK), order_date, total_amount, status

ENTITY: order_items
Purpose: Line-item level order details
Attributes: order_item_id (PK), order_id (FK), product_id (FK), quantity, unit_price, subtotal

Normalization (3NF Explanation – ~220 words)

This database design follows Third Normal Form (3NF) principles. All tables are structured such that non-key attributes depend only on the primary key and not on other non-key attributes.

Functional dependencies are clearly separated: customer information depends solely on customer_id, product details depend on product_id, and transactional data is split into orders and order_items. This separation eliminates redundancy such as repeating product prices or customer emails across orders.

Update anomalies are avoided because changing a customer’s email or a product’s price requires updating only one record. Insert anomalies are prevented since products and customers can exist independently of orders. Delete anomalies are eliminated by separating master and transactional data—deleting an order does not remove product or customer records.

Thus, the schema maintains data integrity, efficiency, and scalability.