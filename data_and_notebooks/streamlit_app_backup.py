# ===============================================================
# 🧠 Imports & Config
# ===============================================================
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import pycountry
import pycountry_convert as pc


st.set_page_config(page_title="Inside Esports Prize Pools & Top Players Careers", layout="wide")

st.markdown("""
<style>

/* Base font and background */
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    font-size: 25px !important;
    color: #222;
    background-color: #c3d7ea;  /* 👈 Change this color if needed */
}

/* Sidebar (navigation panel) */
section[data-testid="stSidebar"] {
    font-size: 1.1rem !important,
    background-color: #c3d7ea;
}

/* st.metric components */
div[data-testid="metric-container"] {
    padding: 1.5rem 0;
}

div[data-testid="metric-container"] .metric-label {
    font-size: 2.1rem !important;
    font-weight: 600 !important;
    opacity: 0.9 !important;
}

div[data-testid="metric-container"] .metric-value {
    transform: scale(2.3);
    font-weight: bold !important;
}

/* Optional: dropdowns and checkboxes */
.stSelectbox label, .stCheckbox label {
    font-size: 1.1rem !important;
}

</style>
""", unsafe_allow_html=True)





# ===============================================================
# 📦 Load Data
# ===============================================================
def load_games_data():
    df = pd.read_csv("./games_metadata_enriched.csv")
    df['TotalUSDPrize'] = df['TotalUSDPrize'].fillna(0)
    df['TotalPlayers'] = df['TotalPlayers'].fillna(0)
    df['TotalTournaments'] = df['TotalTournaments'].fillna(0)
    return df

games_df = load_games_data()

# ===============================================================
# 📊 Slide 1 – Prize Pool Bar Chart (Top 15)
# ===============================================================

def slide_1_prize_bar():
    st.markdown("<h2 style='color:#00b4d8;'>🎯 Slide 1 – Top Games by Prize Pool</h2>", unsafe_allow_html=True)

    # Dropdown filter
    game_types = ["All"] + sorted(games_df['GameType'].dropna().unique())
    selected_type = st.selectbox("🎮 Filter by Game Type", game_types)

    # Filtered dataset
    if selected_type == "All":
        filtered_df = games_df.copy()
    else:
        filtered_df = games_df[games_df["GameType"] == selected_type].copy()

    # Slice top 15 by prize
    top15_df = filtered_df.sort_values(by='TotalUSDPrize', ascending=False).head(15).copy()
    top15_df["PrizeMillions"] = top15_df["TotalUSDPrize"] / 1_000_000
    top15_df["PrizeText"] = top15_df["PrizeMillions"].apply(lambda x: f"${x:.0f}M")

    # KPI scope
    show_top15_kpis = st.checkbox("🔍 Show KPIs for Top 15 only", value=False)
    kpi_df = top15_df if show_top15_kpis else filtered_df

    # Color palette
    custom_colors = {
        'MOBA': '#5f78ff',
        'Battle Royale': '#ff6361',
        'FPS': '#43d9a5',
        'Sports': '#b266ff',
        'RTS': '#ffa600',
        'Card Game': '#00c2ff',
        'Auto Battler': '#ffc658',
        'Other': '#aaaaaa'
    }

    # Create bar chart
    fig_bar = px.bar(
        top15_df,
        x="PrizeMillions",
        y="GameName",
        color="GameType",
        color_discrete_map=custom_colors,
        orientation="h",
        text="PrizeText",
        title="Top 15 Esports Games by Total Prize Pool",
        labels={"PrizeMillions": "Prize Pool (Million USD)", "GameName": "Game"}
    )

    # Build mapping BEFORE looping over traces
    customdata_map = {
        row["GameName"]: [row["GameType"], row["TotalPlayers"], row["TotalTournaments"]]
        for _, row in top15_df.iterrows()
    }

    # Inject correct customdata per trace
    for trace in fig_bar.data:
        trace_customdata = [customdata_map[game] for game in trace.y]
        trace.update(
            customdata=trace_customdata,
            hovertemplate=(
                "<b>Game Type:</b> %{customdata[0]}<br>" +
                "<b>Game:</b> %{y}<br>" +
                "<b>Prize Pool:</b> $%{x:.1f}M<br>" +
                "<b>Total Players:</b> %{customdata[1]}<br>" +
                "<b>Total Tournaments:</b> %{customdata[2]}<extra></extra>"
            )
        )

    # Layout update
    fig_bar.update_layout(
        xaxis_title="Total Prize Pool (in Millions USD)",
        yaxis_title="",
        yaxis=dict(autorange="reversed", color="white"),
        xaxis=dict(color="white"),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='white', size=14),
        height=750,
        title=dict(x=0.3, font=dict(color="white", size=26)),
        showlegend=True,
        legend=dict(font=dict(color='white'))
    )
    fig_bar.update_layout(
        font=dict(size=29),  # Global font
        title=dict(font=dict(size=24)),
        xaxis=dict(title_font=dict(color="white", size=20), tickfont=dict(color="white", size=18)),
        yaxis=dict(title_font=dict(size=20), tickfont=dict(color="white", size=18))
    )

    # KPI display
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Prize", f"${kpi_df['TotalUSDPrize'].sum():,.0f}")
    col2.metric("Games", len(kpi_df))
    col3.metric("Players", f"{int(kpi_df['TotalPlayers'].sum()):,}")
    col4.metric("Tournaments", f"{int(kpi_df['TotalTournaments'].sum()):,}")

    # Display chart
    col1, col2 = st.columns([2.3,0.7])
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.markdown(
        "<div style='margin-top:80px'></div><p style='color:black; font-size:1.2rem;'>💡 The global prize pool exceeds $1.8B — but most of it is concentrated in just a few titles. "
        "This chart highlights the top 15, while KPIs reflect your current filter scope (all games or top 15 only).</p>",
        unsafe_allow_html=True
    )
    # Footer comment



