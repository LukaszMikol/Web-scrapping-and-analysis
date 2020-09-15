import scrapy
from scrapy import Selector
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time


class TableSpider(scrapy.Spider):
    name = 'table'
    allowed_domains = ['file:///home/lukas/course/scrapy/premierLeague_static/index.html']
    start_urls = ['file:///home/lukas/course/scrapy/premierLeague_static/index.html']

    def __init__(self):
        ''' Saving file  '''
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        driver.set_window_size(1600, 900)
        driver.get('https://www.premierleague.com/tables/')

        # close advert
        driver.find_element_by_xpath("//a[@id='advertClose']").click()
        time.sleep(5)

        # scroll down
        driver.execute_script("window.scrollTo(0, 200)")
        time.sleep(1)
        # dropdown ul element
        driver.find_elements_by_css_selector(
            '#mainContent > div.tabbedContent > div.mainTableTab.active > div:nth-child(1) > section > div:nth-child(3) > div.current')[
            0].click()

        time.sleep(2)

        # click to season 2019/2020
        driver.find_elements_by_css_selector(
            '#mainContent > div.tabbedContent > div.mainTableTab.active > div:nth-child(1) > section > div.dropDown.active.open > ul > li:nth-child(3)')[
            0].click()
        time.sleep(5)

        self.html = driver.page_source

        with(open('index.html', 'w')) as f:
            f.write(self.html)

        driver.close()

    def parse(self, response):
        rows = response.xpath('//*[@id="mainContent"]/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr[position() mod 2 = 1]')

        for row in rows:
            yield {
                'Position': row.xpath('.//td[2]/span[1]/text()').get(),
                'Club': row.xpath('.//td[3]/a/span[2]/text()').get(),
                'Played': row.xpath('.//td[4]/text()').get(),
                'Won': row.xpath('.//td[5]/text()').get(),
                'Drawn': row.xpath('.//td[6]/text()').get(),
                'Lost': row.xpath('.//td[7]/text()').get(),
                'GF': row.xpath('.//td[8]/text()').get(),
                'GA': row.xpath('.//td[9]/text()').get(),
                'GD': row.xpath('.//td[10]/text()').get(),
                'Points': row.xpath('.//td[11]/text()').get(),
            }

            # table['Position'] = row.xpath('.//td[2]/span[1]/text()').get()
            # table['Club'] = row.xpath('.//td[3]/a/span[2]/text()').get()
            # table['Played'] = row.xpath('.//td[4]/text()').get()
            # table['Won'] = row.xpath('.//td[5]/text()').get()
            # table['Drawn'] = row.xpath('.//td[6]/text()').get()
            # table['Lost'] = row.xpath('.//td[7]/text()').get()
            # table['GF'] = row.xpath('.//td[8]/text()').get()
            # table['GA'] = row.xpath('.//td[9]/text()').get()
            # table['GD'] = row.xpath('.//td[10]/text()').get()
            # table['Points'] = row.xpath('.//td[11]/text()').get()
            #
            # yield table

