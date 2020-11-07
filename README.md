# Shopify Analytics
For each month, the program calculates the monthly Refund Rate as follows,
```
Refund Rate = sum(Refunds) / sum(Sales)
```
Orders made in the last 14 days are omitted from the analysis, as they have not had sufficient time for refunds to be made.
#### Installation
```
pip install pandas
pip install pytest
```
#### Testing
```
pytest
```
#### Process
1. In Shopify, choose "Orders" from the menu on left-hand side of screen.
2. Press button for "Export".
![Screenshot](https://github.com/johntelforduk/shopify-analytics/blob/master/export_orders_screenshot.jpg)

3. Select "All orders" and "Plain CSV file". Press "Export transactions histories" button.
4. Put the `transactions.csv` file in this project's home directory.
5. Run the command `python rate_of_returns.py`

The file `refund_rate.csv` will be created. You can then load this file into Excel, etc. for subsequent graphing, etc.
