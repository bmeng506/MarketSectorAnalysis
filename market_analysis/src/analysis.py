import pandas as pd
import numpy as np
from typing import Dict

class MarketAnalyzer:
    def __init__(self, data: pd.DataFrame, risk_free_rate: float):
        self.data = data
        self.metrics = {}
        self.risk_free_rate = risk_free_rate
        self.returns = None

    def calculate_daily_returns(self) -> pd.DataFrame:
        self.returns = self.data.pct_change()
        return self.returns

    def calculate_metrics(self) -> Dict:
        if self.returns == None:
            self.calculate_daily_returns()
        
        total_return = (self.data.iloc[-1] / self.data.iloc[0])
        annual_returns = (total_return) ** (252 / len(self.data)) - 1

        volatility = self.returns.std() * np.sqrt(252)

        sharpe_ratio = (annual_returns - self.risk_free_rate) / volatility

        correlation = self.returns.corr()

        cumulative_returns = (1 + self.returns).cumprod()

        self.metrics = {
            'Annual Returns': annual_returns.to_dict(),
            'Volatility': volatility.to_dict(),
            'Sharpe Ratio': sharpe_ratio.to_dict(),
            'Correlation': correlation,
            'Cumulative Returns': cumulative_returns
        }

        return self.metrics
    
    def create_report(self) -> str:
        report = 'Stock Market Analysis Report: '
        report += '-' * 25 + '\n\n'

        print("Available metrics:", self.metrics.keys())

        for sector in self.data.columns:
            report += f"{sector} Sector:\n"

            try:
                annual_return = float(self.metrics['Annual Returns'][sector])
                volatility = float(self.metrics['Volatility'][sector])
                sharpe = float(self.metrics['Sharpe Ratio'][sector])

                report += f"Annual Return: {round(annual_return * 100, 2)}%\n"
                report += f"Volatility: {round(volatility * 100, 2)}%\n"
                report += f"Sharpe Ratio: {round(sharpe, 2)}\n"
                report += '-' * 25 + '\n'

            except Exception as e:
                print(f"Error processing {sector}: {str(e)}")
                continue

        return report






