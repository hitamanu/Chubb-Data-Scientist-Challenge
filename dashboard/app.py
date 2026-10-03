from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Mexico P&C Portfolio",
    page_icon="📊",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "portfolio_mexico_filled.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["policy_start_date"] = pd.to_datetime(
        df["policy_start_date"],
        dayfirst=True,
        errors="coerce"
    )

    df["year"] = df["policy_start_date"].dt.year

    return df

df = load_data()


st.title("Mexico P&C Portfolio")
st.caption(
    "Written Premium Performance & Growth Analysis"
    "by Industry and Geography"
)


st.sidebar.header("Filters")

available_years = sorted(
    df["year"].dropna().unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Year",
    available_years
)

industry_options = [
    "All"
] + sorted(
    df["industry_final"]
    .dropna()
    .unique()
    .tolist()
)

selected_industry = st.sidebar.selectbox(
    "Industry",
    industry_options
)

state_options = [
    "All"
] + sorted(
    df["state"]
    .dropna()
    .unique()
    .tolist()
)

selected_state = st.sidebar.selectbox(
    "State",
    state_options
)

municipality_source = df.copy()

if selected_state != "All":
    municipality_source = municipality_source[
        municipality_source["state"] == selected_state
    ]

municipality_options = [
    "All"
] + sorted(
    municipality_source["municipality"]
    .dropna()
    .unique()
    .tolist()
)

selected_municipality = st.sidebar.selectbox(
    "Municipality",
    municipality_options
)

filtered = df.copy()

if selected_industry != "All":
    filtered = filtered[
        filtered["industry_final"] == selected_industry
    ]

if selected_state != "All":
    filtered = filtered[
        filtered["state"] == selected_state
    ]

if selected_municipality != "All":
    filtered = filtered[
        filtered["municipality"] == selected_municipality
    ]


current = filtered[
    filtered["year"] == selected_year
]

previous = filtered[
    filtered["year"] == selected_year - 1
]

current_premium = current["premium"].sum()
previous_premium = previous["premium"].sum()

if previous_premium > 0:
    premium_growth = (
        current_premium / previous_premium
    ) - 1
else:
    premium_growth = None

premium_change = (
    current_premium - previous_premium
)

policies = current["policy_id"].nunique()
clients = current["ClientId"].nunique()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Written Premium",
    f"${current_premium / 1_000_000:,.1f}M"
)

col2.metric(
    "Premium Growth YoY",
    f"{premium_growth:.1%}"
    if premium_growth is not None
    else "N/A",
    f"${premium_change / 1_000_000:+,.1f}M"
    if previous_premium > 0
    else None
)

col3.metric(
    "Policies",
    f"{policies:,}"
)

col4.metric(
    "Clients",
    f"{clients:,}"
)

st.subheader("Key Insights")

if previous_premium > 0:

    premium_direction = (
        "increased"
        if premium_change > 0
        else "decreased"
    )

    insight_1 = (
        f"Written Premium {premium_direction} "
        f"{abs(premium_growth):.1%} versus "
        f"{selected_year - 1}, representing an absolute "
        f"change of MXN ${abs(premium_change):,.0f}."
    )

else:

    insight_1 = (
        "Year-over-year growth is not available because "
        "there is no prior-year observation."
    )

st.markdown(f"**Portfolio:** {insight_1}")

trend = (
    filtered
    .groupby("year", as_index=False)
    .agg(
        premium=("premium", "sum")
    )
)

fig_trend = px.line(
    trend,
    x="year",
    y="premium",
    markers=True,
    title="Written Premium Trend"
)

fig_trend.update_yaxes(
    title="Premium (MXN)"
)

