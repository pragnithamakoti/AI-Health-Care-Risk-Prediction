# Power BI Dashboard Blueprint: Nexus AI Healthcare System

This document outlines the architecture, layout, DAX formulas, and UI/UX guidelines for creating the enterprise-grade **Nexus AI Healthcare System** Power BI dashboard.

## 🎨 1. Theme & UI/UX Guidelines
To match the startup-grade, modern healthcare platform aesthetic:
- **Background Color:** Deep Dark Gray/Black (`#0E1117` or `#0B0E14`)
- **Card Backgrounds:** Glassmorphism style (`#1A202C` with 80% transparency/blur)
- **Primary Highlights:** Neon Cyan (`#00F3FF`), Neon Blue (`#0057FF`)
- **Risk Colors:** Healthy (Emerald `#10B981`), Medium Risk (Amber `#F59E0B`), High Risk (Crimson `#EF4444`)
- **Typography:** Segoe UI or DIN (San-serif, modern, clean)
- **Visuals:** Use glowing effects, rounded borders (radius: 10px), and subtle shadows on cards.

## 📄 2. Page Structure

### Page 1: Executive Overview
- **Objective:** High-level summary for hospital administrators.
- **Visuals:** KPI Cards at the top. Area charts showing Month-over-Month growth.
- **Features:** Dynamic titles based on selected date ranges.

### Page 2: Disease Analytics
- **Objective:** Deep dive into specific diseases.
- **Visuals:** Heatmaps (Correlation), Line charts (Moving average of trends), Donut charts (Prevalence).
- **Features:** Drill-through to Patient Demographics for specific disease segments.

### Page 3: Lifestyle & Risk Analysis
- **Objective:** Analyze how lifestyle impacts health scores.
- **Visuals:** Scatter plots (BMI vs Risk), Bar charts (Smoking/Stress to disease correlation).

### Page 4: Patient Demographics
- **Objective:** Understand the patient base.
- **Visuals:** Tree maps (Age Groups), Sankey charts (Flow from lifestyle to disease).
- **Features:** Advanced slicers (Age bin, Gender, Region).

### Page 5: AI Prediction Insights (Tooltip & Drill-through)
- **Objective:** Highlight AI model outputs.
- **Visuals:** Gauge charts (Confidence Score), Tornado charts (Feature Importance).

## 🧮 3. Advanced DAX Measures

### Core KPIs
```dax
Total Patients = COUNTROWS(Patients)

High Risk Patients = CALCULATE(COUNTROWS(Patients), Patients[RiskLevel] = "High")

Critical Risk Percentage = DIVIDE([High Risk Patients], [Total Patients], 0)

Average BMI = AVERAGE(Patients[BMI])

Recovery Rate = CALCULATE(COUNTROWS(Patients), Patients[Status] = "Recovered") / [Total Patients]

Mortality Risk Score = AVERAGE(Predictions[MortalityProb]) * 100

Smoking Percentage = CALCULATE(COUNTROWS(Patients), Patients[Smoking_Habit] = "Regular") / [Total Patients]
```

### Advanced Analytics
```dax
MoM Patient Growth = 
VAR CurrentMonth = [Total Patients]
VAR PrevMonth = CALCULATE([Total Patients], PREVIOUSMONTH(Calendar[Date]))
RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth, 0)

Rolling 30-Day Risk Average = 
CALCULATE(
    AVERAGE(Predictions[Overall_Risk_Score]),
    DATESINPERIOD(Calendar[Date], MAX(Calendar[Date]), -30, DAY)
)

Readmission Risk Index = 
AVERAGEX(
    FILTER(Patients, Patients[PriorAdmissions] > 1),
    Predictions[ReadmissionProb]
)

Hospital Resource Utilization = 
DIVIDE(
    SUM(Admissions[DaysInHospital]),
    [Total Patients]
)
```

### Predictive Analytics
```dax
AI Confidence Score = AVERAGE(Predictions[Model_Confidence])

Future Risk Forecast = 
CALCULATE(
    [Rolling 30-Day Risk Average] * 1.05, -- 5% projected increase based on trend
    DATEADD(Calendar[Date], 1, MONTH)
)
```

## 🛠️ 4. Advanced Power BI Features to Implement
1. **Bookmarks & Navigation:** Use bookmarks to toggle between "Clinical View" and "Operational View" without changing pages.
2. **Drill-through:** Right-click a high-risk demographic segment on Page 4 to drill through to Page 5 (AI Insights) for that specific cohort.
3. **Tooltip Pages:** Create a custom tooltip page. When hovering over a patient point on a scatter plot, show their full medical history and AI prediction scores.
4. **Conditional Formatting:** Apply dynamic colors to the "Risk Escalation Detection" tables. Red for >80% risk, Yellow for 50-80%, Green for <50%.

*Built for portfolio, enterprise SaaS demonstration, and top-tier analytics presentations.*
