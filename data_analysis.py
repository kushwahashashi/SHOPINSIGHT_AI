import pandas as pd

# ==============================
# SHOPINSIGHT AI
# E-commerce Customer & Sales Intelligence
# ==============================

# Load all datasets
customers = pd.read_csv("olist_customers_dataset.csv")
geolocation = pd.read_csv("olist_geolocation_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")
reviews = pd.read_csv("olist_order_reviews_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
sellers = pd.read_csv("olist_sellers_dataset.csv")
category_translation = pd.read_csv("product_category_name_translation.csv")

print("\n======================================")
print("     SHOPINSIGHT AI")
print(" E-commerce Customer & Sales Intelligence")
print("======================================\n")

print("All datasets loaded successfully!\n")

# Show dataset sizes
print("DATASET SIZES")
print("--------------------------------------")
print("Customers:", customers.shape)
print("Geolocation:", geolocation.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Orders:", orders.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)
print("Category Translation:", category_translation.shape)

print("\n======================================")
print("Data loading completed successfully!")
print("======================================")

# ==============================
# DATA QUALITY CHECK
# ==============================

print("\n\nDATA QUALITY CHECK")
print("======================================")

datasets = {
    "Customers": customers,
    "Geolocation": geolocation,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Orders": orders,
    "Products": products,
    "Sellers": sellers,
    "Category Translation": category_translation
}

for name, df in datasets.items():
    print(f"\n{name}")
    print("--------------------------------------")
    print("Rows:", len(df))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

    # ==============================
# MISSING VALUES BY COLUMN
# ==============================

print("\n\nMISSING VALUES BY COLUMN")
print("======================================")

for name, df in datasets.items():
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) > 0:
        print(f"\n{name}")
        print("--------------------------------------")
        print(missing)

        # ==============================
# ORDER STATUS ANALYSIS
# ==============================

print("\n\nORDER STATUS ANALYSIS")
print("======================================")

status_counts = orders["order_status"].value_counts()

print(status_counts)

print("\nOrder Status Percentage")
print("--------------------------------------")

status_percentage = orders["order_status"].value_counts(normalize=True) * 100

for status, percentage in status_percentage.items():
    print(f"{status}: {percentage:.2f}%")

    # ==============================
# SALES & REVENUE ANALYSIS
# ==============================

print("\n\nSALES & REVENUE ANALYSIS")
print("======================================")

total_sales = order_items["price"].sum()
total_freight = order_items["freight_value"].sum()
total_revenue = total_sales + total_freight

total_orders = orders["order_id"].nunique()
total_items = order_items["order_id"].count()

average_order_value = total_sales / total_orders

print(f"Total Product Sales: R$ {total_sales:,.2f}")
print(f"Total Freight Value: R$ {total_freight:,.2f}")
print(f"Total Revenue including Freight: R$ {total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Items Sold: {total_items:,}")
print(f"Average Order Value: R$ {average_order_value:,.2f}")

# ==============================
# MONTHLY SALES TREND
# ==============================

print("\n\nMONTHLY SALES TREND")
print("======================================")

# Convert order purchase date to datetime
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# Create year-month column
orders["year_month"] = orders["order_purchase_timestamp"].dt.to_period("M")

# Calculate monthly orders
monthly_orders = (
    orders.groupby("year_month")["order_id"]
    .nunique()
)

print("\nMonthly Orders:")
print(monthly_orders)

# Merge orders with order items
sales_data = order_items.merge(
    orders[["order_id", "year_month"]],
    on="order_id",
    how="inner"
)

# Calculate monthly sales
monthly_sales = (
    sales_data.groupby("year_month")["price"]
    .sum()
)

print("\nMonthly Sales:")
print(monthly_sales)

# ==============================
# TOP PRODUCT CATEGORIES
# ==============================

print("\n\nTOP PRODUCT CATEGORIES")
print("======================================")

# Merge products with category translation
products_with_category = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

# Merge order items with product information
category_sales = order_items.merge(
    products_with_category[
        ["product_id", "product_category_name_english"]
    ],
    on="product_id",
    how="left"
)

# Calculate sales by category
top_categories = (
    category_sales
    .groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 15 Categories by Sales:")
print(top_categories.head(15))

# ==============================
# CUSTOMER INTELLIGENCE
# ==============================

print("\n\nCUSTOMER INTELLIGENCE")
print("======================================")

# Merge orders with customer information
customer_order_data = orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

# Count orders per unique customer
customer_orders = (
    customer_order_data
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

# Customer statistics
total_unique_customers = customer_orders.shape[0]
repeat_customers = (customer_orders > 1).sum()
one_time_customers = (customer_orders == 1).sum()

repeat_customer_rate = (
    repeat_customers / total_unique_customers
) * 100

print(f"Total Unique Customers: {total_unique_customers:,}")
print(f"One-Time Customers: {one_time_customers:,}")
print(f"Repeat Customers: {repeat_customers:,}")
print(f"Repeat Customer Rate: {repeat_customer_rate:.2f}%")

print("\nTop 10 Customers by Number of Orders:")
print("--------------------------------------")
print(customer_orders.sort_values(ascending=False).head(10))

# ==============================
# CUSTOMER SPENDING ANALYSIS
# ==============================

print("\n\nCUSTOMER SPENDING ANALYSIS")
print("======================================")

# Add customer_unique_id to order items
customer_spending = order_items.merge(
    orders[["order_id", "customer_id"]],
    on="order_id",
    how="left"
)

customer_spending = customer_spending.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

# Calculate total spending per unique customer
customer_revenue = (
    customer_spending
    .groupby("customer_unique_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("Top 10 Customers by Total Spending:")
print("--------------------------------------")
print(customer_revenue.head(10))

print("\nCustomer Spending Statistics:")
print("--------------------------------------")
print(f"Average Customer Spending: R$ {customer_revenue.mean():,.2f}")
print(f"Highest Customer Spending: R$ {customer_revenue.max():,.2f}")
print(f"Lowest Customer Spending: R$ {customer_revenue.min():,.2f}")

# ==============================
# CUSTOMER VALUE SEGMENTATION
# ==============================

print("\n\nCUSTOMER VALUE SEGMENTATION")
print("======================================")

# Segment customers based on total spending
customer_segments = pd.cut(
    customer_revenue,
    bins=[0, 100, 500, float("inf")],
    labels=["Low Value", "Medium Value", "High Value"]
)

print("Customer Segment Distribution:")
print("--------------------------------------")
print(customer_segments.value_counts())

print("\nCustomer Segment Percentage:")
print("--------------------------------------")
print(
    (customer_segments.value_counts(normalize=True) * 100)
    .round(2)
)

# ==============================
# REVENUE BY CUSTOMER SEGMENT
# ==============================

print("\n\nREVENUE BY CUSTOMER SEGMENT")
print("======================================")

segment_revenue = customer_revenue.groupby(customer_segments).sum()

print("Revenue by Customer Segment:")
print("--------------------------------------")
print(segment_revenue)

print("\nRevenue Percentage by Segment:")
print("--------------------------------------")
print(
    (segment_revenue / segment_revenue.sum() * 100)
    .round(2)
)

# ==============================
# REPEAT CUSTOMER REVENUE ANALYSIS
# ==============================

print("\n\nREPEAT CUSTOMER REVENUE ANALYSIS")
print("======================================")

# Number of orders per unique customer
customer_order_count = (
    orders
    .merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left"
    )
    .groupby("customer_unique_id")["order_id"]
    .count()
)

# Create customer type
customer_type = customer_order_count.apply(
    lambda x: "Repeat Customer" if x > 1 else "One-Time Customer"
)

# Match customer type with revenue
customer_type_revenue = customer_revenue.to_frame("revenue")
customer_type_revenue["customer_type"] = customer_type

revenue_by_type = (
    customer_type_revenue
    .groupby("customer_type")["revenue"]
    .sum()
)

print("Revenue by Customer Type:")
print("--------------------------------------")
print(revenue_by_type)

print("\nRevenue Percentage by Customer Type:")
print("--------------------------------------")
print(
    (revenue_by_type / revenue_by_type.sum() * 100)
    .round(2)
)# ==============================
# REPEAT CUSTOMER REVENUE ANALYSIS
# ==============================

print("\n\nREPEAT CUSTOMER REVENUE ANALYSIS")
print("======================================")

# Number of orders per unique customer
customer_order_count = (
    orders
    .merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left"
    )
    .groupby("customer_unique_id")["order_id"]
    .count()
)

# Create customer type
customer_type = customer_order_count.apply(
    lambda x: "Repeat Customer" if x > 1 else "One-Time Customer"
)

# Match customer type with revenue
customer_type_revenue = customer_revenue.to_frame("revenue")
customer_type_revenue["customer_type"] = customer_type

revenue_by_type = (
    customer_type_revenue
    .groupby("customer_type")["revenue"]
    .sum()
)

print("Revenue by Customer Type:")
print("--------------------------------------")
print(revenue_by_type)

print("\nRevenue Percentage by Customer Type:")
print("--------------------------------------")
print(
    (revenue_by_type / revenue_by_type.sum() * 100)
    .round(2)
)

# ==============================
# REPEAT CUSTOMER REVENUE ANALYSIS
# ==============================

print("\n\nREPEAT CUSTOMER REVENUE ANALYSIS")
print("======================================")

# Number of orders per unique customer
customer_order_count = (
    orders
    .merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left"
    )
    .groupby("customer_unique_id")["order_id"]
    .count()
)

# Create customer type
customer_type = customer_order_count.apply(
    lambda x: "Repeat Customer" if x > 1 else "One-Time Customer"
)

# Match customer type with revenue
customer_type_revenue = customer_revenue.to_frame("revenue")
customer_type_revenue["customer_type"] = customer_type

revenue_by_type = (
    customer_type_revenue
    .groupby("customer_type")["revenue"]
    .sum()
)

print("Revenue by Customer Type:")
print("--------------------------------------")
print(revenue_by_type)

print("\nRevenue Percentage by Customer Type:")
print("--------------------------------------")
print(
    (revenue_by_type / revenue_by_type.sum() * 100)
    .round(2)
)


# ==============================
# MONTHLY AVERAGE ORDER VALUE
# ==============================

print("\n\nMONTHLY AVERAGE ORDER VALUE")
print("======================================")

orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M")

monthly_orders = (
    orders
    .groupby("order_month")["order_id"]
    .nunique()
)

monthly_revenue = (
    order_items
    .merge(
        orders[["order_id", "order_month"]],
        on="order_id",
        how="left"
    )
    .groupby("order_month")["price"]
    .sum()
)

monthly_aov = monthly_revenue / monthly_orders

print("Monthly Average Order Value:")
print("--------------------------------------")
print(monthly_aov.round(2))




# ==============================
# PRODUCT PERFORMANCE ANALYSIS
# ==============================

print("\n\nPRODUCT PERFORMANCE ANALYSIS")
print("======================================")

product_sales = (
    order_items
    .groupby("product_id")
    .agg(
        units_sold=("order_item_id", "count"),
        total_revenue=("price", "sum")
    )
    .sort_values("total_revenue", ascending=False)
)

# Add product category information
product_sales = product_sales.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

print("Top 10 Products by Revenue:")
print("--------------------------------------")
print(product_sales.head(10))

print("\nTop 10 Products by Units Sold:")
print("--------------------------------------")
print(
    product_sales
    .sort_values("units_sold", ascending=False)
    .head(10)
)

# ==============================
# CATEGORY PERFORMANCE ANALYSIS
# ==============================

print("\n\nCATEGORY PERFORMANCE ANALYSIS")
print("======================================")

category_performance = (
    order_items
    .merge(
        products[["product_id", "product_category_name"]],
        on="product_id",
        how="left"
    )
    .groupby("product_category_name")
    .agg(
        units_sold=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        average_price=("price", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print("Top 15 Categories by Revenue:")
print("--------------------------------------")
print(category_performance.head(15).round(2))

# ==============================
# SELLER PERFORMANCE ANALYSIS
# ==============================

print("\n\nSELLER PERFORMANCE ANALYSIS")
print("======================================")

seller_performance = (
    order_items
    .groupby("seller_id")
    .agg(
        items_sold=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print("Top 10 Sellers by Revenue:")
print("--------------------------------------")
print(seller_performance.head(10).round(2))

print("\nTop 10 Sellers by Items Sold:")
print("--------------------------------------")
print(
    seller_performance
    .sort_values("items_sold", ascending=False)
    .head(10)
)
# ==============================
# SELLER PERFORMANCE ANALYSIS
# ==============================

print("\n\nSELLER PERFORMANCE ANALYSIS")
print("======================================")

seller_performance = (
    order_items
    .groupby("seller_id")
    .agg(
        items_sold=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print("Top 10 Sellers by Revenue:")
print("--------------------------------------")
print(seller_performance.head(10).round(2))

print("\nTop 10 Sellers by Items Sold:")
print("--------------------------------------")
print(
    seller_performance
    .sort_values("items_sold", ascending=False)
    .head(10)
)

# ==============================
# SELLER PERFORMANCE ANALYSIS
# ==============================

print("\n\nSELLER PERFORMANCE ANALYSIS")
print("======================================")

seller_performance = (
    order_items
    .groupby("seller_id")
    .agg(
        items_sold=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print("Top 10 Sellers by Revenue:")
print("--------------------------------------")
print(seller_performance.head(10).round(2))

print("\nTop 10 Sellers by Items Sold:")
print("--------------------------------------")
print(
    seller_performance
    .sort_values("items_sold", ascending=False)
    .head(10)
)

# ==============================
# SELLER PERFORMANCE ANALYSIS
# ==============================

print("\n\nSELLER PERFORMANCE ANALYSIS")
print("======================================")

seller_performance = (
    order_items
    .groupby("seller_id")
    .agg(
        items_sold=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print("Top 10 Sellers by Revenue:")
print("--------------------------------------")
print(seller_performance.head(10).round(2))

print("\nTop 10 Sellers by Items Sold:")
print("--------------------------------------")
print(
    seller_performance
    .sort_values("items_sold", ascending=False)
    .head(10)
)





# ==============================
# SELLER PERFORMANCE ANALYSIS
# ==============================

print("\n\nSELLER PERFORMANCE ANALYSIS")
print("======================================")

seller_performance = (
    order_items
    .groupby("seller_id")
    .agg(
        items_sold=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print("Top 10 Sellers by Revenue:")
print("--------------------------------------")
print(seller_performance.head(10).round(2))

print("\nTop 10 Sellers by Items Sold:")
print("--------------------------------------")
print(
    seller_performance
    .sort_values("items_sold", ascending=False)
    .head(10)
)

# ==============================
# SELLER REVENUE CONTRIBUTION
# ==============================

print("\n\nSELLER REVENUE CONTRIBUTION")
print("======================================")

seller_revenue_share = (
    seller_performance["total_revenue"]
    / seller_performance["total_revenue"].sum()
    * 100
)

top_10_seller_revenue = seller_performance.head(10)["total_revenue"].sum()
total_seller_revenue = seller_performance["total_revenue"].sum()

print(f"Total Seller Revenue: R$ {total_seller_revenue:,.2f}")
print(f"Top 10 Seller Revenue: R$ {top_10_seller_revenue:,.2f}")
print(
    f"Top 10 Seller Revenue Share: "
    f"{(top_10_seller_revenue / total_seller_revenue * 100):.2f}%"
)

print("\nTop 10 Sellers Revenue Share:")
print("--------------------------------------")
print(seller_revenue_share.head(10).round(2))


# ==============================
# CUSTOMER REVIEW ANALYSIS
# ==============================

print("\n\nCUSTOMER REVIEW ANALYSIS")
print("======================================")

review_distribution = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

print("Review Score Distribution:")
print("--------------------------------------")
print(review_distribution)

average_review = reviews["review_score"].mean()

print("\nAverage Review Score:")
print("--------------------------------------")
print(f"{average_review:.2f} / 5")

valid_reviews = reviews["review_score"].notna().sum()

positive_reviews = (
    (reviews["review_score"] >= 4).sum()
    / valid_reviews
    * 100
)

negative_reviews = (
    (reviews["review_score"] <= 2).sum()
    / valid_reviews
    * 100
)

print(f"\nPositive Reviews (4-5): {positive_reviews:.2f}%")
print(f"Negative Reviews (1-2): {negative_reviews:.2f}%")


# ==============================
# DELIVERY PERFORMANCE ANALYSIS
# ==============================

print("\n\nDELIVERY PERFORMANCE ANALYSIS")
print("======================================")

# Convert delivery dates to datetime
orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"],
    errors="coerce"
)

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

# Calculate delivery time in days
delivery_data = orders.dropna(
    subset=[
        "order_purchase_timestamp",
        "order_delivered_customer_date"
    ]
).copy()

delivery_data["delivery_days"] = (
    delivery_data["order_delivered_customer_date"]
    - delivery_data["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60 * 24)

print("Delivery Time Statistics:")
print("--------------------------------------")
print(f"Average Delivery Time: {delivery_data['delivery_days'].mean():.2f} days")
print(f"Fastest Delivery: {delivery_data['delivery_days'].min():.2f} days")
print(f"Longest Delivery: {delivery_data['delivery_days'].max():.2f} days")

print("\nDelivery Time Distribution:")
print("--------------------------------------")

delivery_bins = pd.cut(
    delivery_data["delivery_days"],
    bins=[0, 3, 7, 14, 30, float("inf")],
    labels=[
        "0-3 Days",
        "4-7 Days",
        "8-14 Days",
        "15-30 Days",
        "30+ Days"
    ]
)

print(delivery_bins.value_counts().sort_index())



# ==============================
# VISUALIZATION - MONTHLY SALES TREND
# ==============================

import matplotlib.pyplot as plt

monthly_sales = (
    order_items
    .merge(orders[["order_id", "order_purchase_timestamp"]], on="order_id")
)

monthly_sales["order_purchase_timestamp"] = pd.to_datetime(
    monthly_sales["order_purchase_timestamp"]
)

monthly_sales["month"] = (
    monthly_sales["order_purchase_timestamp"]
    .dt.to_period("M")
)

monthly_sales_data = (
    monthly_sales
    .groupby("month")["price"]
    .sum()
)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales_data.index.astype(str),
    monthly_sales_data.values,
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (R$)")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()


# ==============================
# VISUALIZATION - ORDER STATUS
# ==============================

order_status = orders["order_status"].value_counts()

plt.figure(figsize=(10, 6))

plt.bar(
    order_status.index,
    order_status.values
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==============================
# VISUALIZATION - ORDER STATUS
# ==============================

order_status = orders["order_status"].value_counts()

plt.figure(figsize=(10, 6))

plt.bar(
    order_status.index,
    order_status.values
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()




# ==============================
# VISUALIZATION - TOP PRODUCT CATEGORIES
# ==============================

category_sales = (
    order_items
    .merge(products[["product_id", "product_category_name"]], on="product_id")
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

plt.bar(
    category_sales.index,
    category_sales.values
)

plt.title("Top 10 Product Categories by Sales")
plt.xlabel("Product Category")
plt.ylabel("Sales (R$)")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()



# ==============================
# VISUALIZATION - REVENUE BY CUSTOMER SEGMENT
# ==============================

segment_revenue = (
    customer_revenue
    .groupby(customer_segments)
    .sum()
)

plt.figure(figsize=(8, 6))

plt.bar(
    segment_revenue.index.astype(str),
    segment_revenue.values
)

plt.title("Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue (R$)")

plt.tight_layout()
plt.show()


# ==============================
# VISUALIZATION - REVIEW SCORE DISTRIBUTION
# ==============================

review_counts = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8, 6))

plt.bar(
    review_counts.index.astype(str),
    review_counts.values
)

plt.title("Customer Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.show()


# ==============================
# VISUALIZATION - DELIVERY TIME DISTRIBUTION
# ==============================

delivery_counts = (
    delivery_bins
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(10, 6))

plt.bar(
    delivery_counts.index.astype(str),
    delivery_counts.values
)

plt.title("Delivery Time Distribution")
plt.xlabel("Delivery Time")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()