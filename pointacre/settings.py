# Scrapy settings for pointacre project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pointacre'

SPIDER_MODULES = ['pointacre.spiders']
NEWSPIDER_MODULE = 'pointacre.spiders'

FEED_URI='export.csv'
FEED_FORMAT='csv'

ITEM_PIPELINES={
    'pointacre.pipelines.PointacrePipeline':100
}
LOG_ENABLED=True
LOG_LEVEL='INFO'
USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'
COOKIES_ENABLED=False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pointacre (+http://www.yourdomain.com)'
