'''
This python code can be used to generate temperature bar graphs
using matplotlib & data from https://www.accuweather.com/ 
- AccuWeather Terms Of Use - https://www.accuweather.com/en/legal 
'''
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
fake_headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer":"https://www.google.com/",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "sec-ch-ua":'''" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"''',
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"Windows"   
}
startTempFormat = False
Date1_Repeat = False
Already_Plotted = False
def generate_graph(regioncode, regionname, month, year, callback):
    web_url = 'https://www.accuweather.com/en/in/{}/{}/{}-weather/{}?year={}'.format(regionname,regioncode,month,regioncode,year)
    html_text = requests.get(web_url, headers=fake_headers).text
    soup = BeautifulSoup(html_text, 'html.parser')

    days = soup.find_all("div", {"class": "date"})
    min_t = soup.find_all("div", {"class": "low"})
    max_t = soup.find_all("div", {"class": "high"})

    dates = []
    minT = []
    maxT = []
    avgT = []

    def draw_graph():
        global Already_Plotted
        Already_Plotted = True
        if(len(dates) == 0):
            callback("Error - Invalid Data OR Scrape Error.")
        else:
            plt.style.use('dark_background')
            plt.title('Temperature of {} during {} {}'.format(regionname, month.capitalize(), year))
            plt.bar(dates, maxT, color="orange")
            plt.bar(dates, minT, color="#2ca0d8")
            plt.plot(dates, avgT, color="red")
            plt.legend(['Average Temperature','Maximum Temperature','Minimum Temperature'])
            plt.xlabel('➔ Days in {} ➔'.format(month.capitalize()))
            plt.ylabel('➔ Temperature ➔')
            plt.show()
            callback("Done.")

    def format_tempstr(d, n, x):
        global startTempFormat
        global Date1_Repeat
        global Already_Plotted

        day = int(d.replace('\t','').replace('\n','').replace(' ','').replace('°',''))
        min = int(n.replace('\t','').replace('\n','').replace(' ','').replace('°',''))
        max = int(x.replace('\t','').replace('\n','').replace(' ','').replace('°',''))

        if(day == 1):
            if(Date1_Repeat == False):
                startTempFormat = True
                Date1_Repeat = True
            else:
                startTempFormat = False
                draw_graph()

        if(startTempFormat == True):
            dates.append("{}".format(day))
            maxT.append(max)
            minT.append(min)
            avgT.append(int((max+min)/2))
 
    i = 0
    while(i < (len(days)-1)):
        format_tempstr(days[i].string, min_t[i].string, max_t[i].string)
        i+=1
    if(Already_Plotted == False):
        draw_graph()

print("\n⌜                                                           ⌝")
print("  █████████████████████████████████████████████████████████  ")
print("  ██████████     ᴛᴇᴍᴘᴇʀᴀᴛᴜʀᴇ ɢʀᴀᴘʜ ɢᴇɴᴇʀᴀᴛᴏʀ       ████████  ")
print("  ██████████ ʙᴀꜱᴇᴅ ᴏɴ ʜᴛᴛᴘꜱ://ᴡᴡᴡ.ᴀᴄᴄᴜᴡᴇᴀᴛʜᴇʀ.ᴄᴏᴍ/ ████████  ")
print("  █████████████████████████████████████████████████████████  ")
print("⌞                                                           ⌟")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def input_and_start():
    def select_region():
        region_input_val = input("\n-> Enter your state/region :- ")
        query = requests.get("https://www.accuweather.com/web-api/autocomplete?query={}&language=en-us".format(region_input_val), headers=fake_headers).json()
        confirmation = input("<- Is Your State/Region -> {}, {}".format(query[0]["administrativeArea"]["localizedName"], query[0]["country"]["localizedName"])+ " (y/n, default = y) :- ")
        if(confirmation == "n"):
            select_region()
        else:
            dotherest(query[0]["key"], query[0]["administrativeArea"]["localizedName"])
    def dotherest(regioncode, regionname):
        year = input("\n-> Enter a Year after 2015 :- ")
        month = input("-> Enter the Month of {} :- ".format(year))
        print("-> Generating Graph for {} {} .....".format(month.capitalize(), year))
        def callback(log):
            global startTempFormat
            global Date1_Repeat
            global Already_Plotted
            startTempFormat = False
            Date1_Repeat = False
            Already_Plotted = False
            print("-> {}".format(log))
            selection = input("<- Do you want to exit? (y/n, default = y) ")
            if(selection == "n"):
                print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                input_and_start()
            else:
                import sys
                print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                sys.exit()
        generate_graph(regioncode,regionname,month,year,callback)
    select_region()
input_and_start()