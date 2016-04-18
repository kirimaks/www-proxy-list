import process

proxy_obj = process.init_proxy_list()

for i in range(25):
    print(process.get_proxy_str(proxy_obj))
