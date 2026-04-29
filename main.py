# main.py
# -------------------------------------------------------
# Entry point — run this file to trigger the scan
# Usage:  python main.py
#         python main.py --add       (add a product interactively)
#         python main.py --history   (show past alert logs)
# -------------------------------------------------------

import argparse
from scanner.alert_scanner import run_scan
from reports.report_generator import generate_report
from utils.add_product import add_product_interactive
from utils.view_history import view_alert_history


def main():
    parser = argparse.ArgumentParser(description="Expired Product Alert System")
    parser.add_argument("--add",     action="store_true", help="Add a new product to the database")
    parser.add_argument("--history", action="store_true", help="View past alert log entries")
    args = parser.parse_args()

    if args.add:
        add_product_interactive()
    elif args.history:
        view_alert_history()
    else:
        flagged = run_scan()
        generate_report(flagged)


if __name__ == "__main__":
    main()