fig_trend.update_xaxes(
    dtick=1
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


industry_current = (
    current
    .groupby(
        "industry_final",
        as_index=False
    )
    .agg(
        premium=("premium", "sum")
    )
    .sort_values(
        "premium",
        ascending=True
    )
)

fig_industry = px.bar(
    industry_current,
    x="premium",
    y="industry_final",
    orientation="h",
    title=f"Written Premium by Industry — {selected_year}"
)

fig_industry.update_xaxes(
    title="Premium (MXN)"
)

fig_industry.update_yaxes(
    title=""
)


industry_year = (
    filtered[
        filtered["year"].isin(
            [selected_year - 1, selected_year]
        )
    ]
    .groupby(
        ["industry_final", "year"],
        as_index=False
    )
    .agg(
        premium=("premium", "sum")
    )
)

industry_pivot = (
    industry_year
    .pivot(
        index="industry_final",
        columns="year",
        values="premium"
    )
    .fillna(0)
)

if selected_year not in industry_pivot.columns:
    industry_pivot[selected_year] = 0

if selected_year - 1 not in industry_pivot.columns:
    industry_pivot[selected_year - 1] = 0

industry_pivot["premium_change"] = (
    industry_pivot[selected_year]
    - industry_pivot[selected_year - 1]
)

industry_change = (
    industry_pivot[
        ["premium_change"]
    ]
    .reset_index()
    .sort_values(
        "premium_change",
        ascending=True
    )
)

fig_change = px.bar(
    industry_change,
    x="premium_change",
    y="industry_final",
    orientation="h",
    title=f"Premium Change by Industry — {selected_year} vs {selected_year - 1}"
)

fig_change.update_xaxes(
    title="Premium Change (MXN)"
)

fig_change.update_yaxes(
    title=""
)

valid_industry_change = industry_change.dropna(
    subset=["premium_change"]
)

if (
    selected_year > df["year"].min()
    and selected_industry == "All"
    and not valid_industry_change.empty
):

    top_positive = valid_industry_change.loc[
        valid_industry_change["premium_change"].idxmax()
    ]

    top_negative = valid_industry_change.loc[
        valid_industry_change["premium_change"].idxmin()
    ]

    st.markdown("#### Industry Highlights")

    st.markdown(
        f"**Largest positive contributor:** "
        f"{top_positive['industry_final']} "
        f"with a Premium increase of "
        f"MXN ${top_positive['premium_change']:,.0f}."
    )

    st.markdown(
        f"**Largest negative contributor:** "
        f"{top_negative['industry_final']} "
        f"with a Premium decrease of "
        f"MXN ${abs(top_negative['premium_change']):,.0f}."
    )

elif selected_year == df["year"].min():

    st.markdown(
        "#### Industry Highlights\n"
        "Year-over-year industry comparisons are not available "
        "for the first year in the portfolio."
    )

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_industry,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig_change,
        use_container_width=True
    )

st.subheader("Geographic Analysis")

state_year = (
    filtered[
        filtered["year"].isin(
            [selected_year - 1, selected_year]
        )
    ]
    .groupby(
        ["state", "year"],
        as_index=False
    )
    .agg(
        premium=("premium", "sum"),
        policies=("policy_id", "nunique"),
        clients=("ClientId", "nunique")
    )
)

state_pivot = (
    state_year
    .pivot(
        index="state",
        columns="year",
        values="premium"
    )
    .fillna(0)
)

if selected_year not in state_pivot.columns:
    state_pivot[selected_year] = 0

if selected_year - 1 not in state_pivot.columns:
    state_pivot[selected_year - 1] = 0

state_pivot["premium"] = (
    state_pivot[selected_year]
)

state_pivot["premium_previous_year"] = (
    state_pivot[selected_year - 1]
)

if selected_year == df["year"].min():

    state_pivot["premium_change"] = pd.NA
    state_pivot["premium_growth_yoy"] = pd.NA

else:

    state_pivot["premium_change"] = (
        state_pivot["premium"]
        - state_pivot["premium_previous_year"]
    )

    state_pivot["premium_growth_yoy"] = (
        state_pivot["premium"]
        .div(
            state_pivot[
                "premium_previous_year"
            ].replace(0, pd.NA)
        )
        .sub(1)
    )

