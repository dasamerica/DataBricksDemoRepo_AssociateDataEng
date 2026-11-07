# Databricks notebook source
# MAGIC %sql
# MAGIC USE CATALOG demoworkspace;
# MAGIC USE schema default;
# MAGIC
# MAGIC SHOW TABLES;
# MAGIC
# MAGIC SHOW TABLES in global_temp;
# MAGIC
# MAGIC
# MAGIC SELECT * FROM global_temp.global_temp_view_latest_phones;