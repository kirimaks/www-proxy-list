At first run "create_proxy_list.py" (or add to cron) to generate list of proxy servers.
```sh
>>> from proxy_list.get_proxy import GetProxy
>>> pl = GetProxy()
```
```sh
>>> for i in range(5):pl.get_proxy()
... 
'http://190.199.140.54:8080'
'http://190.207.239.200:8080'
'http://36.66.73.190:3128'
'http://182.93.224.38:8080'
'http://183.111.169.207:3128'
>>> 
```

Feel free to open an issue.
