import mysql.connector
import csv
from datetime import datetime
import os


REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="atm_monitoring"
)

cursor = conn.cursor(dictionary=True)


cursor.execute("""
    SELECT 
        DATE(transaction_time) AS day,
        COUNT(*) AS total_transactions,
        SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_transactions,
        SUM(amount) AS total_amount
    FROM transactions
    GROUP BY DATE(transaction_time)
    ORDER BY day
""")

daily_rows = cursor.fetchall()

with open(os.path.join(REPORTS_DIR, "daily_summary_report.csv"),
          "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Date",
        "Total Transactions",
        "Failed Transactions",
        "Total Amount"
    ])

    for row in daily_rows:
        writer.writerow([
            row["day"],
            row["total_transactions"],
            row["failed_transactions"],
            row["total_amount"]
        ])


fraud_alerts = []

# Rule 1: High Frequency Withdrawals
cursor.execute("""
    SELECT customer_id, COUNT(*) AS txn_count
    FROM transactions
    WHERE transaction_type = 'withdrawal'
      AND transaction_time >= NOW() - INTERVAL 1 HOUR
    GROUP BY customer_id
    HAVING COUNT(*) > 3
""")

for row in cursor.fetchall():
    fraud_alerts.append([
        "High Frequency Withdrawals",
        row["customer_id"],
        f"Withdrawals: {row['txn_count']}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])

# Rule 2: High Amount Withdrawal
cursor.execute("""
    SELECT customer_id, amount
    FROM transactions
    WHERE amount > 50000
""")

for row in cursor.fetchall():
    fraud_alerts.append([
        "High Amount Withdrawal",
        row["customer_id"],
        f"Amount: {row['amount']}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])

# Rule 3: Multiple ATM Usage
cursor.execute("""
    SELECT customer_id, COUNT(DISTINCT atm_id) AS atm_count
    FROM transactions
    WHERE transaction_time >= NOW() - INTERVAL 1 HOUR
    GROUP BY customer_id
    HAVING COUNT(DISTINCT atm_id) > 1
""")

for row in cursor.fetchall():
    fraud_alerts.append([
        "Multiple ATM Usage",
        row["customer_id"],
        f"ATMs Used: {row['atm_count']}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])

# Rule 4: Failed PIN Attempts
cursor.execute("""
    SELECT customer_id, COUNT(*) AS failed_attempts
    FROM transactions
    WHERE status = 'failed'
      AND transaction_type = 'withdrawal'
      AND transaction_time >= NOW() - INTERVAL 1 HOUR
    GROUP BY customer_id
    HAVING COUNT(*) > 3
""")

for row in cursor.fetchall():
    fraud_alerts.append([
        "Failed PIN Attempts",
        row["customer_id"],
        f"Failed Attempts: {row['failed_attempts']}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])

total_frauds = len(fraud_alerts)

with open(os.path.join(REPORTS_DIR, "fraud_alerts.csv"),
          "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Fraud Rule",
        "Customer ID",
        "Details",
        "Detected Time"
    ])

    writer.writerows(fraud_alerts)
    writer.writerow([])
    writer.writerow(["TOTAL FRAUDS DETECTED", total_frauds])


cursor.close()
conn.close()
