# from django.test import TestCase

# Create your tests here.

import datetime

# today = datetime.date.today()
today = '2021-03-09'
y = datetime.datetime.strptime(today, '%Y-%m-%d')
print(y)

n = y - datetime.timedelta(days=12)
print(n)