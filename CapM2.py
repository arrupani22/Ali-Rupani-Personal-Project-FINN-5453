import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk, Text, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from yahoo_fin import stock_info as si

def get_five_year_treasury_rate():
    """Fetch the latest 5-year Treasury yield as the risk-free rate."""
    try:
        latest_data = si.get_quote_table("^FVX")
        yield_ = latest_data["Previous Close"]
        return float(yield_) / 100
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch 5-year Treasury rate: {e}")
        raise

def fetch_stock_data(symbol, start_date, end_date):
    """Fetch the stock and S&P 500 data along with the stock's beta."""
    try:
        stock_data = si.get_data(symbol, start_date=start_date, end_date=end_date)[['close']]
        stock_data.columns = ['Close']

        sp500_data = si.get_data("^GSPC", start_date=start_date, end_date=end_date)[['close']]
        sp500_data.columns = ['Close']

        beta = si.get_quote_table(symbol)["Beta (5Y Monthly)"]
        return stock_data, beta, sp500_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {symbol}: {e}")
        raise

def calculate_percentage_change(data):
    """Calculate percentage change relative to the initial data point."""
    initial_value = data.iloc[0]
    return (data - initial_value) / initial_value * 100

def perform_analysis():
    """Perform CAPM analysis and plot the results."""
    ticker = ticker_entry.get().upper()
    end_date = datetime.now()
    start_date = datetime(end_date.year - 5, end_date.month, end_date.day)

    # Clear previous results
    capm_result_text.delete(1.0, tk.END)
    stock_result_text.delete(1.0, tk.END)
    sp500_result_text.delete(1.0, tk.END)
    capm_difference_text.delete(1.0, tk.END)
    sp500_difference_text.delete(1.0, tk.END)

    try:
        # Fetch data
        stock_data, beta, sp500_data = fetch_stock_data(ticker, start_date, end_date)

        # Calculate percentage changes for plotting
        stock_percentage_changes = calculate_percentage_change(stock_data['Close'])
        sp500_percentage_changes = calculate_percentage_change(sp500_data['Close'])

        # CAPM Analysis - use cumulative market return
        RISK_FREE_RATE = get_five_year_treasury_rate()
        cumulative_market_return = sp500_percentage_changes / 100
        expected_returns = RISK_FREE_RATE + beta * (cumulative_market_return - RISK_FREE_RATE)
        capm_returns = expected_returns * 100  # Convert to percentage for plotting

        # Calculate the differences
        capm_difference = stock_percentage_changes.iloc[-1] - capm_returns.iloc[-1]
        sp500_difference = stock_percentage_changes.iloc[-1] - sp500_percentage_changes.iloc[-1]

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(stock_percentage_changes, label=f"{ticker} Actual Returns", linewidth=1.5, color='blue')
        ax.plot(sp500_percentage_changes, label="S&P 500 Returns", linestyle="-", linewidth=1.5, color='green')
        ax.plot(capm_returns, label=f"{ticker} CAPM Expected Returns", linestyle="-", linewidth=1.5, color='orange')
        ax.set_title(f"{ticker} vs. S&P 500 vs. CAPM Expected Returns Over The Last 5 Years")
        ax.set_xlabel("Date")
        ax.set_ylabel("Percentage Change (%)")
        ax.legend()
        ax.grid(True)
        ax.set_xlim([start_date, end_date])

        # Embed the plot in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=7, column=0, padx=10, pady=10, columnspan=2)
        canvas.draw()

        # Display the results and differences in text boxes
        capm_result_text.insert(tk.END, f"Expected 5-year Return (CAPM): {capm_returns.iloc[-1]:.2f}%")
        stock_result_text.insert(tk.END, f"Actual 5-year Return for {ticker}: {stock_percentage_changes.iloc[-1]:.2f}%")
        sp500_result_text.insert(tk.END, f"S&P 500 5-year Return: {sp500_percentage_changes.iloc[-1]:.2f}%")
        capm_difference_text.insert(tk.END, f"Difference (Stock vs CAPM): {capm_difference:.2f}%")
        sp500_difference_text.insert(tk.END, f"Difference (Stock vs S&P 500): {sp500_difference:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during analysis: {e}")
# GUI setup
window = tk.Tk()
window.title("Stock CAPM Analysis Tool")

ticker_label = ttk.Label(window, text="Enter Stock Ticker:")
ticker_label.grid(row=0, column=0, padx=10, pady=10)

ticker_entry = ttk.Entry(window)
ticker_entry.grid(row=0, column=1, padx=10, pady=10)

analyze_button = ttk.Button(window, text="Analyze", command=perform_analysis)
analyze_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

capm_label = ttk.Label(window, text="CAPM Expected Return:")
capm_label.grid(row=2, column=0, padx=10, pady=10)
capm_result_text = Text(window, height=2, width=40)
capm_result_text.grid(row=2, column=1, padx=10, pady=10)

stock_label = ttk.Label(window, text="Stock Actual Return:")
stock_label.grid(row=3, column=0, padx=10, pady=10)
stock_result_text = Text(window, height=2, width=40)
stock_result_text.grid(row=3, column=1, padx=10, pady=10)

sp500_label = ttk.Label(window, text="S&P 500 Return:")
sp500_label.grid(row=4, column=0, padx=10, pady=10)
sp500_result_text = Text(window, height=2, width=40)
sp500_result_text.grid(row=4, column=1, padx=10, pady=10)

capm_difference_label = ttk.Label(window, text="Difference (Stock vs CAPM):")
capm_difference_label.grid(row=5, column=0, padx=10, pady=10)
capm_difference_text = Text(window, height=2, width=40)
capm_difference_text.grid(row=5, column=1, padx=10, pady=10)

sp500_difference_label = ttk.Label(window, text="Difference (Stock vs S&P 500):")
sp500_difference_label.grid(row=6, column=0, padx=10, pady=10)
sp500_difference_text = Text(window, height=2, width=40)
sp500_difference_text.grid(row=6, column=1, padx=10, pady=10)

window.mainloop()