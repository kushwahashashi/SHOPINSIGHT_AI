import streamlit as st
import pandas as pd
import os

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SHOPINSIGHT AI",
    page_icon="🛒",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

/* Main title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 2px;
}

.subtitle {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 10px;
}

/* Section headings */
.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #172554;
    margin-top: 15px;
    margin-bottom: 12px;
}

/* KPI cards */
div[data-testid="metric-container"] {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.07);
}

/* Metric label */
div[data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 600;
}

/* Metric value */
div[data-testid="stMetricValue"] {
    color: #172554;
    font-weight: 800;
}

/* Profile */
.profile-name {
    text-align: center;
    color: #172554;
    font-size: 17px;
    font-weight: 750;
    margin-top: 6px;
}

.profile-role {
    text-align: center;
    color: #64748b;
    font-size: 12px;
}

/* Insight cards */
.insight-card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    border-left: 5px solid #2563eb;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
    margin-bottom: 10px;
}

.insight-title {
    color: #172554;
    font-size: 16px;
    font-weight: 750;
}

.insight-text {
    color: #64748b;
    font-size: 14px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    padding: 25px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

orders = pd.read_csv("olist_orders_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")
reviews = pd.read_csv("olist_order_reviews_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")


# =========================================================
# BASIC CALCULATIONS
# =========================================================

total_orders = orders["order_id"].nunique()
total_customers = customers["customer_unique_id"].nunique()
total_items = len(order_items)
total_revenue = order_items["price"].sum()

average_order_value = total_revenue / total_orders


# =========================================================
# HEADER
# =========================================================

header_col, profile_col = st.columns([5, 1])

with header_col:

    st.markdown(
        '<div class="main-title">🛒 SHOPINSIGHT AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'E-commerce Customer & Sales Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Business intelligence dashboard for customer, sales and "
        "e-commerce performance analysis."
    )


with profile_col:

    if os.path.exists("profile_photo.jpg"):

        st.image(
            "profile_photo.jpg",
            width=110
        )

    st.markdown(
        '<div class="profile-name">Shashi Kushwaha</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="profile-role">'
        'Data Analyst | Project Developer'
        '</div>',
        unsafe_allow_html=True
    )


st.divider()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown(
    '<div style="text-align:center;padding:10px 0 18px 0;">'
    '<div style="font-size:27px;font-weight:800;color:#172554;">'
    '🛒 SHOPINSIGHT AI'
    '</div>'
    '<div style="font-size:13px;color:#64748b;margin-top:5px;">'
    'E-commerce Intelligence'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.sidebar.divider()

dashboard_page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Dashboard",
        "📈 Sales Analytics",
        "🛍️ Product Performance",
        "👥 Customer Intelligence",
        "⭐ Customer Reviews",
        "🚚 Delivery Analytics",
        "🧠 Business Insights"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        font-size:12px;
        padding:10px 0;
    ">
        Built with Python + Streamlit<br>
        Olist E-commerce Dataset
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# BUSINESS OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📊 Business Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"R$ {total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "📦 Items Sold",
        f"{total_items:,}"
    )

with col5:
    st.metric(
        "🧾 Avg Order Value",
        f"R$ {average_order_value:,.2f}"
    )


st.divider()


# =========================================================
# DATE PREPARATION
# =========================================================

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)


# =========================================================
# MONTHLY ORDERS
# =========================================================

