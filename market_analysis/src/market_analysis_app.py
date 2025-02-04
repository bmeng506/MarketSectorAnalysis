import streamlit as st
from data_collection import DataCollection
from analysis import MarketAnalyzer
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("Market Sector Analysis")
    
    # Date inputs
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=365)
    
    # Collect data
    collector = DataCollection()
    data = collector.get_data(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    # Analysis
    analyzer = MarketAnalyzer(data, risk_free_rate=0.03)
    metrics = analyzer.calculate_metrics()
    
    # Display metrics
    st.header("Market Metrics")
    st.write("Annual Returns:", metrics['Annual Returns'])
    st.write("Volatility:", metrics['Volatility'])
    st.write("Sharpe Ratios: (RFR: 0.03)", metrics['Sharpe Ratio'])
    
    # Risk-Return Plot
    st.subheader("Risk-Return Analysis")
    returns = pd.Series(metrics['Annual Returns'])
    vols = pd.Series(metrics['Volatility'])
    sharpe = pd.Series(metrics['Sharpe Ratio'])

    fig = plt.figure(figsize = (12, 8))
    plt.scatter(vols, returns)

    plt.margins(x = 0.1, y = 0.1)
    
    for sector in returns.index:

        plt.annotate(
            f"{sector}\nSharpe: {sharpe[sector]:.2f}",
            (vols[sector], returns[sector]),
            xytext = (-7, 12) if sector in ['Information Technology', 'Communication Services'] else (0, 12),
            textcoords = 'offset points',
            horizontalalignment = 'center'
        )

    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Annual Return')
    plt.title('Risk-Return Analysis by Sector')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Correlation Heatmap
    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(metrics['Correlation'], 
                annot=True, 
                cmap='coolwarm',
                center=0,
                fmt='.2f',
                ax=ax)
    ax.set_title('Sector Correlations')
    st.pyplot(fig)

    st.subheader("Sector Performance Comparison")
    st.text("Growth of $1")

    fig = plt.figure(figsize = (12, 8))
    for column in metrics['Cumulative Returns'].columns:
        plt.plot(metrics['Cumulative Returns'].index,
                 metrics['Cumulative Returns'][column],
                 label = column)
    plt.title('Sector Performance Comparison')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return $')
    plt.legend(bbox_to_anchor = (1.05, 1), loc = 'upper left', borderaxespad = 0.)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

if __name__ == "__main__":
    main()