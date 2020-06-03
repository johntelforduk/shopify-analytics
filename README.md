# Shopify Analytics
For each month, the program calculates the monthly Refund Rate as follows,
```
Refund Rate = sum(Refunds) / sum(Sales)
```
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
1. In Shopify, do export of transactions.
2. Put the `transactions.csv` file in this project's home directory.
3. Run the command `python rate_of_returns.py`

The file `refund_rate.csv` will be created. You can then load this file into Excel, etc. for subsequent graphing, etc.
