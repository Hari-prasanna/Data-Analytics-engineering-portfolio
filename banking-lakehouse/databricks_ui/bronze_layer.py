# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC > #**Auto loader**

# COMMAND ----------


#config
source_data = "s3://hari-data-engineering-workspace/banking-lakehouse/raw_data/"

target_table = "banking_lakehouse.bronze.raw_transactions"

clipboard = "s3://hari-data-engineering-workspace/banking-lakehouse/checkpoints/raw_transactions/"

#reading_s3

df_raw = (spark.readStream
          .format("cloudFiles") #activates the auto loader
          .option("cloudFiles.format","csv")
          .option("cloudFiles.inferColumnTypes", "true")
          .option("header","true")
          .option("cloudFiles.schemaLocation", clipboard) # auto loader to save the info to clipbaord
          .load(source_data)
          )
#writing_as_delta_table

query = (df_raw.writeStream
         .format("delta")
         .option("checkpointLocation",clipboard)
         .trigger(availableNow=True)
         .table(target_table)
        )

query.awaitTermination()
print(f"data is landed in {target_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC # Check

# COMMAND ----------

# MAGIC %sql
# MAGIC
#MAGIC SELECT *
# MAGIC FROM banking_lakehouse.bronze.raw_transactions
# MAGIC ORDER BY step
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC Droping test

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DROP TABLE IF EXISTS banking_lakehouse.bronze.raw_transactions;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER SCHEMA banking_lakehouse.bronze
# MAGIC ENABLE PREDICTIVE OPTIMIZATION;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DESCRIBE DETAIL banking_lakehouse.bronze.raw_transactions
