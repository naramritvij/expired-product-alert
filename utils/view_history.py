# utils/view_history.py
# -------------------------------------------------------
# Queries alert_log and prints a history summary
# -------------------------------------------------------

from db.connection import get_connection


def view_alert_history():
    """Show the last 30 alert log entries from Oracle."""

    sql = """
        SELECT
            al.alert_id,
            p.product_name,
            al.alert_type,
            al.days_left,
            TO_CHAR(al.logged_at, 'YYYY-MM-DD HH24:MI') AS logged_at
        FROM alert_log al
        JOIN products p ON al.product_id = p.product_id
        ORDER BY al.logged_at DESC
        FETCH FIRST 30 ROWS ONLY
    """

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            print("\n  No alert history found.\n")
            return

        print(f"\n  Alert History (last 30 entries)")
        print(f"  {'─'*70}")
        print(f"  {'#':<5} {'PRODUCT':<25} {'TYPE':<15} {'DAYS':>6}  {'LOGGED AT'}")
        print(f"  {'─'*70}")

        for row in rows:
            alert_id, name, atype, days, logged = row
            days_str = f"{days}" if days is not None else "N/A"
            print(f"  {alert_id:<5} {name[:24]:<25} {atype:<15} {days_str:>6}  {logged}")

        print()

    finally:
        conn.close()
