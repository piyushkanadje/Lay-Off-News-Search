import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import argparse
# from IPython.display import clear_output 
class RedditLayoffSpider(scrapy.Spider):
    name = "reddit_layoff"


    def __init__(self, count, max_pages,next_page,start_url):
        self.count=int(count)
        self.max_pages=max_pages
        self.next_page=next_page
        self.start_urls=[start_url]
   

    def parse(self, response):
       
        for post in response.css('div.search-result.search-result-link.has-thumbnail.has-linkflair'):
            print("p",post.css('span[class=search-time] time::attr(datetime)').extract_first())
            yield {
                'title': post.css('a.search-title.may-blank::text').get(),
                'date': post.css('span[class=search-time] time::attr(datetime)').extract_first().split("T")[0],
                'description': post.css('a.search-title.may-blank::text').get(),
                'url':post.css("div[class=search-result-meta] a::attr(href)").extract_first()
            }
        next_selector = response.xpath('//span[@class="nextprev"]/a/@href')
        # clear_output()
        for url in next_selector.extract():


            yield scrapy.Request(url, callback=self.parse)

class BloombergLayoffCrawlerSpider(scrapy.Spider):
    name = "bloomberg_layoff_crawler_spider"
    # query="https://www.bloomberg.com/search?query=layoffs"
    # start_urls = [
    #     'https://www.bloomberg.com/search?query=layoffs',
    #    ]
    download_delay=1.5

    def __init__(self, count, max_pages,next_page,start_url):
        self.count=int(count)
        self.max_pages=max_pages
        self.next_page=next_page
        self.start_urls=[start_url]
        self.query=start_url


    def parse(self, response):

        # print(response)
        for post in response.css("div.storyItem__aaf871c1c5"):
            yield {
                'title': post.css("a.headline__3a97424275::text").get(),
                'date': post.css("div.publishedAt__dc9dff8db4::text").get(),
               
                'description': post.css("a.summary__a759320e4a::text").get(),
                'url':post.css("div[class=storyItem__aaf871c1c5] a::attr(href)").extract_first()
            }

        # data = json.loads(response.body)
        # clear_output()
        if self.count<200:
          # next_page = data['page'] + 1 
            self.next_page+=1
            self.count+=1
            yield scrapy.Request(self.query +"&page=" +str(self.next_page)+"&sort=time:desc")


        # next_page = response.css("a.next-page::attr(href)").get()
        # for a in response.css('button.button__f6b7ccfb8d secondary__ed561f3e09'):
        #     yield response.follow(a, callback=self.parse)
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

# Run the spider
class TCLayoffCrawlerSpider(scrapy.Spider):
    name = "tc_layoff_crawler_spider"
    # query="https://search.techcrunch.com/search;_ylt=AwrgMPUiF.tjbDIAMM2nBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?p=layoffs&fr=techcrunch&b=1&pz=10&bct=0&xargs=0"
    # start_urls = [
    #     "https://search.techcrunch.com/search;_ylt=AwrgMPUiF.tjbDIAMM2nBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?p=layoffs&fr=techcrunch&b=1&pz=10&bct=0&xargs=0",
    #   ]
    download_delay=1.5
    # count=1
    # next_page=1
    def __init__(self, count, max_pages,next_page,start_url):
        self.count=int(count)
        self.max_pages=max_pages
        self.next_page=next_page
        self.start_urls=[start_url]
        self.query=start_url


    def parse(self, response):

        # print(response)
        for post in response.css("div.d-tc"):
            yield {
                'title': post.css("a.fz-20.lh-22.fw-b::text").get(),
                'date': post.css("span.pl-15.bl-1-666::text").get(),
              
                'description': post.css("p.fz-14.lh-20.c-777::text").get(),
                'url': post.css("div[class=d-tc] a::attr(href)").extract_first()
            }

        # data = json.loads(response.body)
        # clear_output()
        if self.count<18:
          # next_page = data['page'] + 1 
            self.next_page+=10
            self.count+=1
            self.query=f"https://search.techcrunch.com/search;_ylt=AwrgMPUiF.tjbDIAMM2nBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?p=layoffs&fr=techcrunch&b={self.next_page}&pz=10&bct=0&xargs=0"
            print(self.query)
            yield scrapy.Request(self.query)
