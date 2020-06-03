# Do some analytics on Shopify transactions.

import pandas as pd
from datetime import datetime, timedelta


class Analytics:

    def __init__(self, filename: str, datetime_now, refund_window: int):
        raw = pd.read_csv(filename)

        clean = raw[raw['Status'].isin(['success'])]                # Filter down to successful transactions only.

        # Filter down to Sales only.
        sales = clean[clean['Kind'].isin(['sale'])].rename(columns={'Amount': 'Sales'})

        refunds = clean[clean['Kind'].isin(['refund'])]             # Filter down to Refunds only.

        # Make a table with total refunds paid for each 'Name'.
        total_refunds = refunds.groupby('Name')['Amount'].sum().reset_index(name='Refunds')

        # Join the Sales and Refunds tables together.
        sales_and_refunds = pd.merge(sales, total_refunds, on='Name', how='outer')

        # For sales with no refund associated with them, replace Refunds of NaN with zero.
        sales_and_refunds.fillna(0, inplace=True)

        # Discard sales in the last <refund_window> days, because those sales haven't had time to have refunds yet.
        cutoff = datetime.strftime((datetime_now + timedelta(days=-refund_window)),  "%Y-%m-%d")
        valid_sales_and_refunds = sales_and_refunds[sales_and_refunds['Created At'] < cutoff].copy()

        # Add column Year Month.
        ym_list = []
        for index, row in valid_sales_and_refunds.iterrows():
            ym_list.append(row['Created At'][0:7])
        valid_sales_and_refunds['Year Month'] = ym_list

        self.monthly = (valid_sales_and_refunds
                        .groupby('Year Month')
                        .agg({'Sales': 'sum', 'Refunds': 'sum'})
                        .reset_index())

        self.monthly['Refund Rate'] = self.monthly['Refunds'] / self.monthly['Sales']
