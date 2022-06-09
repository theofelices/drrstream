import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

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
        usecols='A:L',
        nrows=1000,
    )

    return df


df = get_excel()


# ---SIDEBAR---
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Response", "Early Recovery", "Risk Resiliency"],
        default_index=0,
    )


st.sidebar.header("Filter Options:")

year = st.sidebar.multiselect(
    "Select Year:",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

province = st.sidebar.multiselect(
    "Select Province:",
    options=df["Province"].unique(),
    default=df["Province"].unique()
)

lgu = st.sidebar.multiselect(
    "Select Municipality:",
    options=df["Municipality"].unique(),
    default=df["Municipality"].unique()
)

disaster = st.sidebar.multiselect(
    "Select Disaster:",
    options=df["Disaster"].unique(),
    default=df["Disaster"].unique()
)

items = st.sidebar.multiselect(
    "Select Items:",
    options=df["Items"].unique(),
    default=df["Items"].unique()
)

df_select = df.query(
    "Year == @year & Municipality == @lgu & Province == @province & Disaster == @disaster & Items == @items"
)

if selected == "Response":
    # st.dataframe(df_select)
    # ---Mainpage---

    st.title(":bar_chart: Response Dashboard")
    st.markdown("##")

    total_releases = int(df_select["Qty_released"].sum())
    total_amount = df_select["Total_cost"].sum().round(decimals=2)
    total_lgus = list(df_select.Municipality.value_counts())

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.subheader("Total FNFI Released:")
        st.subheader(f"{total_releases: ,}")

    with middle_column:
        st.subheader("Total Amount")
        st.subheader(f"{total_amount: ,}")

    with right_column:
        st.subheader("No. of LGUs")
        st.subheader(f"{len(total_lgus): ,}")

    # ---Visualization

    fnfi_by_qtr = (

        df_select.groupby(by=["Quarter"]).sum()[
            ["Qty_released"]].sort_values(by="Qty_released")

    )

    vis_quarter_fnfi = px.bar(
        fnfi_by_qtr,
        x=fnfi_by_qtr.index,
        y="Qty_released",
        orientation="v",
        title="<b>FNFI Release by Qtr.</b>",
        color_discrete_sequence=["#0083B8"] * len(fnfi_by_qtr),
        template="plotly_white",
    )

    vis_quarter_fnfi.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))

    )

    fnfi_items = (

        df_select.groupby(by=["Items"]).sum()[
            ["Qty_released"]].sort_values(by="Qty_released")

    )

    vis_fnfi = px.bar(
        fnfi_items,
        x="Qty_released",
        y=fnfi_items.index,
        orientation="h",
        title="<b>FNFI Releases.</b>",
        color_discrete_sequence=["#0083B8"] * len(fnfi_items),
        template="plotly_white",
    )

    disaster_releases = (
        df_select.groupby(by=["Disaster"]).sum()[
            ["Qty_released"]].sort_values(by="Qty_released")

    )

    vis_disaster = px.pie(
        disaster_releases,
        values='Qty_released',
        hover_name='Qty_released'
    )

    vis_bar_disaster = px.bar(
        disaster_releases,
        x="Qty_released",
        y=disaster_releases.index,
        orientation="h",
        title="<b>Releases by Disaster.</b>",
        color_discrete_sequence=["#0083B8"] * len(fnfi_items),
        template="plotly_white",
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(vis_quarter_fnfi, use_container_width=True)
    right_column.plotly_chart(vis_fnfi, use_containter_width=True)

    pie_col, bar_col = st.columns(2)
    pie_col.write(vis_disaster, use_container_width=True)
    bar_col.plotly_chart(vis_bar_disaster, use_container_width=True)

if selected == "Early Recovery":
    st.title("Early Recovery Dashboard")

if selected == "Risk Resiliency":
    st.title("Risk Resiliency Dashboard")
