<div align="center">

# 📊 CSV vs. Avro vs. Parquet: Choosing the Right Big Data File Format
### *How Storage Architecture Saves 85% in Disk Space & Accelerates Analytical Queries by 10×*

**by Rositsa Racheva Kaloyanova**  
📅 *November 5, 2026*

<br/>

[![Launch 3D Presentation](https://img.shields.io/badge/%E2%96%B6_LAUNCH_3D_PRESENTATION-CLICK_HERE_TO_WATCH-00f5d4?style=for-the-badge&labelColor=162238)](https://raw.githack.com/rositsaracheva/ironhack-course/c2e90f4/Week%2005/Day%2004/Presentacion_3D_Isometric_v3.html)

*(Backup link: [Open via GitHub HTMLPreview](https://htmlpreview.github.io/?https://github.com/rositsaracheva/ironhack-course/blob/c2e90f4/Week%2005/Day%2004/Presentacion_3D_Isometric_v3.html))*

</div>

---

## ⌨️ Presentation Controls

- **`←` / `→` or `Space`**: Navigate between slides (`01` to `07`)
- **`M`**: Toggle 3D Isometric Map Overview (click any station node to zoom in)
- **`T`**: Start / Pause the 5-minute presentation timer
- **`F`**: Toggle Fullscreen mode

---

## 📋 Presentation Agenda

1. **`01 // OVERVIEW`**: 5-Minute Technical Defense & 3D Storage Volume Comparison (`100 GB` CSV vs. `48 GB` Avro vs. `15 GB` Parquet)
2. **`02 // CSV BOTTLENECK`**: Why Plain-Text CSV Fails at Scale (Full-Table Scan Bottleneck)
3. **`03 // ROW VS COLUMNAR`**: Physical Disk Architecture (`Row-Oriented` Write Optimization vs. `Column-Oriented` Read Optimization)
4. **`04 // APACHE AVRO`**: Self-Describing `.avsc` JSON Header, Binary Blocks & Schema Evolution
5. **`05 // APACHE PARQUET`**: Column Pruning, Predicate Pushdown (`min/max` statistics) & Snappy/Dictionary Compression
6. **`06 // SPEC MATRIX`**: Head-to-Head Engineering Decision Matrix
7. **`07 // DATA LAKE MAP`**: Production Medallion Architecture (Landing `CSV/JSON` ➔ Bronze `Avro` ➔ Gold `Parquet`)
