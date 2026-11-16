# Week 07 - Day 01: Fashion Styles Data Visualization & Dashboards (Tableau)

This folder contains the complete solution for the **`styles.csv`** visualization exercise built in **Tableau Public**, covering all 12 charts across **Basic**, **Intermediate**, and **Advanced Analysis**.

---

## 🌐 Live Interactive Dashboards (Tableau Public)

You can view and interact with the dashboards directly in the browser without downloading any software:

| Dashboard | Charts Included | Live Link |
| :--- | :--- | :--- |
| **Dashboard 1–4 (Basic Analysis)** | 1. Products by Gender<br>2. MasterCategory Products<br>3. Products by Season<br>4. Products by Year | [🔗 Open Dashboard 1–4 Online](https://public.tableau.com/views/Dashboards9-12/Dashboard1-4) |
| **Dashboard 5–8 (Intermediate Analysis)** | 5. Stacked Bar Chart (`masterCategory` vs `subCategory`)<br>6. BaseColour by Gender (with Gender Slicer/Filter)<br>7. Top 5 Article Types<br>8. Season vs Usage Matrix | [🔗 Open Dashboard 5–8 Online](https://public.tableau.com/views/Dashboards9-12/Dashboard5-8) |
| **Dashboard 9–12 (Advanced Analysis)** | 9. BaseColour Trend (`Men` vs `Women` over `Year`)<br>10. Category Hierarchy (`masterCategory` > `subCategory` > `articleType`)<br>11. Popular vs Less Popular (`> 500` Calculated Field)<br>12. Year vs Count Scatter (by `Season`) | [🔗 Open Dashboard 9–12 Online](https://public.tableau.com/views/Dashboards9-12/Dashboard9-12) |

---

## 📊 Summary of Completed Visualizations

### 1. Basic Data Visualization
1. **Products by Gender:** Horizontal bar chart showing total product count per `gender`. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/ProductsbyGender))
2. **MasterCategory Products:** Vertical column chart displaying the count of products by `masterCategory`. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/MasterCategoryProducts))
3. **Products by Season:** Pie chart showing the proportion of products across different `season` values. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/ProductsbySeason))
4. **Products by Year:** Line chart representing the number of products added each `year`. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/ProductsbyYear))

### 2. Intermediate Analysis
5. **MasterCategory vs SubCategory:** Stacked bar chart showing `masterCategory` broken down by `subCategory` with counts. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/5_Stackedbarchart))
6. **BaseColour by Gender:** Distribution of `baseColour` with an interactive `gender` filter/slicer. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/6_BaseColourbyGender))
7. **Top 5 Article Types:** Column chart filtered to the top 5 most common `articleType` categories (`Tshirts`, `Shirts`, `Casual Shoes`, `Watches`, `Sports Shoes`). ([View Sheet](https://public.tableau.com/views/Dashboards9-12/7_Top5ArticleTypes))
8. **Season vs Usage Matrix:** Matrix/crosstab visual displaying `season` vs `usage` product counts with row and column totals. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/8_SeasonvsUsageMatrix))

### 3. Advanced Analysis
9. **BaseColour Popularity Trend:** Line trend analysis showing how `baseColour` popularity changes over `year` for **Men** and **Women** separately. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/9_BaseColourTrend))
10. **Category Hierarchy:** Drill-down hierarchy (`Master Category` $\rightarrow$ `Sub Category` $\rightarrow$ `Article Type`) showing total products. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/10_CategoryHierarchy))
11. **Popular vs Less Popular (Calculated Field):** Uses the FIXED LOD formula:
    ```text
    IF { FIXED [Article Type] : COUNT([Id]) } > 500 THEN "Popular" ELSE "Less Popular" END
    ```
    to classify and visualize products appearing more than 500 times vs. 500 or fewer times. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/11_PopularvsLessPopular))
12. **Year vs Product Count Scatter Chart:** Scatter plot of `year` vs product count with `season` as the color legend. ([View Sheet](https://public.tableau.com/views/Dashboards9-12/12_YearvsCountScatter))

---

## 📁 Files in This Folder

- **`Styles_Dashboards_1-12.twbx`** — Complete packaged Tableau workbook containing all 12 sheets, all 3 dashboards, and the data extract (open with Tableau Desktop or Tableau Public).
- **`styles.csv`** — Source dataset (44,446 product records).
- **`POWER BI(styles.csv).docx`** — Original exercise instructions.
