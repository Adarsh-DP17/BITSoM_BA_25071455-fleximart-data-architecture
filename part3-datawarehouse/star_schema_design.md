# Star Schema Design – FlexiMart Data Warehouse

## Section 1: Schema Overview

### FACT TABLE: fact_sales
**Grain:** One row per product per order line item  
**Business Process:** Sales transactions

**Measures (Numeric Facts):**
- quantity_sold: Number of units sold
- unit_price: Price per unit at time of sale
- discount_amount: Discount applied
- total_amount: Final amount (quantity × unit_price − discount)

**Foreign Keys:**
- date_key → dim_date
- product_key → dim_product
- customer_key → dim_customer

---

### DIMENSION TABLE: dim_date
**Purpose:** Enables time-based analysis  
**Type:** Conformed dimension  

**Attributes:**
- date_key (PK): Surrogate key (YYYYMMDD)
- full_date: Actual calendar date
- day_of_week: Day name
- day_of_month: Numeric day
- month: Month number
- month_name: Month name
- quarter: Financial quarter
- year: Calendar year
- is_weekend: Weekend indicator

---

### DIMENSION TABLE: dim_product
**Purpose:** Stores descriptive product details  

**Attributes:**
- product_key (PK): Surrogate key
- product_id: Source system ID
- product_name: Product name
- category: Product category
- subcategory: Product subcategory
- unit_price: Product price

---

### DIMENSION TABLE: dim_customer
**Purpose:** Stores customer demographic information  

**Attributes:**
- customer_key (PK): Surrogate key
- customer_id: Source system ID
- customer_name: Full name
- city: City
- state: State
- customer_segment: Customer type

---

## Section 2: Design Decisions

The fact table granularity is defined at the product-level per transaction, enabling highly detailed sales analysis. This allows accurate aggregation across time, customer, and product dimensions.

Surrogate keys are used in all dimension tables to improve query performance and maintain consistency, even if source system identifiers change. Natural keys can be unreliable across systems, while surrogate keys remain stable.

This design supports drill-down and roll-up analysis by leveraging hierarchical attributes in the date dimension. Analysts can move seamlessly from yearly summaries to monthly or daily sales trends, making the schema optimal for OLAP workloads.

---

## Section 3: Sample Data Flow

**Source Transaction:**  
Order #101, Customer “John Doe”, Product “Laptop”, Quantity 2, Price ₹50,000

**Data Warehouse Representation:**

**fact_sales**
