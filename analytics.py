# Do some analytics on Shopify transactions.

import pandas as pd
from datetime import datetime, timedelta


class Analytics:

    def __init__(self, filename: str, datetime_now, refund_window: int):
        raw = pd.read_csv(filename)

        clean = raw[raw['Status'].isin(['success'])]                # Filter down to successful transactions only.

        ###############
        # Sales
        ###############
        sales_only = clean[clean['Kind'].isin(['sale'])]            # Filter down to Sales only.

        # Discard sales in the last <refund_window> days, because those sales haven't had time to have refunds yet.
        fortnight_ago = datetime.strftime((datetime_now + timedelta(days=-refund_window)),  "%Y-%m-%d")
        sales = sales_only[sales_only['Created At'] < fortnight_ago].copy()

        # Add column Year Month.
        ym_list = []
        for index, row in sales.iterrows():
            ym_list.append(self.year_month(date_str=row['Created At'][0:10], delta_days=0))
        sales['Year Month'] = ym_list

        # Aggregate sales by Year Month dimension.
        monthly_sales = sales.groupby('Year Month')['Amount'].sum().reset_index(name='Sales')

        ###############
        # Refunds
        ###############
        refunds = clean[clean['Kind'].isin(['refund'])].copy()      # Filter down to Refunds only.

        # Add column Year Month, shifted by Refund Window number of days.
        ym_list = []
        for index, row in refunds.iterrows():
            ym_list.append(self.year_month(date_str=row['Created At'][0:10], delta_days=-refund_window))
        refunds['Year Month'] = ym_list

        # Aggregate refunds by Year Month dimension.
        monthly_refunds = refunds.groupby('Year Month')['Amount'].sum().reset_index(name='Refunds')

        ###############
        # Refund Rate
        ###############
        self.sales_and_refunds = pd.merge(monthly_sales, monthly_refunds, on='Year Month', how='outer')
        self.sales_and_refunds.fillna(0, inplace=True)
        self.sales_and_refunds['Return Rate'] = self.sales_and_refunds['Refunds'] / self.sales_and_refunds['Sales']

    @staticmethod
    def year_month(date_str: str, delta_days: int) -> str:
        """For parm date string (yyyy-mm-dd), return it as a year-month string (yyyy-mm). The parm date will be moved
        forward or backwards in time by the parm delta number of days."""
        ym = datetime.strptime(date_str, "%Y-%m-%d")
        adjusted_date = ym + timedelta(days=delta_days)
        return str(adjusted_date.year) + '-' + str(adjusted_date.month).zfill(2)
