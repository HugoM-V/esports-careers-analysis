# 🎮 Esports Careers & Earnings Analysis

📊 **Exploring career patterns, income distribution, and global dynamics among the top 1000 esports players**  
🏆 *Final project for the Data Analytics bootcamp at SPICED Academy – Mar–Jun 2025*

---

## 🚀 Live App

👉 [**Open the interactive Streamlit dashboard**](https://esports-careers.streamlit.app)  
*(Optimized for 1920×1080 — on smaller screens, adjusting browser zoom may improve readability)*

---

## 🧠 Project Summary

This project takes a **deep-dive into professional esports careers**, focusing on the **top 1000 earning players** as listed on EsportsEarnings.com in **June 2025** (fixed dataset).

The goal:  
- Explore how esports careers are structured over time  
- Identify income distribution patterns and geographic trends  
- Build an **interactive dashboard** for exploring the data by game, region, or career profile  

While some aspects of the esports ecosystem are not covered in detail (e.g. team vs solo games, sponsorships, smaller tournaments), the dataset is rich enough to highlight **recurring patterns** and give a representative picture of the competitive scene.

---

## 📌 Main Insights

From the analysis, we surfaced a variety of metrics and visualizations, including:

- **Average career length** and variance by game genre  
- **Earnings per year** and how they evolve over a career  
- **"Earnings shapes"** — identifying profiles such as steady builders vs spike earners  
- **Geographic distribution** of top players and regional dominance by game  
- The disproportionate impact of certain titles (e.g. *Dota 2* represents 44% of total earnings, but only ~20% of top players)  

The focus is on **recognizing patterns**, not predicting future performance.

---

## 📂 Project Files

- `/app/` – Streamlit app source code  
- `/data_and_notebooks/` – Raw, cleaned, and enriched datasets (top players, games, regions), plus Jupyter notebooks for API data extraction, cleaning, exploration, and visualizations  
- `/sql/` – SQL queries  
- `requirements.txt` – Dependencies for running the dashboard locally  

---

## 🧰 Tools & Technologies

- **SQL** – Initial exploration, joins, and data validation  
- **Python (pandas, numpy)** – Data cleaning, enrichment, and transformations  
- **Plotly** – Interactive visualizations for the dashboard  
- **Streamlit** – Building and deploying the interactive app  
- **API integration** – Retrieving structured data from EsportsEarnings  
- **Manual enrichment** – Mapping Game IDs to genres and regions

---

## ⚙️ Challenges & Learnings

During the project, I faced several challenges:

- **Data integration** — Merging API data with manually enriched fields (genres, team/solo indicators)  
- **Visualization clarity** — Ensuring charts remained readable despite large data ranges and outliers  
- **App layout** — Adapting Streamlit for consistent rendering on large displays while keeping it usable on smaller screens  

These constraints influenced design choices and reinforced the importance of **balancing analytical depth with user accessibility**.

---

## 🔜 Potential Next Steps

The dataset offers many unexplored angles, such as:

- Comparing **team-based vs solo** game career dynamics  
- Studying **genre-specific volatility** in earnings  
- Expanding to include **tournament-level or match-level** statistics  
- Automating data refresh to track changes over time

The richness of the dataset makes it easy to get lost in exploration — prioritizing key questions was essential for delivering a clear and usable final product.

---

## 👤 Author

**Hugo Malta-Vacas**  
Aspiring Data Analyst | Former CX Manager | Esports enthusiast  
📍 Berlin | 🇨🇭 CH/DE  
🔗 [LinkedIn](https://www.linkedin.com/in/hmaltavacas/) | [GitHub](https://github.com/HugoM-V)
