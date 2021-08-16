# Tree Distribution Scraper

### The web scraper for collecting tree genus distribution data.

The goal of this project is to implement the web scraper that collects tree species distribution data for given list of tree genera.
The distribution of tree species is collected from U.S. National Plant Germplasm System (https://npgsweb.ars-grin.gov/gringlobal/search).

## Getting Started

These instructions will get you a copy of the project up and running on 
your local machine for development and testing purposes.

### Prerequisites

* Python [3.6] - https://www.python.org/
* Anaconda - https://www.anaconda.com/

Detailed information about installation and configurations are provided at developers' site.

## Technology Stack

* Python [3.6]
* Scrapy
* Selenium

### Build

Step-by-step instructions for creating an environment [on Windows 10]:
* Navigate to project directory in Command Prompt (cmd).
* Use ``conda`` to create new environment with required dependencies.
  ```
  conda create --name <env> --file requirements.txt
  ```

### Run

Step-by-step instructions for running the scraper [on Windows 10]:
* Specify the list of genera in the ``trees.csv`` file.
* Start the data scraping using the following command:
  ```
  python main.py
  ```

All collected data should be saved in ``tree_distribution.csv`` file.
Any errors are saved to the ``output.log`` file.

Please notice that by default the application is running with the usage of 8 processes.
You can increase the number of processes that collects the data by changing ``constants.py`` file.

## Author

* **Michał Koziara** 
