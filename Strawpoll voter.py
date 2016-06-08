from selenium import webdriver
from time import sleep
import pyautogui
import requests
import bs4

pollnum = "99999999"
element_id = "FIELD ID GOES HERE"

proxy_website = bs4.BeautifulSoup(requests.get("https://www.us-proxy.org/").text)

preparsed_list = proxy_website.select("td")
postparsed_list = []

for i in preparsed_list:
    if "." in str(i):
        proxy_address = str(i) + ":" + str(preparsed_list[preparsed_list.index(i) + 1])
        postparsed_list.append(proxy_address)

postparsed_list = [i.translate(None, "<>td/") for i in postparsed_list]

f2 = open("proxy_fail.txt", "r+")
failed_proxy = f2.read().splitlines()
f2.close()

f2 = open("proxy_fail.txt", "a")

f = open("proxy.txt", "a")
for new_proxy in postparsed_list:
    f.write(new_proxy + "\n")
f.close()

f = open("proxy.txt", "r+")
proxy = f.read().splitlines()
proxy = set(proxy)
proxy = [i for i in proxy if i not in failed_proxy]
f.seek(0)
for line in proxy:
    f.write(line + "\n")
f.truncate()



print("You have " + str(len(proxy)) + " entries in your proxy file.")

future_file = []

for i in proxy:
    webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
        "httpProxy":i,
        "ftpProxy":i,
        "sslProxy":i,
        "noProxy":None,
        "proxyType":"MANUAL",
        "autodetect":False
    }
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(40)
    print("Using " + i)
    try:
        driver.get("http://www.strawpoll.me/" + pollnum)
        driver.find_element_by_id(element_id).click()
    except:
        print("Failure")
        f2.write(i + "\n")
        try:
            driver.close()
        except:
            print("Driver wouldn't close.")
            pass
    else:
        print("Success")
        future_file.append(i)
        sleep(.5)
        driver.find_element_by_xpath("html/body/main/form/footer/button[1]").click()
        sleep(3)
        driver.close()


f.seek(0)
for successful_proxy in future_file:
    f.write(i + "\n")
f.truncate()
f.close()
