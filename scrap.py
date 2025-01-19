# arena-breakout-infinite
from playwright.sync_api import sync_playwright

twitchname = "arena-breakout-infinite"

def askfortwitchcategory():
    # print("Please enter the category you want to scrap: ")
    # twitchname = input()
    url = "https://www.twitch.tv/directory/category/" + twitchname + "/clips?range=24hr"
    
    return url


def scrapurlclipsfromtwitch():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(askfortwitchcategory())

        page.wait_for_timeout(5000)

        clip_links = page.locator("a[href*='/clip/']").all()
        extracted_links = list(set(["https://www.twitch.tv" + link.get_attribute("href") for link in clip_links]))

        with open("twitchclips.txt", "w") as f:
            for link in extracted_links:
                f.write(link + "\n") 

        browser.close()

scrapurlclipsfromtwitch()



