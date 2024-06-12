from goose3 import Goose, Article
import concurrent.futures
import requests.adapters
import pandas as pd


def scrape_urls(urls_to_scrape, n_threads=32) -> pd.DataFrame:
    """
    Scrapes `urls_to_scrape` concurrently with Goose using `n_threads`.

    Returns a Pandas dataframe
    """

    with Goose() as g:
        session = requests.Session()
        session.headers["User-agent"] = g.config.browser_user_agent
        # increase pool size to enable more concurrent requests
        adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        if g.fetcher is not None:
            g.fetcher._connection = session

        def scrape_url(url):
            try:
                goose_article = g.extract(url=url)
            except Exception as e:
                print(f"Failed to scrape: {e}")
                goose_article = {"exception": str(e)}
            return goose_article

        with concurrent.futures.ThreadPoolExecutor(n_threads) as executor:
            scraping_results = list(executor.map(scrape_url, urls_to_scrape))

    scraped_articles = []
    for url, goose_scrape in zip(urls_to_scrape, scraping_results):
        article_object = {
            "url": url,
            "exception": None,
            "scrape_time": pd.Timestamp.utcnow(),
            "timestamp": None,
            "publish_datetime_utc": None,
            "title": None,
            "cleaned_text": None,
            "authors": None,
            "infos": None,
        }
        if type(goose_scrape) is dict and "exception" in goose_scrape:
            article_object["exception"] = goose_scrape["exception"]
        elif type(goose_scrape) is Article:
            if goose_scrape.publish_datetime_utc is not None:
                article_object["publish_datetime_utc"] = str(
                    pd.Timestamp(goose_scrape.publish_datetime_utc)
                )

            article_object["cleaned_text"] = goose_scrape.cleaned_text
            article_object["title"] = goose_scrape.title
            article_object["authors"] = goose_scrape.authors
            article_object["infos"] = goose_scrape.infos

        scraped_articles.append(article_object)

    return pd.DataFrame(scraped_articles)
