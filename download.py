from playwright.async_api import async_playwright
import os
import requests
from rich.console import Console
from rich.live import Live
from time import sleep

console = Console()

def download_video(video_url, save_path):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        with Live("[bold green]Downloading video...", refresh_per_second=4) as live:
            with open(save_path, "wb") as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        live.update("[bold green]Downloading video .")
                        sleep(0.2)
                        live.update("[bold green]Downloading video ..")
                        sleep(0.2)
                        live.update("[bold green]Downloading video ...")
                        sleep(0.2)
                        video_file.write(chunk)
    except Exception as e:
        console.print(f"[bold red]Failed to download video: {e}[/bold red]")


async def scrapvideofromurl():
    async with async_playwright() as p:
        chrome_path = "/usr/bin/google-chrome"

        browser = await p.chromium.launch(headless=True, executable_path=chrome_path)
        context = await browser.new_context()
        page = await context.new_page()

        video_counter = 1

        with open("twitchclips.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                console.print(f"[bold cyan]Processing URL: {line}[/bold cyan]")
                try:
                    await page.goto(line, timeout=30000)

                    await page.wait_for_selector("video[src]", timeout=20000)

                    video_locator = page.locator("video[src]")
                    video_src = await video_locator.get_attribute("src")

                    if video_src:
                        video_name = f"video{video_counter}.mp4"
                        save_path = os.path.join("downloaded_videos", video_name)
                        os.makedirs("downloaded_videos", exist_ok=True)

                        download_video(video_src, save_path)
                        video_counter += 1
                    else:
                        console.print("[bold red]Video URL not found.[/bold red]")
                except Exception as e:
                    console.print(f"[bold red]Error processing URL {line}: {e}[/bold red]")

        await browser.close()