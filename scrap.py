from playwright.sync_api import sync_playwright
from download import scrapvideofromurl
# arena-breakout-infinite

def  askfortwitchcategory(textinput):
    url = "https://www.twitch.tv/directory/category/" + textinput + "/clips?range=24hr"
    scrapurlclipsfromtwitch(url)
    return url


def scrapurlclipsfromtwitch(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_timeout(5000)

        clip_links = page.locator("a[href*='/clip/']").all()
        extracted_links = list(set(["https://www.twitch.tv" + link.get_attribute("href") for link in clip_links]))

        with open("twitchclips.txt", "w") as f:
            for link in extracted_links:
                f.write(link + "\n") 

        scrapvideofromurl()
        browser.close()