class NYTLayoffCrawlerSpider(scrapy.Spider):
    name = "nyt_layoff_crawler_spider"
    # query="https://www.nytimes.com/search?query=layoffs"
    # start_urls = [
    #     "https://www.nytimes.com/search?query=layoffs",
    #    ]
    download_delay=1.5
    def __init__(self, count, max_pages,next_page,start_url):
        self.count=int(count)
        self.max_pages=max_pages
        self.next_page=next_page
        self.start_urls=[start_url]
        self.query=start_url


    def parse(self, response):

        # print(response)
        
        for post in response.css("li.css-1l4w6pd"):
            print("d ",post.css("li[class=css-1l4w6pd] span::text").extract_first())#post.xpath('/span[@class="css-17ubb9w"]').extract_first())
            #if post.css("span[class=css-e1lvw9] a::attr(href)").extract_first():
            date=post.css("div[class=css-e1lvw9] a::attr(href)").extract_first().split('/')
            # clear_output()
            yield {
                'title': post.css("h4.css-2fgx4k::text").get(),
                'date': date[1]+"-"+date[2]+"-"+date[3],#post.css("li[class=css-1l4w6pd] span::text").extract_first(),

                'description': post.css("p.css-16nhkrn::text").get(),
                'url':"www.nytimes.com"+ post.css("div[class=css-e1lvw9] a::attr(href)").extract_first()
            }

        # data = json.loads(response.body)
        # if self.count<8:
        #   # next_page = data['page'] + 1 
        #   self.next_page+=10
          
        #   self.count+=1
        #   self.query=f"https://search.techcrunch.com/search;_ylt=AwrgMPUiF.tjbDIAMM2nBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?p=layoffs&fr=techcrunch&b={self.next_page}&pz=10&bct=0&xargs=0"
        #   print(self.query)
        #   yield scrapy.Request(self.query)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ct", "--count", help = "count")
    parser.add_argument("-mp", "--maxpages", help = "max pages")
    parser.add_argument("-np", "--nextpage", help = "next page")
    parser.add_argument("-o", "--output", help = "output filename")
    parser.add_argument("-f", "--format", help = "output file format")
    args = parser.parse_args()
    mp= args.maxpages if args.maxpages else 1000
    ct = args.count if args.count else 0
    np=args.nextpage if args.nextpage else 1
    of= args.output if args.output else '/gdrive/MyDrive/IR/rdbtcnyt.json'
    format=args.format if args.format else 'json'
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        # 'FEED_FORMAT': 'csv',
        'FEED_FORMAT': format,
        'FEED_URI': of,
        # 'FEED_URI':'quotes.csv'
       

    })
    

    
    process.crawl(BloombergLayoffCrawlerSpider,  count=ct,
        max_pages=mp,
        next_page=np, start_url="https://www.bloomberg.com/search?query=layoffs")
    process.crawl(RedditLayoffSpider,  count=ct,
        max_pages=mp,
        next_page=np, start_url="https://old.reddit.com/search?q=layoffs")
    process.crawl(TCLayoffCrawlerSpider,  count=ct,
        max_pages=mp,
        next_page=np, start_url="https://search.techcrunch.com/search;_ylt=AwrgMPUiF.tjbDIAMM2nBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?p=layoffs&fr=techcrunch&b=1&pz=10&bct=0&xargs=0")
    process.crawl(NYTLayoffCrawlerSpider,  count=ct,
        max_pages=mp,
        next_page=np,start_url="https://www.nytimes.com/search?query=layoffs")
    
    process.start()

if __name__ == '__main__':
    main()
