# from django.test import TestCase

# Create your tests here.

import datetime

# today = datetime.date.today()
today = '2021-2-5'
y = datetime.datetime.strptime(today, '%Y-%m-%d')
print(datetime.datetime.strftime(y, '%Y-%m-%d'))
#
n = y - datetime.timedelta(days=1)
n= datetime.datetime.strftime(n, '%Y-%m-%d')
print(n)
# a = 4.7
# b = "%.1f" % (a / 3)
# print(b)