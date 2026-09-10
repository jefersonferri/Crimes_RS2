# Rio Grande do Sul Public Safety Data Analysis

## Overview

This project analyzes crime statistics across municipalities
in Rio Grande do Sul, Brazil, from 2016 to 2025.

The objective is to identify temporal, geographic and
behavioral patterns in crime statistics using Python,
SQL and Power BI.

## Business Questions

- How has crime evolved over time?
- Which municipalities account for the highest volume?
- Which crime categories show the strongest trends?
- Are there seasonal patterns?
- How does each municipality compare with the state average?

## Tools

- Python
- Pandas
- PostgreSQL
- SQL
- Power BI
- DAX
- Git/GitHub

## Data Pipeline

Excel → Python ETL → PostgreSQL → SQL → Power BI

ETL Challenge: The original source files available here [raw_data](raw_data/) contained different spreadsheet layouts and header positions across years. A Python/Pandas [crimes2](crimes2.py) pipeline was developed to automatically identify the header based on the "Municípios" field, normalize the monthly datasets and consolidate the historical data.

## Key Skills Demonstrated

- Data cleaning
- ETL
- Data validation
- SQL
- Data modeling
- DAX
- KPI development
- Time-series analysis
- Geographic analysis
- Data visualization

## Dashboard

[imagens do Power BI]

## Key Findings