monthly_orders = (
    orders
    .assign(
        month=orders["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month")
    .size()
)


# =========================================================
# MONTHLY SALES
# =========================================================

orders_with_sales = orders.merge(
    order_items[["order_id", "price"]],
    on="order_id",
    how="left"
)

monthly_sales = (
    orders_with_sales
    .assign(
        month=orders_with_sales["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month")["price"]
    .sum()
)


# =========================================================
# SALES & ORDERS SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📈 Sales Performance</div>',
    unsafe_allow_html=True
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.markdown("### 🛒 Monthly Orders")

    st.line_chart(
        monthly_orders,
        use_container_width=True
    )


with chart_col2:

    st.markdown("### 💰 Monthly Revenue")

    st.line_chart(
        monthly_sales,
        use_container_width=True
    )


st.divider()


# =========================================================
# PRODUCT CATEGORY PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">🛍️ Product Category Performance</div>',
    unsafe_allow_html=True
)

category_sales = (
    order_items
    .groupby("product_id")
    .agg(
        revenue=("price", "sum"),
        units=("order_item_id", "count")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

# Merge product categories

category_data = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

category_revenue = (
    category_data
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(
    category_revenue.rename("Revenue"),
    use_container_width=True
)


st.divider()


# =========================================================
# CUSTOMER INTELLIGENCE
# =========================================================

st.markdown(
    '<div class="section-title">👥 Customer Intelligence</div>',
    unsafe_allow_html=True
)

customer_spending = order_items.merge(
    orders[["order_id", "customer_id"]],
    on="order_id",
    how="left"
)

customer_spending = customer_spending.merge(
    customers[
        ["customer_id", "customer_unique_id"]
    ],
    on="customer_id",
    how="left"
)

customer_revenue = (
    customer_spending
    .groupby("customer_unique_id")["price"]
    .sum()
)


customer_segments = pd.cut(
    customer_revenue,
    bins=[0, 100, 500, float("inf")],
    labels=[
        "Low Value",
        "Medium Value",
        "High Value"
    ]
)

segment_counts = (
    customer_segments
    .value_counts()
    .sort_index()
)


customer_col1, customer_col2 = st.columns(2)

with customer_col1:

    st.markdown("### 👤 Customer Value Segments")

    st.bar_chart(
        segment_counts.rename("Customers"),
        use_container_width=True
    )


with customer_col2:

    st.markdown("### 💰 Revenue by Customer Segment")

    segment_revenue = (
        customer_revenue
        .groupby(customer_segments)
        .sum()
    )

    segment_revenue.index.name = "Customer Segment"
    segment_revenue.name = "Revenue"

    st.bar_chart(
        segment_revenue,
        use_container_width=True
    )


st.divider()


# =========================================================
# CUSTOMER REVIEWS
# =========================================================

st.markdown(
    '<div class="section-title">⭐ Customer Reviews</div>',
    unsafe_allow_html=True
)

review_counts = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

average_rating = reviews["review_score"].mean()

positive_reviews = (
    (reviews["review_score"] >= 4).mean() * 100
)

negative_reviews = (
    (reviews["review_score"] <= 2).mean() * 100
)


review_col1, review_col2, review_col3 = st.columns(3)

with review_col1:

    st.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f}/5"
    )

with review_col2:

    st.metric(
        "😊 Positive Reviews",
        f"{positive_reviews:.1f}%"
    )

with review_col3:

    st.metric(
        "⚠️ Negative Reviews",
        f"{negative_reviews:.1f}%"
    )


st.bar_chart(
    review_counts.rename("Reviews"),
    use_container_width=True
)


st.divider()


# =========================================================
# DELIVERY PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">🚚 Delivery Performance</div>',
    unsafe_allow_html=True
)

orders_delivery = orders[
    [
        "order_id",
        "order_purchase_timestamp",
        "order_delivered_customer_date"
    ]
].copy()

orders_delivery[
    "order_delivered_customer_date"
] = pd.to_datetime(
    orders_delivery["order_delivered_customer_date"],
    errors="coerce"
)

orders_delivery["delivery_days"] = (
    orders_delivery["order_delivered_customer_date"]
    - orders_delivery["order_purchase_timestamp"]
).dt.total_seconds() / 86400


average_delivery = orders_delivery[
    "delivery_days"
].mean()


delivery_bins = pd.cut(
    orders_delivery["delivery_days"],
    bins=[
        0,
        3,
        7,
        14,
        30,
        float("inf")
    ],
    labels=[
        "0-3 days",
        "4-7 days",
        "8-14 days",
        "15-30 days",
        "30+ days"
    ]
)

delivery_counts = (
    delivery_bins
    .value_counts()
    .sort_index()
)


delivery_col1, delivery_col2 = st.columns([1, 2])

with delivery_col1:

    st.metric(
        "🚚 Average Delivery",
        f"{average_delivery:.1f} days"
    )

    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">
                💡 Delivery Insight
            </div>
            <div class="insight-text">
                Most orders are delivered within the
                8–30 day range. Long delivery times
                represent an opportunity for operational improvement.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with delivery_col2:

    st.bar_chart(
        delivery_counts.rename("Orders"),
        use_container_width=True
    )


st.divider()


# =========================================================
# KEY BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Key Business Insights</div>',
    unsafe_allow_html=True
)

insight1, insight2, insight3 = st.columns(3)

with insight1:

    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">
                💰 Revenue
            </div>
            <div class="insight-text">
                The business generated substantial revenue
                across a broad range of product categories.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with insight2:

    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">
                👥 Customer Value
            </div>
            <div class="insight-text">
                High-value customers represent a small customer
                segment but contribute disproportionately to revenue.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with insight3:

    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">
                ⭐ Customer Experience
            </div>
            <div class="insight-text">
                Customer ratings are generally positive,
                while delivery performance remains an area
                for potential improvement.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🛒 <b>SHOPINSIGHT AI</b>
        <br>
        E-commerce Customer & Sales Intelligence
        <br><br>
        Developed by <b>Shashi Kushwaha</b>
    </div>
    """,
    unsafe_allow_html=True
)