import streamlit as st
import pandas as pd
import plotly.express as px
import src.database as db

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Admin Dashboard 📊")

# Refresh Button
if st.button("Refresh Data"):
    st.rerun()

# Fetch Data
df = db.fetch_all_submissions()

if df.empty:
    st.info("No submissions yet.")
else:
    # 1. High-level Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Submissions", len(df))
    with col2:
        st.metric("Average Rating", f"{df['rating'].mean():.2f} / 5.0")

    st.divider()

    # 2. Analytics (Distribution)
    st.subheader("Rating Distribution")
    rating_counts = df['rating'].value_counts().reset_index()
    rating_counts.columns = ['Rating', 'Count']
    
    fig = px.bar(
        rating_counts, 
        x='Rating', 
        y='Count', 
        text='Count',
        title="Submissions by Star Rating",
        color='Rating',
        category_orders={"Rating": [1, 2, 3, 4, 5]}
    )
    fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 3. Detailed View
    st.subheader("Recent Submissions")
    
    # Display as a dataframe with specific columns
    display_df = df[['created_at', 'rating', 'review', 'summary', 'recommendations']]
    st.dataframe(
        display_df,
        column_config={
            "created_at": st.column_config.DatetimeColumn("Date", format="D MMM YYYY, h:mm a"),
            "rating": st.column_config.NumberColumn("Rating", format="%d ⭐"),
            "review": "User Review",
            "summary": "AI Summary",
            "recommendations": "AI Recommendations"
        },
        use_container_width=True,
        hide_index=True
    )
