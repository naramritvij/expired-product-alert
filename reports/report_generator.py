# reports/report_generator.py
# -------------------------------------------------------
# Generates a terminal summary + CSV report
# -------------------------------------------------------

import csv
import os
from datetime import datetime


STATUS_LABEL = {
    "EXPIRED":       "EXPIRED",
    "EXPIRING_SOON": "Expiring Soon",
}

STATUS_COLOR = {
    "EXPIRED":       "\033[91m",   # red
    "EXPIRING_SOON": "\033[93m",   # yellow
}
RESET = "\033[0m"


def print_terminal_report(products):
    """Pretty-print the flagged products to the terminal."""

    expired       = [p for p in products if p["status"] == "EXPIRED"]
    expiring_soon = [p for p in products if p["status"] == "EXPIRING_SOON"]
    total_value   = sum(p["stock_value"] for p in products)

    # Summary box
    print(f"  {'SUMMARY':}")
    print(f"  {'─'*50}")
    print(f"  {'Expired products:':<30} {len(expired)}")
    print(f"  {'Expiring soon:':<30} {len(expiring_soon)}")
    print(f"  {'Total at-risk stock value:':<30} ${total_value:,.2f}")
    print(f"  {'─'*50}\n")

    # Detail table
    header = f"  {'STATUS':<15} {'PRODUCT':<25} {'QTY':>5} {'DAYS':>6}  {'LOCATION':<20} {'VALUE':>10}"
    print(header)
    print(f"  {'─'*85}")

    for p in products:
        color = STATUS_COLOR.get(p["status"], "")
        days  = p["days_until_expiry"]
        days_str = f"{days}d" if days >= 0 else f"{abs(days)}d ago"
        line = (
            f"  {color}{STATUS_LABEL[p['status']]:<15}{RESET}"
            f" {p['product_name'][:24]:<25}"
            f" {p['quantity']:>5}"
            f" {days_str:>6}"
            f"  {(p['location'] or 'N/A')[:19]:<20}"
            f" ${p['stock_value']:>9,.2f}"
        )
        print(line)

    print(f"\n  {'─'*85}\n")


def export_csv(products):
    """Write flagged products to a timestamped CSV in the reports/ folder."""

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"reports/alert_report_{timestamp}.csv"

    fieldnames = [
        "status", "product_name", "barcode", "category_name",
        "quantity", "unit_price", "stock_value",
        "expiry_date", "days_until_expiry", "location"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for p in products:
            row = dict(p)
            if row.get("expiry_date"):
                row["expiry_date"] = row["expiry_date"].strftime("%Y-%m-%d")
            writer.writerow(row)

    print(f"  Report saved → {filename}\n")
    return filename


def generate_report(products):
    """Entry point: print terminal report + export CSV."""
    if not products:
        return

    print_terminal_report(products)
    export_csv(products)
