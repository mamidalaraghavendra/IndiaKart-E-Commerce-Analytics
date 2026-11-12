import pandas as pd
from pathlib import Path
project_folder = Path(__file__).resolve().parent.parent
customer_file = project_folder / "customers DA.csv"
customers = pd.read_csv(customer_file)
print(customers.head())

print("Dataset Shape:", customers.shape) #Number of rows and columns
print("Column Names:", customers.columns.tolist()) #Names of all columns
print("Data Types:\n", customers.dtypes) #Data type of each column

print("\nMissing Values:")
print(customers.isnull().sum()) #missing values in every coloums and  counts 

print("\nDuplicate Rows:", customers.duplicated().sum()) #check complete duplicate rows
print("Duplicate Customer IDs:", customers["customer_id"].duplicated().sum()) #check duplicate id's

print("\nAge Range:")  # Check the minimum and maximum customer age
print("Minimum Age:", customers["age"].min())
print("Maximum Age:", customers["age"].max())

print("\nNegative Spending Records:",  # Check for negative spending
      (customers["total_spent"] < 0).sum())

print("\nVerification Values:")   # Check customer verification values
print(customers["is_verified"].value_counts().sort_index())

print("\nActive Status Values:")   # Check customer active-status values
print(customers["is_active"].value_counts().sort_index())


# Profile all 8 IndiaKart datasets

file_names = {
    "customers": "customers DA.csv",
    "orders": "orders DA.csv",
    "order_items": "order_items DA.csv",
    "products": "products DA.csv",
    "payments": "payments DA.csv",
    "returns": "returns DA.csv",
    "inventory": "inventory DA.csv",
    "suppliers": "suppliers DA.csv"
}

tables = {}

for table_name, file_name in file_names.items():
    file_path = project_folder / file_name
    df = pd.read_csv(file_path)
    tables[table_name] = df

    print("\n" + "=" * 50)
    print("TABLE:", table_name)
    print("Rows and columns:", df.shape)

    print("\nColumn data types:")
    print(df.dtypes)

    print("\nMissing values per column:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())


# Check the status of orders with missing delivery dates
orders = tables["orders"]

missing_delivery = orders[orders["delivered_date"].isnull()]

print("\nOrders with missing delivery dates:")
print(missing_delivery["status"].value_counts())


# Check payment statuses and refund information
payments = tables["payments"]

print("\nPayment Status Counts:")
print(payments["status"].value_counts())

print("\nRefund Amount Counts:")
print(payments["refund_amount"].value_counts())

print("\nPayments with positive refund amounts:")
print((payments["refund_amount"] > 0).sum())


# Check for duplicate order IDs
orders = tables["orders"]

print("\n--- Order ID Validation ---")
print("Total orders:", len(orders))
print("Unique order IDs:", orders["order_id"].nunique())
print(
    "Duplicate order IDs:",
    orders["order_id"].duplicated().sum()
)

# Check orders above ₹5 lakh
orders = tables["orders"]

large_orders = orders[orders["final_amount"] > 500000]

print("\n--- Large Order Validation ---")
print("Orders above ₹5 lakh:", len(large_orders))

print("\nLarge order details:")
print(
    large_orders[
        ["order_id", "customer_id", "status", "final_amount"]
    ].head(10)
)


# Check whether delivery dates are earlier than order dates
orders = tables["orders"]

orders["order_date"] = pd.to_datetime(
    orders["order_date"], dayfirst=True, errors="coerce"
)

orders["delivered_date"] = pd.to_datetime(
    orders["delivered_date"], dayfirst=True, errors="coerce"
)

delivered_orders = orders[orders["status"] == "Delivered"]

invalid_dates = delivered_orders[
    delivered_orders["delivered_date"].notna()
    & (delivered_orders["delivered_date"] < delivered_orders["order_date"])
]

print("\n--- Delivery Date Validation ---")
print("Delivered orders:", len(delivered_orders))
print("Delivered orders missing delivery date:",
      delivered_orders["delivered_date"].isna().sum())
print("Delivery dates earlier than order dates:", len(invalid_dates))

print(invalid_dates[["order_id", "order_date", "delivered_date"]].head(10))


# Payment status and failure-rate analysis
payments = tables["payments"]

total_payments = len(payments)
failed_payments = (payments["status"] == "Failed").sum()
successful_payments = (payments["status"] == "Success").sum()

failure_rate = (failed_payments / total_payments) * 100

print("\n--- Payment Validation ---")
print("Total payments:", total_payments)
print("Successful payments:", successful_payments)
print("Failed payments:", failed_payments)
print(f"Payment failure rate: {failure_rate:.2f}%")


# Check referential integrity between order_items and orders
orders = tables["orders"]
order_items = tables["order_items"]

order_ids = set(orders["order_id"])

orphan_items = order_items[
    ~order_items["order_id"].isin(order_ids)
]

print("\n--- Order Items Relationship Check ---")
print("Total order items:", len(order_items))
print("Order items with unmatched order IDs:", len(orphan_items))

print(
    orphan_items[["item_id", "order_id"]].head(10)
)

# Check referential integrity between returns and orders
returns = tables["returns"]
orders = tables["orders"]

order_ids = set(orders["order_id"])

orphan_returns = returns[
    ~returns["order_id"].isin(order_ids)
]

print("\n--- Returns Relationship Check ---")
print("Total returns:", len(returns))
print("Returns with unmatched order IDs:", len(orphan_returns))

print(
    orphan_returns[["return_id", "order_id"]].head(10)
)



# Check Inventory Stock Status

inventory = tables["inventory"]

print("\n--- Inventory Stock Status Check ---")

print("Total inventory records:", len(inventory))

print("\nStock Status Counts:")
print(inventory["status"].value_counts(dropna=False))

print("\nOut of Stock Records:")
out_of_stock = inventory[
    inventory["status"].astype(str).str.strip().str.lower() == "out of stock"
]

print("Total Out of Stock records:", len(out_of_stock))
print(out_of_stock.head(10))


#  Check Customers With Zero Orders

customers = tables["customers"]

zero_order_customers = customers[
    customers["total_orders"] == 0
]

print("\n--- Customers With Zero Orders ---")
print("Total customers:", len(customers))
print("Customers with zero orders:", len(zero_order_customers))
print(
    "Percentage of customers with zero orders:",
    round(len(zero_order_customers) / len(customers) * 100, 2),
    "%"
)


# Missing Value Percentages
print("\n--- Missing Value Percentage Check ---")

for table_name, df in tables.items():
    print(f"\nTable: {table_name}")

    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100

    missing_report = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing Percentage": missing_percentage.round(2)
    })

    print(missing_report[missing_report["Missing Count"] > 0])

