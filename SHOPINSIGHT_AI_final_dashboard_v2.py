
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import base64

# -----------------------------
# PAGE
# -----------------------------
st.set_page_config(
    page_title="SHOPINSIGHT AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# PATHS
# Works even if the .py file is launched from Downloads,
# while the CSVs remain inside SHOPINSIGHT_AI.
# -----------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
CWD = Path.cwd()
PROJECT_DIR = Path(r"C:\Users\kushw\OneDrive\Desktop\SHOPINSIGHT_AI")

def find_file(filename):
    candidates = [
        SCRIPT_DIR / filename,
        CWD / filename,
        PROJECT_DIR / filename,
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f7ff;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071b41 0%, #0b2b61 55%, #111b4d 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] * {
    color: #eef4ff;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(105deg, #dcecff 0%, #e8efff 45%, #d9e9ff 100%);
    border: 1px solid #d3e1ff;
    border-radius: 18px;
    padding: 22px 26px;
    margin-bottom: 18px;
    box-shadow: 0 8px 28px rgba(45, 78, 140, .10);
}

.hero-title {
    font-size: 27px;
    font-weight: 800;
    color: #0b2a63;
    margin: 0;
}

.hero-sub {
    color: #365486;
    margin-top: 6px;
    font-size: 14px;
}

.hero-quote {
    color: #2450a6;
    font-size: 13px;
    font-weight: 600;
    text-align: right;
    padding-top: 7px;
}

.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #102d67;
    margin: 18px 0 12px 2px;
}

.kpi {
    background: white;
    border: 1px solid #e1e8f6;
    border-radius: 16px;
    padding: 16px 17px 13px 17px;
    min-height: 128px;
    box-shadow: 0 7px 22px rgba(25, 54, 105, .08);
}

.kpi-label {
    color: #50658c;
    font-size: 12px;
    font-weight: 700;
}

