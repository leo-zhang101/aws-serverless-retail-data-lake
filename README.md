# AWS Serverless Retail Data Platform

This repository contains a serverless data platform built on AWS.  
The project demonstrates a realistic end-to-end data pipeline using tools commonly used in modern data engineering roles.

The pipeline ingests retail transaction data, processes it through a **Medallion architecture (Raw → Bronze → Silver → Gold)** and exposes analytics tables that can be queried with **Athena**.

The dataset models a simplified **Australian retail scenario (AUD currency, NSW/VIC/QLD regions)**.

---

## Architecture

![Architecture](docs/architecture.png)

Pipeline flow:

CSV → Lambda → S3 Raw → Glue ETL → Bronze → Silver → Gold → Athena

---

## Tech Stack

- AWS S3
- AWS Glue (PySpark)
- AWS Athena
- AWS Lambda
- AWS EventBridge
- Terraform
- Python
- Parquet
- dbt

---

## Project Structure