# ===============================================================
# 📊 Slide 2 – Prize distribution top 5k-1k
# ===============================================================

def slide_2_prize_distribution():
    """
    Slide 2 – Displays the prize distribution among the top 1000 or 5000 esports players.
    Includes linear/log scale toggle and dynamic chart updates.
    """
    st.markdown("<h2 style='color:#00b4d8;'>📈 Slide 2 – Earnings Distribution by Player Rank</h2>", unsafe_allow_html=True)

    # Load data
    df_5000 = pd.read_csv("./top_5000_players.csv")
    df_5000_sorted = df_5000.sort_values(by="TotalUSDPrize", ascending=False).reset_index(drop=True)
    df_5000_sorted["Rank"] = df_5000_sorted.index + 1

    # Toggle for subset
    selection = st.radio("🎯 Select player scope", ["Top 1000", "Top 5000"], horizontal=True)

    if selection == "Top 1000":
        df_display = df_5000_sorted.head(1000)
        title = "Top 1000 Players – Earnings Distribution"
        line_color = 'deepskyblue'
    else:
        df_display = df_5000_sorted
        title = "Top 5000 Players – Earnings Distribution"
        line_color = 'deepskyblue'

    # Total earnings KPI
    if selection == "Top 1000":
        total_prize = df_display["TotalUSDPrize"].sum()
        st.markdown(
            f"<div style='color:black; font-size:1.4rem; margin-top:-1rem; padding-bottom:0.5rem;'>Total Prize: <strong>${total_prize:,.0f}</strong></div>",
            unsafe_allow_html=True
        )
    else:
        total_prize = df_display["TotalUSDPrize"].sum()
        st.markdown(
            f"<div style='color:black; font-size:1.4rem; margin-top:-1rem; padding-bottom:0.5rem;'>Total Prize: <strong>${total_prize:,.0f}</strong></div>",
            unsafe_allow_html=True
        )


    # Chart
    fig = px.area(
        df_display,
        x="Rank",
        y="TotalUSDPrize",
        title=title,
        template="plotly_dark",
    )

    fig.update_traces(
        line=dict(color=line_color, width=3),
        hovertemplate="<b>Rank:</b> %{x}<br>" +
                "<b>Player:</b> %{customdata[0]}<br>" +
                "<b>Total Earnings:</b> $%{y:,.0f}<extra></extra>",
        customdata=df_display[["CurrentHandle"]]
    )

    fig.update_layout(
        xaxis_title="Player Rank",
        yaxis_title="Total Prize (USD)",
        xaxis=dict(
            tickfont=dict(size=22, color='white'),
            title_font=dict(size=22, color='white')
        ),
        yaxis=dict(
            tickfont=dict(size=22, color='white'),
            title_font=dict(size=22, color='white')
        ),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='white', size=14),
        height=700,
        title=dict(x=0.3, font=dict(color="white", size=32)),
    )

    # Ligne médiane
    median_val = df_display["TotalUSDPrize"].median()
    fig.add_hline(
        y=median_val,
        line_dash="dot",
        line_color="red",
        annotation=dict(
            text=f"Median ≈ ${median_val/1000:.0f}K",
            font=dict(color="red", size=19, weight="bold"),
            x=0.11,
            xanchor="right",
            yanchor="bottom",
            showarrow=False,
            bgcolor="rgba(0,0,0,0.4)"
        )
    )
    # Annotation
    def add_prize_annotation(fig, df, threshold, label=None, color="white", ax_offset=60, ay_offset=-40):
        row = df[df["TotalUSDPrize"] >= threshold].tail(1)
        if not row.empty:
            rank = int(row["Rank"].values[0])
            prize = int(row["TotalUSDPrize"].values[0])
            fig.add_annotation(
                x=rank,
                y=prize,
                text=f"{label}",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                ax=ax_offset,
                ay=ay_offset,
                font=dict(color=color, size=22),
                bgcolor="rgba(0,0,0,0.6)",
                bordercolor=None,
                borderwidth=1
            )
    add_prize_annotation(fig, df_display, threshold=1_000_000, label="$1M", color="deepskyblue")
    add_prize_annotation(fig, df_display, threshold=500_000, label="$500K", color="deepskyblue", ax_offset=80)

    if selection == "Top 5000":
        add_prize_annotation(fig, df_display, threshold=100_000, label="$100K", color="deepskyblue", ax_offset=100)



    # ➡️ Display side-by-side: map left, bar right
    col1, col2 = st.columns([2,1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown(
            """
            <div style='color:black; font-size:1.2rem;'><div style='margin-top:130px'></div>
                <p>💡 Earnings decline <b>very sharply</b> as rank increases — the curve is extremely steep.</p>
                <p>💡 Showing both top 1000 and 5000 helps highlight how earnings are distributed across a wider pool.</p>
                <p>💡 We focus on the top 1000 for the rest of the analysis to keep consistent, detailed career insights.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ===============================================================
# 📊 Slide 3 – Geographic distribution
# ===============================================================

def slide_3_geographic_distribution():
    st.markdown("<h2 style='color:#00b4d8;'>🌍 Geographic Distribution of Top Esports Players</h2>", unsafe_allow_html=True)

    # 📅 Load player data
    players_df = pd.read_csv("players_profiles_with_id.csv")
    players_df['CountryCode'] = players_df['CountryCode'].fillna('').str.upper()

    # ISO2 → ISO3 via pycountry
    iso2_to_iso3 = {country.alpha_2: country.alpha_3 for country in pycountry.countries}
    players_df['CountryISO3'] = players_df['CountryCode'].map(iso2_to_iso3)

    # ISO3 → Continent via pycountry_convert
    def iso3_to_continent_func(iso3):
        try:
            iso2 = pc.country_alpha3_to_country_alpha2(iso3)
            continent_code = pc.country_alpha2_to_continent_code(iso2)
            return {
                "AF": "Africa",
                "AS": "Asia",
                "EU": "Europe",
                "NA": "North America",
                "OC": "Oceania",
                "SA": "South America"
            }.get(continent_code, "Unknown")
        except:
            return "Unknown"

    players_df["Continent"] = players_df["CountryISO3"].apply(iso3_to_continent_func)

    # All ISO3 and Country Names
    all_iso3 = [country.alpha_3 for country in pycountry.countries]
    iso3_to_name = {country.alpha_3: country.name for country in pycountry.countries}
    df_all = pd.DataFrame({
        "CountryISO3": all_iso3,
        "CountryName": [iso3_to_name[iso3] for iso3 in all_iso3]
    })

    # Stats
    df_stats = players_df.groupby("CountryISO3").agg(
        PlayerCount=("TotalUSDPrize", "count"),
        TotalPrize=("TotalUSDPrize", "sum"),
        AvgPrize=("TotalUSDPrize", "mean")
    ).reset_index()

    df_country = df_all.merge(df_stats, on="CountryISO3", how="left")
    continent_map = players_df[["CountryISO3", "Continent"]].drop_duplicates(subset="CountryISO3").set_index("CountryISO3")["Continent"]
    df_country["Continent"] = df_country["CountryISO3"].map(continent_map)
    df_country[["PlayerCount", "TotalPrize", "AvgPrize"]] = df_country[["PlayerCount", "TotalPrize", "AvgPrize"]].fillna(0)

    # 🔄 Toggle
    metric = st.radio("Select the metric to display:", ["Player Count", "Total Prize (USD)"])
    metric_column = "PlayerCount" if metric == "Player Count" else "TotalPrize"
    title_map = {
        "PlayerCount": "Number of Top 1000 Players per Country",
        "TotalPrize": "Total Prize Money by Country (USD)"
    }

    # Hover
    df_country['HoverText'] = [
        f"{row['CountryName']}<br>Players: {int(row['PlayerCount'])}"
        f"<br>Total earnings: ${row['TotalPrize']:,.0f}"
        f"<br>Average per player: ${row['AvgPrize']:,.0f}"
        for _, row in df_country.iterrows()
    ]

    # Color scale
    custom_colorscale = [
        [0.0, "#ffffff"],
        [0.00001, "#bfe0eb"],
        [0.1, "#6fb5d1"],
        [0.3, "#4a8cbf"],
        [0.5, "#7a5eb6"],
        [0.7, "#c55fa0"],
        [0.9, "#f27c5b"],
        [1.0, "#f4c542"]
    ]

    # Map
    fig_map = go.Figure(data=go.Choropleth(
        locations=df_country['CountryISO3'],
        z=df_country[metric_column],
        locationmode='ISO-3',
        colorscale=custom_colorscale,
        colorbar_title=title_map[metric_column],
        zmin=0,
        zmax=df_country[metric_column].max(),
        text=df_country['HoverText'],
        hoverinfo='text'
    ))

    fig_map.update_layout(
        title_text=title_map[metric_column],
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            bgcolor='#0b132b',
            center=dict(lat=20, lon=0),
            projection_scale=1.1,
        ),
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        height=700,
        font=dict(color='white'),
        title_x=0.25,
        title_font=dict(size=30, color='white'),

    )
    fig_map.data[0].colorbar.title = None
    fig_map.data[0].colorbar.tickfont = dict(color='white', size=13)

    # Continents
    df_continent = df_country.groupby("Continent").agg({
        "PlayerCount": "sum",
        "TotalPrize": "sum"
    }).reset_index()

    continent_order = ["Asia", "Europe", "North America", "South America", "Oceania", "Africa"]
    df_continent["Continent"] = pd.Categorical(df_continent["Continent"], categories=continent_order, ordered=True)
    df_continent = df_continent.sort_values("Continent")

    cols = st.columns(min(len(df_continent), 6))
    for i, (index, row) in enumerate(df_continent.iterrows()):
        value = row[metric_column]
        label = row["Continent"]
        formatted = f"{int(value):,}" if metric_column == "PlayerCount" else f"${value / 1_000_000:,.2f}M"
        
        cols[i].markdown(f"""
            <div style="text-align: center; padding: 5px 0;">
                <div style="font-size: 1.1rem; color: #222;">{label}</div>
                <div style="font-size: 1.8rem; font-weight: 600; color: black;">{formatted}</div>
            </div>
        """, unsafe_allow_html=True)


    # Top 10 bar chart
    top10 = df_country.nlargest(10, metric_column).sort_values(metric_column)
    top10['HoverText'] = [
        f"{row['CountryName']}<br>Players: {int(row['PlayerCount'])}"
        f"<br>Total earnings: ${row['TotalPrize']:,.0f}"
        f"<br>Average per player: ${row['AvgPrize']:,.0f}"
        for _, row in top10.iterrows()
    ]

    bar_text = (
        top10["PlayerCount"].astype(int).astype(str) + " "
        if metric_column == "PlayerCount"
        else top10["TotalPrize"].apply(lambda x: f"${x/1e6:.1f}M ")
    )

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=top10[metric_column],
        y=top10["CountryName"],
        orientation="h",
        text=bar_text,
        textposition='auto',
        textfont=dict(size=20),
        marker=dict(
            color=top10[metric_column],
            colorscale=custom_colorscale,
            cmin=0,
            cmax=df_country[metric_column].max(),
            line=dict(width=0)
        ),
        hovertemplate="%{customdata}<extra></extra>",
        customdata=top10["HoverText"]
    ))

    fig_bar.update_layout(
        title_text=f"Top 10 Countries by {metric}",
        title_font=dict(size=30, color='white'),
        title_x=0.3,
        paper_bgcolor="#0b132b",
        plot_bgcolor="#0b132b",
        font=dict(color="white", size=14),
        xaxis=dict(
            title=dict(text=metric, font=dict(size=22, color='white')),
            tickfont=dict(size=20, color='white')
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=20, color='white'),
            automargin=True
        ),
        margin=dict(l=200),
        height=700
    )
    fig_bar.update_coloraxes(colorbar_title=None, showscale=False)

    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # ➔ Final display
    col1, col2 = st.columns([1.7,1.3])
    with col1:
        st.plotly_chart(fig_map, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)


# ===============================================================
# 📊 Slide 4 – Careers Structure
# ===============================================================

def slide_4_careers_structure():
    st.markdown("<h2 style='color:#00b4d8;'>💥 Career Length and Tournaments Intensity of Top 1000 Esports Players</h2>", unsafe_allow_html=True)

    # ---------------------------------------------
    # Load and preprocess data
    # --------------------------------------------

    # Load tournament data
    career_df = pd.read_csv("scatter_df_export.csv")

    # Clean and compute key metrics
    career_df = career_df[
        (career_df["CareerLengthYears"] > 0.25) &
        (career_df["TotalTournaments"] > 0) &
        (~career_df["GameType"].isna())
    ].copy()

    career_df["TournamentsPerYear"] = career_df["TotalTournaments"] / career_df["CareerLengthYears"]

    # Compression function for soft Y-axis scaling
    def compress_y(val, threshold=300, factor=0.4):
        return val if val <= threshold else threshold + (val - threshold) * factor

    career_df["CompressedTournaments"] = career_df["TotalTournaments"].apply(compress_y)

    # ---------------------------------------------
    # UI – GameType filter
    # ---------------------------------------------

    gametypes = ["All"] + sorted(career_df["GameType"].unique())
    selected_type = st.selectbox("🎮 Filter by Game Type", gametypes)

    if selected_type == "All":
        filtered_df = career_df.copy()
    else:
        filtered_df = career_df[career_df["GameType"] == selected_type]

    # ---------------------------------------------
    # KPIs – Median duration and tournaments
    # ---------------------------------------------

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Median Career Length", f"{filtered_df['CareerLengthYears'].median():.1f} years")
    with col2:
        st.metric("Median Tournaments Played", f"{int(filtered_df['TotalTournaments'].median())}")

    # ---------------------------------------------
    # Scatter Plot with compressed Y axis
    # ---------------------------------------------

    tick_values_raw = [50, 100, 200, 300, 400, 500, 600, 700]
    tick_values_compressed = [compress_y(val) for val in tick_values_raw]
    tick_labels = ["50", "100", "200", "300", "400", "500", "600", "700"]

    fig = px.scatter(
        filtered_df,
        x="CareerLengthYears",
        y="CompressedTournaments",
        color="GameType",
        labels={
            "CareerLengthYears": "Career Length (years)",
            "CompressedTournaments": "Total Tournaments Played",  # utilisé pour l'axe Y uniquement
        },
        hover_data={
            "CurrentHandle": True,
            "GameName": True,
            "GameType": True,
            "CareerLengthYears": ':.1f',
            "TotalTournaments": True,
            "CompressedTournaments": False  # ⛔️ ne s'affiche pas au hover
        },
        opacity=1,
        title="Career Structure"
    )

    # Formatage de l’ordre d'affichage du hover
    fig.update_traces(
        hovertemplate=
            "Player: %{customdata[0]}<br>" +
            "Game: %{customdata[1]}<br>" +
            "Game Type: %{customdata[2]}<br>" +
            "Career Length: %{customdata[3]:.1f} years<br>" +
            "Total Tournaments Played: %{customdata[4]}<extra></extra>",
        customdata=filtered_df[[
            "CurrentHandle", "GameName", "GameType", "CareerLengthYears", "TotalTournaments"
        ]]
    )


    fig.update_layout(
        title_font=dict(size=30, color='white'),
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        font=dict(color='white', size=14),
        title_x=0.4,
        height=700,
        legend=dict(
        title="Game Type",
        title_font=dict(size=18, color='white'),
        font=dict(size=16, color='white')),
        xaxis=dict(
            title=dict(font=dict(size=22, color='white')),
            tickfont=dict(size=20, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=20, color='white'),
            tickvals=tick_values_compressed,
            ticktext=tick_labels,
            title=(dict(text="Total Tournaments Played",font=dict(size=22, color='white')))
        )
    )

    # ---------------------------------------------
    # Bar Plot 
    # ---------------------------------------------

    # Use full dataset for barplot (independent of selectbox)
    counts = career_df["GameType"].value_counts()
    valid_types = counts[counts >= 20].index
    barplot_df = career_df[career_df["GameType"].isin(valid_types)]

    # Recalculate medians
    summary_df = barplot_df.groupby("GameType").agg(
        MedianCareerLength=("CareerLengthYears", "median"),
        MedianTournamentsPerYear=("TournamentsPerYear", "median"),
        Count=("PlayerId", "count")
    ).reset_index().sort_values("MedianCareerLength", ascending=False)



    # Create grouped bar chart using Plotly
    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        x=summary_df["GameType"],
        y=summary_df["MedianCareerLength"],
        name="Career Length"
    ))

    fig_bar.add_trace(go.Bar(
        x=summary_df["GameType"],
        y=summary_df["MedianTournamentsPerYear"],
        name="Tournaments / Year"
    ))
    for i, row in summary_df.iterrows():
        fig_bar.add_annotation(
            x=row["GameType"],
            y=max(row["MedianCareerLength"], row["MedianTournamentsPerYear"]) + 0.5,
            text=f"{row['Count']}<br>players",
            showarrow=False,
            font=dict(color="white", size=17),
            yanchor="bottom"
        )
    # Apply saved visual style
    fig_bar.update_layout(
        title="Career Duration vs Intensity by Popular Game Type",
        title_font=dict(size=30, color='white'),
        title_x=0.12,
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        font=dict(color='white', size=14),
        height=700,
        legend=dict(
            title="Metric (medians)",
            title_font=dict(size=18, color='white'),
            font=dict(size=16, color='white')
        ),
        xaxis=dict(
            title=dict(text="Game Type", font=dict(size=22, color='white')),
            tickfont=dict(size=20, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title=dict(text="Years & Tournaments per Year", font=dict(size=22, color='white')),
            tickfont=dict(size=20, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        barmode='group'
    )

    # ➡️ Display side-by-side: map left, bar right
    col1, col2 = st.columns([1.7,1.3])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)


# ===============================================================
# 🧭 Slide Navigation
# ===============================================================
slide = st.sidebar.radio("Navigate Slides", [
    "Intro",
    "Top Games",
    "Players Gains Distribution",
    "Geographic distribution",
    "Careers Structure",
    "TBD",
    "TBD",
    "TBD",
    "Conclusion"
])

if slide == "Intro":
    st.image("test.png", use_container_width=True)

    st.markdown("""
    <p style='font-size:32px; line-height:1.7;'>
    🎮 <strong>Welcome</strong> to this interactive data exploration project on the economics of professional esports players.
    </p>

    <p style='font-size:32px; line-height:1.7;'>
    📊 This dashboard presents insights from a detailed analysis of the <strong>top 1000 earning players</strong> in esports history, 
    along with the broader prize pool landscape across competitive games.
    </p>

    <p style='font-size:32px; line-height:1.7;'>
    📁 All data comes from <em>EsportEarnings.com</em> public API, retrieved in <strong>June 2025</strong>. 
    It includes aggregated statistics on tournaments, players, and prize pools per game.
    </p>

    <p style='font-size:32px; line-height:1.7;'>
    👉 Use the sidebar to navigate slide by slide.
    </p>
    """, unsafe_allow_html=True)



elif slide == "Top Games":
    slide_1_prize_bar()

elif slide == "Players Gains Distribution":
    slide_2_prize_distribution()

elif slide == "Geographic distribution":
    slide_3_geographic_distribution()

elif slide == "Careers Structure":
    slide_4_careers_structure()

else:
    st.title(slide)
    st.markdown("🔧 This slide is under construction.")
