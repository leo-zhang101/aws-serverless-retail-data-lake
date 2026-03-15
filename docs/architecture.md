# Architecture

Medallion layout: raw → bronze → silver → gold. Data flows from CSV through Glue ETL to Athena/dbt.

## Flow

```
Sample CSV → Lambda → raw/ → Glue raw_to_bronze → bronze/
                                         → Glue bronze_to_silver → silver/
                                         → Glue silver_to_gold → gold/
                                                                    → Athena (external tables)
                                                                    → dbt (marts)
                                                                    → QuickSight
```

## Layers

| Layer | Format | Notes |
|-------|--------|-------|
| Raw | CSV | As-landed. load_date partition. |
| Bronze | Parquet | + ingestion_ts, load_date, source_table. Overwrite per partition. |
| Silver | Parquet | Cleaned, deduped, typed. Metadata cols dropped. |
| Gold | Parquet | Analytics tables + pass-through dims. |

## Design notes

- **load_date partition**: Daily batch. Athena can prune by partition.
- **Overwrite**: Full refresh per load_date. No merge/upsert.
- **Left joins**: Orders without store_id still appear in daily_sales (store_state=Unknown).
- **Skip missing tables**: One failed read doesn't kill the job.
- **Athena over Redshift**: Cheaper for small data; no cluster.
- **dbt on Athena**: Glue does ETL; dbt does modelling and tests.
