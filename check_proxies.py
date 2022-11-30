import threading
import queue

import requests

q = queue.Queue()
valid_proxies = []

with open("proxy_list.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            r = requests.get(
                "http://ipinfo.io",
                proxies={"http": proxy, "https": proxy},
                # timeout=5,
            )
        except:
            continue

        if r.status_code == 200:
            valid_proxies.append(proxy)
            print(proxy)


for _ in range(100):
    threading.Thread(target=check_proxy).start()

# save valid proxies in valid_proxies.txt
with open("valid_proxies.txt", "w") as f:
    f.write("\n".join(valid_proxies))
