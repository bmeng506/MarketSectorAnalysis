import pandas as pd
import yfinance as yf
import logging

class DataCollection:
    def __init__(self): 
        self.logger = logging.getLogger('DataCollection')
        self.sector_etfs = {
            'Information Technology': 'XLK',
	        'Industrials': 'XLI',
	        'Financials': 'XLF',
	        'Communication Services': 'XLC',
	        'Real Estate': 'XLRE',
	        'Energy': 'XLE',
	        'Consumer Discretionary': 'XLY',
	        'Materials': 'XLB',
            'Health Care': 'XLV',
	        'Utilities': 'XLU',
	        'Consumer Staples': 'XLP'
        }
    
    def get_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        all_data = {}
        
        for sector, symbol in self.sector_etfs.items():
            self.logger.info(f"Fetching data for {sector} ({symbol})")
            try:
                ticker = yf.Ticker(symbol)
                df = ticker.history(start = start_date, end = end_date)

                if df is None:
                    self.logger.warning(f"Received None data for {symbol}")
                    continue

                if df.empty:
                    self.logger.warning(f"Received empty data for {symbol}")
                    continue
                
                if 'Close' not in df.columns:
                    self.logger.warning(f"No Close price column for {symbol}")
                    continue 

                close_prices = df['Close']
                if close_prices.isna().any():
                    self.logger.warning(f"Found NaN values in {symbol} data")
                    close_prices = close_prices.fillna(method='ffill')
                
                if len(close_prices) < 2:
                    self.logger.warning(f"Insufficient data points for {symbol}")
                    continue
                
                # Store valid data
                all_data[sector] = close_prices
                self.logger.info(f"Successfully collected {len(close_prices)} data points for {symbol}")
                
            except Exception as e:
                self.logger.error(f"Error processing {symbol}: {str(e)}")


        if not all_data:
            raise ValueError("No valid data collected for any sector")
        
        # Create DataFrame
        df = pd.DataFrame(all_data)
        self.logger.info(f"Created DataFrame with shape: {df.shape}")

        # Save raw data with error handling
        try:
            df.to_csv('market_analysis/data/raw_market_data.csv', index=False)

            self.logger.info("Raw data saved successfully")
        except Exception as e:
            self.logger.warning(f"Could not save raw data: {str(e)}")
        
        return df


