<a name="readme-top"></a>

<div align="center">
  
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<h3 align="center">MT5Scraper V0.9.5</h3>

  <p align="center">
    Scraper to easily extract historical forex, stock, ect. prices from MetaTrader5 with Python 
    <br />
    <a href="https://github.com/XO30/MT5Scraper"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/XO30/MT5Scraper/blob/main/example.ipynb">View Demo</a>
    ·
    <a href="https://github.com/XO30/MT5Scraper/issues">Report Bug</a>
    ·
    <a href="https://github.com/XO30/MT5Scraper/issues">Request Feature</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

MT5Scraper is designed to help obtaining historical price data from MetaTrader5 and simplify the process. It is possible to list all available symbols as a tree with the MT5Scraper class. So it is very easy to retrieve and save data for the desired symbols.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started

To use the module some requirements must be met and some simple steps must be taken.


### Prerequisites

In order to work with the MT5Scraper class, it is necessary that MetaTrader 5 is already installed on the system. In addition, an account must be set up so that the queries can be made.


### Installation



MetaTrader5 provides a lot of binary wheels but only for w32 and w64. No Linux, no MacOS and no source code. Accordingly, as MT5Scraper requires MetaTrader5, the installation is only possible under Windows.

Install the module with pip
   ```sh
   pip3 install git+https://github.com/XO30/MT5Scraper
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Import Module
Import the class MT5Scraper from the library mt5_scraper
```py
from mt5_scraper import MT5Scraper
```


### Initialize Class
Make an instance of the class

In total, the following 3 parameters must be passed:
* login: login to your MT5 account
* server: server name of the account
* password: password to the account
```py
scraper = MT5Scraper(1234, 'SERVERNAME', 'PASSWORD')
print(scraper)
```


### Get the total number of symbols
With the method get_symbol_count you get the number of symbols the account has in total.
```py
scraper.get_symbol_count()
```


### Get all symbols
With the method get_symbols you get a list of all symbols. Additionally the whole structure is displayed as a tree.
```py
all_symbols = scraper.get_symbols()
```


### Get specific symbols
It is possible to pass the following parameters to the method get_symbols:
* symbol_path: path, to the desired symbols
* visualize: should the tree structure be output
```py
stocks_switzerland = scraper.get_symbols('Stocks/Switzerland/Software & IT Services', visualize=True)
```


# Get historical data
with the method get_historical_data you can download the historical prices of the desired symbols. The method has the following parameters:
* symbol_list: list containing the desired symbols
* timeframe: desired timeframe (D1, H1, etc.)
* start_date: prices from (Y, M, D, h, m, s)
* end_date: prices until (Y, M, D, h, m, s)
* save: True if dataframe should be saved else False
* save_path: folder Path to save the csv

In total there are 21 timeframes to choose: M1, M2, M3, M4, M5, M6, M10, M12, M15, M20, M30, H1, H2, H3, H4, H6, H8, H12, D1, W1, MN1
```py
data = scraper.get_historical_data(stocks_switzerland,
                                   'H1',
                                   (2022, 1, 1),
                                   (2023, 1, 11, 13, 0),
                                   save=True,
                                   save_path='stocks_switzerland_D1')
```
```py
data['TEMN.S']
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the Apache-2.0 license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Stefan Siegler: dev@siegler.one

Project Link: [https://github.com/XO30/MT5Scraper](https://github.com/XO30/MT5Scraper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/XO30/MT5Scraper.svg?style=for-the-badge
[contributors-url]: https://github.com/XO30/MT5Scraper/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/XO30/MT5Scraper.svg?style=for-the-badge
[forks-url]: https://github.com/XO30/MT5Scraper/network/members
[stars-shield]: https://img.shields.io/github/stars/XO30/MT5Scraper.svg?style=for-the-badge
[stars-url]: https://github.com/XO30/MT5Scraper/stargazers
[issues-shield]: https://img.shields.io/github/issues/XO30/MT5Scraper.svg?style=for-the-badge
[issues-url]: https://github.com/XO30/MT5Scraper/issues
[license-shield]: https://img.shields.io/github/license/XO30/MT5Scraper.svg?style=for-the-badge
[license-url]: https://github.com/XO30/MT5Scraper/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/stefan-siegler-04b116205