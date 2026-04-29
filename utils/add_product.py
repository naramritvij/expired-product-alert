# utils/add_product.py
# -------------------------------------------------------
# Interactive CLI to insert a new product into Oracle
# -------------------------------------------------------

from db.connection import get_connection
from datetime import datetime


def add_product_interactive():
    """Prompt the user and INSERT a new product row."""

    print("\n  Add New Product")
    print("  " + "─" * 40)

    name       = input("  Product name:       ").strip()
    barcode    = input("  Barcode (optional): ").strip() or None
    category   = input("  Category ID (1=Dairy, 2=Bakery, 3=Frozen, 4=Produce, 5=Beverages): ").strip()
    quantity   = input("  Quantity:           ").strip()
    price      = input("  Unit price ($):     ").strip()
    expiry_str = input("  Expiry date (YYYY-MM-DD): ").strip()
    location   = input("  Store location:     ").strip() or None

    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
    except ValueError:
        print("\n  [ERROR] Invalid date format. Use YYYY-MM-DD.")
        return

    sql = """
        INSERT INTO products
            (product_name, barcode, category_id, quantity, unit_price, expiry_date, location)
        VALUES
            (:name, :barcode, :cat_id, :qty, :price, :expiry, :loc)
    """

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, {
            "name":   name,
            "barcode": barcode,
            "cat_id": int(category),
            "qty":    int(quantity),
            "price":  float(price),
            "expiry": expiry_date,
            "loc":    location,
        })
        conn.commit()
        cursor.close()
        print(f"\n  Product '{name}' added successfully.\n")
    except Exception as e:
        print(f"\n  [ERROR] Could not insert product: {e}\n")
    finally:
        conn.close()
