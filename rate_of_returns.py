# Analyse rate of returns.

import analytics as an
from _datetime import datetime

analysis = an.Analytics(filename='transactions.csv', datetime_now=datetime.now(), refund_window=14)

print(analysis.sales_and_refunds.head(100))

analysis.sales_and_refunds.to_csv('refund_rate.csv', index=False, float_format='%.3f')
