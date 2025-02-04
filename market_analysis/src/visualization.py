import matplotlib.pyplot as plt
import seaborn as sb
from typing import Dict
import pandas as pd

class Visualizer:
    def __init__(self, metrics: Dict):
        self.metrics = metrics
        plt.style.use('classic')
    
    def one_performance_graph(self):
        plt.figure(figsize = (12, 6))
        self.metrics['Cumulative Returns'].plot()
        plt.title('Sector Performance Comparison')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return $')
        plt.legend(bbox_to_anchor = (1.05, 1), loc = 'upper left')
        plt.tight_layout()
        plt.savefig('market_analysis/output/figures/performance.png')
        plt.close()
    
    def correlation_heatmap(self):
        plt.figure(figsize = (12, 6))
        sb.heatmap(self.metrics['Correlation'], 
                   annot = True,
                   cmap = 'coolwarm',
                   center = 0,
                   fmt = '.2f')
        plt.title('Sector Correlations')
        plt.tight_layout()
        plt.savefig('market_analysis/output/figures/correlation.png')
        plt.close()
    
    def risk_return_graph(self):
        returns = pd.Series(self.metrics['Annual Returns'])
        vols = pd.Series(self.metrics['Volatility'])
        sharpe = pd.Series(self.metrics['Sharpe Ratio'])

        plt.figure(figsize = (14, 8))
        plt.scatter(vols, returns)

        for sector in returns.index:
            plt.annotate(f"{sector}\nSharpe: {sharpe[sector]:.2f}",
                         xy = (vols[sector], returns[sector]),
                         xytext = (-5, 10),
                         textcoords = 'offset points',
                         horizontalalignment = 'center'
            )

        plt.xlabel('Volatility (Risk)')
        plt.ylabel('Annual Return')
        plt.title('Risk-Return Analysis By Sector')

        plt.tight_layout()
        plt.savefig('market_analysis/output/figures/risk_return.png')
        plt.close()

    def create_plots(self):
        self.one_performance_graph()
        self.correlation_heatmap()
        self.risk_return_graph()

