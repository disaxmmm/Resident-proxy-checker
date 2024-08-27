import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_proxy(proxy, retries=3):
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        
        attempt = 0
        while attempt < retries:
            try:
                response = requests.get("http://ip-api.com/json", proxies=proxies, timeout
                if response.status_code == 400:
                    print(f"Прокси {proxy} вернул 400 Bad Request и был пропущен.")
                    break

                data = response.json()


                if data['status'] == 'success':
                    org = data.get('org', '')
                    isp = data.get('isp', '')
                    mobile = data.get('mobile', False)
                    proxy_type = data.get('proxy', False)

                    if org and isp and not mobile and not proxy_type and "Hosting" not in org and "Data Center" not in isp:
                        with open('checked.txt', 'a') as checked_file:
                            checked_file.write(f"{proxy} \n")
                        print(f"Прокси {proxy} является резидентским.")
                        return proxy
                break  
            except requests.exceptions.RequestException as e:
                attempt += 1
                if attempt >= retries:
                    pass
    except requests.exceptions.RequestException as e:
        pass
    return None

with open('proxy.txt', 'r') as file:
    proxy_list = [proxy.strip() for proxy in file.readlines()]

with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list}
    
    for future in as_completed(future_to_proxy):
        proxy = future_to_proxy[future]
        result = future.result()

print("Проверка всех прокси завершена.")

time.sleep(15)

input("Нажмите Enter, чтобы завершить работу...")