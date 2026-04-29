# scanner/alert_scanner.py
# -------------------------------------------------------
# Scans Oracle DB for expired / expiring-soon products
# and writes results to the alert_log table
# -------------------------------------------------------

import cx_Oracle
from db.connection import get_connection
from datetime import datetime


def fetch_flagged_products(conn):
    """
    Pull all products whose status is EXPIRED or EXPIRING_SOON
    from the v_expiry_status view.
    """
    sql = """
        SELECT
            product_id,
            product_name,
            barcode,
            category_name,
            quantity,
            unit_price,
            stock_value,
            expiry_date,
            location,
            days_until_expiry,
            status
        FROM v_expiry_status
        WHERE status IN ('EXPIRED', 'EXPIRING_SOON')
        ORDER BY days_until_expiry ASC
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0].lower() for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows


def log_alerts(conn, flagged_products):
    """
    Insert a record into alert_log for each flagged product.
    Skips products already logged today to avoid duplicates.
    """
    check_sql = """
        SELECT COUNT(*) FROM alert_log
        WHERE product_id = :pid
        AND TRUNC(logged_at) = TRUNC(SYSDATE)
        AND alert_type = :atype
    """
    insert_sql = """
        INSERT INTO alert_log (product_id, alert_type, days_left)
        VALUES (:pid, :atype, :days)
    """
    cursor = conn.cursor()
    logged_count = 0

    for product in flagged_products:
        cursor.execute(check_sql, {
            "pid":   product["product_id"],
            "atype": product["status"]
        })
        already_logged = cursor.fetchone()[0]

        if not already_logged:
            cursor.execute(insert_sql, {
                "pid":  product["product_id"],
                "atype": product["status"],
                "days":  product["days_until_expiry"]
            })
            logged_count += 1

    conn.commit()
    cursor.close()
    return logged_count


def run_scan():
    """
    Main scan function — connects, fetches flagged products,
    logs alerts, and returns results for reporting.
    """
    print(f"\n{'='*55}")
    print(f"  Expired Product Alert Scanner")
    print(f"  Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}\n")

    conn = get_connection()

    try:
        flagged = fetch_flagged_products(conn)

        if not flagged:
            print("  All products are within safe expiry range.")
            return []

        new_logs = log_alerts(conn, flagged)
        print(f"  Found {len(flagged)} flagged product(s) — {new_logs} new alert(s) logged.\n")
        return flagged

    finally:
        conn.close()