state_pivot["premium_growth_yoy"] = (
    state_pivot["premium"]
    .div(
        state_pivot["premium_previous_year"]
        .replace(0, pd.NA)
    )
    .sub(1)
)

state_analysis = (
    state_pivot[
        [
            "premium",
            "premium_previous_year",
            "premium_change",
            "premium_growth_yoy"
        ]
    ]
    .reset_index()
)

state_premium = (
    state_analysis
    .sort_values(
        "premium",
        ascending=True
    )
)

fig_state_premium = px.bar(
    state_premium,
    x="premium",
    y="state",
    orientation="h",
    title=f"Written Premium by State — {selected_year}",
    labels={
        "premium": "Written Premium (MXN)",
        "state": ""
    }
)

fig_state_premium.update_layout(
    showlegend=False
)

fig_state_premium.update_xaxes(
    tickprefix="$",
    separatethousands=True
)

state_change = (
    state_analysis
    .sort_values(
        "premium_change",
        ascending=True
    )
)

fig_state_change = px.bar(
    state_change,
    x="premium_change",
    y="state",
    orientation="h",
    title=(
        f"Premium Change by State — "
        f"{selected_year} vs {selected_year - 1}"
    ),
    labels={
        "premium_change": "Premium Change (MXN)",
        "state": ""
    }
)

fig_state_change.add_vline(
    x=0,
    line_width=1
)

fig_state_change.update_xaxes(
    tickprefix="$",
    separatethousands=True
)

geo_left, geo_right = st.columns(2)

with geo_left:
    st.plotly_chart(
        fig_state_premium,
        use_container_width=True
    )

with geo_right:
    st.plotly_chart(
        fig_state_change,
        use_container_width=True
    )

valid_growth = (
    state_analysis[
        state_analysis[
            "premium_growth_yoy"
        ].notna()
    ]
    .sort_values(
        "premium_growth_yoy",
        ascending=True
    )
)

fig_state_growth = px.bar(
    valid_growth,
    x="premium_growth_yoy",
    y="state",
    orientation="h",
    title=f"Premium Growth YoY by State — {selected_year}",
    labels={
        "premium_growth_yoy": "Premium Growth YoY",
        "state": ""
    }
)

fig_state_growth.add_vline(
    x=0,
    line_width=1
)

fig_state_growth.update_xaxes(
    tickformat=".0%"
)

st.plotly_chart(
    fig_state_growth,
    use_container_width=True
)

st.subheader("State Performance Detail")

state_table = (
    state_analysis
    .sort_values(
        "premium",
        ascending=False
    )
    .copy()
)

state_table["premium"] = (
    state_table["premium"]
    / 1_000_000
)

state_table["premium_change"] = (
    state_table["premium_change"]
    / 1_000_000
)

state_table = state_table.rename(
    columns={
        "state": "State",
        "premium": "Premium (MXN M)",
        "premium_change": "Premium Change (MXN M)",
        "premium_growth_yoy": "Premium Growth YoY"
    }
)

st.dataframe(
    state_table[
        [
            "State",
            "Premium (MXN M)",
            "Premium Change (MXN M)",
            "Premium Growth YoY"
        ]
    ],
    hide_index=True,
    use_container_width=True,
    column_config={
        "Premium (MXN M)": st.column_config.NumberColumn(
            format="$%.1f M"
        ),
        "Premium Change (MXN M)": st.column_config.NumberColumn(
            format="$%+.1f M"
        ),
        "Premium Growth YoY": st.column_config.NumberColumn(
            format="percent"
        )
    }
)

st.divider()

st.caption(
    "Premium represents written premium grouped by policy inception year. "
    "YoY Growth compares the selected year with the previous inception year. "
    "Unknown industries are retained to preserve transparency regarding "
    "unresolved industry classifications."
)
