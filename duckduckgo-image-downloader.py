from selenium import webdriver
import requests
import time
import base64


def images(query):
    browser = webdriver.Chrome('./chromedriver.exe')
    browser.get("https://duckduckgo.com/?q=" + query +"&iax=images&ia=images")
    infiniteScroll(browser, 1)
    imgArr = browser.find_elements_by_css_selector(".tile--img__img.js-lazyload")

    for index, img in enumerate(imgArr):
        print("Downloading " + str(index + 1) + "/" + str(len(imgArr)))
        src = img.get_attribute("src")
        name = nameGenerator(index + 1)

        if "base64" in src[0:50]:
            
            pass
        else:
            downloadWithProgress(src, name)

    browser.quit()


def infiniteScroll(browser, loadMoreMax):
    SCROLL_PAUSE_TIME = 1
    counter = 0

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            if loadMoreMax == counter:
                break
            else:
                try:
                    browser.find_element_by_css_selector(".mye4qd").click()
                    counter = counter + 1
                except Exception as ex:
                    print(ex)
                    break
        last_height = new_height


def nameGenerator(index):
    return "./img/img" + str(index) + ".jpg"



def downloadWithProgress(link, name):
    with open(name, "wb") as f:
        print("Downloading %s" % name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                print("\r\n[%s%s]" % ('=' * done, ' ' * (50-done)), flush=True)


def saveFromBase64(base64Data, name):
    open(name, 'w').write(base64.decodestring(base64Data))


def main():
    images("")


main()
