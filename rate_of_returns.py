# Analyse rate of returns.

import analytics as an
from _datetime import datetime

analysis = an.Analytics(filename='transactions_export_1.csv', datetime_now=datetime.now(), refund_window=14)

print(analysis.monthly.head(1000))

analysis.monthly.to_csv('refund_rate.csv', index=False, float_format='%.3f')
