# AWS Serverless Retail Data Platform

Production-style **serverless data lake platform** for retail analytics built on AWS using **S3, Glue, Athena, Lambda and Terraform**.

This project demonstrates how a modern **Medallion Architecture (Raw → Bronze → Silver → Gold)** pipeline can be implemented using fully serverless AWS services.

The project uses an **Australian retail context (AUD, NSW, VIC, QLD)** to reflect the market I am targeting as a Data Engineer.

---

# Architecture

![Architecture](docs/architecture.png)

Pipeline overview:

CSV Data → Lambda → S3 Raw → Glue ETL → Bronze → Silver → Gold → Athena Analytics

---

# Tech Stack

AWS S3  
AWS Glue (PySpark ETL)  
AWS Athena  
AWS Lambda  
AWS EventBridge  
Terraform  
Python  
Parquet  
dbt  

---

# Project Structure

serverless-aws-data-platform

ingestion/                 Lambda ingestion logic  
glue_jobs/                 ETL jobs (raw → bronze → silver → gold)  
infrastructure/terraform/  Infrastructure as Code  
sql/athena/                Athena table definitions and queries  
dbt/                       Analytics models  
tests/                     Data pipeline tests  
docs/                      Architecture and runbooks  
sample_data/               Sample retail datasets  

---

# Pipeline Flow

1. Lambda uploads raw CSV files into the **S3 raw layer**
2. Glue job **raw_to_bronze** converts raw CSV files into **Parquet datasets**
3. Glue job **bronze_to_silver** cleans and standardizes the data
4. Glue job **silver_to_gold** produces analytics-ready tables
5. Athena queries **Gold tables** for business analytics

---

# Medallion Data Lake Layers

Raw Layer

Original CSV files uploaded by Lambda ingestion.

Bronze Layer

Raw data converted into Parquet format with minimal transformation.

Silver Layer

Cleaned and standardized datasets.

Gold Layer

Analytics-ready aggregated tables used for reporting and business insights.

---

# Gold Analytics Tables

daily_sales

Daily revenue metrics aggregated by state.

product_performance

Product-level sales and revenue analysis.

customer_value

Customer lifetime value metrics.

All tables are partitioned by **load_date** to improve Athena query performance.

---

# Key Outcomes

This project demonstrates the ability to:

Build a **serverless Medallion data lake architecture**

Ingest retail datasets using **AWS Lambda**

Transform raw CSV data into **analytics-ready Parquet datasets**

Run distributed ETL with **AWS Glue**

Query partitioned analytics tables using **Athena**

Provision cloud infrastructure using **Terraform**

---

# Design Decisions

Athena over Redshift

Athena was chosen because:

Serverless architecture  
No cluster management  
Low cost for ad-hoc analytics  

---

load_date parameter

The pipeline supports a **load_date parameter** to:

Enable reproducible pipeline runs  
Support backfills  
Simplify debugging  

---

Overwrite vs Append

Overwrite is used instead of append because:

Simpler for a portfolio project  
Easier to validate transformations  

---

Left Joins

Reference tables use **left joins** to prevent data loss when dimension data is incomplete.

---

# Data Storage Optimization

Datasets are stored in **Parquet format** to reduce storage cost and improve query performance.

Gold tables are **partitioned by load_date** to optimize Athena queries.

---

# Runtime Evidence

Example Athena query:

SELECT *
FROM daily_sales
WHERE load_date = '2024-03-14';

Query Result:

![Athena Query Result](docs/athena_query_result.png)

The successful query confirms that:

Glue ETL jobs executed successfully  
Gold tables were generated correctly  
Athena can query the serverless data lake  

---

# Data Quality

Basic validation rules are applied during transformation.

Examples:

customer_id must not be null  

order_id must be unique  

amount_aud must be greater than 0  

quantity must be greater than 0  

More details:

docs/data_quality_checks.md

---

# Estimated Cost

This project uses a fully serverless architecture.

Estimated monthly cost for small datasets:

S3 storage: < $1  
Glue jobs: < $5  
Athena queries: < $2  
Lambda execution: < $1  

Total estimated monthly cost: **under $10 per month**

---

# Current Scope

Lambda ingestion  
Medallion ETL pipeline  
Athena analytics queries  
Terraform infrastructure provisioning  
Basic data quality validation  

---

# Limitations

Sample datasets only  

No CDC ingestion  

Glue jobs executed manually  

Limited monitoring and alerting  

No CI/CD deployment pipeline  

---

# Future Improvements

Add Step Functions orchestration  

Add CI/CD pipeline for Terraform and Glue  

Add automated data quality validation  

Add monitoring and alerting  

Add dashboard layer (QuickSight or Streamlit)  

---

# Why This Project

This project demonstrates **end-to-end Data Engineering capabilities**:

Data ingestion  

ETL pipeline design  

Analytics modelling  

Cloud infrastructure automation  

The design intentionally mirrors patterns used in **modern cloud data platforms**.