.kpi-value {
    color: #0d3276;
    font-size: 25px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-note {
    color: #18a566;
    font-size: 11px;
    margin-top: 8px;
    font-weight: 600;
}

.card {
    background: white;
    border: 1px solid #e1e8f6;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 7px 22px rgba(25, 54, 105, .07);
}

.profile-card {
    background: linear-gradient(135deg, #e7f0ff 0%, #f7eaff 100%);
    border: 1px solid #d8def7;
    border-radius: 17px;
    padding: 17px;
    box-shadow: 0 7px 22px rgba(25, 54, 105, .08);
}

.profile-name {
    color: #102d67;
    font-size: 16px;
    font-weight: 800;
}

.profile-role {
    color: #60759d;
    font-size: 11px;
}
.profile-photo {
    width: 92px;
    height: 92px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center top;
    border: 4px solid white;
    box-shadow: 0 6px 18px rgba(37, 59, 120, .20);
}
.profile-online {
    display: inline-block;
    background: #19b36b;
    color: white;
    font-size: 9px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 999px;
    margin-top: 6px;
}


.insight {
    background: linear-gradient(135deg, #111f62, #3d28b8);
    color: white;
    border-radius: 17px;
    padding: 17px;
    box-shadow: 0 8px 24px rgba(50, 45, 150, .18);
}

.insight h4 {
    margin: 0 0 8px 0;
}

.insight p {
    font-size: 12px;
    line-height: 1.55;
    margin: 5px 0;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e1e8f6;
    padding: 12px;
    border-radius: 14px;
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
}

button[kind="secondary"] {
    border-radius: 10px;
}

.small-muted {
    color: #7183a5;
    font-size: 11px;
}

.footer {
    background: linear-gradient(90deg, #23156f, #4331c8, #6426c9);
    color: white;
    border-radius: 14px;
    padding: 13px 18px;
    margin-top: 18px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    names = [
        "olist_orders_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_customers_dataset.csv",
        "olist_order_reviews_dataset.csv",
        "olist_products_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_sellers_dataset.csv",
        "product_category_name_translation.csv",
    ]
    paths = {n: find_file(n) for n in names}
    missing = [n for n, p in paths.items() if p is None]
    if missing:
        raise FileNotFoundError(
            "CSV files not found: " + ", ".join(missing) +
            ". Keep the CSV files inside SHOPINSIGHT_AI."
        )

    return (
        pd.read_csv(paths[names[0]]),
        pd.read_csv(paths[names[1]]),
        pd.read_csv(paths[names[2]]),
        pd.read_csv(paths[names[3]]),
        pd.read_csv(paths[names[4]]),
        pd.read_csv(paths[names[5]]),
        pd.read_csv(paths[names[6]]),
        pd.read_csv(paths[names[7]]),
    )

orders, items, customers, reviews, products, payments, sellers, translation = load_data()

# -----------------------------
# PREP
# -----------------------------
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"], errors="coerce"
)

items["price"] = pd.to_numeric(items["price"], errors="coerce").fillna(0)
items["freight_value"] = pd.to_numeric(items["freight_value"], errors="coerce").fillna(0)
payments["payment_value"] = pd.to_numeric(payments["payment_value"], errors="coerce").fillna(0)

orders = orders.dropna(subset=["order_id"])

total_orders = orders["order_id"].nunique()
total_customers = customers["customer_unique_id"].nunique()
total_items = len(items)
total_sales = items["price"].sum()
aov = total_sales / total_orders if total_orders else 0

# Translation
if "product_category_name_english" in translation.columns:
    products = products.merge(
        translation,
        on="product_category_name",
        how="left"
    )
    products["category_display"] = products["product_category_name_english"].fillna(
        products["product_category_name"].fillna("Unknown")
    )
else:
    products["category_display"] = products["product_category_name"].fillna("Unknown")

# Item/category data
item_product = items.merge(
    products[["product_id", "category_display"]],
    on="product_id",
    how="left"
)
item_product["category_display"] = item_product["category_display"].fillna("Unknown")

# Customer map
customer_map = customers[["customer_id", "customer_unique_id"]]
item_orders = item_product.merge(
    orders[["order_id", "customer_id", "order_purchase_timestamp", "order_status"]],
    on="order_id",
    how="left"
)
item_orders = item_orders.merge(customer_map, on="customer_id", how="left")

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div style="padding:8px 4px 20px 4px;">
            <div style="font-size:22px;font-weight:800;letter-spacing:-.5px;">🛒 SHOPINSIGHT <span style="color:#c084fc;">AI</span></div>
            <div style="font-size:10px;color:#b8c8e8;margin-top:4px;">Smarter Insights. Bigger Sales.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    nav = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Sales Analytics",
            "Product Performance",
            "Customer Intelligence",
            "Customer Reviews",
            "Delivery Analytics",
            "Payment Analysis",
            "Seller Analytics",
            "Business Insights",
            "Demo Shop",
        ],
        label_visibility="visible"
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#142e72,#4c1d95);
                    padding:15px;border-radius:14px;text-align:center;">
            <div style="font-size:28px;">🤖</div>
            <b>AI Business Insights</b>
            <div style="font-size:10px;color:#d9e4ff;margin-top:5px;">
                Turn your data into smarter decisions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# HEADER + PROFILE
# -----------------------------
profile_path = find_file("profile_photo.jpg")

c1, c2 = st.columns([4.8, 1.15])

with c1:
    st.markdown(
        '<div style="font-size:12px;font-weight:700;color:#5c70a0;margin:0 0 7px 4px;">SHOPINSIGHT AI  /  EXECUTIVE DASHBOARD</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Good Morning, Shashi! 👋</div>
            <div class="hero-sub">Here's what's happening with your store today.</div>
            <div class="hero-quote">“Data drives decisions,<br>insights drive growth.” 📈</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    photo_html = ""
    if profile_path:
        try:
            photo_bytes = Path(profile_path).read_bytes()
            photo_html = '<img class="profile-photo" src="data:image/jpeg;base64,' + base64.b64encode(photo_bytes).decode("ascii") + '">'
        except Exception:
            photo_html = ""

    st.markdown(
        f"""
        <div class="profile-card" style="text-align:center;padding:14px 12px;">
            {photo_html}
            <div class="profile-name" style="margin-top:8px;">Shashi Kushwaha</div>
            <div class="profile-role">Data Analyst | Project Developer</div>
            <span class="profile-online">● Online</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# DASHBOARD
# -----------------------------
if nav == "Dashboard":

    st.markdown('<div class="section-title">📊 Executive Overview</div>', unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">💰 Total Revenue</div>
            <div class="kpi-value">R$ {total_sales:,.0f}</div>
            <div class="kpi-note">↑ Product sales</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">🛒 Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-note">↑ Unique orders</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">👥 Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-note">↑ Unique customers</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">📦 Items Sold</div>
            <div class="kpi-value">{total_items:,}</div>
            <div class="kpi-note">↑ Units sold</div>
        </div>
        """, unsafe_allow_html=True)

    with k5:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">🏷️ Avg Order Value</div>
            <div class="kpi-value">R$ {aov:,.2f}</div>
            <div class="kpi-note">Sales ÷ orders</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div style="background:linear-gradient(100deg,#e7f0ff,#f4e9ff);border:1px solid #dce5f8;border-radius:14px;padding:11px 15px;margin:14px 0 4px 0;color:#31528c;font-size:12px;">'
        '✨ <b>Executive tip:</b> Focus on repeat-customer retention, high-value segments and 30+ day deliveries for the biggest improvement opportunities.'
        '</div>',
        unsafe_allow_html=True
    )

    # Complete-month filter for clean trend
    monthly = (
        orders.dropna(subset=["order_purchase_timestamp"])
        .assign(month=lambda x: x["order_purchase_timestamp"].dt.to_period("M").astype(str))
        .groupby("month")
        .agg(orders=("order_id", "nunique"))
        .reset_index()
    )

    monthly_sales = (
        item_orders.dropna(subset=["order_purchase_timestamp"])
        .assign(month=lambda x: x["order_purchase_timestamp"].dt.to_period("M").astype(str))
        .groupby("month")
        .agg(revenue=("price", "sum"))
        .reset_index()
    )

    monthly = monthly.merge(monthly_sales, on="month", how="left")
    monthly["revenue"] = monthly["revenue"].fillna(0)

    # Remove very small partial tail months from visual trend
    if len(monthly) > 3:
        monthly = monthly.iloc[:-1].copy()

    st.markdown('<div class="section-title">📈 Sales Performance</div>', unsafe_allow_html=True)
    a, b = st.columns(2)

    with a:
        st.markdown("#### 🛒 Monthly Orders")
        st.line_chart(monthly.set_index("month")["orders"])

    with b:
        st.markdown("#### 💰 Monthly Revenue")
        st.line_chart(monthly.set_index("month")["revenue"])

    st.markdown('<div class="section-title">📊 Product Category Performance</div>', unsafe_allow_html=True)

    cat = (
        item_product.groupby("category_display")
        .agg(
            Revenue=("price", "sum"),
            Units=("order_item_id", "count")
        )
        .sort_values("Revenue", ascending=False)
        .head(10)
    )
    st.bar_chart(cat[["Revenue"]])

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("#### 🏆 Top 10 Products by Revenue")
        prod = (
            item_product.groupby(["product_id", "category_display"])
            .agg(
                Revenue=("price", "sum"),
                Units=("order_item_id", "count")
            )
            .reset_index()
            .sort_values("Revenue", ascending=False)
            .head(10)
        )
        prod["Revenue"] = prod["Revenue"].round(2)
        st.dataframe(prod, hide_index=True, use_container_width=True)

    with right:
        st.markdown("#### 👥 Customer Segments")
        customer_revenue = (
            item_orders.groupby("customer_unique_id")["price"]
            .sum()
            .rename("revenue")
        )
        bins = [-np.inf, 50, 200, np.inf]
        labels = ["Low Value", "Medium Value", "High Value"]
        segments = pd.cut(customer_revenue, bins=bins, labels=labels)
        seg_counts = segments.value_counts().reindex(labels).fillna(0).astype(int)
        st.bar_chart(seg_counts.rename("Customers"))

    r1, r2 = st.columns(2)

    with r1:
        st.markdown("#### ⭐ Customer Reviews")
        review_counts = reviews["review_score"].value_counts().sort_index()
        st.bar_chart(review_counts.rename("Reviews"))
        avg_rating = reviews["review_score"].mean()
        st.caption(f"Average rating: **{avg_rating:.2f}/5**")

    with r2:
        st.markdown("#### 🚚 Delivery Performance")
        delivered = orders[
            orders["order_delivered_customer_date"].notna() &
            orders["order_purchase_timestamp"].notna()
        ].copy()
        delivered["delivered_at"] = pd.to_datetime(
            delivered["order_delivered_customer_date"], errors="coerce"
        )
        delivered["delivery_days"] = (
            delivered["delivered_at"] - delivered["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400
        delivered = delivered.dropna(subset=["delivery_days"])
        delivered = delivered[delivered["delivery_days"] >= 0]

        if not delivered.empty:
            st.metric("Average Delivery", f"{delivered['delivery_days'].mean():.1f} days")
            buckets = pd.cut(
                delivered["delivery_days"],
                bins=[0, 3, 7, 14, 30, np.inf],
                labels=["0–3", "4–7", "8–14", "15–30", "30+"],
                include_lowest=True
            )
            st.bar_chart(buckets.value_counts().reindex(
                ["0–3", "4–7", "8–14", "15–30", "30+"]
            ).fillna(0).rename("Orders"))

    st.markdown(
        """
        <div class="footer">
            💡 <b>Ready to grow your business?</b>
            &nbsp; Use SHOPINSIGHT AI to turn customer, product and sales data into better decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# SALES
# -----------------------------
elif nav == "Sales Analytics":
    st.markdown('<div class="section-title">📈 Sales Analytics</div>', unsafe_allow_html=True)

    sales = item_orders.copy()
    sales["month"] = sales["order_purchase_timestamp"].dt.to_period("M").astype(str)

    monthly = sales.groupby("month").agg(
        Revenue=("price", "sum"),
        Units=("order_item_id", "count"),
        Orders=("order_id", "nunique")
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", f"R$ {total_sales:,.2f}")
    c2.metric("Orders", f"{total_orders:,}")
    c3.metric("AOV", f"R$ {aov:,.2f}")

    st.markdown("#### Monthly Revenue")
    st.line_chart(monthly["Revenue"])

    st.markdown("#### Monthly Orders")
    st.line_chart(monthly["Orders"])

    st.download_button(
        "📥 Download Sales CSV",
        monthly.reset_index().to_csv(index=False).encode("utf-8"),
        "sales_analytics.csv",
        "text/csv"
    )

# -----------------------------
# PRODUCT
# -----------------------------
elif nav == "Product Performance":
    st.markdown('<div class="section-title">🏆 Product Performance</div>', unsafe_allow_html=True)

    product_perf = (
        item_product.groupby(["product_id", "category_display"])
        .agg(
            Units=("order_item_id", "count"),
            Revenue=("price", "sum"),
            Average_Price=("price", "mean")
        )
        .reset_index()
    )

    product_perf["Revenue"] = product_perf["Revenue"].round(2)
    product_perf["Average_Price"] = product_perf["Average_Price"].round(2)

    st.markdown("#### Top Products by Revenue")
    st.dataframe(
        product_perf.sort_values("Revenue", ascending=False).head(20),
        hide_index=True,
        use_container_width=True
    )

    st.markdown("#### Top Products by Units")
    st.dataframe(
        product_perf.sort_values("Units", ascending=False).head(20),
        hide_index=True,
        use_container_width=True
    )

# -----------------------------
# CUSTOMER
# -----------------------------
elif nav == "Customer Intelligence":
    st.markdown('<div class="section-title">👥 Customer Intelligence</div>', unsafe_allow_html=True)

    cr = item_orders.groupby("customer_unique_id").agg(
        Orders=("order_id", "nunique"),
        Revenue=("price", "sum")
    )

    one_time = (cr["Orders"] == 1).sum()
    repeat = (cr["Orders"] > 1).sum()
    repeat_rate = repeat / len(cr) * 100 if len(cr) else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Unique Customers", f"{len(cr):,}")
    c2.metric("Repeat Customers", f"{repeat:,}")
    c3.metric("Repeat Rate", f"{repeat_rate:.2f}%")

    segments = pd.cut(
        cr["Revenue"],
        bins=[-np.inf, 50, 200, np.inf],
        labels=["Low Value", "Medium Value", "High Value"]
    )

    st.markdown("#### Customer Value Segmentation")
    st.bar_chart(segments.value_counts().reindex(
        ["Low Value", "Medium Value", "High Value"]
    ).fillna(0).rename("Customers"))

    st.markdown("#### Highest-Value Customers")
    top_customers = cr.sort_values("Revenue", ascending=False).head(20).reset_index()
    st.dataframe(top_customers, hide_index=True, use_container_width=True)

# -----------------------------
# REVIEWS
# -----------------------------
elif nav == "Customer Reviews":
    st.markdown('<div class="section-title">⭐ Customer Reviews</div>', unsafe_allow_html=True)

    avg = reviews["review_score"].mean()
    positive = reviews["review_score"].isin([4, 5]).mean() * 100
    negative = reviews["review_score"].isin([1, 2]).mean() * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Rating", f"{avg:.2f}/5")
    c2.metric("Positive Reviews", f"{positive:.2f}%")
    c3.metric("Negative Reviews", f"{negative:.2f}%")

    counts = reviews["review_score"].value_counts().sort_index()
    st.bar_chart(counts.rename("Reviews"))

# -----------------------------
# DELIVERY
# -----------------------------
elif nav == "Delivery Analytics":
    st.markdown('<div class="section-title">🚚 Delivery Analytics</div>', unsafe_allow_html=True)

    d = orders[
        orders["order_purchase_timestamp"].notna() &
        orders["order_delivered_customer_date"].notna()
    ].copy()

    d["delivered_at"] = pd.to_datetime(
        d["order_delivered_customer_date"], errors="coerce"
    )
    d["delivery_days"] = (
        d["delivered_at"] - d["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    d = d[(d["delivery_days"] >= 0)].dropna(subset=["delivery_days"])

    if not d.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Average", f"{d['delivery_days'].mean():.2f} days")
        c2.metric("Fastest", f"{d['delivery_days'].min():.2f} days")
        c3.metric("Longest", f"{d['delivery_days'].max():.2f} days")

        buckets = pd.cut(
            d["delivery_days"],
            bins=[0, 3, 7, 14, 30, np.inf],
            labels=["0–3 days", "4–7 days", "8–14 days", "15–30 days", "30+ days"],
            include_lowest=True
        )
        st.bar_chart(buckets.value_counts().reindex(
            ["0–3 days", "4–7 days", "8–14 days", "15–30 days", "30+ days"]
        ).fillna(0).rename("Orders"))

# -----------------------------
# PAYMENT
# -----------------------------
elif nav == "Payment Analysis":
    st.markdown('<div class="section-title">💳 Payment Method Analysis</div>', unsafe_allow_html=True)

    payment_summary = (
        payments.groupby("payment_type")
        .agg(
            Transactions=("payment_type", "count"),
            Payment_Value=("payment_value", "sum")
        )
        .sort_values("Payment_Value", ascending=False)
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Payment Value")
        st.bar_chart(payment_summary["Payment_Value"])
    with c2:
        st.markdown("#### Transactions")
        st.bar_chart(payment_summary["Transactions"])

    st.dataframe(
        payment_summary.reset_index().round(2),
        hide_index=True,
        use_container_width=True
    )

# -----------------------------
# SELLER
# -----------------------------
elif nav == "Seller Analytics":
    st.markdown('<div class="section-title">🏪 Seller Analytics</div>', unsafe_allow_html=True)

    seller_perf = (
        items.groupby("seller_id")
        .agg(
            Units=("order_item_id", "count"),
            Revenue=("price", "sum"),
            Average_Item_Price=("price", "mean")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    st.dataframe(
        seller_perf.head(25).round(2),
        hide_index=True,
        use_container_width=True
    )

    top10_share = (
        seller_perf.head(10)["Revenue"].sum() / seller_perf["Revenue"].sum() * 100
        if seller_perf["Revenue"].sum() else 0
    )
    st.metric("Top 10 Seller Revenue Share", f"{top10_share:.2f}%")
    st.bar_chart(seller_perf.head(10).set_index("seller_id")["Revenue"])

# -----------------------------
# INSIGHTS
# -----------------------------
elif nav == "Business Insights":
    st.markdown('<div class="section-title">🤖 AI Business Insights</div>', unsafe_allow_html=True)

    avg_rating = reviews["review_score"].mean()
    positive = reviews["review_score"].isin([4, 5]).mean() * 100

    customer_rev = item_orders.groupby("customer_unique_id")["price"].sum()
    high_share = (customer_rev > 200).mean() * 100

    st.markdown(
        f"""
        <div class="insight">
            <h4>🧠 Smart Business Summary</h4>
            <p>💰 Total product sales are <b>R$ {total_sales:,.2f}</b> across <b>{total_orders:,}</b> orders.</p>
            <p>👥 The dataset contains <b>{total_customers:,}</b> unique customers.</p>
            <p>⭐ Average review score is <b>{avg_rating:.2f}/5</b>, with <b>{positive:.1f}%</b> positive reviews.</p>
            <p>🎯 Customers spending above R$200 represent about <b>{high_share:.1f}%</b> of customers; this group is useful for retention and loyalty campaigns.</p>
            <p>🚚 Delivery analytics should focus on the 30+ day group to reduce customer dissatisfaction and support costs.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# DEMO SHOP
# -----------------------------
elif nav == "Demo Shop":
    st.markdown('<div class="section-title">🛍️ Demo Shop</div>', unsafe_allow_html=True)
    st.caption("Demo shopping experience using the real Olist product catalogue. No real payment is processed.")

    search = st.text_input("🔎 Search Product ID")
    category = st.selectbox(
        "Category",
        ["All"] + sorted(item_product["category_display"].dropna().unique().tolist())
    )

    shop = (
        item_product.groupby(["product_id", "category_display"])
        .agg(
            Price=("price", "mean"),
            Units_Sold=("order_item_id", "count")
        )
        .reset_index()
    )

    if search:
        shop = shop[shop["product_id"].str.contains(search.strip(), case=False, na=False)]

    if category != "All":
        shop = shop[shop["category_display"] == category]

    shop = shop.sort_values("Units_Sold", ascending=False).head(30)

    if shop.empty:
        st.warning("No products found.")
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(shop.iterrows()):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="card">
                        <div style="font-size:28px;">📦</div>
                        <b style="color:#163a7a;">{row['product_id']}</b>
                        <div class="small-muted">{row['category_display']}</div>
                        <h3 style="color:#163a7a;">R$ {row['Price']:.2f}</h3>
                        <div class="small-muted">Units sold: {int(row['Units_Sold']):,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.write("")
                st.button("🛒 Add to Demo Cart", key=f"cart_{i}")

st.caption("SHOPINSIGHT AI • E-commerce Customer & Sales Intelligence • Built with Python, Pandas & Streamlit")
