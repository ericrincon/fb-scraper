import argparse

from scraper import scraper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    scraper.scrape(args.username, args.password)

if __name__ == '__main__':
    main()