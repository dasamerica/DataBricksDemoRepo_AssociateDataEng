# Databricks notebook source
# MAGIC %md
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../../Databricks-Certified-Data-Engineer-Associate/Includes/Copy-Datasets

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_bookstore}/customers-json")
display(files)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json/export_001.json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json/export_*.json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM json.`${dataset.bookstore}/customers-json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *,
# MAGIC     input_file_name() source_file
# MAGIC   FROM json.`${dataset.bookstore}/customers-json`;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM text.`${dataset.bookstore}/customers-json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM binaryFile.`${dataset.bookstore}/customers-json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM csv.`${dataset.bookstore}/books-csv`

# COMMAND ----------

# DBTITLE 1,Célula 12
dbutils.widgets.text("external_location", "abfss://unity-catalog-storage@dbstorage5nuhdkogzauf2.dfs.core.windows.net/7405616581380398/external_storage")

external_location = dbutils.widgets.get("external_location")
if "<EXTERNAL-URL>" in external_location:
    external_location = "abfss://unity-catalog-storage@dbstorage5nuhdkogzauf2.dfs.core.windows.net/7405616581380398/external_storage"
dbutils.fs.cp(f"{dataset_bookstore}/books-csv", f"{external_location}/books-csv", recurse=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE books_csv
# MAGIC   (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
# MAGIC USING CSV
# MAGIC OPTIONS (
# MAGIC   header = "true",
# MAGIC   delimiter = ";"
# MAGIC )
# MAGIC LOCATION "${external_location}/books-csv"

# COMMAND ----------

# DBTITLE 1,Cell 14
# MAGIC %sql
# MAGIC SELECT book_id, title, author, category, CAST(price AS DOUBLE) AS price
# MAGIC FROM read_files(
# MAGIC   'abfss://unity-catalog-storage@dbstorage5nuhdkogzauf2.dfs.core.windows.net/7405616581380398/external_storage/books-csv',
# MAGIC   format => 'csv',
# MAGIC   header => 'true',
# MAGIC   delimiter => ';'
# MAGIC )

# COMMAND ----------

# MAGIC %sql DESCRIBE EXTENDED books_csv

# COMMAND ----------

files = dbutils.fs.ls(f"{external_location}/books-csv")
display(files)

# COMMAND ----------

# DBTITLE 1,Cell 17
books_df = spark.read.table("books_csv").cache()
books_df.count()

(books_df.write
        .mode("append")
        .format("csv")
        .option('header', 'true')
        .option('delimiter', ';')
        .save(f"{external_location}/books-csv"))

# COMMAND ----------

files = dbutils.fs.ls(f"{external_location}/books-csv")
display(files)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM books_csv

# COMMAND ----------

# MAGIC %sql REFRESH TABLE books_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM books_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE customers AS
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json`;
# MAGIC
# MAGIC DESCRIBE EXTENDED customers;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE books_unparsed AS
# MAGIC SELECT * FROM csv.`${dataset.bookstore}/books-csv`;
# MAGIC
# MAGIC SELECT * FROM books_unparsed;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TEMP VIEW books_tmp_vw
# MAGIC    (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
# MAGIC USING CSV
# MAGIC OPTIONS (
# MAGIC   path = "${dataset.bookstore}/books-csv/export_*.csv",
# MAGIC   header = "true",
# MAGIC   delimiter = ";"
# MAGIC );
# MAGIC
# MAGIC CREATE TABLE books AS
# MAGIC   SELECT * FROM books_tmp_vw;
# MAGIC   
# MAGIC SELECT * FROM books

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED books
# MAGIC

# COMMAND ----------

