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

- AWS S3
- AWS Glue (PySpark ETL)
- AWS Athena
- AWS Lambda
- AWS EventBridge
- Terraform
- Python
- Parquet
- dbt (analytics modelling)

---

# Project Structure
