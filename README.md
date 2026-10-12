# China University Rankings Dashboard

## Step 1 — Dataset and decision-maker

**Dataset.** `data.csv` is the supplied *Best-Global-Universities-China* CSV. It contains 582 university records and 13 fields, including university name, city, province, category, national rank, score, language, and tags. One row represents one university in the ranking snapshot. The file is a small tabular CSV (about 77 KB) and is suitable for a public Streamlit repository. Dataset search/source link: https://www.kaggle.com/datasets?search=Best%20Global%20Universities%20China (the supplied file should be matched to the exact Kaggle record before publication).

**Decision-maker.** The dashboard is for an education-market analyst or university partnership manager who compares institutions across regions and categories when building a shortlist for outreach, benchmarking, or program partnerships.

## Step 2 — Why a dashboard?

The user checks the same comparison questions repeatedly: which provinces have the largest pool of institutions, which categories have stronger scores, and which universities are at the top of a selected market. If the decision-maker sees a concentrated province or a high-scoring category on this dashboard, they will prioritize that segment for research and partnership outreach.

Without the dashboard, they would repeatedly open the CSV, clean placeholder values, sort by rank, and make one-off charts. That creates avoidable time cost and increases the risk of comparing the wrong subset or overlooking a regional pattern.

A dashboard fits this recurring workflow better than a weekly email because the analyst needs interactive slices by province and category. A static report would require a new version for every question; an alert would be too narrow for exploratory shortlisting.

## Step 3 — What matters

### EDA findings

- Shape: 582 rows × 13 columns.
- The most common categories are STEM (207), comprehensive (172), and normal (155).
- The data covers 32 provinces and 54 city values; Jiangsu, Shandong, Henan, Liaoning, and Beijing are among the largest province groups.
- The score field contains numeric values plus `-` placeholders, so score summaries exclude unavailable scores.
- The university type field is sparse: most records contain `-`, so it is not used as a headline comparison.

### Dashboard elements

- **Headline numbers:** universities in the current view, average numeric score, and the top-ranked university. These answer “how large is this shortlist, how strong is it on average, and who leads it?” within five seconds.
- **Province bar chart:** explains the size and geographic concentration of the current selection.
- **Score box plot by category:** explains score spread and makes category differences visible without implying that a single average tells the whole story.
- **Filters:** province, category, top-N table size, and an option to keep only rows with numeric scores. These are the controls a partnership analyst can use directly.
- **Detail table:** supports follow-up after the overview; it is at the bottom because it is for shortlist inspection rather than the first decision.

### Deliberately omitted

1. **Language of instruction:** it may be interesting for international programs, but it does not change the first-pass regional and ranking shortlist and is too granular for the main page.
2. **Slug, aliases, and tags as charts:** these are identifiers or semi-structured metadata. Showing them as charts would add visual noise without supporting a clear action.

### Misleading or incomplete data

The CSV is a frozen snapshot, so no time trend can be inferred. Placeholder `-` values are treated as unavailable: category and type display as `Unknown`, while score calculations exclude missing scores. The app states the snapshot period and refresh plan above the KPIs. The ranking and score should be treated as source-published indicators, not as a complete measure of institutional quality.

### Page order

The page starts with the title and context, then filters, then three KPIs, followed by the two explanatory charts, and finally the shortlist table. This follows the decision flow: notice the current situation, understand why it looks that way, then inspect records to act.

## Step 4 — Refresh and review decision

In production, refresh the data **annually**, after the ranking publisher releases a new edition. The source is a ranking snapshot rather than a live operational system, so hourly or daily refreshes would not change a decision and would create unnecessary maintenance. The analyst can review the dashboard monthly during partnership planning and again when a new ranking edition arrives.

Track the average score and the number of universities in the selected province/category. A practical action threshold is a change of **10% or more** in average score or shortlist size between ranking editions: that should trigger a review of the target list and a check of the source methodology. Stale data can cause outreach to focus on institutions whose rank or category has materially changed; a one-week delay is immaterial, while a full ranking-edition delay can distort annual planning.

## Run locally

```bash
uv init
uv add streamlit pandas plotly
streamlit run app.py
```

For Streamlit Cloud, set Python to 3.14 in Advanced settings and deploy this folder. The required submission URLs are the deployed app URL and the public GitHub repository URL.

