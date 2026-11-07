# Databricks notebook source
dbutils.widgets.text("external_location", 'abfss://unity-catalog-storage@dbstorage5nuhdkogzauf2.dfs.core.windows.net/7405616581380398')
external_location = dbutils.widgets.get("external_location")

# COMMAND ----------

# DBTITLE 1,Create and populate managed table
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS demoworkspace.default.managed_default
# MAGIC   (width INT, length INT, height INT);
# MAGIC
# MAGIC INSERT INTO demoworkspace.default.managed_default
# MAGIC VALUES (3, 2, 1)

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended demoworkspace.default.managed_default

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE demoworkspace.default.external_default
# MAGIC   (width INT, length INT, height INT)
# MAGIC LOCATION '${external_location}/external_default';
# MAGIC
# MAGIC INSERT INTO demoworkspace.default.external_default
# MAGIC VALUES (3 INT, 2 INT, 1 INT)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED demoworkspace.default.external_default

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE demoworkspace.default.managed_default;
# MAGIC
# MAGIC DROP TABLE demoworkspace.default.external_default;

# COMMAND ----------

# MAGIC %fs ls '${external_location}/external_default'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA demoworkspace.new_default

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE demoworkspace.new_default_2

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DATABASE EXTENDED demoworkspace.new_default

# COMMAND ----------

# DBTITLE 1,Create tables in new schema
# MAGIC %sql
# MAGIC USE CATALOG demoworkspace;
# MAGIC USE SCHEMA new_default;
# MAGIC
# MAGIC CREATE TABLE managed_new_default
# MAGIC   (width INT, length INT, height INT);
# MAGIC   
# MAGIC INSERT INTO managed_new_default
# MAGIC VALUES (3, 2, 1);
# MAGIC
# MAGIC -- -----------------------------------
# MAGIC
# MAGIC CREATE TABLE external_new_default
# MAGIC   (width INT, length INT, height INT)
# MAGIC LOCATION '${external_location}/external_new_default';
# MAGIC   
# MAGIC INSERT INTO external_new_default
# MAGIC VALUES (3, 2, 1);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED managed_new_default

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED external_new_default

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE managed_new_default;
# MAGIC DROP TABLE external_new_default;

# COMMAND ----------

display(dbutils.fs.ls(f'{external_location}/external_new_default'))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA custom
# MAGIC MANAGED LOCATION '${external_location}/custom'

# COMMAND ----------

spark.sql("DESCRIBE DATABASE EXTENDED custom")

# COMMAND ----------

# MAGIC %sql
# MAGIC USE SCHEMA custom;
# MAGIC
# MAGIC CREATE TABLE managed_custom
# MAGIC   (width INT, length INT, height INT);
# MAGIC   
# MAGIC INSERT INTO managed_custom
# MAGIC VALUES (3 INT, 2 INT, 1 INT);
# MAGIC
# MAGIC -----------------------------------
# MAGIC
# MAGIC CREATE TABLE external_custom
# MAGIC   (width INT, length INT, height INT)
# MAGIC LOCATION '${external_location}/external_custom';
# MAGIC   
# MAGIC INSERT INTO external_custom
# MAGIC VALUES (3 INT, 2 INT, 1 INT);

# COMMAND ----------

# MAGIC %sql DESCRIBE EXTENDED managed_custom

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED external_custom

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE managed_custom;
# MAGIC DROP TABLE external_custom;

# COMMAND ----------

display(dbutils.fs.ls(f'{external_location}/external_custom'))