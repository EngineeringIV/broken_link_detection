from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'kb'
        ]
    )
except SystemExit:
    pass