# Do some analytics on Shopify transactions.

import pandas as pd
from datetime import datetime, timedelta


class Analytics:

    def __init__(self, filename: str, datetime_now, refund_window: int):
        raw = pd.read_csv(filename)

        # Filter down to successful transactions only.
        clean = raw[raw['Status'].isin(['success'])]

        # Filter down to sales only.
        sales_only = clean[clean['Kind'].isin(['sale'])]

        # Discard sales in the last <refund_window> days, because those sales haven't had time to have refunds yet.
        fortnight_ago = datetime.strftime((datetime_now + timedelta(days=-refund_window)),  "%Y-%m-%d")
        sales = sales_only[sales_only['Created At'] < fortnight_ago].copy()

        year_month = []
        for index, row in sales.iterrows():

            # Get the date part of the Created At string alone (discard time).
            dts = row['Created At'][0:10]
            created_at = datetime.strptime(dts, "%Y-%m-%d")

            ym = str(created_at.year) + '-' + str(created_at.month).zfill(2)
            year_month.append(ym)
        sales['Year Month'] = year_month

        monthly_sales = sales.groupby('Year Month')['Amount'].sum().reset_index(name='Sales')

        ###############
        refunds = clean[clean['Kind'].isin(['refund'])].copy()

        year_month = []
        for index, row in refunds.iterrows():

            # Get the date part of the Created At string alone (discard time).
            dts = row['Created At'][0:10]
            created_at = datetime.strptime(dts, "%Y-%m-%d")

            # A refund today is considered to be related to a sale <refund_window> days ago.
            fortnight_earlier = created_at + timedelta(days=-refund_window)
            ym = str(fortnight_earlier.year) + '-' + str(fortnight_earlier.month).zfill(2)
            year_month.append(ym)
        refunds['Year Month'] = year_month

        monthly_refunds = refunds.groupby('Year Month')['Amount'].sum().reset_index(name='Refunds')

        #############
        self.sales_and_refunds = pd.merge(monthly_sales, monthly_refunds, on='Year Month', how='outer')
        self.sales_and_refunds.fillna(0, inplace=True)
        self.sales_and_refunds['Return Rate'] = self.sales_and_refunds['Refunds'] / self.sales_and_refunds['Sales']
