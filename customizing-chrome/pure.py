from selenium import webdriver
from time import sleep
# webdriver.remote.webdriver.import_cdp()
import webbrowser

def main():
    driver = webdriver.Chrome()
    print(dir(driver))
    targets = driver.execute_cdp_cmd("Target.getTargets", {})
    print(targets)
    webs = webbrowser.get()
    print(type(webs))
    print(dir(webs))
    #print(webs.basename)
    #print(webs.args)

if __name__ == "__main__":
    main()