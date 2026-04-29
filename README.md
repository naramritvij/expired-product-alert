# Expired Product Alert System 🛒

A real-world Python + Oracle SQL tool that automatically scans store inventory, flags products that are **expired or expiring soon**, logs alerts to the database, and exports a timestamped CSV report — all from the command line.

Built to solve a genuine retail operations problem: stores lose thousands of dollars monthly to expired, unsold inventory sitting undetected on shelves.

---

## Features

- Connects Python directly to an Oracle DB using `cx_Oracle`
- Flags products based on **per-category alert thresholds** (e.g. dairy alerts 3 days before expiry, frozen foods alert 14 days before)
- Logs every alert to an `alert_log` table — no duplicate logs per day
- Colour-coded terminal output (red = expired, yellow = expiring soon)
- Exports a timestamped `.csv` report to the `reports/` folder
- Add new products interactively via CLI (`--add`)
- View alert history from the database (`--history`)

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Application logic |
| Oracle SQL (XE / 21c) | Data storage |
| cx_Oracle | Python → Oracle connector |
| python-dotenv | Secure credential management |

---

## Folder Structure

```
expired_product_alert/
│
├── main.py                   # Entry point
├── requirements.txt
├── .env.example              # Copy → .env and fill in credentials
├── .gitignore
│
├── sql/
│   └── schema.sql            # CREATE TABLE, sequences, seed data, view
│
├── config/
│   └── db_config.py          # Loads DB credentials from .env
│
├── db/
│   └── connection.py         # Oracle connection helper
│
├── scanner/
│   └── alert_scanner.py      # Core scan logic + alert logging
│
├── reports/
│   └── report_generator.py   # Terminal + CSV report output
│
└── utils/
    ├── add_product.py         # CLI: add a product interactively
    └── view_history.py        # CLI: view past alert logs
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/expired-product-alert.git
cd expired-product-alert
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `cx_Oracle` requires Oracle Instant Client to be installed on your machine.  
> Download it from [Oracle's website](https://www.oracle.com/database/technologies/instant-client.html) and add it to your system PATH.

### 4. Set up your `.env` file

```bash
copy .env.example .env      # Windows
cp .env.example .env        # macOS / Linux
```

Edit `.env` with your Oracle credentials:

```
DB_USER=your_username
DB_PASSWORD=your_password
DB_DSN=localhost:1521/XEPDB1
```

### 5. Run the SQL schema in Oracle

Open SQL*Plus, SQL Developer, or any Oracle client and run:

```sql
@sql/schema.sql
```

This creates the tables, sequences, and seeds sample products.

---

## Usage

### Run the daily scan

```bash
python main.py
```

**Sample output:**

```
=======================================================
  Expired Product Alert System
  Run time: 2025-09-12 08:30:00
=======================================================

  Found 4 flagged product(s) — 4 new alert(s) logged.

  SUMMARY
  ──────────────────────────────────────────────────
  Expired products:              2
  Expiring soon:                 2
  Total at-risk stock value:     $87.43
  ──────────────────────────────────────────────────

  STATUS          PRODUCT                    QTY   DAYS  LOCATION              VALUE
  ─────────────────────────────────────────────────────────────────────────────────────
  EXPIRED         Croissants 6-pack            12  1d ago  Bakery Shelf 2       $77.88
  EXPIRED         Baby Spinach 200g            18  2d ago  Produce D2           $71.82
  Expiring Soon   Whole Milk 2L                20     2d   Fridge A1            $99.80
  Expiring Soon   Greek Yogurt 500g            15     1d   Fridge A2            $52.35

  Report saved → reports/alert_report_20250912_083000.csv
```

### Add a new product

```bash
python main.py --add
```

### View alert history

```bash
python main.py --history
```

---

## Database Schema

```
categories          products              alert_log
──────────          ──────────            ──────────
category_id  PK     product_id   PK       alert_id    PK
category_name       product_name          product_id  FK
alert_days          barcode               alert_type
                    category_id  FK       days_left
                    quantity              logged_at
                    unit_price
                    expiry_date
                    location
                    created_at
```

---

## Real-World Impact

Retail stores, pharmacies, food banks, and restaurants all face losses from expired stock. This system provides:

- **Automated daily scanning** instead of manual shelf checks
- **Category-specific alert windows** (dairy vs. frozen vs. produce have different lead times)
- **Audit trail** via the `alert_log` table
- **Stock value visibility** so managers can prioritize high-value clearance items

---

## Future Improvements

- [ ] Email notifications when expired products are found
- [ ] Web dashboard using Flask to view alerts in a browser
- [ ] Scheduled auto-run using Windows Task Scheduler or cron
- [ ] Discount suggestion engine (auto-calculate clearance price)

---

## Author

**Your Name**  
[GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)
