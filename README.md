bitcoin_search.py is Python3 textbased program to make searches to bitcoin data on CoinGecko's public API. It is mine (Vesa Lukka, VesaL@iki.fi) reply to Vincit Rising Star Pre-assignment (see: https://vincit.fi/risingstar/ ).

Environment:
You need to have python3 installed (made with Python 3.9.6 64-bit)

Option1:
  1. Run with python3. ie.: python3 bitcoin_search.py
  2. program then asks to dates to make bitcoin searches between then
  3. program prints results to terminal where You started program

Option2:
  1. Add two dates to terminal as arguments ie.: python3 bitcoin_search.py 2020-03-01 2021-08-01
dates can be given in format yyyy-mm-dd , yyyy.mm.dd , dd-mm-yyyy or dd.mm.yyyy
If only one date is given program uses Option1. If one of the dates is invalid (like 2021-02-31)
program uses Option1.
  2. program prints results to terminal where You started program
  
 Since coin data is available only since 2013-04-28, dates before that are invalid. Allso future dates are invalid.
