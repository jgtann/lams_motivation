import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

# Page config
st.set_page_config(page_title="Student Data Dashboard", layout="wide")
st.title("📊 Student Data by Region")

# Load the data
file_path = "data/students_byregion_for_analysis.csv"
df = pd.read_csv(file_path)

# Clean region names
regions = df['region'].str.strip()
df['region'] = regions

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
selected_regions = st.sidebar.multiselect("Select Regions", options=df['region'].unique(), default=df['region'].unique())

min_pop, max_pop = st.sidebar.slider("Filter by Current Student Population", 
                                     min_value=int(df['curr_stu_pop'].min()), 
                                     max_value=int(df['curr_stu_pop'].max()),
                                     value=(int(df['curr_stu_pop'].min()), int(df['curr_stu_pop'].max())))

# Filter data
filtered_df = df[(df['region'].isin(selected_regions)) & 
                 (df['curr_stu_pop'] >= min_pop) & (df['curr_stu_pop'] <= max_pop)]

# Display filtered data table
st.subheader("📋 Filtered Data Table")
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
grid_options = gb.build()
AgGrid(filtered_df, gridOptions=grid_options, enable_enterprise_modules=True, height=300)

# Visualizations
st.subheader("📈 Visual Analytics")

# Graduates vs Entrants
fig1 = px.bar(filtered_df, x='region', y=['graduates', 'entrants'], barmode='group', title='Graduates vs Entrants by Region')
st.plotly_chart(fig1, use_container_width=True)

# Preschool Distribution
preschool_df = filtered_df[['region', 'no_preschool', '1y_preschool', '2y_preschool', '3y_preschool']].melt(id_vars='region',
    var_name='Preschool Duration', value_name='Count')
fig2 = px.bar(preschool_df, x='region', y='Count', color='Preschool Duration', title='Preschool Duration Distribution',
              barmode='stack')
st.plotly_chart(fig2, use_container_width=True)

# Gender Pie
st.subheader("👧 Gender Distribution")
for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['region']}")
    fig = px.pie(names=['Female', 'Male'], values=[row['female'], row['curr_stu_pop'] - row['female']],
                 title=f"Gender Ratio in {row['region']}")
    st.plotly_chart(fig, use_container_width=True)

# Grade-wise student numbers
grade_cols = [col for col in df.columns if col.startswith('grade')]
grade_df = filtered_df[['region'] + grade_cols].melt(id_vars='region', var_name='Grade', value_name='Students')
fig3 = px.line(grade_df, x='Grade', y='Students', color='region', markers=True, title='Grade-wise Student Numbers')
st.plotly_chart(fig3, use_container_width=True)

# Estimated 2024 Graduates Histogram
fig4 = px.histogram(filtered_df, x='est_2024_grads', nbins=20, title='Distribution of Estimated 2024 Graduates')
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.caption("Dashboard built with ❤️ using Streamlit and Plotly")
