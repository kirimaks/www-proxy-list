# proxy_list
Some script to get random list of proxy servers from internet.

>>> from proxy_list.get_proxy import GetProxy
>>> px = GetProxy()
*** Connect to database ***
>>> for i in range(10):print(px.get_proxy())
... 
*** Generate new proxy ***
http://81.213.144.156:8086
*** Generate new proxy ***
http://124.120.79.27:8888
*** Generate new proxy ***
http://186.91.38.137:8080
*** Generate new proxy ***
http://186.95.82.207:8080
*** Generate new proxy ***
https://94.141.179.58:3128
*** Generate new proxy ***
http://186.89.80.53:8080
*** Generate new proxy ***
http://124.122.220.232:8888
*** Generate new proxy ***
http://190.207.204.218:8080
*** Generate new proxy ***
http://58.8.193.131:8888
*** Generate new proxy ***
http://219.85.242.94:8088
>>> 
