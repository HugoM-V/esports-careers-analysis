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




st.markdown("""
<style>

/* Base layout and font */
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.55rem ;
    color: #222;
    background-color: #c3d7ea;
    padding-top: 0rem !important;
}
            
/* Reduce top margin globally */
section.main > div.block-container {
    padding-top: 0.5rem !important;
}
header, .block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Remove Streamlit default top white bar */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0rem !important;
}

/* Optional: widen layout globally */
.block-container {
    max-width: 95% !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
}

/* Remove excess spacing above titles */
h1, h2 {
    margin-top: 0rem !important;
    padding-top: 0rem !important;
}

            /* Réduction des marges entre les blocs */
.css-1kyxreq, .css-5rimss, .css-1r6slb0, .css-1dp5vir, .css-1v0mbdj, .stSelectbox, .stCheckbox {
    margin-top: 0rem !important;
    margin-bottom: 0rem !important;
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* Réduction des marges entre composants spécifiques */
h2, .stMarkdown, .stTextInput, .stSelectbox, .stCheckbox, .stMetric {
    margin-top: -0.4rem !important;
    margin-bottom: -0.6rem !important;
}


/* Taille des valeurs KPI */
div[data-testid="stMetricValue"] > div {
    font-size: 2rem !important;
    font-weight: 700 !important;
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
    st.markdown("<h2 style='color:#0077b6;'>Which games capture the most prize money in esports?</h2>", unsafe_allow_html=True)



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
    st.markdown("""""", unsafe_allow_html=True)
    col7, col8 = st.columns([0.05, 9.95])
    with col7:
        show_top15_kpis = st.checkbox("", value=False)
    with col8:
        st.markdown(" <span style='font-size:20px;'>🔍 Show KPIs for Top 15 only</span>", unsafe_allow_html=True)

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
        'Fighting': '#e377c2',      # couleur cohérente avec Plotly pastel
        'Strategy': '#bcbd22',      # jaune olive doux
        'Racing': '#17becf'         # bleu clair
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

    fig_bar.update_layout(
        xaxis_title="Total Prize Pool (in Millions USD)",
        yaxis_title="",
        yaxis=dict(
            autorange="reversed",
            color="white",
            tickfont=dict(color="white", size=24)
        ),
        xaxis=dict(
            color="white",
            tickfont=dict(color="white", size=24),
            showgrid=True,  # ✅ Active les lignes verticales
            gridcolor='rgba(255, 255, 255, 0.1)',  # ✅ Couleur blanche très transparente
            gridwidth=1
        ),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='white', size=18),
        height=700,
        title=dict(x=0.3, font=dict(color="white", size=26)),
        showlegend=True,
        legend=dict(
            title="Game Type",
            title_font=dict(size=1.4 * 16, color='white'),
            font=dict(size=1.3 * 16, color='white')
        )
)

    fig_bar.update_layout(
        title=dict(
            text=f"Top 15 Esports Games by Total Prize Pool",
            font=dict(size=32, color="white"),
            x=0.5,
            y=0.97,  # 👈 contrôle vertical
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(title_font=dict(color="white", size=26), tickfont=dict(color="white", size=24)),
        yaxis=dict(title_font=dict(size=22), tickfont=dict(color="white", size=20))
    )
    fig_bar.update_traces(
        textfont=dict(
            family="Arial Bold",  # ou "Helvetica Bold", etc.
            size=20
        )
    )
    # Add a dummy column to shift content to the right
    buffer, col1, col2, col3, col4 = st.columns([0.5, 1.3, 0.7, 1, 1])

    # Empty buffer column
    with buffer:
        st.empty() 

    # KPIs
    col1.metric("Total Prize", f"${kpi_df['TotalUSDPrize'].sum():,.0f}")
    col2.metric("Games", len(kpi_df))
    col3.metric("Players", f"{int(kpi_df['TotalPlayers'].sum()):,}")
    col4.metric("Tournaments", f"{int(kpi_df['TotalTournaments'].sum()):,}")


    # Slide layout (text left, chart right)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<br><br><br>", unsafe_allow_html=True)  # ⬅️ ajoute 2 sauts de ligne
        st.markdown("""
**Tournament rewards in esports are highly concentrated.**

**MOBAs**, **Battle Royale**, and **FPS** dominate the top spots, with **Dota 2**, **Fortnite**, and **CS:GO** leading in their genres.

The top 15 games account for **$1.4B out of 1.8B** in total prize money — that’s nearly **77%** of all distributed rewards across 200 titles.

Despite the variety of games played competitively, **only a handful concentrate the lion’s share of prize pool earnings.**


        """)

    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)




# ===============================================================
# 📊 Slide 2 – Prize distribution top 5k-1k
# ===============================================================

def slide_2_prize_distribution():
    """
    Slide 2 – Displays the prize distribution among the top 1000 or 5000 esports players.
    Includes linear/log scale toggle and dynamic chart updates.
    """
    st.markdown("<h2 style='color:#0077b6;'>How is prize money distributed among players?</h2>", unsafe_allow_html=True)

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
            f"<div style='color:black; font-size:1.4rem; margin-top:-1rem; padding-bottom:0.5rem;'>Total Earnings: <strong>${total_prize:,.0f}</strong></div>",
            unsafe_allow_html=True
        )
    else:
        total_prize = df_display["TotalUSDPrize"].sum()
        st.markdown(
            f"<div style='color:black; font-size:1.4rem; margin-top:-1rem; padding-bottom:0.5rem;'>Total Earnings: <strong>${total_prize:,.0f}</strong></div>",
            unsafe_allow_html=True
        )


    # Chart
    fig = px.area(
        df_display,
        x="Rank",
        y="TotalUSDPrize",
        template="plotly_dark",
    )

    fig.update_traces(
        line=dict(color=line_color, width=1),
        mode="lines+markers",  # 👈 ajoute les points visibles
        marker=dict(size=5),  # 👈 style des points
        hovertemplate="<b>Rank:</b> %{x}<br>" +
                "<b>Player:</b> %{customdata[0]}<br>" +
                "<b>Total Earnings:</b> $%{y:,.0f}<extra></extra>",
        customdata=df_display[["CurrentHandle"]]
    )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=30, color="white"),
            x=0.5,
            y=0.97,  # 👈 contrôle vertical
            xanchor='center',
            yanchor='top'
        ),
        xaxis_title="Player Rank",
        yaxis_title="Total Prize (USD)",
        xaxis=dict(
            tickfont=dict(size=26, color='white'),
            title_font=dict(size=24, color='white'),
        ),
        yaxis=dict(
            tickfont=dict(size=26, color='white'),
            title_font=dict(size=24, color='white')
        ),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='white', size=14),
        height=700,
    )

    # Ligne médiane
    median_val = df_display["TotalUSDPrize"].median()
    fig.add_hline(
        y=median_val,
        line_dash="dot",
        line_color="red",
        annotation=dict(
            text=f"Median ≈ ${median_val/1000:.0f}K",
            font=dict(color="red", size=33, weight="bold"),
            x=0.95,
            xanchor="right",
            yanchor="bottom",
            showarrow=False,
            bgcolor="rgba(0,0,0,0.4)",
        )
    )
    # Annotation
    def add_prize_annotation(fig, df, threshold, label=None, color="white", ax_offset=60, ay_offset=-120):
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
                arrowwidth=3,
                ax=ax_offset,
                ay=ay_offset,
                font=dict(color=color, size=30),
                bgcolor="rgba(0,0,0,0.6)",
                bordercolor=None,
                borderwidth=1
            )
    add_prize_annotation(fig, df_display, threshold=1_000_000, label="$1M", color="deepskyblue")
    add_prize_annotation(fig, df_display, threshold=500_000, label="$500K", color="deepskyblue", ax_offset=80)

    if selection == "Top 5000":
        add_prize_annotation(fig, df_display, threshold=100_000, label="$100K", color="deepskyblue", ax_offset=100)
        add_prize_annotation(fig, df_display, threshold=200_000, label="$200K", color="deepskyblue", ax_offset=100)




    # ➡️ Display side-by-side: map left, bar right
    col1, col2 = st.columns([2,1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # ⬅️ ajoute 2 sauts de ligne
        st.markdown(
            """
            **This chart shows the **total earnings** of the Top **1000**/5000 players, ranked from the highest to the lowest**.

            Each point represents a single player — the chart connects these points for visual clarity, but earnings are calculated individually.

            Almost **200 players** crossed the **$1M milestone**, and nearly **half of the Top 1000** earned **at least 500K**.

            Around **3,500 players** managed to reach **$100K or more** in total earnings.
            """)
        st.info("**For the rest of this analysis, we focus exclusively on the **Top 1000 players** to ensure more consistent and detailed insights.**")

# ===============================================================
# 📊 Slide 3 – Geographic distribution
# ===============================================================

def slide_3_geographic_distribution():
    st.markdown("<h2 style='color:#0077b6;'>Where do top players come from and which regions lead the scene?</h2>", unsafe_allow_html=True)

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
    metric = st.radio("Select the metric to display (from top 1000):", ["Player Count", "Total Prize (USD)"])
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
        margin=dict(l=30, r=50, t=60, b=50),  # ⬅️ réduit les marges autour de la figure

        legend=dict(font=dict(size=25)),
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        height=600,
        font=dict(color='white'),
        title=dict(
            text=f"Top 10 Countries by {metric}",
            font=dict(size=30, color="white"),
            x=0.5,
            y=0.97,  # 👈 contrôle vertical
            xanchor='center',
            yanchor='top'
        ),

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

    fig_map.update_traces(
    colorbar=dict(
        tickfont=dict(size=23, color="white"),
        )   
    )   

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
        textposition='inside',
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
        title=dict(
            text=f"Top 10 Countries by {metric}",
            font=dict(size=30, color="white"),
            x=0.5,
            y=0.97,  # 👈 contrôle vertical
            xanchor='center',
            yanchor='top'
        ),
        paper_bgcolor="#0b132b",
        plot_bgcolor="#0b132b",
        font=dict(color="white", size=14),
        xaxis=dict(
            title=dict(text=metric, font=dict(size=26, color='white')),
            tickfont=dict(size=24, color='white'),
            showgrid=True,  # ✅ Active les lignes verticales
            gridcolor='rgba(255, 255, 255, 0.2)',  # ✅ Couleur blanche très transparente
            gridwidth=3
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=23, color='white'),
            automargin=True
        ),
        margin=dict(l=220),
        height=600
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
    st.markdown("<h2 style='color:#0077b6;'>How long and intense are esports careers at the top level?</h2>", unsafe_allow_html=True)

    # ---------------------------------------------
    # Load and preprocess data
    # --------------------------------------------

    # Load tournament data
    career_df = pd.read_csv("scatter_df_export.csv")

    career_df["GameType"] = career_df["GameType"].astype(str).str.strip()

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
        filtered_df = career_df.copy().reset_index(drop=True)
    else:
        filtered_df = career_df[career_df["GameType"] == selected_type].reset_index(drop=True)



    # ---------------------------------------------
    # KPIs – Median duration and tournaments
    # ---------------------------------------------
    st.markdown("""""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        st.metric("Median Career Length", f"{filtered_df['CareerLengthYears'].median():.1f} years")
    with col2:
        st.metric("Median Total Tournaments Played", f"{filtered_df['TotalTournaments'].median():.1f}")
    with col3:
        st.metric("Median Tournaments / Year", f"{filtered_df['TournamentsPerYear'].median():.1f}")


    # ---------------------------------------------
    # Scatter Plot with compressed Y axis
    # ---------------------------------------------

    custom_colors = {
        'MOBA': '#5f78ff',
        'Battle Royale': '#ff6361',
        'FPS': '#43d9a5',
        'Sports': '#b266ff',
        'RTS': '#ffa600',
        'Card Game': '#00c2ff',
        'Auto Battler': '#ffc658',
        'Fighting': '#e377c2', 
    }

    tick_values_raw = [50, 100, 200, 300, 400, 500, 600, 700]
    tick_values_compressed = [compress_y(val) for val in tick_values_raw]
    tick_labels = ["50", "100", "200", "300", "400", "500", "600", "700"]

    filtered_df = filtered_df.reset_index(drop=True)

    if selected_type == "All":
        filtered_df = career_df.copy().reset_index(drop=True)
    else:
        filtered_df = career_df[career_df["GameType"] == selected_type].reset_index(drop=True)


# Tri défensif
    filtered_df = filtered_df.sort_values(by=["CareerLengthYears", "CompressedTournaments"]).reset_index(drop=True)

    fig = px.scatter(
        filtered_df,
        x="CareerLengthYears",
        y="CompressedTournaments",
        color="GameType",
        color_discrete_map=custom_colors,
        labels={
            "CareerLengthYears": "Career Length (years)",
            "CompressedTournaments": "Total Tournaments Played",
        },
        hover_data={
            "CurrentHandle": True,
            "GameName": True,
            "GameType": True,
            "CareerLengthYears": ':.1f',
            "TotalTournaments": True,
            "CompressedTournaments": False
        },
        opacity=1,
    )

    fig.update_traces(marker=dict(size=8, opacity=0.9))



    fig.update_layout(
        title_font=dict(size=30, color='white'),
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        font=dict(color='white', size=14),
        title=dict(
            text="Career Structure",
            font=dict(size=30, color="white"),
            x=0.5,
            y=0.97,  # 👈 contrôle vertical
            xanchor='center',
            yanchor='top'
    ),
        height=650,
        legend=dict(
        title="Game Type",
        title_font=dict(size=20, color='white'),
        font=dict(size=20, color='white')),
        xaxis=dict(
            title=dict(font=dict(size=22, color='white')),
            tickfont=dict(size=24, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=24, color='white'),
            tickvals=tick_values_compressed,
            ticktext=tick_labels,
            title=(dict(text="Total Tournaments Played",font=dict(size=22, color='white')))
        )
    )
    # Median
    median_career_length = filtered_df["CareerLengthYears"].median()

    # Line
    fig.add_vline(
        x=median_career_length,
        line=dict(color='rgba(255,0,0,0.5)', dash='dash', width=2),
        annotation_text=f"Median ≈ {median_career_length:.1f} yrs",
        annotation_position="top",
        annotation_font=dict(color='red', size=24),
        annotation_xshift=-100,
        annotation_y=0.95
    )


    # ---------------------------------------------
    # Bar Plot 
    # ---------------------------------------------

    # Filter for gametypes with at least 20 players
    counts = career_df["GameType"].value_counts()
    valid_types = counts[counts >= 10].index
    barplot_df = career_df[career_df["GameType"].isin(valid_types)]

    # Recalculate medians for the updated plot
    summary_df = barplot_df.groupby("GameType").agg(
        MedianTournamentsPerYear=("TournamentsPerYear", "median"),
        Count=("PlayerId", "count")
    ).reset_index().sort_values("MedianTournamentsPerYear", ascending=False)

    # Define custom colors consistent with previous visualizations
    custom_colors = {
        'MOBA': '#5f78ff',
        'Battle Royale': '#ff6361',
        'FPS': '#43d9a5',
        'Sports': '#b266ff',
        'RTS': '#ffa600',
        'Card Game': '#00c2ff',
        'Auto Battler': '#ffc658',
        'Fighting': '#e377c2', 
    }

    # Create single-bar chart for intensity (Tournaments/Year)
    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        x=summary_df["GameType"],
        y=summary_df["MedianTournamentsPerYear"],
        marker_color=[custom_colors.get(gt, '#888') for gt in summary_df["GameType"]],
        name="Median Tournaments / Year"
    ))




    # Apply layout styling
    fig_bar.update_layout(
    title=dict(
        text="Tournaments per Year (median)",
        font=dict(size=30, color="white"),
        x=0.5,
        y=0.97,  # 👈 contrôle vertical
        xanchor='center',
        yanchor='top'
    ),
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        font=dict(color='white', size=14),
        height=650,
        legend=dict(
            title="Metric",
            title_font=dict(size=8, color='white'),
            font=dict(size=20, color='white'),
            x=0.75,
            y=0.95,
            bgcolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(
            #title=dict(text="Game Type", font=dict(size=22, color='white')),
            title=None,
            tickfont=dict(size=22, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            #title=dict(text="Median Tournaments per Year", font=dict(size=22, color='white')),
            title=None,
            tickfont=dict(size=24, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # ➡️ Display side-by-side: text + map left, bar right
    col1, col2, col3 = st.columns([2, 1, 1])

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)  # ⬅️ ajoute 2 sauts de ligne
        st.markdown(
            """
            **This section explores how long esports careers last, and how active players are during their career.**

            Each point on the left chart represents one player, positioned by **career length** (x-axis) and **total tournaments played** (y-axis).
            
            The bar chart reveals what the scatter doesn't show clearly: **tournament frequency varies greatly** among genres. 
            """,
            unsafe_allow_html=True
        )
        st.info("**Important note**: Over 70% of these top players are still active, meaning **many careers are far from over**.")

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------
# Load Data (use st.cache_data to avoid recomputation)
# ---------------------------------------------
def load_data():
    df = pd.read_csv("scatter_df_export.csv")
    df["AvgEarningsPerYear"] = df["TotalUSDPrize"] / df["CareerLengthYears"]
    return df

scatter_df = load_data()

# ---------------------------------------------
# Slide 5 – Median Yearly Earnings by Game Type
# ---------------------------------------------
def slide_5__yearly_earnings():
    st.markdown("<h2 style='color:#0077b6;'>Do some game types offer more stable income than others?</h2>", unsafe_allow_html=True)
    st.markdown("""
                    """)
    # Custom color palette
    custom_colors = {
        'MOBA': '#5f78ff',
        'Battle Royale': '#ff6361',
        'FPS': '#43d9a5',
        'Sports': '#b266ff',
        'RTS': '#ffa600',
        'Card Game': '#00c2ff',
        'Auto Battler': '#ffc658',
        'Fighting': '#e377c2',
        'Strategy': '#bcbd22',
        'Racing': '#17becf'
    }


    # Filter: Only GameTypes with ≥ 10 players
    game_counts = scatter_df["GameType"].value_counts()
    valid_gametypes = game_counts[game_counts >= 10].index
    filtered_df = scatter_df[scatter_df["GameType"].isin(valid_gametypes)]

    # Compute median earnings per year by GameType
    median_by_game = (
        filtered_df.groupby("GameType")["AvgEarningsPerYear"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )

    # Plot the bar chart
    fig = px.bar(
        median_by_game,
        x="GameType",
        y="AvgEarningsPerYear",
        color="GameType",
        color_discrete_map=custom_colors,
        labels={
            "GameType": "Game Type",
            "AvgEarningsPerYear": "Median Earnings per Year (USD)"
        },
        title="Median Yearly Earnings"
    )

    # Add number of players as annotations at the bottom of each bar
    for i, row in median_by_game.iterrows():
        gametype = row["GameType"]
        count = filtered_df[filtered_df["GameType"] == gametype].shape[0]
        fig.add_annotation(
            x=gametype,
            y=2000,  # offset above the zero line
            text=f"{count} players",
            showarrow=False,
            font=dict(color="black", size=24),
            yanchor="bottom"
        )

    # Global median line (dashed)
    global_median = filtered_df["AvgEarningsPerYear"].median()
    fig.add_hline(
        y=global_median,
        line_dash="dash",
        line_color="red",
        annotation_text="Global Median",
        annotation_position="top right",
        annotation_font_color="red",
        annotation_font_size=27,
        annotation_xshift=-580,
        annotation_yshift=5  # 👈 Taille du texte ici

    )

    # Style settings
    fig.update_layout(
        title=dict(
            text="Yearly Earnings by Game Type",
            font=dict(size=34, color='white'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        font=dict(color='white', size=14),
        height=650,
        xaxis=dict(
            title=None,
            tickfont=dict(size=24, color='white'),
            showgrid=False
        ),
        yaxis=dict(
            title_font=dict(size=26, color='white'),
            tickfont=dict(size=24, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.3)'
        ),
        showlegend=False
    )



    # KPIs with custom formatting
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <p style='font-size:30px; margin-bottom:0;'>Global Median Yearly Earnings</p>
            <p style='font-size:45px; font-weight:bold; margin-top:0;'>${int(global_median):,}</p>
            """,
            unsafe_allow_html=True
        )

    with col2:
        top_game = median_by_game.iloc[0]["GameType"]
        top_value = median_by_game.iloc[0]["AvgEarningsPerYear"]
        st.markdown(
            f"""
            <p style='font-size:30px; margin-bottom:0;'>Top</p>
            <p style='font-size:45px; font-weight:bold; color:#8b0000; margin-top:0;'>{top_game} (${int(top_value):,})</p>
            """,
            unsafe_allow_html=True
        )

    with col3:
        bottom_game = median_by_game.iloc[-1]["GameType"]
        bottom_value = median_by_game.iloc[-1]["AvgEarningsPerYear"]
        st.markdown(
            f"""
            <p style='font-size:30px; margin-bottom:0;'>Bottom</p>
            <p style='font-size:45px; font-weight:bold; color:#1e3a8a; margin-top:0;'>{bottom_game} (${int(bottom_value):,})</p>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
    f"""


    """)
    # Display chart

    col1, col2 = st.columns([0.7, 2.3])

    with col1:



        st.markdown("<br><br>", unsafe_allow_html=True)  # ⬅️ ajoute 2 sauts de ligne

        st.markdown(
            """
            <p style='font-size:26px; font-weight:bold;'>This chart compares median yearly earnings across game types and among top 1000 players.</p>
            <p style='font-size:24px;'>MOBAs and Battle Royale games tend to offer higher rewards, whereas RTS and Fighting games generally lag behind — likely because they predate the esports surge of the last decade and are less represented in our sample.</p>
            <p style='font-size:24px; font-weight:bold;'>These differences highlight how much game design and timing can influence income potential.

</p>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<p style='font-size:24px; color:gray;'>Only game types with ≥10 players included.</p>", unsafe_allow_html=True)

# ===============================================================
# 📊 Slide 6 – Earnings Shape
# ===============================================================
def slide_6_earnings_shape():

    # TITLE + SUBTITLE
    st.markdown("""
        <h2 style='color:#0077b6; margin-bottom: 0px;'>Do top players build wealth steadily or through a few spikes?</h2>
        <p style='font-size:30px; color:#004b6e; margin-top: 2px; margin-bottom: 25px;'>
            What career shapes define the top 1000?
        </p>
    """, unsafe_allow_html=True)


    # ---- DATA IMPORT ----
    df = pd.read_csv("scatter_df_export.csv")  # <-- adapte le chemin si besoin

    # ---- FILTER: Only main GameTypes (≥50 players) ----
    valid_gametypes = df["GameType"].value_counts()
    valid_gametypes = valid_gametypes[valid_gametypes >= 10].index
    df = df[df["GameType"].isin(valid_gametypes)]

    # ---- CLASSIFICATION: Based on Top10PctEarningsRatio ----
    bins = [0, 0.30, 0.55, 0.8, 1.01]
    labels = ["Steady", "Balanced", "Spiky", "Explosive"]
    df["CareerProfile"] = pd.cut(df["Top10PctEarningsRatio"], bins=bins, labels=labels, include_lowest=True)

    # ---- COUNTS FOR PLOT ----
    df_counts = (
        df.groupby(["CareerProfile", "GameType"])
        .size()
        .reset_index(name="Count")
    )

    # ---- KPI METRICS ----
    total_players = len(df)
    profile_distribution = df["CareerProfile"].value_counts(normalize=True).reindex(labels)

    # ---- CUSTOM COLORS ----
    custom_colors = {
        'MOBA': '#5f78ff',
        'Battle Royale': '#ff6361',
        'FPS': '#43d9a5',
        'Sports': '#b266ff',
        'RTS': '#ffa600',
        'Card Game': '#00c2ff',
        'Auto Battler': '#ffc658',
        'Fighting': '#e377c2', 
    }


    kpi_cols = st.columns(4)

    descriptions = {
        "Steady": "Earnings spread consistently across tournaments",
        "Balanced": "A few peaks, but overall consistent",
        "Spiky": "Heavily reliant on major wins",
        "Explosive": "Almost everything came from a handful of events"
    }

    colors = {
        "Steady": "#00b4d8",
        "Balanced": "#0091c2",
        "Spiky": "#f95d6a",
        "Explosive": "#d62728"
    }

    for i, profile in enumerate(["Steady", "Balanced", "Spiky", "Explosive"]):
        pct = profile_distribution[profile]
        with kpi_cols[i]:
            st.markdown(
                f"""
                <div style='text-align: center; line-height: 1.3;'>
                    <p style='font-size:32px; font-weight:bold; color:black; margin-bottom:6px;'>{profile}</p>
                    <p style='font-size:44px; font-weight: bold; color:{colors[profile]}; margin: 0;'>{pct*100:.1f}%</p>
                    <p style='font-size:24px; color:black; margin-top:6px;'>{descriptions[profile]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---- LAYOUT ----
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)  # ⬅️ ajoute 2 sauts de ligne

        st.markdown(
            """
            <p style='font-size:1rem;'>
            <b>To better understand how players built their earnings, we grouped them into four career profiles — based on how concentrated their income is around their biggest wins.
            </b></p>
            """,
            unsafe_allow_html=True
        )


        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(
            """
            <p style='font-size:24px;'><b>Classification logic:</b><br>
            Players are classified based on the <b>share of their total earnings</b> that came from their <b>top 10% most lucrative tournaments</b>.
            </p>
            <p style='font-size:24px;'>
            - <b>Steady</b>: ≤ 30% from top 10% tournaments<br>
            - <b>Balanced</b>: 30–55%<br>
            - <b>Spiky</b>: 55–80%<br>
            - <b>Explosive</b>: > 80%
            </p>
            """,
            unsafe_allow_html=True
        )

    with col2:
        fig = px.bar(
            df_counts,
            x="CareerProfile",
            y="Count",
            color="GameType",
            color_discrete_map=custom_colors,
            barmode="stack",
            category_orders={"CareerProfile": labels},
            labels={
                "CareerProfile": "Career Profile",
                "Count": "Number of Players",
                "GameType": "Game Type"
            },
            title=""
        )

        fig.update_layout(
            title=dict(
                text="Number of Players per Career Profile",
                font=dict(size=28, color='white'),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor='#0b132b',
            plot_bgcolor='#0b132b',
            font=dict(color='white', size=20),
            height=650,
            margin=dict(t=100, l=10, r=140, b=10),  # ➕ marge droite plus large pour la légende
            xaxis=dict(
                title="Career Profile",
                title_font=dict(size=26, color='white'),
                tickfont=dict(size=24, color='white')
            ),
            yaxis=dict(
                title="Number of Players",
                title_font=dict(size=26, color='white'),
                tickfont=dict(size=24, color='white')
            ),
            legend=dict(
                orientation="v",  # ➡️ vertical
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # ➡️ décalé juste à l'intérieur
                bgcolor='rgba(0,0,0,0)',
                font=dict(size=22, color="white"),
                title_font=dict(size=24, color="white")
            )
        )


        st.plotly_chart(fig, use_container_width=True)


# ===============================================================
# 📊 Slide 7 – Career Archetypes
# ===============================================================

import pandas as pd
import plotly.express as px

# Chargement des données tournois
df = pd.read_csv("tournaments_corrected_with_handles_and_games.csv")
df["EndDate"] = pd.to_datetime(df["EndDate"])
df.sort_values(by=["CurrentHandle", "EndDate"], inplace=True)
df["CumulativePrize"] = df.groupby("CurrentHandle")["USDPrizePerPlayer"].cumsum()

# Chargement du fichier avec GameType
game_type_df = pd.read_csv("scatter_df_export.csv")[["CurrentHandle", "GameId", "GameType"]].drop_duplicates()

# Merge GameType sur le dataframe principal
df = df.merge(game_type_df, on=["CurrentHandle", "GameId"], how="left")

# Palette personnalisée par GameType
game_type_colors = {
    "MOBA": "#ff6b6b",
    "RTS": "#f7b801",
    "FPS": "#6a4c93",
    "Battle Royale": "#1982c4",
    "Fighting": "#8ac926",
    "Card/Board": "#ff924c",
    "Sports": "#1f7a8c",
    "Racing": "#c32bad",
    "Other": "#cccccc"
}

# Fonction timeline par joueur, avec couleurs par GameType
def create_timeline_chart(player_list, title):
    filtered = df[df["CurrentHandle"].isin(player_list)].copy()
    filtered.sort_values(by=["CurrentHandle", "EndDate"], inplace=True)
    filtered["CumulativePrize"] = filtered.groupby("CurrentHandle")["USDPrizePerPlayer"].cumsum()

    # Récupération des couleurs via GameType (si connu)
    color_map = {}
    for player in player_list:
        game_type = filtered[filtered["CurrentHandle"] == player]["GameType"].dropna().unique()
        color = game_type_colors.get(game_type[0], "#ffffff") if len(game_type) > 0 else "#ffffff"
        color_map[player] = color

    fig = px.line(
        filtered,
        x="EndDate",
        y="CumulativePrize",
        color="CurrentHandle",
        line_group="CurrentHandle",
        labels={"CumulativePrize": "Cumulative Earnings (USD)", "EndDate": "Date"},
        title=title,
        color_discrete_map=color_map
    )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=28, color='white'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='#0b132b',
        plot_bgcolor='#0b132b',
        font=dict(color='white', size=20),
        height=400,
        margin=dict(t=100, l=10, r=140, b=10),
        xaxis=dict(
            title=None,
            title_font=dict(size=22, color='white'),
            tickfont=dict(size=24, color='white')
        ),
        yaxis=dict(
            title="Cumulative Earnings (USD)",
            title_font=dict(size=24, color='white'),
            tickfont=dict(size=24, color='white')
        ),
        legend=dict(
            title="Player",
            orientation="v",
            yanchor="top",
            y=0.95,
            xanchor="left",
            x=1.02,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=24, color="white"),
            title_font=dict(size=20, color="white")
        )
    )
    return fig

#Colors

import matplotlib.colors as mcolors

def hex_to_rgba(hex_color, alpha=0.8):
    """Convert a hex color to an rgba string accepted by Plotly."""
    rgb = mcolors.to_rgb(hex_color)
    return f"rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, {alpha})"






def slide_7__career_archetypes():
    st.markdown("<h2 style='color:#0077b6;'>What pro esports careers really look like?</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style='font-size:30px; color:#004b6e; margin-top: 2px; margin-bottom: 25px;'>
            From different games and players, shared career patterns emerge.
        </p>
    """, unsafe_allow_html=True)

    # Ligne 1
    col1, col2, col3 = st.columns([1,2,2])

    with col1:
        st.markdown("<br>", unsafe_allow_html=True)  # ⬅️ ajoute 2 sauts de ligne

        st.markdown(
        """
        <p style='font-size:24px; line-height:1.6;'>
        These individual trajectories illustrate how different career shapes translate into real earnings paths.  </p>
         <p style='font-size:24px; line-height:1.6;'>From early big wins to slow, long-term accumulation, <b>each archetype tells a different story</b> — shaped by game type, timing, and opportunity.
        </p>
        """,
        unsafe_allow_html=True
    )

    with col2:
        players_outliers = ["Bugha", "Collapse"]
        fig_outliers = create_timeline_chart(players_outliers, "Heavy Hitters")
        add_game_annotations(fig_outliers, df, players_outliers)
        st.plotly_chart(fig_outliers, use_container_width=True)
        

    with col3:
        players_sprinter = ["Atif Butt","sitetampo"]
        fig_sprinter = create_timeline_chart(players_sprinter, "Fast Risers")
        add_game_annotations(fig_sprinter, df, players_sprinter)
        st.plotly_chart(fig_sprinter, use_container_width=True)

    # Ligne 2
    players_marathon = ["Lyn", "ShoWTimE"]
    fig_marathon = create_timeline_chart(players_marathon, "Steady Climbers")
    add_game_annotations(fig_marathon, df, players_marathon)
    st.plotly_chart(fig_marathon, use_container_width=True)


def add_game_annotations(fig, df, player_list):
    for i, player in enumerate(player_list):
        player_df = df[df["CurrentHandle"] == player]
        if player_df.empty:
            continue

        point_index = int(len(player_df) * 0.5)
        point_index = min(point_index, len(player_df) - 1)
        row = player_df.iloc[point_index]

        game_name = row.get("GameName", "Unknown Game")
        #handle = row.get("CurrentHandle")
        game_type = str(row["GameType"]).strip() if pd.notna(row["GameType"]) else "Unknown Type"

        # Couleur principale et fond
        color = game_type_colors.get(game_type, "#ffffff")
        rgba_bg = hex_to_rgba(color, alpha=1)

        text = f"<b>{game_name}</b><br><i>{game_type}</i>"

        fig.add_annotation(
            x=row["EndDate"],
            y=row["CumulativePrize"],
            text=text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            ax=-100,
            ay=-70 + i * 30,
            font=dict(color="black", size=20),
            bgcolor=rgba_bg,
            bordercolor=color,
            borderwidth=2
        )

# ===============================================================
# Conclusion
# ===============================================================

def slide_8__conclusion():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#0077b6;'>So... what does it take to build a standout career in esports?</h2>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    # ➤ Deux colonnes pour Key takeaways + image
    col1, col2 = st.columns([2.8, 2.2])  # Tu peux ajuster les proportions ici si tu veux

    with col1:
        st.markdown(
            """
            <p style='font-size:32px; font-weight:bold;'>Key takeaways:</p>

            <ul style='font-size:28px; line-height:1.8;'>
                <li><strong>Game choice matters.</strong> Different genres lead to different career dynamics.</li>
                <li><strong>There is no single path.</strong> Some players succeed fast, others build over time.</li>
                <li><strong>Success is spiky.</strong> Most players rely on a few key tournaments.</li>
                <li><strong>Prize money ≠ full picture.</strong> Sponsorships, teams and brand also matter — but the data reveals structural patterns that shape those journeys.</li>
            </ul>
            """, unsafe_allow_html=True
        )

    with col2:
        st.image("intro5.jpg", use_container_width=True, caption="Team Vitality – CS2 Major Champions – Austin (June 22, 2025)")

    # ➤ Retour en pleine largeur

    st.markdown(
        """
        <p style='font-size:32px; font-weight:bold;'>Final thoughts:</p>
        <p style='font-size:28px;'>
        Building a career in esports isn’t just about <strong>winning</strong>. It’s about <strong>dedication</strong>, <strong>game choice</strong>, and <strong>being ready to deliver — when it counts most.</strong>
        </p>

        <p style='font-size:28px; margin-top:20px; font-style:italic; color:black;'>
        We often only see the public wins — but data reveals the silent grind, the volatility, and the deeper patterns that shape a career.
        </p>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <hr style='margin-top:40px; margin-bottom:10px;'>
        <p style='font-size:18px; color:black;'>Thanks for reading — and if this sparked ideas or questions, feel free to reach out!</p>
        <p style='font-size:18px; color:black;'>Project by <strong>Hugo Malta-Vacas</strong> — Final Bootcamp Presentation, June 2025<br>
        <a href='https://www.linkedin.com/in/hugomaltavacas/' target='_blank' style='color:#00b4d8;'>Connect on LinkedIn</a></p>
        """, unsafe_allow_html=True
    )

# ===============================================================
# 🧭 Slide Navigation — Horizontal Tabs
# ===============================================================
tabs = st.tabs([
    "Intro",
    "Context",  # temporaire
    "Top Games",
    "Gains Distribution",
    "Geographic distribution",
    "Careers Structure",
    "Yearly Earnings",
    "Earnings Shape",
    "Players Archetypes",
    "Conclusion"
])


with tabs[0]:
    st.markdown("<h1 style='font-size:2.5rem; text-align:center; margin-top:1rem; color:#0077b6;'>Behind the Screens:<br>What Top Esports Careers Really Look Like?</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:10px; margin-bottom:2rem;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 3.5])  # texte à gauche, image à droite

    with col1:
        st.markdown("""
        <div style='margin-top: 0.1rem; font-size:1.1rem; line-height:1.7;'>
            <p style='font-size:1.25rem;'>
                <strong>Esports is booming — but what does it take to build a standout career?</strong>
            <p>
            This project dives into the careers of the <strong>Top 1000 highest-earning players</strong>, exploring how <strong>success takes shape</strong> across <strong>games, genres, and years of competition</strong>.
            </p>


        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin-top:1rem; margin-bottom:0rem;'>", unsafe_allow_html=True)


        st.markdown("""
        <div style='margin-top: 2rem; padding: 1rem; background-color: #1c2c45; border-radius: 0.5rem; font-size:0.8rem; color:#ccc; line-height:1.6;'>
        • <strong>Data source:</strong> public API from <em>EsportEarnings.com</em> (June 2025) — covering the Top 1000 highest-earning players at this time.<br>
        • <strong>Focus on tournament earnings only </strong>— salaries, sponsorships, or streaming revenue are not included, as they are rarely public or consistent enough.<br>
        • Additional players and games metadata provides essential context for analyzing broader career patterns.
        </div>
        """, unsafe_allow_html=True)


    # Créer un conteneur vide pour afficher les images
    with col2:
        st.image("intro1.jpg", use_container_width=True, caption="PUBG Global Invitational – Berlin (2018)")









with tabs[1]:  # Game Types (TEMP)
    st.image("game_examples.png", use_container_width=True)

with tabs[2]:  # Top Games
    slide_1_prize_bar()

with tabs[3]:  # Players Gains Distribution
    slide_2_prize_distribution()

with tabs[4]:  # Geographic distribution
    slide_3_geographic_distribution()

with tabs[5]:  # Careers Structure
    slide_4_careers_structure()

with tabs[6]:  # Yearly Earnings
    slide_5__yearly_earnings()

with tabs[7]:  # Earnings Shape
    slide_6_earnings_shape()

with tabs[8]:  # Players
    slide_7__career_archetypes()

with tabs[9]:  # Conclusion
    slide_8__conclusion()

    

