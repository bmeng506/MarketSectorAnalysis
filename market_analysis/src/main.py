import logging
import os
from data_collection import DataCollection
from analysis import MarketAnalyzer
from visualization import Visualizer
from datetime import datetime, timedelta

def setup_logging():
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s - %(levelname)s - %(message)s',
        handlers = [
            logging.FileHandler('../market_analysis.log'),
            logging.StreamHandler()
        ]
    )

def setup_directories():
    directories = [
        '../output',
        '../output/reports',
        '../output/figures',
        '../data'
    ]
    for directory in directories: 
        os.makedirs(directory, exist_ok = True)

def main():
    
    setup_directories()
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        end_date = datetime.now()
        end_date = end_date - timedelta(days = 1)
        start_date = end_date - timedelta(days = 365)

        logger.info(f"Collecting data from {start_date.date()} to {end_date.date()}")
        collector = DataCollection()
        data = collector.get_data(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        # input risk-free rate as a float, 0.03 in this instance
        analyzer = MarketAnalyzer(data, risk_free_rate = 0.03)
        metrics = analyzer.calculate_metrics()

        report = analyzer.create_report()
        with open('market_analysis/output/reports/analysis_report.txt', 'w') as file:
            file.write(report)
        logger.info(f"Analysis report written to {'../output/reports/analysis_report'}")

        visual = Visualizer(metrics)
        visual.create_plots()
        logger.info('Visualization completed')
        


    except Exception as e: 
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        print("An error occured: " + str(e))

if __name__ == '__main__':
    main()

