import proxy_process

proxy_obj = proxy_process.init_proxy_list()

for i in range(25):
    print(proxy_process.get_proxy_str(proxy_obj))
