from playwright.async_api import async_playwright
from download import scrapvideofromurl


async def askfortwitchcategory(textinput):
    url = f"https://www.twitch.tv/directory/category/{textinput}/clips?range=24hr"
    await scrapurlclipsfromtwitch(url)
    return url


async def scrapurlclipsfromtwitch(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        await page.wait_for_timeout(5000)

        clip_links = await page.locator("a[href*='/clip/']").all()
        extracted_links = list(set([f"https://www.twitch.tv{await link.get_attribute('href')}" for link in clip_links]))

        with open("twitchclips.txt", "w") as f:
            for link in extracted_links:
                f.write(link + "\n")

        await browser.close()
        await scrapvideofromurl()
