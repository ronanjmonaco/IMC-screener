#  Deployment Guide

## Local Development

1. **Install Python** (if not already installed)
   - Download from python.org or use Microsoft Store

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access the App**
   - Open browser and go to: http://localhost:8501

## Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial Argentine ADR Portfolio Analysis"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: app.py
   - Click "Deploy"

## Features Included

 **15 Argentine ADRs** pre-loaded
 **Automatic data loading** on page entry
 **CAPM Analysis** with Beta, Alpha, R-squared
 **Normality Tests** (Jarque-Bera, Shapiro-Wilk)
 **Distribution Charts** with normal overlay
 **Efficient Frontier** with Monte Carlo simulation
 **Interactive charts** with Plotly
 **Professional UI** with custom styling
 **Real-time data** from Yahoo Finance
 **Responsive design** for all devices

## Usage Instructions

1. **Load Portfolio**: Click " Load Argentine ADRs"
2. **Set Date Range**: Choose analysis period
3. **View Analysis**: Navigate through tabs
4. **Add Stocks**: Use sidebar for custom stocks

## Technical Stack

- **Frontend**: Streamlit
- **Data**: yfinance (Yahoo Finance API)
- **Charts**: Plotly
- **Statistics**: SciPy
- **Data Processing**: Pandas, NumPy

## Support

For issues or questions, check the README.md file.
