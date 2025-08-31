import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# Page configuration
st.set_page_config(
    page_title=" Argentine ADR Portfolio Analysis",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

# Argentine ADR symbols
ARGENTINE_ADRS = {
    "BBAR.BA": "BBVA Banco Francés",
    "BMA.BA": "Banco Macro",
    "CEPU.BA": "Central Puerto",
    "CRESY": "Cresud",
    "EDN.BA": "Edenor",
    "GGAL.BA": "Grupo Financiero Galicia",
    "IRS.BA": "IRSA",
    "LOMA.BA": "Loma Negra",
    "MELI": "Mercado Libre Inc.",
    "PAM.BA": "Pampa Energía",
    "SUPV.BA": "Grupo Supervielle",
    "TEO.BA": "Telecom Argentina",
    "TGS.BA": "Transportadora de Gas del Sur",
    "TS": "Tenaris",
    "YPF.BA": "YPF"
}

@st.cache_data
def fetch_stock_data(symbol, start_date, end_date):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)
        if not data.empty:
            return data
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def calculate_returns(prices):
    """Calculate daily returns"""
    return prices.pct_change().dropna()

def calculate_portfolio_metrics(returns):
    """Calculate portfolio metrics"""
    if returns.empty:
        return None
    
    metrics = {
        'mean_return': returns.mean() * 252,  # Annualized
        'volatility': returns.std() * np.sqrt(252),  # Annualized
        'sharpe_ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)),
        'var_95': np.percentile(returns, 5),
        'max_drawdown': (returns.cumsum() - returns.cumsum().expanding().max()).min()
    }
    return metrics

def calculate_capm(stock_returns, market_returns):
    """Calculate CAPM metrics"""
    if stock_returns.empty or market_returns.empty:
        return None
    
    # Align returns
    aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    if len(aligned_data) < 30:  # Need minimum data points
        return None
    
    stock_ret = aligned_data.iloc[:, 0]
    market_ret = aligned_data.iloc[:, 1]
    
    # Calculate beta
    covariance = np.cov(stock_ret, market_ret)[0, 1]
    market_variance = np.var(market_ret)
    beta = covariance / market_variance
    
    # Calculate alpha (assuming risk-free rate = 0.04)
    rf_rate = 0.04 / 252  # Daily risk-free rate
    alpha = stock_ret.mean() - (rf_rate + beta * (market_ret.mean() - rf_rate))
    
    # Calculate R-squared
    correlation = np.corrcoef(stock_ret, market_ret)[0, 1]
    r_squared = correlation ** 2
    
    return {
        'beta': beta,
        'alpha': alpha * 252,  # Annualized
        'r_squared': r_squared,
        'correlation': correlation
    }

def perform_normality_tests(returns):
    """Perform normality tests"""
    if returns.empty:
        return None
    
    # Jarque-Bera test
    jb_stat, jb_pvalue = stats.jarque_bera(returns)
    
    # Shapiro-Wilk test
    sw_stat, sw_pvalue = stats.shapiro(returns)
    
    # Calculate skewness and kurtosis
    skewness = stats.skew(returns)
    kurtosis = stats.kurtosis(returns)
    
    return {
        'jarque_bera_stat': jb_stat,
        'jarque_bera_pvalue': jb_pvalue,
        'shapiro_wilk_stat': sw_stat,
        'shapiro_wilk_pvalue': sw_pvalue,
        'skewness': skewness,
        'kurtosis': kurtosis,
        'is_normal': jb_pvalue > 0.05 and sw_pvalue > 0.05
    }

