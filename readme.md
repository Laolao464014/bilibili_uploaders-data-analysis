📊 Bilibili UP Collaboration Value Analysis Platform

&nbsp;	An interactive data analysis platform built with Streamlit, specifically designed for analyzing Bilibili UP creators' video performance and collaboration value.



🎯 Project Overview

&nbsp;	This project aims to analyze Bilibili UP creators' video data through data visualization, providing data support for brand collaborations, content planning, and business decisions. The platform offers multi-dimensional UP creator performance analysis and intelligent recommendation features.



🚀 Quick Start

&nbsp; Prerequisites

&nbsp;	1.Python 3.8 or higher

&nbsp;	2.pip (Python package manager)



Installation Steps

&nbsp;	1.Clone or Download Project

&nbsp;	bash

&nbsp;		# If using Git repository

&nbsp;		git clone <repository-url>

&nbsp;		cd bilibili-analysis-platform

&nbsp;	2.Install Dependencies

&nbsp;	bash

&nbsp;		pip install -r requirements.txt

&nbsp;	3.Prepare Data File

&nbsp; 		1.Name the original data file as bilibili\_data.xlsx and place it in the project root directory

&nbsp;		2.Or use the built-in sample data feature

&nbsp;	4.Launch Application

&nbsp;	bash

&nbsp;		# Option 1: Launch data preparation tool (recommended for first use)

&nbsp;		streamlit run data\_preparation.py



&nbsp;		# Option 2: Launch main application directly

&nbsp;		streamlit run main.py

&nbsp;	5.Access Application

&nbsp;		Open browser and visit: http://localhost:8501



📁 Project Structure

&nbsp;	text

&nbsp;	bilibili-analysis-platform/

&nbsp;	├── main.py                 # Main application entry

&nbsp;	├── data\_preparation.py     # Data preparation tool

&nbsp;	├── pages/                  # Multi-page application

&nbsp;	│   ├── 1\_📊\_Data\_Overview.py

&nbsp;	│   ├── 2\_📈\_Deep\_Analysis.py

&nbsp;	│   └── 3\_🤝\_UP\_Recommendation.py

&nbsp;	├── utils/                  # Utility modules

&nbsp;	│   ├── \_\_init\_\_.py

&nbsp;	│   ├── data\_loader.py     # Data loading and aggregation

&nbsp;	│   ├── charts.py          # Visualization charts

&nbsp;	│   └── config.py          # Configuration parameters

&nbsp;	├── data\_cleaner.py        # Data cleaning module

&nbsp;	├── requirements.txt       # Python dependencies

&nbsp;	├── README.md             # Project documentation

&nbsp;	├── bilibili\_data.xlsx    # Original data file (manual addition required)

&nbsp;	└── cleaned\_bilibili\_data.xlsx  # Cleaned data (automatically generated)



📊 Data Description

&nbsp;	Data Source

&nbsp;		1.Original Data: Bilibili UP creator video data (Excel format)

&nbsp;		2.Data Scope: Includes UP creator information, video performance, interaction data, etc.

&nbsp;		3.Update Frequency: Based on original data file updates

&nbsp;	Data Fields

&nbsp;		1.Basic Information: UP creator name, content domain, gender

&nbsp;		2.Video Data: Video title, play count, coin count, like count, danmu count

&nbsp;		3.Aggregated Metrics: Total plays, average plays, video count, comprehensive score

&nbsp;	Data Cleaning

&nbsp;		Automated processing includes:

&nbsp;			1.✅ Numerical format standardization (handling "10k" units)

&nbsp;			2.✅ Missing value imputation

&nbsp;			3.✅ Data type conversion

&nbsp;			4.✅ Duplicate data removal



🛠️ Technology Stack

&nbsp;	1.Frontend Framework: Streamlit

&nbsp;	2.Data Processing: Pandas, NumPy

&nbsp;	3.Visualization: Plotly, Altair

&nbsp;	4.Data Cleaning: Custom cleaning pipeline

&nbsp;	5.Caching Optimization: Streamlit caching



🔧 Main Features

&nbsp;	📊 Data Overview Page

&nbsp;		1.Key metrics dashboard (video count, UP creator count, average plays, etc.)

&nbsp;		2.Domain distribution analysis (pie charts, bar charts)

&nbsp;		3.Raw data preview

&nbsp;		4.Interactive data filtering



&nbsp;	📈 Deep Analysis Page

&nbsp;		1.UP creator comprehensive influence analysis (scatter plots)

&nbsp;		2.Video data statistics (TOP 5 videos, data distribution)

&nbsp;		3.Cross-domain performance comparison

&nbsp;		4.Multi-dimensional data exploration

🤝 UP Creator Recommendation Page

&nbsp;	1.Configurable recommendation weights (play count, average plays, video count, stability)

&nbsp;	2.Domain-based filtering recommendations

&nbsp;	3.UP creator detailed analysis

&nbsp;	4.Personalized collaboration suggestions



🎮 User Guide

&nbsp;	First-time Use

&nbsp;		1.Run data\_cleaner.py for data cleaning

&nbsp;		2.Check data quality and statistical information

&nbsp;		3.Launch main application to start analysis

&nbsp;	Regular Use

&nbsp;		1.Select analysis page from left sidebar

&nbsp;		2.Use filters to target specific data

&nbsp;		3.View interactive charts and analysis results

&nbsp;		4.Adjust weight parameters in UP recommendation page for personalized suggestions

&nbsp;	Data Filtering Options

&nbsp;		1.Content Domain: Multiple selection filter

&nbsp;		2.UP Creator Gender: Multiple selection filter

&nbsp;		3.Play Count Range: Slider selection

&nbsp;		4.Time Range: Date selection (if time data available)



⚙️ Configuration

&nbsp;	Weight Configuration

&nbsp;		Adjustable weights in UP recommendation page:

&nbsp;		Total Play Count Weight (Default: 0.3)

&nbsp;		Average Play Count Weight (Default: 0.2)

&nbsp;		Video Count Weight (Default: 0.2)

&nbsp;		Stability Weight (Default: 0.3)



&nbsp;	Caching Configuration

&nbsp;		Data loading: @st.cache\_data

&nbsp;		Cache duration: 3600 seconds (1 hour)

📈 Analysis Dimensions

&nbsp;	UP Creator Level Analysis

&nbsp;		1.Influence: Total play count, comprehensive score

&nbsp;		2.Stability: Average play count, play count volatility

&nbsp;		3.Productivity: Video count, update frequency

&nbsp;		4.Engagement: Like rate, coin rate, danmu density

&nbsp;	Video Level Analysis

&nbsp;		1.Popular Videos: TOP play count analysis

&nbsp;		2.Interaction Analysis: Relationships between likes, coins, danmu

&nbsp;		3.Domain Comparison: Performance differences across domains

&nbsp;	Business Value Assessment

&nbsp;		1.Spread Value: Play count and coverage range

&nbsp;		2.Engagement Value: User participation level

&nbsp;		3.Stability Value: Content quality consistency



