from scraper import InstagramScraper
from excel import ExcelReport
from config import ACCOUNTS


def main():

    scraper = InstagramScraper()
    excel = ExcelReport()

    try:

        scraper.start()

        for account in ACCOUNTS:

            scraper.open_profile(account)

            reels = scraper.collect_recent_reels()

            scraper.print_summary(reels)

            excel.add_account_sheet(
                account_name=account,
                reels=reels
            )

        report_path = excel.save()

        print("\n" + "=" * 80)
        print("✅ Scraping Completed Successfully!")
        print(f"📄 Excel Report: {report_path}")
        print("=" * 80)

    except Exception as e:

        print("\n" + "=" * 80)
        print("❌ ERROR OCCURRED")
        print(e)
        print("=" * 80)

    finally:

        scraper.stop()


if __name__ == "__main__":
    main()