# Part 2 – NoSQL Database Analysis (MongoDB)

## Objective

The objective of Part 2 is to analyze the suitability of a NoSQL database for managing a highly diverse product catalog and to implement practical MongoDB operations.

---

## Description

As FlexiMart expands its product catalog, the data becomes increasingly heterogeneous, with different products having different attributes and nested data such as customer reviews. This part evaluates the limitations of relational databases for such use cases and demonstrates how MongoDB can address these challenges.

---

## Tasks Completed

### Theory Analysis
- Identified limitations of relational databases for flexible product schemas
- Explained how MongoDB supports schema flexibility and embedded documents
- Discussed trade-offs of using MongoDB compared to MySQL

### Practical Implementation
- Inserted product catalog data into MongoDB
- Executed queries for:
  - Category-based filtering
  - Price-based filtering
  - Aggregation on embedded reviews
  - Update operations
  - Category-level analytics

---

## Files Included

- `nosql_analysis.md` – Theoretical analysis of NoSQL usage
- `mongodb_operations.js` – MongoDB CRUD and aggregation operations
- `products_catalog.json` – Sample product catalog data

---

## Outcome

This part demonstrates how MongoDB enables flexible schema design, efficient handling of nested data, and scalable querying for modern e-commerce platforms.
