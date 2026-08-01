# Architecture

## Project Name

Israel Economic Data Platform

## Business Goal

The platform collects, stores, processes, and exposes official Israeli economic and labor-market data for analysis and decision-making.

The first version focuses on:

- Job vacancies
- Unemployment
- Salaries
- Industries
- Regions

Future versions may include:

- Consumer Price Index
- Bank of Israel interest rate
- Population
- Exchange rates

## Main Technologies

- Google Cloud Platform
- Cloud Storage
- BigQuery
- Python
- Cloud Run Jobs
- Cloud Scheduler
- Power BI
- GitHub

## High-Level Architecture

```text
Official Data Sources
CBS / Bank of Israel / Government APIs
                |
                v
Cloud Run Job - Python Ingestion
                |
                v
Cloud Storage Data Lake
landing / archive / rejected / metadata / logs
                |
                v
BigQuery RAW
                |
                v
BigQuery STG
Data cleaning, validation and standardization
                |
                v
BigQuery DWH
Dimensions and Facts
                |
                v
BigQuery MART
Business views and analytical datasets
                |
                v
Power BI

```text
Add initial architecture documentation
