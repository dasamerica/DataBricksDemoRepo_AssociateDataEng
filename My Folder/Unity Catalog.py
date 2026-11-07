# Databricks notebook source
# MAGIC %sql
# MAGIC select current_metastore()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS demoworkspace.hr_db;
# MAGIC
# MAGIC CREATE TABLE demoworkspace.hr_db.employees (id INT, name STRING, salary DOUBLE, city STRING);
# MAGIC
# MAGIC INSERT INTO demoworkspace.hr_db.employees
# MAGIC VALUES (1, "Anna", 2500, "Paris"),
# MAGIC        (2, "Thomas", 3000, "London"),
# MAGIC        (3, "Bilal", 3500, "Paris"),
# MAGIC        (4, "Maya", 2000, "Paris"),
# MAGIC        (5, "Sophie", 2500, "London"),
# MAGIC        (6, "Adam", 3500, "London"),
# MAGIC        (7, "Ali", 3000, "Paris");
# MAGIC
# MAGIC CREATE VIEW demoworkspace.hr_db.paris_employees_vw
# MAGIC AS SELECT * FROM demoworkspace.hr_db.employees WHERE city = 'Paris';

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED demoworkspace.hr_db.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT SELECT ON TABLE demoworkspace.hr_db.employees TO `account users`;

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT USE SCHEMA on SCHEMA demoworkspace.hr_db to `account users`;
# MAGIC     
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT USE CATALOG on CATALOG demoworkspace to `account users`

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from system.access.audit