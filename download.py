from playwright.sync_api import sync_playwright
import os
import requests


def download_video(video_url, save_path):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        with open(save_path, "wb") as video_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  
                    video_file.write(chunk)
    except Exception as e:
        print(f"Failed to download video: {e}")


def scrapvideofromurl():
    with sync_playwright() as p:

        chrome_path = "/usr/bin/google-chrome"

        browser = p.chromium.launch(headless=False, executable_path=chrome_path)
        context = browser.new_context()
        page = context.new_page()

        video_counter = 1

        with open("twitchclips.txt", "r") as f:
            for line in f:
                line = line.strip()  
                if not line:
                    continue 

                print(f"Processing URL: {line}")
                try:
                    page.goto(line, timeout=30000)  

                    page.wait_for_selector("video[src]", timeout=20000)

                    video_locator = page.locator("video[src]")
                    video_src = video_locator.get_attribute("src")

                    if video_src:
                        
                        video_name = f"video{video_counter}.mp4"
                        save_path = os.path.join("downloaded_videos", video_name)
                        os.makedirs("downloaded_videos", exist_ok=True)
                        
                        download_video(video_src, save_path)
                        video_counter += 1

                    else:
                        print("Video URL not found.")
                except Exception as e:
                    print(f"Error processing URL {line}: {e}")

        browser.close()


if __name__ == "__main__":
    scrapvideofromurl()