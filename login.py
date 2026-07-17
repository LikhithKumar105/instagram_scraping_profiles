from playwright.sync_api import sync_playwright
from config import SESSION_FILE


def main():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context()

        page = context.new_page()

        page.goto("https://www.instagram.com/")

        print("=" * 60)
        print("Login to Instagram.")
        print("After Instagram Home loads, press ENTER.")
        print("=" * 60)

        input()

        context.storage_state(path=str(SESSION_FILE))

        print()

        print("Session saved successfully.")

        print(SESSION_FILE)

        browser.close()


if __name__ == "__main__":
    main()