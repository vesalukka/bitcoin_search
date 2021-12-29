from json import JSONDecoder
from datetime import datetime, timedelta
from dateutil import tz
import sys
from urllib.request import urlopen

def date_ui(text: str):
    result = None
    while result == None:
        help =""
        while not help.isnumeric():
            print(text)
            help = input("year or enter to exit program: ")
            if help == "":
                sys.exit(0)
        s_year = int(help)
        help =""
        while not help.isnumeric():
            help = input("month (1-12): ")
        s_month = int(help)
        help =""
        while not help.isnumeric():
            help = input("day[1-31]: ")
        s_day = int(help)
        try:
            result = datetime(s_year, s_month, s_day, 0, 0, 0, 0, tz.tzutc())
        except ValueError:
            print(f"Date was not possible. Try again.")
            result = None
    return result

def ask_dates():
    start = date_ui(" _First give start date (later than 2013-04-27)_ ")
    end = date_ui("Then give end date: ")
    return start, end

def coin_gecko_search(start: datetime, end: datetime):
    end = end + timedelta(hours=1)

    # if dayrange is 90 days or more, everything fine and using that
    if end.timestamp() - start.timestamp() > 90*24*60*60:
        start_seconds = int(start.timestamp())
        end_seconds = int(end.timestamp()) 

    # if dayrange is less than 90 days, still using 90 days
    # to get daily values (not hourly), from start day
    elif datetime.now().timestamp() - start.timestamp() > 90*24*60*60:
        start_seconds = int(start.timestamp()) 
        end_seconds = int(start.timestamp())+ 90*24*60*60 + 60*60

    # if dayrange is less than 90 days, still using 90 days
    # this time 90 days before from end day (becouse 90 days from start day is in the future)
    # "that's heavy, doc"
    else: 
        end_seconds = int(datetime.now().timestamp())
        start_seconds = end_seconds - 91*24*60*60

    # url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=eur&from=1577836800&to=1609376400"
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=eur&from={start_seconds}&to={end_seconds}"
    print(f"Using url to get data over internet:")
    print(f"'{url}'")
    data_from_request = urlopen(url)
    json_data = JSONDecoder().decode(str(data_from_request.read(), 'utf8'))
   
    prices_data= json_data['prices']
    total_volumes_data = json_data["total_volumes"]
    prices = []
    total_volumes = []

    for price in prices_data:
        # in this if statement using original start and end times, so unusefull search results are filtered out
        if  price[0] /1000 - start.timestamp() + 60*60 > 0 and end.timestamp() - price[0] /1000 > 0:
            prices.append( (datetime.fromtimestamp(price[0] /1000, tz.tzutc()), price[1] ) )

    for volume_day in total_volumes_data:
        # in this if statement using original start and end times, so unusefull search results are filtered out
        if  volume_day[0] /1000 - start.timestamp() + 60*60 > 0 and end.timestamp() - volume_day[0] /1000 > 0:
            total_volumes.append( (datetime.fromtimestamp(volume_day[0] /1000, tz.tzutc()), volume_day[1]))

    
    print("Coin data succesfully fetched and parsed.")
    print()
    return prices, total_volumes


def finding_bear_trend(prices: list):
    best_start = prices[0]
    best_end = prices[0]
    start_day = prices[0]
    end_day = None
    for i in range(1, len(prices)):
        if prices[i][1] < prices[i-1][1]:
            end_day = prices[i]
            if end_day[0] - start_day[0] > best_end[0] - best_start[0]:
                best_start = start_day
                best_end = end_day
        else:
            start_day = prices[i]
    return best_start, best_end

def highest_volume(total_volumes: list):
    def volume_key(one: tuple):
        return one[1]
    return sorted(total_volumes, key=volume_key, reverse=True)[0]

def find_buy_sell(prices: list):
    price_diff = 0
    l_best= None
    h_best = None
    for i in range(len(prices)-1):
        for j in range(i+1, len(prices)):
            if prices[j][1]-prices[i][1] > price_diff:
                price_diff = prices[j][1]-prices[i][1]
                l_best = prices[i]
                h_best = prices[j]
    return l_best, h_best

def argumentParsing():
    start = None
    end = None
    if len(sys.argv) > 0:
        for argument in sys.argv:
            if argument[0].isnumeric():
                if argument.count("-") > 1:
                    parts = argument.split("-")
                elif argument.count(".") > 1:
                    parts = argument.split(".")
                if start == None:
                    try : 
                        start = datetime(int(parts[0]), int(parts[1]), int(parts[2]), 0,0,0,0, tz.tzutc())
                    except ValueError:
                        try:
                            start = datetime(int(parts[2]), int(parts[1]), int(parts[0]), 0,0,0,0, tz.tzutc())
                        except ValueError:
                            start = None
                else:
                    try : 
                        end = datetime(int(parts[0]), int(parts[1]), int(parts[2]), 0,0,0,0, tz.tzutc())
                    except ValueError:
                        try:
                            end = datetime(int(parts[2]), int(parts[1]), int(parts[0]), 0,0,0,0, tz.tzutc())
                        except ValueError:
                            end = None
                    if end != None:
                        return start, end
    return start, end

