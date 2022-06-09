import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Response Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)


@st.cache
def get_excel():
    df = pd.read_excel(
        io='drrs_aug.xlsx',
        engine='openpyxl',
        sheet_name='data',
        skiprows=1,
        usecols='A:K',
        nrows=1000,
    )

    return df


df = get_excel()


# ---SIDEBAR---

st.sidebar.header("Please Filter Here:")
lgu = st.sidebar.multiselect(
    "Select LGU:",
    options=df["Municipality"].unique(),
    default=df["Municipality"].unique()
)

htype = st.sidebar.multiselect(
    "Select House Type:",
    options=df["House_type"].unique(),
    default=df["House_type"].unique()
)

hcondition = st.sidebar.multiselect(
    "Select House Condition:",
    options=df["House_condition"].unique(),
    default=df["House_condition"].unique()
)

hlocation = st.sidebar.multiselect(
    "Select House Location:",
    options=df["House_location"].unique(),
    default=df["House_location"].unique()
)

df_select = df.query(
    "Municipality == @lgu & House_type == @htype & House_condition == @hcondition & House_location == @hlocation"
)

# st.dataframe(df_select)
# ---Mainpage---

st.title(":bar_chart: Validation Dashboard")
st.markdown("##")

total_count = int(df_select["Surname"].count())
#lgu_group = df_select["Municipality"].unique()
#lgu_count = lgu_group.count()


left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Families Validated:")
    st.subheader(f"{total_count: ,}")

# with middle_column:
 #   st.subheader("No. of LGUs Validated")
  #  st.subheader(f"{lgu_count: ,}")
