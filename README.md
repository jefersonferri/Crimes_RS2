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

ETL Challenge:  The data was downloaded from the Public Safety Secretariat of Rio Grande do Sul, Brazil [SSP/RS](https://www.ssp.rs.gov.br/indicadores-criminais). Because the original files had varying spreadsheet layouts and inconsistent header positions across different years, a Python/Pandas pipeline [crimes2.py](crimes2.py) was developed. This script automatically identifies the correct header row by locating the "Municípios" field, normalizes the monthly datasets, and consolidates the historical data. Following this automated consolidation, some remaining noise was manually cleaned using Excel. The final, cleaned dataset is available in [crimes_RS_compilado](crimes_RS_compilado.xlsx).

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