def euros_to_string(originaleuros: float):
    euros = originaleuros
    volume_euros_string = ""

    if euros > 1000000000:
        help = euros // 1000000000
        volume_euros_string += str(help)[0:-2] + " "
        euros = euros - help * 1000000000
    
    if euros > 1000000:
        help = euros // 1000000
        if volume_euros_string != "":
            if help < 10:
                volume_euros_string += "00"
            elif help < 100:
                volume_euros_string += "0"
        volume_euros_string += str(help)[0:-2] + " "
        euros = euros - help * 1000000
    
    if euros > 1000:
        help = euros // 1000
        if volume_euros_string != "":
            if help < 10:
                volume_euros_string += "00"
            elif help < 100:
                volume_euros_string += "0"
        volume_euros_string += str(help)[0:-2] + " "
        euros = euros - help * 1000

    
    help = euros // 1
    if volume_euros_string != "":
        if help < 10:
            volume_euros_string += "00"
        elif help < 100:
            volume_euros_string += "0"
    volume_euros_string += str(help)[0:-2]

    return volume_euros_string

def main():
    print("Welcome to Scrooge McDuck's Bitcoin search by Vesa Lukka (VesaL@iki.fi).")
    start, end  = argumentParsing()
    if start == None or end == None:
        start, end = ask_dates()
    elif end < start:
        v = end
        end = start
        start = v
    start_string = start.strftime("%Y-%m-%d")
    end_string = end.strftime("%Y-%m-%d")

    # bitcoin history starts 2013-04-28 at coin gecko
    start_line = datetime.fromtimestamp(1367107200, tz.tzutc())
    start_line_string = start_line.strftime("%Y-%m-%d")
    if start.timestamp() - start_line.timestamp() < 0 or end.timestamp() - start_line.timestamp() < 0:
        
        print(f"Requested date range starting from {start_string} and ending to {end_string}, but coin data available only later than {start_line_string}.")
        print(f"Make new request with starting date later than {start_line_string}.")
        return 
    if datetime.now().timestamp() - start.timestamp() < 0 or datetime.now().timestamp() -end.timestamp() < 0:
        print(f"Date range is in the future.")
        print(f"At the moment this program can make only data searches from past.")
        return

    print("Using Day range:")
    print(f"{start_string } - {end_string }")
    print()
    print("Starting coin data search:")
    prices, total_volumes = coin_gecko_search(start, end)

    # A How many days is the longest bearish (downward) trend within a given date range?
    print("A.")
    print("Q: How many days is the longest bearish (downward) trend within a given date range?")

    start_b, end_b = finding_bear_trend(prices)
    
    if end_b[0]-start_b[0] < timedelta(hours=12):
        print(f"A: In range from {start_string} to {end_string} there was no bearish trend.")
    else:
        intervaltime = end_b[0]-start_b[0]
        start_b_string = start_b[0].strftime("%Y-%m-%d")
        end_b_string = end_b[0].strftime("%Y-%m-%d")
        print(f"A: In range from {start_string} to {end_string} \
longest bearish trend was {intervaltime.days} days between {start_b_string} and {end_b_string}. \
Bitcoin's price fell from {euros_to_string(start_b[1])} euros to \
{euros_to_string(end_b[1])} euros.")
    print()

    # B Which date within a given date range had the highest trading volume?
    print("B.")
    print("Q: Which date within a given date range had the highest trading volume?")
    volume_day = highest_volume(total_volumes)
    volume_day_string = volume_day[0].strftime("%Y-%m-%d")
    
    euros = volume_day[1]
    volume_euros_string = euros_to_string(euros)
    
    print(f"A: In range from {start_string} to {end_string} highest trading volume in single day was \
{volume_day_string}, then volume was {volume_euros_string} euros.")
    print()

    # C The day to buy and the day to sell. In the case when one should neither buy nor sell, return an indicative output of your choice.
    print("C")
    print("Q: Whichs dates are best to buy and sell within a given date range")
    buy, sell = find_buy_sell(prices)
    if buy == None or sell == None:
        print(f"A: In range from {start_string} to {end_string} prices fell. Should neither buy or sell.")
    else: 
        buy_day_string = buy[0].strftime("%Y-%m-%d")
        sell_day_string = sell[0].strftime("%Y-%m-%d")
        gain = (sell[1]/buy[1])*100-100
        if gain > 100:
            gain_string_procent = str(gain)[0:5]
        else:
            gain_string_procent = str(gain)[0:4]

        print(f"A: In range from {start_string} to {end_string} the best day to buy was {buy_day_string} at price {euros_to_string(buy[1])} euros and sell \
{sell_day_string} at price {euros_to_string(sell[1])} euros. Gain {gain_string_procent}%.")

if __name__ == "__main__":
    main()