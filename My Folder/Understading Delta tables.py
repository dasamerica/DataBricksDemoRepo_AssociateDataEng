# Databricks notebook source
# MAGIC %sql
# MAGIC USE CATALOG default

# COMMAND ----------

# DBTITLE 1,Create employees table
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS demoworkspace.default.employees
# MAGIC (id INT, name STRING, salary DOUBLE)
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO demoworkspace.default.employees
# MAGIC VALUES 
# MAGIC   (1, "Adam", 3500.0),
# MAGIC   (2, "Sarah", 4020.5);
# MAGIC
# MAGIC INSERT INTO demoworkspace.default.employees
# MAGIC VALUES
# MAGIC   (3, "John", 2999.3),
# MAGIC   (4, "Thomas", 4000.3);
# MAGIC
# MAGIC INSERT INTO demoworkspace.default.employees
# MAGIC VALUES
# MAGIC   (5, "Anna", 2500.0);
# MAGIC
# MAGIC INSERT INTO demoworkspace.default.employees
# MAGIC VALUES
# MAGIC   (6, "Kim", 6200.3)
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql DESCRIBE DETAIL demoworkspace.default.employees

# COMMAND ----------

# DBTITLE 1,Inspect employees table details
# MAGIC %sql
# MAGIC DESCRIBE DETAIL demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE demoworkspace.default.employees 
# MAGIC SET salary = salary + 100
# MAGIC WHERE name LIKE "A%"

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql DESCRIBE HISTORY demoworkspace.default.employees