# Validate Date and Numeric Data Types

print("\n--- Orders: Date and Amount Data Types ---")

orders = tables["orders"]

print("\nDate columns:")
print(orders[["order_date", "delivered_date"]].dtypes)

print("\nAmount columns:")
amount_columns = [
    col for col in orders.columns
    if "amount" in col.lower()
]

print(orders[amount_columns].dtypes)

print("\n--- Payments: Date and Amount Data Types ---")

payments = tables["payments"]

payment_date_columns = [
    col for col in payments.columns
    if "date" in col.lower()
]

payment_amount_columns = [
    col for col in payments.columns
    if "amount" in col.lower()
]

print("\nDate columns:")
print(payments[payment_date_columns].dtypes)

print("\nAmount columns:")
print(payments[payment_amount_columns].dtypes)


# Validate Payment Dates

payments = tables["payments"]

print("\n--- Payment Date Validation ---")

print("\nOriginal payment_date data type:")
print(payments["payment_date"].dtype)

print("\nSample payment dates:")
print(payments["payment_date"].head(10))

# Convert payment_date into datetime format
payment_dates = pd.to_datetime(
    payments["payment_date"],
    dayfirst=True,
    errors="coerce"
)

print("\nConverted payment_date data type:")
print(payment_dates.dtype)

print(
    "Invalid or missing payment dates:",
    payment_dates.isna().sum()
)

print("\nRefund date missing count:")
print(payments["refund_date"].isna().sum())



#  Check Negative Numeric Values

print("\n--- Numeric Data Quality Check ---")

numeric_checks = {
    "orders": ["total_amount", "gst_amount",
               "discount_amount", "final_amount"],
    "payments": ["amount", "refund_amount"],
    "order_items": ["quantity", "unit_price"],
    "inventory": ["quantity_available", "quantity_reserved",
                  "unit_cost", "total_inventory_value"]
}

