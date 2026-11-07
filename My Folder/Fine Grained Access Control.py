# Databricks notebook source
run ../../Databricks-Certified-Data-Engineer-Associate/Includes/Copy-Datasets

# COMMAND ----------

# MAGIC %sql DESCRIBE TABLE customers_details

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW customers_vw AS
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     CASE 
# MAGIC       WHEN is_account_group_member('admins_demo') THEN email
# MAGIC       ELSE 'REDACTED'
# MAGIC     END AS email,
# MAGIC     gender,
# MAGIC     CASE 
# MAGIC       WHEN is_account_group_member('admins_demo') THEN first_name
# MAGIC       ELSE 'REDACTED'
# MAGIC     END AS first_name,
# MAGIC     CASE 
# MAGIC       WHEN is_account_group_member('admins_demo') THEN last_name
# MAGIC       ELSE 'REDACTED'
# MAGIC     END AS last_name,
# MAGIC     CASE 
# MAGIC       WHEN is_account_group_member('admins_demo') THEN street
# MAGIC       ELSE 'REDACTED'
# MAGIC     END AS street,
# MAGIC     city,
# MAGIC     country
# MAGIC   FROM customers_details

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers_vw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers_vw
# MAGIC WHERE 
# MAGIC   CASE 
# MAGIC     WHEN is_account_group_member('admins_demo') THEN TRUE
# MAGIC     ELSE country = "France"
# MAGIC   END

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION mask_email(email STRING)
# MAGIC RETURN CASE WHEN is_account_group_member('admins_demo') THEN email
# MAGIC             ELSE '***@***.***'
# MAGIC        END;

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE customers_details ALTER COLUMN email SET MASK mask_email;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION geo_filter(country STRING)
# MAGIC RETURN IF(is_account_group_member('admins_demo'), true, country="France");

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE customers_details SET ROW FILTER geo_filter ON (country);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers_details

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE customers_details ALTER COLUMN email DROP MASK;
# MAGIC ALTER TABLE customers_details DROP ROW FILTER;

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE customers_details SET TAGS ('geo_restricted');
# MAGIC
# MAGIC ALTER TABLE customers_details ALTER COLUMN country SET TAGS ('geo_restricted');

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE customers_details ALTER COLUMN email SET TAGS ('pii' = 'email_address');

# COMMAND ----------

# DBTITLE 1,Create masking policy
# MAGIC %sql
# MAGIC CREATE OR REPLACE POLICY pii_email_masking_policy
# MAGIC ON SCHEMA demoworkspace.default
# MAGIC COLUMN MASK mask_email
# MAGIC TO `account users` 
# MAGIC FOR TABLES
# MAGIC MATCH COLUMNS has_tag_value('pii','email_address') AS e
# MAGIC ON COLUMN e

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE POLICY geo_filtering_policy
# MAGIC ON SCHEMA demoworkspace.default
# MAGIC ROW FILTER demoworkspace.default.geofilter
# MAGIC TO `account users` 
# MAGIC FOR TABLES
# MAGIC WHEN true
# MAGIC MATCH COLUMNS (city, country) AS g
# MAGIC USING COLUMNS (g)

# COMMAND ----------

# DBTITLE 1,Create geo filtering policy
# MAGIC %sql
# MAGIC CREATE OR REPLACE POLICY geo_filtering_policy
# MAGIC ON SCHEMA demoworkspace.default
# MAGIC ROW FILTER demoworkspace.default.geo_filter
# MAGIC TO `account users` 
# MAGIC FOR TABLES
# MAGIC WHEN has_tag('geo_restricited')
# MAGIC MATCH COLUMNS has_tag('geo_restricited') AS g
# MAGIC USING COLUMNS (g)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers_details