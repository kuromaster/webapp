import datetime
import pandas

string = 'Fri, 12 Mar 2021 19:37:25 GMT'
if ( type (string) is  datetime.datetime) or (type (string) is  datetime.date) or (type(string) is pandas.Timestamp):
    print("is Date")
else:
    print("unluck")

print("time: " + str(datetime.datetime.strftime(string, '%Y-%m-%d %H:%M:%S')))
