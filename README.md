# broken_link_detection
 A Python-based ScraPy scrawler to detect broken links in Lenovo's knowledge management base
 
 ## Motivation
 Lenovo Knowledge Management base is an important piece of Lenovo support platform. It hosts a large number of self-help documents to address different issues related to a variety of products. However, customers are complaining that there are links within many documents that lead to a "Page Not Found" result. These documents are considered documents with broken links. The current broken link identification process is consist of receiving alerts of all possible broken links from Adobe Analytics and manually verify every single broken link, which is really time-consuming and inefficient. 
 
 The project leverages the Scrapy web crawler functionalities to crawl through all the Adobe Analytics alerted broken links, determine if they indeed lead to "Page Not Found", and generate a broken link report with document IDs, document title, document country codes, document languages, document links, broken link titles, and broken link URLs

## File Structure
- Python files
  - kb_spider.py (in kb/kb/spiders): the main function that defines the spider structure and logics
  - settings.py (in kb/kb): the script to configure middleware settings for splash
  - runner.py (in kb/kb): the script to run the crawler

- Data files (In "Data" folder)
  - Report_0125.xlsx: the raw input with all the alerted potential broken link documents from Adobe Analytics
 
 ## Techniques and Overall Design Logic
The crawler is based on ScraPy. Since the Lenovo support website uses JavaScript and is considered to be dynamically loaded, I also used Splash for Scrapy and Javascript integration. 

For the broken link identification logic, the crawler will first try to find the alerted link name in the document. If found, then it would follow the link and if "Page Not Found" is in the header of the resulting page. If so, it would write down the information to the output report. If no matches is found, it would try to crawl all the available URL in the document and record any that leads to "Page Not Found"

## Installation
- Install Docker
- Install all requirements in the requirements.txt file
- Run the crawler with command "docker run -it -p 8050:8050 --rm scrapinghub/splash"

## Analysis Results
With this broken link detection tool, the broken link identification process is streamlined. This helps the knowledge management team to focus more on eliminating broken links. I established a broken link removal weekly cadence for both English and non-English documents and helped to reduce broken links reported by 67% in 6 months.

