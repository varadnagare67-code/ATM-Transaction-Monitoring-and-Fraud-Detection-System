ATM Transaction Monitoring & Fraud Detection System
📌 Project Overview

This project is a rule-based ATM Transaction Monitoring and Fraud Detection System built using Python and MySQL.
It analyzes ATM transaction data to generate daily operational summaries and detect suspicious or fraudulent activities, exporting the results into structured CSV reports.

The system is designed as a batch-processing backend application, similar to how real-world banking monitoring systems work.

🎯 Key Features
✅ Daily Transaction Summary

Total transactions per day

Failed transactions per day

Total transaction amount per day

Exported as a single consolidated CSV file

🚨 Fraud Detection Rules

The system detects and logs fraud alerts based on the following rules:

High-frequency withdrawals (more than 3 withdrawals in 1 hour)

High-amount withdrawals (amount greater than ₹50,000)

Multiple ATM usage by the same customer within 1 hour

Failed PIN attempts (more than 3 failed withdrawals in 1 hour)

📊 Reporting

daily_summary_report.csv → operational summary

fraud_alerts.csv → all detected fraud alerts + total fraud count

Silent execution (no console output)

🛠️ Tech Stack

Programming Language: Python 3

Database: MySQL

Libraries:

mysql-connector-python

csv

Output Format: CSV files

📂 Project Structure
ATM-Fraud-Detection-System/
│
├── src/
│   └── fraud_monitor.py
│
├── sql/
│   └── schema.sql
│
├── reports/
│   ├── daily_summary_report.csv
│   └── fraud_alerts.csv
│
├── requirements.txt
└── README.md