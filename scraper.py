from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
from utils import is_within_last_days
from config import DAYS_TO_FETCH

from config import (
    SESSION_FILE,
    HEADLESS,
    ACTION_DELAY,
    MAX_SCROLLS,
)

from models import Reel
from utils import convert_views

class InstagramScraper:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS
        )

        self.context = self.browser.new_context(
            storage_state=str(SESSION_FILE)
        )

        self.page = self.context.new_page()

        self.page.set_default_timeout(15000)

    def open_profile(self, username):
        
        self.current_username = username
        url = f"https://www.instagram.com/{username}/reels/"

        print()

        print("=" * 70)

        print(username)

        print("=" * 70)

        self.page.goto(
            url,
            wait_until="networkidle"
        )

        self.page.wait_for_timeout(
            ACTION_DELAY * 1000
        )

    def collect_visible_reels(self):

        reels = []

        cards = self.page.locator(
            "a[href*='/reel/']:visible"
        )

        total = cards.count()

        print(f"Visible : {total}")

        PINNED_REELS_TO_SKIP = 3

        for i in range(PINNED_REELS_TO_SKIP, total):

            try:

                card = cards.nth(i)

                href = card.get_attribute("href")

                if not href:
                    continue

                url = "https://www.instagram.com" + href

                # icon = card.locator(
                #     "svg[aria-label='View count icon']"
                # )
                icon = card.locator(
                        "svg[aria-label*='View'], svg[aria-label*='view']"
                    )

                if not icon.count():
                    continue

                views = (
                    icon
                    .locator("xpath=..")
                    .locator("xpath=following-sibling::span")
                    .inner_text()
                )

                reels.append(

                    Reel(

                        url=url,

                        views_text=views,

                        views=convert_views(views)

                    )

                )

            except Exception as e:

                print(e)

        return reels
    
    def collect_recent_reels(self):

        recent_reels = []
        seen_urls = set()

        scroll_count = 0

        while scroll_count < MAX_SCROLLS:

            scroll_count += 1

            print(f"\n========== Scroll #{scroll_count} ==========")

            visible_reels = self.collect_visible_reels()

            stop_scraping = False

            for reel in visible_reels:

                if reel.url in seen_urls:
                    continue

                seen_urls.add(reel.url)

                print(f"Checking: {reel.url}")

                try:
                    metadata = self.get_reel_metadata(reel.url)
                except Exception as e:
                    print(f"Failed to read metadata for {reel.url}: {e}")
                    continue

                posted_date = metadata["posted_date"]

                if posted_date is None:
                    continue

                reel.posted_date = posted_date
                reel.likes = metadata["likes"]
                reel.likes_text = metadata["likes_text"]
                print(f"Likes: {reel.likes_text} ({reel.likes})")

                print(f"Posted: {posted_date}")

                age = datetime.now(timezone.utc) - posted_date

                print(f"Age: {age.days} days")
                # ---------------------------

                if is_within_last_days(posted_date, DAYS_TO_FETCH):

                    recent_reels.append(reel)

                    print(f"✓ Added ({len(recent_reels)})")

                else:

                    print("Reached reels older than 7 days.")

                    stop_scraping = True

                    break

            if stop_scraping:
                break

            self.scroll_page()

        return recent_reels
    
    def scroll_page(self):

        self.page.keyboard.press("End")

        self.page.wait_for_timeout(1000)

        self.page.mouse.wheel(0,6000)

        self.page.wait_for_timeout(2000)
    
    def get_reel_metadata(self, reel_url):

        reel_page = self.context.new_page()

        try:

            reel_page.goto(
                reel_url,
                wait_until="networkidle"
            )

            reel_page.locator("time").first.wait_for(timeout=10000)

            datetime_str = (
                reel_page
                .locator("time")
                .first
                .get_attribute("datetime")
            )

            posted_date = None

            if datetime_str:

                posted_date = datetime.fromisoformat(
                    datetime_str.replace("Z", "+00:00")
                )

            # -------------------------
            # Likes
            # -------------------------

            likes = None
            likes_text = None

            try:

                buttons = reel_page.locator("section span[role='button']")

                if buttons.count() >= 1:

                    likes_text = buttons.nth(0).inner_text().strip()

                    likes = convert_views(likes_text)

                    print(f"Likes: {likes_text} ({likes})")

            except Exception as e:

                print(f"Couldn't extract likes: {e}")

            return {
                "posted_date": posted_date,
                "likes": likes,
                "likes_text": likes_text
            }

        finally:
            reel_page.close()
    
    def print_summary(self, reels):

        print()

        print("=" * 70)

        print(f"Total Reels : {len(reels)}")

        print("=" * 70)

        for reel in reels:

            print(

                reel.views,

                reel.views_text,

                reel.url

            )

    def stop(self):

        self.browser.close()

        self.playwright.stop()
        