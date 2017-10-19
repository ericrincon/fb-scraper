import argparse

from fb_scraper import scraper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email')
    parser.add_argument('--password')
    parser.add_argument('--start-page')

    args = parser.parse_args()

    scraper.start(args.email, args.password, start_page=args.start_page)

if __name__ == '__main__':
    main()