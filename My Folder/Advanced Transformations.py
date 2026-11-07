# Databricks notebook source
# MAGIC %run ./Databricks-Certified-Data-Engineer-Associate/Includes/Copy-Datasets

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id, profile:first_name, profile:address:country 
# MAGIC FROM customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT profile 
# MAGIC FROM customers 
# MAGIC LIMIT 1

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW parsed_customers AS
# MAGIC   SELECT customer_id, from_json(profile, schema_of_json('{"first_name":"Thomas","last_name":"Lane","gender":"Male","address":{"street":"06 Boulevard Victor Hugo","city":"Paris","country":"France"}}')) AS profile_struct
# MAGIC   FROM customers;
# MAGIC   
# MAGIC SELECT * FROM parsed_customers

# COMMAND ----------

# MAGIC %sql DESCRIBE parsed_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id, profile_struct.first_name, profile_struct.address.country
# MAGIC FROM parsed_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW customers_final AS
# MAGIC   SELECT customer_id, profile_struct.*
# MAGIC   FROM parsed_customers;
# MAGIC   
# MAGIC SELECT * FROM customers_final

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id, customer_id, books
# MAGIC FROM orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id, customer_id, explode(books) AS book 
# MAGIC FROM orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id,
# MAGIC   collect_set(order_id) AS orders_set,
# MAGIC   collect_set(books.book_id) AS books_set
# MAGIC FROM orders
# MAGIC GROUP BY customer_id

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id,
# MAGIC   collect_set(books.book_id) As before_flatten,
# MAGIC   array_distinct(flatten(collect_set(books.book_id))) AS after_flatten
# MAGIC FROM orders
# MAGIC GROUP BY customer_id

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW orders_enriched AS
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC   SELECT *, explode(books) AS book 
# MAGIC   FROM orders) o
# MAGIC INNER JOIN books b
# MAGIC ON o.book.book_id = b.book_id;
# MAGIC
# MAGIC SELECT * FROM orders_enriched

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW orders_updates
# MAGIC AS SELECT * FROM parquet.`${dataset.bookstore}/orders-new`;
# MAGIC
# MAGIC SELECT * FROM orders 
# MAGIC UNION 
# MAGIC SELECT * FROM orders_updates 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM orders 
# MAGIC INTERSECT 
# MAGIC SELECT * FROM orders_updates 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM orders 
# MAGIC MINUS 
# MAGIC SELECT * FROM orders_updates 

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE transactions AS
# MAGIC
# MAGIC SELECT * FROM (
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     book.book_id AS book_id,
# MAGIC     book.quantity AS quantity
# MAGIC   FROM orders_enriched
# MAGIC ) PIVOT (
# MAGIC   sum(quantity) FOR book_id in (
# MAGIC     'B01', 'B02', 'B03', 'B04', 'B05', 'B06',
# MAGIC     'B07', 'B08', 'B09', 'B10', 'B11', 'B12'
# MAGIC   )
# MAGIC );
# MAGIC
# MAGIC SELECT * FROM transactions