import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="China University Rankings Dashboard", page_icon="🎓", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["score_num"] = pd.to_numeric(df["score"].replace("-", pd.NA), errors="coerce")
    df["rank_num"] = pd.to_numeric(df["national_rank"].replace("-", pd.NA), errors="coerce")
    df["province_display"] = df["province"].replace("-", "Unknown")
    df["category_display"] = df["category"].replace("-", "Unknown")
    df["uni_type_display"] = df["uni_type"].replace("-", "Unknown")
    return df

df = load_data()

st.title("China University Rankings Dashboard | Team China Insights")
st.caption("For education-market analysts and university partnership managers: compare institutions and identify strong regional or category opportunities.")
st.caption("Data: 582 Chinese universities in the supplied CSV snapshot; intended production refresh: annually after the ranking publisher releases a new edition.")

with st.sidebar:
    st.header("Filters")
    provinces = st.multiselect("Province", sorted(df["province_display"].unique()), default=[])
    categories = st.multiselect("University category", sorted(df["category_display"].unique()), default=[])
    top_n = st.slider("Show top N ranked universities", 10, 100, 25, 5)
    only_scored = st.checkbox("Only universities with a numeric score", value=True)

filtered = df.copy()
if provinces:
    filtered = filtered[filtered["province_display"].isin(provinces)]
if categories:
    filtered = filtered[filtered["category_display"].isin(categories)]
if only_scored:
    filtered = filtered[filtered["score_num"].notna()]

ranked = filtered.sort_values(["rank_num", "score_num"], na_position="last").copy()
valid_scores = filtered["score_num"].dropna()
metrics = st.columns(3)
metrics[0].metric("Universities in view", f"{len(filtered):,}")
metrics[1].metric("Average score", f"{valid_scores.mean():,.1f}" if len(valid_scores) else "—")
metrics[2].metric("Top-ranked university", ranked.iloc[0]["name"] if len(ranked) else "—")

if len(filtered):
    left, right = st.columns(2)
    with left:
        st.subheader("Where are the universities?")
        counts = filtered.groupby("province_display", as_index=False).size().sort_values("size", ascending=False).head(15)
        fig = px.bar(counts.sort_values("size"), x="size", y="province_display", orientation="h", labels={"size":"Universities", "province_display":"Province"})
        fig.update_layout(height=430, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Score distribution by category")
        chart_df = filtered[filtered["score_num"].notna()]
        fig = px.box(chart_df, x="category_display", y="score_num", points=False, labels={"category_display":"Category", "score_num":"Score"})
        fig.update_layout(height=430, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Top {min(top_n, len(ranked))} universities in the current view")
    table = ranked.head(top_n)[["national_rank", "name", "name_zh", "city", "province_display", "category_display", "score_num", "tags"]].rename(columns={"national_rank":"National rank", "name":"University", "name_zh":"Chinese name", "city":"City", "province_display":"Province", "category_display":"Category", "score_num":"Score", "tags":"Tags"})
    st.dataframe(table, use_container_width=True, hide_index=True)
else:
    st.warning("No universities match the current filters. Clear one or more filters to continue.")

with st.expander("Data notes and limitations"):
    st.write("The CSV is a frozen snapshot, so the dashboard shows cross-sectional comparisons rather than trends. Nine rows have an unavailable category and most rows have no numeric score; unavailable values are labeled Unknown or excluded from score calculations. The source also contains placeholder '-' values in some fields, which are kept visible in the detail table where relevant.")
