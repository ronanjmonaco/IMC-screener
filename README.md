#  Argentine ADR Portfolio Analysis

A comprehensive Streamlit application for analyzing Argentine ADR (American Depositary Receipt) portfolios with professional financial analysis tools.

##  Features

###  Portfolio Management
- **Auto-load 15 Argentine ADRs** with one click
- **Manual stock addition** for custom portfolios
- **Date range selection** for flexible analysis periods
- **Real-time data** from Yahoo Finance

###  Financial Analysis
- **Portfolio Summary** with key metrics
- **Individual Stock Performance** analysis
- **Risk Metrics** (VaR, Volatility, Sharpe Ratio)
- **Return Analysis** with visualizations

###  Advanced Analytics
- **CAPM Analysis** with Beta, Alpha, and R-squared calculations
- **Normality Tests** (Jarque-Bera, Shapiro-Wilk)
- **Distribution Charts** with normal distribution overlay
- **Efficient Frontier** using Monte Carlo simulation

##  Argentine ADRs Included

| Symbol | Company Name |
|--------|--------------|
| BBAR.BA | BBVA Banco Francés |
| BMA.BA | Banco Macro |
| CEPU.BA | Central Puerto |
| CRESY | Cresud |
| EDN.BA | Edenor |
| GGAL.BA | Grupo Financiero Galicia |
| IRS.BA | IRSA |
| LOMA.BA | Loma Negra |
| MELI | Mercado Libre Inc. |
| PAM.BA | Pampa Energía |
| SUPV.BA | Grupo Supervielle |
| TEO.BA | Telecom Argentina |
| TGS.BA | Transportadora de Gas del Sur |
| TS | Tenaris |
| YPF.BA | YPF |

##  Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd argentine-adr-portfolio
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

##  Usage

1. **Load Argentine ADRs**: Click " Load Argentine ADRs" in the sidebar
2. **Set Date Range**: Choose your analysis period
3. **View Analysis**: Navigate through the analysis tabs
4. **Add Custom Stocks**: Use the sidebar to add individual stocks

##  Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **yfinance**: Yahoo Finance data API
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **plotly**: Interactive charts
- **scipy**: Statistical functions

### Key Functions
- `fetch_stock_data()`: Retrieves stock data from Yahoo Finance
- `calculate_portfolio_metrics()`: Computes risk and return metrics
- `calculate_capm()`: Performs CAPM analysis
- `perform_normality_tests()`: Statistical normality testing
- `generate_efficient_frontier()`: Monte Carlo portfolio optimization

##  Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy automatically

### Local Deployment
```bash
streamlit run app.py --server.port 8501
```

##  Analysis Features

### Portfolio Summary
- Total number of stocks
- Annual return and volatility
- Sharpe ratio
- Maximum drawdown

### CAPM Analysis
- Beta calculation
- Alpha (Jensen's Alpha)
- R-squared (coefficient of determination)
- Correlation with market

### Normality Tests
- Jarque-Bera test for normality
- Shapiro-Wilk test
- Skewness and kurtosis analysis
- Visual normality assessment

### Efficient Frontier
- 10,000 Monte Carlo simulations
- Risk-return optimization
- Portfolio weight analysis
- Interactive frontier visualization

##  Benefits

- **Professional Analysis**: Institutional-grade financial metrics
- **User-Friendly**: Intuitive interface for all skill levels
- **Real-Time Data**: Live market data integration
- **Comprehensive**: Complete portfolio analysis suite
- **Visual**: Interactive charts and graphs
- **Scalable**: Easy to extend with additional features

##  Support

For questions or issues, please open an issue in the repository.

##  License

This project is licensed under the MIT License.
