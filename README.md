# Ali-Rupani-Personal-Project-FINN-5453
Stock CAPM Analysis Tool - README

Fall 2023 Personal Project for FINN 5453 with Dr. Xinde Zhang

Introduction

The Stock CAPM Analysis Tool is a Python application designed to perform a Comparative Analysis of a selected stock against the S&P 500 index using the Capital Asset Pricing Model (CAPM). It provides a graphical user interface (GUI) for easy interaction and visual representation of data.

Features

Fetches real-time stock data and the S&P 500 index data.
Calculates the expected return of a stock based on the CAPM model.
Compares the actual stock return with the expected CAPM return and S&P 500 return.
Graphical representation of stock performance over the last five years.
Error handling for data fetching and analysis process.
Requirements

Python 3.x
Matplotlib
Tkinter
Yahoo_fin
Installation

Ensure Python 3.x is installed.
Install required packages:
Copy code
pip install matplotlib yahoo_fin
Usage

Run the script.
Enter the ticker symbol of the stock you want to analyze.
Click the "Analyze" button to view the results.
Functions

get_five_year_treasury_rate(): Fetches the 5-year Treasury yield.
fetch_stock_data(symbol, start_date, end_date): Retrieves stock and S&P 500 data.
calculate_percentage_change(data): Calculates the percentage change in data.
perform_analysis(): Conducts the CAPM analysis and updates the GUI with results.
GUI Components

Entry field for stock ticker.
Buttons for initiating analysis.
Text boxes displaying the CAPM expected return, stock actual return, and their differences.
License

This project is licensed under the MIT License - see the LICENSE file for details.

Disclaimer

This tool is for informational purposes only. It is not financial advice.

