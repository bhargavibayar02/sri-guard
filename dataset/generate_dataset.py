# generate_dataset.py
# Generates 100 fake bank employees + their activity logs.
# 90% behave normally, 10% behave suspiciously (to give our ML model
# real anomalies to detect).
#
# Run with: python generate_dataset.py  (from inside the dataset/ folder)

import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # fixed seed so results are reproducible for your demo

DEPARTMENTS = ["Finance", "IT", "HR", "Operations", "Compliance"]
ROLES = {
    "Finance": ["Financial Analyst", "Accountant", "Finance Manager"],
    "IT": ["System Admin", "Software Engineer", "IT Support"],
    "HR": ["HR Executive", "HR Manager", "Recruiter"],
    "Operations": ["Operations Analyst", "Branch Manager", "Teller"],
    "Compliance": ["Compliance Officer", "Risk Analyst", "Auditor"],
}
DEVICES = ["Laptop-Win10", "Laptop-Win11", "Desktop-Office", "MacBook-Pro"]
UNKNOWN_DEVICES = ["Unknown-Device-X1", "Personal-Android", "Unregistered-PC"]
LOCATIONS = ["Mumbai-HQ", "Delhi-Branch", "Bangalore-Branch", "Chennai-Branch", "Remote-VPN"]
UNUSUAL_LOCATIONS = ["Unknown-Location", "Foreign-IP-Russia", "Foreign-IP-Nigeria"]
DATABASES = ["None", "Customer DB", "Finance DB", "HR DB", "Payroll DB"]

FIRST_NAMES = ["Arjun", "Priya", "Rahul", "Sneha", "Vikram", "Anita", "Karan", "Divya",
               "Rohan", "Neha", "Amit", "Pooja", "Sanjay", "Kavya", "Manish", "Ritu",
               "Deepak", "Shreya", "Nikhil", "Meera"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Iyer", "Reddy", "Nair", "Gupta", "Singh",
              "Rao", "Mehta", "Joshi", "Kapoor", "Malhotra", "Chopra", "Desai"]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_employees(n=100):
    """Creates the employees.csv file."""
    employees = []
    for i in range(1, n + 1):
        emp_id = f"EMP{i:03d}"
        dept = random.choice(DEPARTMENTS)
        role = random.choice(ROLES[dept])
        working_hours = "09:00-18:00"
        employees.append({
            "employee_id": emp_id,
            "name": random_name(),
            "department": dept,
            "role": role,
            "normal_working_hours": working_hours,
            "registered_face_path": f"registered_faces/{emp_id}.jpg",
        })

    with open("employees.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=employees[0].keys())
        writer.writeheader()
        writer.writerows(employees)

    print(f"Generated {n} employees -> employees.csv")
    return employees


def generate_normal_log(emp_id, base_date):
    """A log entry that looks like normal, safe behavior."""
    login_hour = random.randint(9, 17)  # within normal working hours
    login_time = base_date.replace(hour=login_hour, minute=random.randint(0, 59))
    return {
        "employee_id": emp_id,
        "login_time": login_time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": random.choice(DEVICES),
        "ip_address": f"10.0.{random.randint(0,10)}.{random.randint(1,254)}",
        "failed_logins": random.choice([0, 0, 0, 1]),
        "files_downloaded": random.randint(0, 15),
        "usb_connected": False,
        "database_access": random.choice(["None", "None", "Customer DB"]),
        "admin_access": False,
        "location": random.choice(LOCATIONS),
    }


def generate_suspicious_log(emp_id, base_date):
    """A log entry engineered to look like insider-threat behavior."""
    # Unusual login time: very early morning or late night
    login_hour = random.choice([0, 1, 2, 3, 22, 23])
    login_time = base_date.replace(hour=login_hour, minute=random.randint(0, 59))

    return {
        "employee_id": emp_id,
        "login_time": login_time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": random.choice(UNKNOWN_DEVICES),
        "ip_address": f"185.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
        "failed_logins": random.randint(3, 8),
        "files_downloaded": random.randint(500, 2000),
        "usb_connected": True,
        "database_access": random.choice(["Finance DB", "Payroll DB", "HR DB"]),
        "admin_access": random.choice([True, False]),
        "location": random.choice(UNUSUAL_LOCATIONS),
    }


def generate_logs(employees, days_back=7):
    """Creates the employee_logs.csv file. Each employee gets 1-3 log entries
    across the last `days_back` days. 10% of employees are marked suspicious
    and get suspicious-looking logs; the rest are normal."""

    logs = []
    num_suspicious = int(len(employees) * 0.10)
    suspicious_ids = set(
        emp["employee_id"] for emp in random.sample(employees, num_suspicious)
    )

    print(f"Marking {len(suspicious_ids)} employees as suspicious: {sorted(suspicious_ids)}")

    for emp in employees:
        emp_id = emp["employee_id"]
        is_suspicious = emp_id in suspicious_ids
        num_entries = random.randint(2, 4)

        for _ in range(num_entries):
            days_ago = random.randint(0, days_back - 1)
            base_date = datetime.now() - timedelta(days=days_ago)

            if is_suspicious and random.random() < 0.6:
                # Suspicious employees mostly generate suspicious logs,
                # but occasionally look normal too (more realistic)
                logs.append(generate_suspicious_log(emp_id, base_date))
            else:
                logs.append(generate_normal_log(emp_id, base_date))

    with open("employee_logs.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=logs[0].keys())
        writer.writeheader()
        writer.writerows(logs)

    print(f"Generated {len(logs)} log entries -> employee_logs.csv")


if __name__ == "__main__":
    employees = generate_employees(100)
    generate_logs(employees)
    print("\nDataset generation complete!")
    print("Files created: employees.csv, employee_logs.csv")
    print("Note: registered_faces/ images will be added in Phase 7 (Face Verification)")