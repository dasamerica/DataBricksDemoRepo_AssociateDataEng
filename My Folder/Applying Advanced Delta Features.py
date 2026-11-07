# Databricks notebook source
# MAGIC %sql
# MAGIC select * from demoworkspace.default.employees version as of 4

# COMMAND ----------

# MAGIC %sql
# MAGIC delete from demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC restore table demoworkspace.default.employees to version as of 5

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC optimize demoworkspace.default.employees zorder by id

# COMMAND ----------

# MAGIC %sql
# MAGIC describe detail demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC vacuum demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from demoworkspace.default.employees@v1

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table demoworkspace.default.employees

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from demoworkspace.default.employees