def generate_efficient_frontier(portfolio_data, n_portfolios=10000):
    """Generate efficient frontier using Monte Carlo simulation"""
    if not portfolio_data:
        return None
    
    returns_data = {}
    for symbol, data in portfolio_data.items():
        if data is not None and not data.empty:
            returns_data[symbol] = calculate_returns(data['Close'])
    
    if len(returns_data) < 2:
        return None
    
    # Create returns matrix
    returns_df = pd.DataFrame(returns_data).dropna()
    
    # Calculate mean returns and covariance matrix
    mean_returns = returns_df.mean() * 252
    cov_matrix = returns_df.cov() * 252
    
    # Generate random portfolios
    portfolio_returns = []
    portfolio_volatilities = []
    portfolio_weights = []
    
    for _ in range(n_portfolios):
        weights = np.random.random(len(returns_df.columns))
        weights /= np.sum(weights)
        
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        portfolio_returns.append(portfolio_return)
        portfolio_volatilities.append(portfolio_volatility)
        portfolio_weights.append(weights)
    
    return {
        'returns': portfolio_returns,
        'volatilities': portfolio_volatilities,
        'weights': portfolio_weights,
        'mean_returns': mean_returns,
        'cov_matrix': cov_matrix
    }

def main():
    # Header
    st.markdown('<h1 class="main-header"> Argentine ADR Portfolio Analysis</h1>', unsafe_allow_html=True)
    st.markdown("### Professional Financial Analysis for Argentine ADRs")
    
    # Sidebar
    st.sidebar.header(" Portfolio Management")
    
    # Date range selection
    st.sidebar.subheader(" Date Range")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=start_date)
    with col2:
        end_date = st.date_input("End Date", value=end_date)
    
    # Auto-load Argentine ADRs
    if st.sidebar.button(" Load Argentine ADRs", type="primary"):
        with st.spinner("Loading Argentine ADR data..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            portfolio_data = {}
            for i, (symbol, name) in enumerate(ARGENTINE_ADRS.items()):
                status_text.text(f"Loading {symbol} ({name})...")
                data = fetch_stock_data(symbol, start_date, end_date)
                if data is not None:
                    portfolio_data[symbol] = data
                progress_bar.progress((i + 1) / len(ARGENTINE_ADRS))
            
            st.session_state.portfolio_data = portfolio_data
            st.session_state.loaded = True
            status_text.text(" Portfolio loaded successfully!")
            st.success(f"Loaded {len(portfolio_data)} Argentine ADRs")
    
    # Manual stock addition
    st.sidebar.subheader(" Add Individual Stock")
    new_stock = st.sidebar.text_input("Stock Symbol (e.g., AAPL)")
    if st.sidebar.button("Add Stock"):
        if new_stock:
            data = fetch_stock_data(new_stock, start_date, end_date)
            if data is not None:
                if 'portfolio_data' not in st.session_state:
                    st.session_state.portfolio_data = {}
                st.session_state.portfolio_data[new_stock] = data
                st.success(f"Added {new_stock} to portfolio")
    
    # Clear portfolio
    if st.sidebar.button(" Clear Portfolio"):
        if 'portfolio_data' in st.session_state:
            del st.session_state.portfolio_data
        if 'loaded' in st.session_state:
            del st.session_state.loaded
        st.success("Portfolio cleared")
    
    # Main content
    if 'portfolio_data' in st.session_state and st.session_state.portfolio_data:
        portfolio_data = st.session_state.portfolio_data
        
        # Portfolio Summary
        st.header(" Portfolio Summary")
        
        # Portfolio metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_stocks = len(portfolio_data)
        with col1:
            st.metric("Total Stocks", total_stocks)
        
        # Calculate portfolio returns
        portfolio_returns = {}
        for symbol, data in portfolio_data.items():
            if data is not None and not data.empty:
                returns = calculate_returns(data['Close'])
                if not returns.empty:
                    portfolio_returns[symbol] = returns
        
        if portfolio_returns:
            # Calculate equal-weighted portfolio returns
            returns_df = pd.DataFrame(portfolio_returns).dropna()
            equal_weight_returns = returns_df.mean(axis=1)
            
            portfolio_metrics = calculate_portfolio_metrics(equal_weight_returns)
            
            with col2:
                st.metric("Annual Return", f"{portfolio_metrics['mean_return']:.2%}")
            with col3:
                st.metric("Annual Volatility", f"{portfolio_metrics['volatility']:.2%}")
            with col4:
                st.metric("Sharpe Ratio", f"{portfolio_metrics['sharpe_ratio']:.3f}")
        
        # Stock performance table
        st.subheader(" Individual Stock Performance")
        
        performance_data = []
        for symbol, data in portfolio_data.items():
            if data is not None and not data.empty:
                returns = calculate_returns(data['Close'])
                if not returns.empty:
                    metrics = calculate_portfolio_metrics(returns)
                    performance_data.append({
                        'Symbol': symbol,
                        'Name': ARGENTINE_ADRS.get(symbol, symbol),
                        'Annual Return': f"{metrics['mean_return']:.2%}",
                        'Annual Volatility': f"{metrics['volatility']:.2%}",
                        'Sharpe Ratio': f"{metrics['sharpe_ratio']:.3f}",
                        'VaR (95%)': f"{metrics['var_95']:.2%}"
                    })
        
        if performance_data:
            df_performance = pd.DataFrame(performance_data)
            st.dataframe(df_performance, use_container_width=True)
        
        # Analysis tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            " CAPM Analysis", 
            " Normality Tests", 
            " Distribution Charts", 
            " Efficient Frontier"
        ])
        
        with tab1:
            st.header(" CAPM Analysis")
            
            # Market proxy (using SPY as market proxy)
            market_data = fetch_stock_data("SPY", start_date, end_date)
            
            if market_data is not None and portfolio_returns:
                market_returns = calculate_returns(market_data['Close'])
                
                capm_results = {}
                for symbol, returns in portfolio_returns.items():
                    capm = calculate_capm(returns, market_returns)
                    if capm:
                        capm_results[symbol] = capm
                
                if capm_results:
                    # CAPM results table
                    capm_data = []
                    for symbol, capm in capm_results.items():
                        capm_data.append({
                            'Symbol': symbol,
                            'Name': ARGENTINE_ADRS.get(symbol, symbol),
                            'Beta': f"{capm['beta']:.3f}",
                            'Alpha': f"{capm['alpha']:.3f}",
                            'R-squared': f"{capm['r_squared']:.3f}",
                            'Correlation': f"{capm['correlation']:.3f}"
                        })
                    
                    df_capm = pd.DataFrame(capm_data)
                    st.dataframe(df_capm, use_container_width=True)
                    
                    # Beta distribution chart
                    betas = [capm['beta'] for capm in capm_results.values()]
                    fig_beta = px.histogram(
                        x=betas,
                        title="Beta Distribution",
                        labels={'x': 'Beta', 'y': 'Frequency'},
                        nbins=10
                    )
                    st.plotly_chart(fig_beta, use_container_width=True)
        
        with tab2:
            st.header(" Normality Tests")
            
            if portfolio_returns:
                normality_results = {}
                for symbol, returns in portfolio_returns.items():
                    normality = perform_normality_tests(returns)
                    if normality:
                        normality_results[symbol] = normality
                
                if normality_results:
                    # Normality test results
                    normality_data = []
                    for symbol, normality in normality_results.items():
                        normality_data.append({
                            'Symbol': symbol,
                            'Name': ARGENTINE_ADRS.get(symbol, symbol),
                            'Jarque-Bera p-value': f"{normality['jarque_bera_pvalue']:.4f}",
                            'Shapiro-Wilk p-value': f"{normality['shapiro_wilk_pvalue']:.4f}",
                            'Skewness': f"{normality['skewness']:.3f}",
                            'Kurtosis': f"{normality['kurtosis']:.3f}",
                            'Is Normal': "" if normality['is_normal'] else ""
                        })
                    
                    df_normality = pd.DataFrame(normality_data)
                    st.dataframe(df_normality, use_container_width=True)
        
        with tab3:
            st.header(" Distribution Charts")
            
            if portfolio_returns:
                # Select stock for distribution analysis
                selected_stock = st.selectbox(
                    "Select Stock for Distribution Analysis",
                    list(portfolio_returns.keys()),
                    format_func=lambda x: f"{x} - {ARGENTINE_ADRS.get(x, x)}"
                )
                
                if selected_stock in portfolio_returns:
                    returns = portfolio_returns[selected_stock]
                    
                    # Create distribution chart
                    fig_dist = go.Figure()
                    
                    # Histogram
                    fig_dist.add_trace(go.Histogram(
                        x=returns,
                        name="Actual Returns",
                        nbinsx=20,
                        opacity=0.7,
                        marker_color='#1f77b4'
                    ))
                    
                    # Normal distribution overlay
                    x_norm = np.linspace(returns.min(), returns.max(), 100)
                    y_norm = stats.norm.pdf(x_norm, returns.mean(), returns.std())
                    
                    # Scale normal distribution to match histogram
                    hist, bins = np.histogram(returns, bins=20)
                    scale_factor = len(returns) * (bins[1] - bins[0])
                    y_norm_scaled = y_norm * scale_factor
                    
                    fig_dist.add_trace(go.Scatter(
                        x=x_norm,
                        y=y_norm_scaled,
                        name="Normal Distribution",
                        line=dict(color='red', width=2)
                    ))
                    
                    fig_dist.update_layout(
                        title=f"Return Distribution - {selected_stock}",
                        xaxis_title="Returns",
                        yaxis_title="Frequency",
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig_dist, use_container_width=True)
        
        with tab4:
            st.header(" Efficient Frontier")
            
            if portfolio_returns:
                frontier_data = generate_efficient_frontier(portfolio_data)
                
                if frontier_data:
                    # Create efficient frontier chart
                    fig_frontier = go.Figure()
                    
                    # Scatter plot of portfolios
                    fig_frontier.add_trace(go.Scatter(
                        x=frontier_data['volatilities'],
                        y=frontier_data['returns'],
                        mode='markers',
                        name='Portfolios',
                        marker=dict(
                            size=5,
                            color=frontier_data['returns'],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Return")
                        )
                    ))
                    
                    fig_frontier.update_layout(
                        title="Efficient Frontier",
                        xaxis_title="Portfolio Volatility",
                        yaxis_title="Portfolio Return",
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig_frontier, use_container_width=True)
                    
                    # Portfolio statistics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Min Volatility", f"{min(frontier_data['volatilities']):.2%}")
                    with col2:
                        st.metric("Max Return", f"{max(frontier_data['returns']):.2%}")
                    with col3:
                        st.metric("Max Sharpe", f"{max(frontier_data['returns']) / min(frontier_data['volatilities']):.3f}")
    
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 4rem;">
            <h2> Welcome to Argentine ADR Portfolio Analysis</h2>
            <p style="font-size: 1.2rem; color: #666;">
                Use the sidebar to load Argentine ADRs and start your financial analysis!
            </p>
            <div style="margin-top: 2rem;">
                <h3> Available Argentine ADRs:</h3>
                <ul style="list-style: none; padding: 0;">
                    <li> BBAR - BBVA Banco Francés</li>
                    <li> BMA - Banco Macro</li>
                    <li> CEPU - Central Puerto</li>
                    <li> CRESY - Cresud</li>
                    <li> EDN - Edenor</li>
                    <li> GGAL - Grupo Financiero Galicia</li>
                    <li> IRS - IRSA</li>
                    <li> LOMA - Loma Negra</li>
                    <li> MELI - Mercado Libre Inc.</li>
                    <li> PAM - Pampa Energía</li>
                    <li> SUPV - Grupo Supervielle</li>
                    <li> TEO - Telecom Argentina</li>
                    <li> TGS - Transportadora de Gas del Sur</li>
                    <li> TS - Tenaris</li>
                    <li> YPF - YPF</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
