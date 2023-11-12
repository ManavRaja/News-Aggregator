import scrapy

from datetime import datetime

from news_scraper.items import NewsArticle


class ReutersSpider(scrapy.Spider):
    name = "reuters"
    allowed_domains = ["www.reuters.com"]
    start_urls = ["https://www.reuters.com/world", "https://www.reuters.com/business", "https://www.reuters.com/markets",
                  "https://www.reuters.com/sustainability", "https://www.reuters.com/legal", "https://www.reuters.com/technology"]

    def parse(self, response):
        """
        Get links to all subcategory pages from each page in start_urls.
        Ex. https://www.reuters.com/legal has the subcategories "Government", "Legal Industry", "Litigation", "Transactional", "US Supreme Court"
            as of writing this comment.
        This functions gets the links to all of those subcategories and yields a generator with links to all of those subcategories and tells 
        scrapy to parse those links with the parse_articles() function.
        """
        sections = response.css(
            "button.button__secondary__18moI::attr(data-id)").getall()
        yield from response.follow_all(sections, callback=self.parse_articles)

    def parse_articles(self, response):
        """
        Gets information about each article on subcategory page.
        Information: title, link to article page, datetime that article was written, and link to article's image
        """
        news_article_titles = response.css("div.story-card div.media-story-card__body__3tRWy h3 a::text").getall()

        news_article_links = response.css("div.story-card div.media-story-card__placement-container__1R55- a::attr(href)").getall()

        news_article_written_datetimes = response.css("div.story-card div.media-story-card__body__3tRWy time::text").getall() # TODO: Convert from plaintext to datetime object

        news_article_image_link = response.css("div.story-card div.media-story-card__placement-container__1R55- img::attr(src)").getall()

        articles = []

        # Zip function puts all scraped attributes of an article into a dictionary which gets added to the articles list.
        for title, link, datetime_written, image_link in zip(news_article_titles, news_article_links, news_article_written_datetimes, news_article_image_link):
            article = {
                "title": title, "link": "https://www.reuters.com" + link, "datetime_written": datetime_written, "image_link": image_link}
            articles.append(article)

        # Makes an instance of NewsArticle() which is scrapy item created in ../items.py, populates the fields and yields each article item
        news_article = NewsArticle()
        for article in articles:
            news_article["title"] = article["title"]
            news_article["link"] = article["link"]
            news_article["website"] = ["Reuters", "https://www.reuters.com"]
            news_article["datetime_written"] = article["datetime_written"]
            news_article["image_link"] = article["image_link"]
            news_article["datetime_scraped"] = datetime.now()
            yield news_article
