from playwright.sync_api import sync_playwright


def scrapvideofromurl():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        with open("twitchclips.txt", "r") as f:
            for line in f:
                line = line.strip()  
                if not line:
                    continue 

                print(f"Processing URL: {line}")
                page.goto(line)
                page.wait_for_timeout(5000)  
                
                try:
                    video_locator = page.locator("div.video-ref[data-a-target='video-ref'] video")
                    video_src = video_locator.get_attribute("src")
                    
                    if video_src:
                        print(f"Video URL found: {video_src}")
                        with open("twitchvideos.txt", "a") as output_file:
                            output_file.write(video_src + "\n")
                    else:
                        print("Video URL not found.")
                except Exception as e:
                    print(f"Error processing URL {line}: {e}")

        browser.close()


scrapvideofromurl()
