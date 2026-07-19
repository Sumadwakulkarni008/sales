
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

st.title("📊 Sales Analytics Dashboard")
st.markdown("### Interactive Business Intelligence Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

# ---------------- Sidebar ----------------
st.sidebar.header("🔎 Filters")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

state = st.sidebar.multiselect(
    "State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

start_date = st.sidebar.date_input("Start Date", df["Order Date"].min().date())
end_date = st.sidebar.date_input("End Date", df["Order Date"].max().date())

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["State"].isin(state)) &
    (df["Order Date"] >= pd.to_datetime(start_date)) &
    (df["Order Date"] <= pd.to_datetime(end_date))
].copy()

filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M").astype(str)

# ---------------- KPI ----------------
c1,c2,c3,c4 = st.columns(4)
c1.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
c2.metric("📈 Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
c3.metric("🛒 Orders", filtered_df["Order ID"].nunique())
c4.metric("👥 Customers", filtered_df["Customer ID"].nunique())

st.divider()

# ---------------- Charts Row 1 ----------------
l,r = st.columns(2)

with l:
    cat = filtered_df.groupby("Category",as_index=False)["Sales"].sum()
    fig = px.bar(cat,x="Category",y="Sales",color="Category",text_auto=".2s",
                 title="Sales by Category")
    st.plotly_chart(fig,use_container_width=True)

with r:
    monthly = filtered_df.groupby("Month",as_index=False)["Sales"].sum()
    fig = px.line(monthly,x="Month",y="Sales",markers=True,title="Monthly Sales Trend")
    st.plotly_chart(fig,use_container_width=True)

# ---------------- Charts Row 2 ----------------
l,r = st.columns(2)

with l:
    reg = filtered_df.groupby("Region",as_index=False)["Sales"].sum()
    fig = px.pie(reg,names="Region",values="Sales",title="Sales by Region")
    st.plotly_chart(fig,use_container_width=True)

with r:
    prof = filtered_df.groupby("Category",as_index=False)["Profit"].sum()
    fig = px.bar(prof,x="Category",y="Profit",color="Category",text_auto=".2s",
                 title="Profit by Category")
    st.plotly_chart(fig,use_container_width=True)

st.divider()

# ---------------- Tables ----------------
l,r = st.columns(2)

with l:
    st.subheader("🏆 Top 10 Selling Products")
    top_products = (filtered_df.groupby("Product Name",as_index=False)["Sales"]
                    .sum().sort_values("Sales",ascending=False).head(10))
    st.dataframe(top_products,use_container_width=True)

with r:
    st.subheader("👥 Top 10 Customers")
    top_customers = (filtered_df.groupby("Customer Name",as_index=False)["Sales"]
                     .sum().sort_values("Sales",ascending=False).head(10))
    st.dataframe(top_customers,use_container_width=True)

l,r = st.columns(2)

with l:
    st.subheader("📉 Top 10 Loss-Making Products")
    loss = (filtered_df.groupby("Product Name",as_index=False)["Profit"]
            .sum().sort_values("Profit").head(10))
    st.dataframe(loss,use_container_width=True)

with r:
    st.subheader("🏅 Top 10 States by Sales")
    states = (filtered_df.groupby("State",as_index=False)["Sales"]
              .sum().sort_values("Sales",ascending=False).head(10))
    st.dataframe(states,use_container_width=True)

st.subheader("📄 Filtered Dataset")
st.dataframe(filtered_df,use_container_width=True,height=300)

st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_sales.csv",
    "text/csv"
)
