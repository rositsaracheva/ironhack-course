# 📊 BrewBeats — Executive Dashboards (Live Python App & Tableau)

**Author:** Rositsa Kaloyanova  

[![🚀 Open Live BrewBeats Dashboard](https://img.shields.io/badge/🚀%20OPEN%20LIVE%20DASHBOARD-BrewBeats%20Real--Time%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://week07day03-04-05-miniproject2sectione-casestudystep2-ccet58.streamlit.app)

---

## ⚡ 1. Live Interactive Python Dashboard (Streamlit + Plotly + DuckDB)

👉 **Live Public Link (Click to Open):**  
**[https://week07day03-04-05-miniproject2sectione-casestudystep2-ccet58.streamlit.app](https://week07day03-04-05-miniproject2sectione-casestudystep2-ccet58.streamlit.app)**

- **Source Code:** [Live Python Dashboard/brewbeats_dashboard.py](Live%20Python%20Dashboard/brewbeats_dashboard.py)
- **Features Included:**
  - Connected directly to our Section D `dbt` DuckDB warehouse (`main.stg_coffee_sales`) with cloud CSV fallback
  - **Real-Time POS Simulator** (`➕ 1 Live Sale` button in the sidebar to watch KPIs and charts update live)
  - All **10 Section E Dashboard Requirements** (Executive KPIs 1–4, Revenue by Coffee Type, Revenue by Month, Monthly Sales Trend with Linear Growth Line, Sales by Weekday, Sales by Hour dual-peak curve, Cash vs. Card donut chart)
  - **Bonus Weekday × Hour Staffing & Playlist Heatmap** with an interactive **`💡 How to Read This Chart`** popover button
  - **BrewBeats In-Store Spotify Playlists Tab** (`Spotify_data.csv`) with live danceability/energy/valence sliders

---

## 📈 2. Tableau Packaged Workbook (`.twbx`)

- **File:** [Mini Project 2 - Section E.twbx](Mini%20Project%202%20-%20Section%20E.twbx)
- Contains all 10 required worksheets and executive dashboards built from [cleaned_coffee_sales.csv](cleaned_coffee_sales.csv).
