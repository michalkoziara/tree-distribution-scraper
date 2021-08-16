import logging
import multiprocessing

import numpy as np
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from config import NUMBER_OF_PROCESSES
from driver_generator import DriverGenerator


def crawl(tasks):
    custom_settings = get_project_settings()
    custom_settings['LOG_LEVEL'] = logging.ERROR
    custom_settings['LOG_FILE'] = 'output.log'

    process = CrawlerProcess(custom_settings)
    driver_generator = DriverGenerator()

    def run_spider(_, index=0):
        if index < len(tasks):
            deferred = process.crawl('tree_spider', task=tasks[index], driver=driver_generator.driver)
            deferred.addCallback(run_spider, index + 1)
            return deferred

    run_spider(None)
    process.start()

    del driver_generator
    del process


def main():
    tasks = np.genfromtxt('trees.csv', dtype=str, delimiter=',', skip_header=1)

    with multiprocessing.Pool(NUMBER_OF_PROCESSES) as pool:
        pool.map(crawl, np.array_split(tasks, NUMBER_OF_PROCESSES))


if __name__ == '__main__':
    main()
