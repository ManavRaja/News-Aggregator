import scrapy

from datetime import datetime

from news_scraper.items import NewsArticle


class APNewsSpider(scrapy.Spider):
    name = "apnews"
    allowed_domains = ["apnews.com"]
    start_urls = ["https://apnews.com/world-news",
                  "https://apnews.com/politics", "https://apnews.com/business", "https://apnews.com/us-news", "https://apnews.com/science"]

    def parse(self, response):
        """
        Get links to all subcategory pages from each page in start_urls.
        Ex. "https://apnews.com/business" has the subcategories "Inflation", "Financial Markets", "Business Highlights", "Financial Wellness"
            at the top of the webpage as of writing this comment and "Financial Markets", "Financial Wellness", "Economy", "Tech" in the middle
            of the page.
        This functions gets the links to all of those subcategories and yields a generator with links to all of those subcategories and tells 
        scrapy to parse those links with the parse_articles() function.
        """
        sections_at_top_of_page = response.css(
            "a.AnClick-SectionNav::attr(href)").getall()

        section_in_middle_of_page = response.css(
            "div.PageList-header-title a.Link::attr(href)").getall()

        all_sections = list(
            set(sections_at_top_of_page + section_in_middle_of_page))

        for section in all_sections:
            yield scrapy.Request(url=section, callback=self.parse_articles)

    def parse_articles(self, response):
        """
        Gets information about each article on subcategory page.
        Information: title, link to article page, and link to article's image
        TODO: Figure out a way to get the datetimes for articles since it isn't shown on the subcategory pages.
        """
        news_article_titles = response.css(
            "div.PageList-items-item div.PagePromo div.PagePromo-media a.Link::attr(aria-label)").getall()

        news_article_links = response.css(
            "div.PageList-items-item div.PagePromo div.PagePromo-media a.Link::attr(href)").getall()

        news_article_image_link = response.css(
            "div.PageList-items-item div.PagePromo div.PagePromo-media a.Link picture img::attr(src)").getall()

        articles = []

        # Zip function puts all scraped attributes of an article into a dictionary which gets added to the articles list.
        for title, link, image_link in zip(news_article_titles, news_article_links, news_article_image_link):
            article = {
                "title": title, "link": link, "image_link": image_link}
            articles.append(article)

        # Makes an instance of NewsArticle() which is scrapy item created in ../items.py, populates the fields and yields each article item
        news_article = NewsArticle()
        for article in articles:
            news_article["title"] = article["title"]
            news_article["link"] = article["link"]
            news_article["website"] = ["AP News", "https://apnews.com"]
            news_article["image_link"] = article["image_link"]
            news_article["datetime_scraped"] = datetime.now()
            yield news_article
