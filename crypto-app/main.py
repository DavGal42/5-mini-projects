"""
Author: David Galstyan

Description: A Desktop app which allows the user to upload a file that contains
the symbols of the cryptocurrencies. It generates an excel file with the detailed
information of that cryptocurrencies (Name, Symbol, Current price, Market Cap, Total Volume,
Price Change for 24 hours, etc.). The user is able to name the excel file from the desktop
app window.
"""

import os
import tkinter as tk
import xlsxwriter
import requests


URL = 'https://api.coincap.io/v2/assets'


def get_data_from_url(URL):
    """
        Description: Get data of cryptocurrencies

        Parameters: URL of API
    """
    response = requests.get(URL, timeout=10)
    data = response.json()

    return data


def get_crypto_list(data):
    """
        Description: Get list of cryptocurrencies
        Parameters: Data of cryptocurrencies
    """
    ml = []

    for i in range(10):
        md = {}
        md['name'] = data['data'][i]['name']
        md['symbol'] = data['data'][i]['symbol']
        md['current_price'] = str(round(float(data['data'][i]['priceUsd']), 3)) + '$'
        md['market_cap'] = str(round(float(data['data'][i]['marketCapUsd']))) + '$'
        md['total_volume'] = str(round(float(data['data'][i]['volumeUsd24Hr']))) + '$'
        md['price_24h'] = str(round(float(data['data'][i]['vwap24Hr']))) + '$'
        ml.append(md)

    return ml


def create_first_window():
    """
        Description: Script of the first window
    """
    first_window = tk.Tk()
    first_window.title("Download Tickers")
    first_window.geometry("400x200")
    first_window.configure(bg='#1a2445')

    button = tk.Button(first_window, text="Download", bg='yellow', fg='#1a2445',\
    font=('Roboto', 20, 'bold'), command=lambda: download_txt_file(first_window))

    button.pack(expand=True, padx=20, pady=20)

    first_window.protocol("WM_DELETE_WINDOW", first_window.destroy)

    first_window.mainloop()


def write_to_excel(data, file_path):
    """
        Description: Make an excel file

        Parameters: List of cryptocurrencies and file path
    """
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    headers = ['Name', 'Symbol', 'Current Price', 'Market Cap', 'Total Volume', 'Price 24h']
    
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold)
    
    row = 1
    for crypto in (data):
        worksheet.write(row, 0, crypto['name'])
        worksheet.write(row, 1, crypto['symbol'])
        worksheet.write(row, 2, crypto['current_price'])
        worksheet.write(row, 3, crypto['market_cap'])
        worksheet.write(row, 4, crypto['total_volume'])
        worksheet.write(row, 5, crypto['price_24h'])
        row += 1

    workbook.close()


def download_txt_file(first_window):
    """
        Description: Download a txt file with the names of cryptos and close first window

        Parameters: First window
    """
    cryptocurrencies = [
        "BTC",
        "ETH",
        "USDT",
        "BNB",
        "SOL",
        "USDC",
        "XRP",
        "DOGE",
        "ADA",
        "SHIB"
    ]

    with open("cryptos.txt", 'w', encoding="utf-8") as file:
        for i in range(10):
            file.write(cryptocurrencies[i] + '\n')

    first_window.destroy()
    create_second_window()


def create_second_window():
    """
        Description: Script of the second window
    """
    second_window = tk.Tk()
    second_window.title("Download XLSX File")
    second_window.geometry("500x250")
    second_window.configure(bg='#1a2445')

    label = tk.Label(second_window, text="Enter file name", bg='#1a2445',\
    fg='#8392c9', font=('Roboto', 10, 'bold'))
    label.pack(pady=20)

    entry = tk.Entry(second_window, width=30)
    entry.pack(pady=5)

    button = tk.Button(second_window, text="Download", bg='yellow', fg='#1a2445',\
    font=('Roboto', 20, 'bold'),command=lambda: download_excel_file(second_window, entry))
    button.pack(pady=50)

    second_window.mainloop()


def download_excel_file(second_window, entry):
    """
        Description: Download txt file with names of cryptos and close first window

        Parameters: Second window and entry place 
    """
    data = get_data_from_url(URL)
    cryptos = get_crypto_list(data)
    
    file_name = entry.get()

    if not file_name.endswith('.xlsx'):
        file_name += '.xlsx'
    
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    
    file_path = os.path.join(downloads_folder, file_name)
    
    write_to_excel(cryptos, file_path)
    
    second_window.destroy()


def main():
    """
        The main function
    """
    create_first_window()


if __name__ == '__main__':
    main()
