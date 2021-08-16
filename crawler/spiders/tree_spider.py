import scrapy
from scrapy.http import HtmlResponse
from scrapy.http import TextResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import NPGSWEB_URL
from config import OUTPUT_FILE_FORMAT
from config import OUTPUT_FILE_NAME


class TreeSpider(scrapy.Spider):
    name = "tree_spider"
    custom_settings = {
        "FEEDS": {
            OUTPUT_FILE_NAME + '.' + OUTPUT_FILE_FORMAT: {
                'format': OUTPUT_FILE_FORMAT,
            },
        }
    }

    def __init__(self, task, driver):
        scrapy.Spider.__init__(self)
        self.genus = task
        self.driver = driver

    def start_requests(self):
        yield scrapy.Request(url=NPGSWEB_URL, callback=self.parse)

    def parse(self, response, **kwargs):
        # Start Selenium task to fill genus form.
        self.driver.get(NPGSWEB_URL)
        accepted_names_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='cphBody_cbAccept']"))
        )

        if not accepted_names_button.is_selected():
            accepted_names_button.click()

        genus_name_field = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='cphBody_txtGenus']"))
        )

        genus_name_field.send_keys(self.genus)

        search_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='cphBody_btnSearch']"))
        )
        search_button.click()

        response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        yield from self.parse_genus(response)

    def parse_genus(self, response):
        # Start Scrapy task to get the list of species.
        next_page = response.xpath("//a[@id='MainContent_hlSpecieslist']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_list)

    def parse_list(self, response):
        # Start Selenium task to setup list filters.
        self.driver.get(response.url)
        accepted_names_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@value='accepted']"))
        )

        if not accepted_names_button.is_selected():
            accepted_names_button.click()

        exclude_infraspecific_names_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='chkNoIS']"))
        )

        if not exclude_infraspecific_names_button.is_selected():
            exclude_infraspecific_names_button.click()

        rows_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@class='dt-button buttons-collection buttons-page-length']"))
        )
        rows_button.click()

        all_rows_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@class='dt-button button-page-length']//span[text()='Show all']"))
        )
        all_rows_button.click()

        # Start Scrapy task to open species page.
        response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        yield from response.follow_all(xpath="//table[@id='MainContent_gvSpecies']//td[1]//a",
                                       callback=self.parse_taxonomy)

    def parse_taxonomy(self, response):
        # Start Scrapy task to get current species.
        species = response.xpath("//h4[@class='title']//i//text()").get()

        # Start Selenium task to setup the distribution tab.
        self.driver.get(response.url)
        distro_tab = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@id='distrotab']"))
        )
        distro_tab.click()

        distro_export_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='MainContent_ctrlDistribution_export']"))
        )
        distro_export_button.click()

        rows_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@class='dt-button buttons-collection buttons-page-length']"))
        )
        rows_button.click()

        all_rows_button = WebDriverWait(self.driver, 4).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button//span[text()='All']"))
        )
        all_rows_button.click()

        # Start Scrapy task to get species regions.
        for row in response.xpath("//table[@id='MainContent_ctrlDistribution_ctrlExport_gvResults']//tr"):
            region = {
                'genus': self.genus,
                'species': species,
                'status': row.xpath(".//td[2]//text()").get(),
                'continent': row.xpath(".//td[3]//text()").get(),
                'subcontintent': row.xpath(".//td[4]//text()").get(),
                'country': row.xpath(".//td[5]//text()").get(),
                'state': row.xpath(".//td[6]//text()").get(),
                'note': row.xpath(".//td[7]//text()").get(),
            }

            yield region
