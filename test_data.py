from datetime import datetime

x = '2022-01-11'
y = '2022-01-11' 
z = '2022-01-11'

print(datetime(*[int(i) for i in x.split('-')]))