for table_name, columns in numeric_checks.items():
    df = tables[table_name]

    print(f"\nTable: {table_name}")

    for column in columns:
        if column in df.columns:
            negative_count = (df[column] < 0).sum()
            print(f"{column}: {negative_count} negative values")



# Flag Orders Above ₹5 Lakh

orders = tables["orders"]

large_orders = orders[orders["final_amount"] > 500000]

print("\n--- High-Value Order Check ---")
print("Threshold: ₹5,00,000")
print("Orders above threshold:", len(large_orders))

print("\nOrders requiring investigation:")
print(
    large_orders[
        ["order_id", "customer_id", "status", "final_amount"]
    ].sort_values("final_amount", ascending=False).head(10)
)


# Check Order Item Values

order_items = tables["order_items"]

print("\n--- Order Item Value Check ---")

print("Total order-item records:", len(order_items))

print(
    "Zero or negative quantities:",
    (order_items["quantity"] <= 0).sum()
)

print(
    "Zero or negative unit prices:",
    (order_items["unit_price"] <= 0).sum()
)

print("\nQuantity summary:")
print(order_items["quantity"].describe())

print("\nUnit price summary:")
print(order_items["unit_price"].describe())



#  Inspect Date Columns Across All Tables

date_tables = [
    "customers",
    "products",
    "returns",
    "inventory",
    "suppliers"
]

print("--- Date Column Validation ---")

for table_name in date_tables:
    df = tables[table_name]

    # Find columns whose names contain "date"
    date_columns = [
        col for col in df.columns
        if "date" in col.lower()
    ]

    print(f"\nTABLE: {table_name.upper()}")

    if not date_columns:
        print("No date columns found.")
        continue

    for column in date_columns:
        original = df[column]

        # Convert a temporary copy for validation
        parsed = pd.to_datetime(
            original,
            dayfirst=True,
            errors="coerce"
        )

        # Count non-empty values that failed conversion
        non_empty = (
            original.notna()
            & original.astype(str).str.strip().ne("")
        )
        invalid_count = (non_empty & parsed.isna()).sum()

        print(f"\nColumn: {column}")
        print("Original data type:", original.dtype)
        print("Missing values:", original.isna().sum())
        print("Invalid non-empty dates:", invalid_count)
        print("Successfully parsed dates:", parsed.notna().sum())



# Compact Date Validation Summary

date_tables = [
    "returns",
    "inventory",
    "suppliers"
]

for table_name in date_tables:
    df = tables[table_name]
    date_columns = [
        col for col in df.columns
        if "date" in col.lower()
    ]

    print(f"\n--- {table_name.upper()} ---")

    for col in date_columns:
        parsed = pd.to_datetime(
            df[col], dayfirst=True, errors="coerce"
        )
        non_empty = (
            df[col].notna()
            & df[col].astype(str).str.strip().ne("")
        )
        invalid = (non_empty & parsed.isna()).sum()

        print(
            f"{col}: missing={df[col].isna().sum()}, "
            f"invalid={invalid}, "
            f"parsed={parsed.notna().sum()}"
        )


#  Reconcile High-Value Orders with Order Items

orders = tables["orders"]
order_items = tables["order_items"]

# Select orders above ₹5 lakh
large_orders = orders[
    orders["final_amount"] > 500000
].copy()

# Calculate total item value for each order
item_totals = (
    order_items.groupby("order_id")["total_price"]
    .sum()
    .reset_index()
    .rename(columns={"total_price": "item_total"})
)

# Match order amounts with item totals
reconciliation = large_orders[
    ["order_id", "status", "final_amount"]
].merge(
    item_totals,
    on="order_id",
    how="left"
)

# Calculate the difference
reconciliation["difference"] = (
    reconciliation["final_amount"]
    - reconciliation["item_total"]
)

print("--- High-Value Order Reconciliation ---")
print("High-value orders:", len(reconciliation))
print("Orders without item records:",
      reconciliation["item_total"].isna().sum())

print("\nDifference summary:")
print(reconciliation["difference"].describe())

print("\n10 orders with the largest absolute differences:")
reconciliation["absolute_difference"] = (
    reconciliation["difference"].abs()
)

print(
    reconciliation.sort_values(
        "absolute_difference", ascending=False
    )[
        ["order_id", "status", "final_amount",
         "item_total", "difference"]
    ].head(10).round(2)
)
