import requests
import calendar
import datetime
import time
from requests.exceptions import HTTPError

url = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
year = "2019"
class Crawler:
    def run(self):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.text = response.text
            self.launches = dict()
            self.extract()
            self.build()
        except HTTPError as e:
            print("Http request error!")

    def extract(self):
        self.text = self.text.split('''<span class="mw-headline" id="Suborbital_flights">Suborbital flights''')[0]
        strs = self.text.split('''<span class="nowrap">''')
        for raw_str in strs:
            str = raw_str.split("</span>")[0]
            if(self.validate(str)):
                iso = self.str_to_iso(str)
                if iso not in self.launches:
                    self.launches[iso] = 0
                self.launches[iso] += 1

    def build(self):
        days = 366 if calendar.isleap(int(year)) else 365
        f = open("crawler.csv",'w')
        f.truncate()
        f.write("date, value")
        for i in range(days):
            iso = self.day_to_iso(i)
            f.write("\n")
            if iso in self.launches:
                f.write(iso + ", " + str(self.launches[iso]))
            else:
                f.write(iso + ", 0")

    # Helper function
    def validate(self, str):
        try:
            datetime.datetime.strptime(str, "%d %B")
            return True
        except ValueError:
            return False

    def str_to_iso(self, str, ft = "%Y-%B-%d"):
        strs = str.split(" ")
        date = year + "-" + strs[1] + "-" + strs[0]
        iso = datetime.datetime.strptime(date,ft).isoformat() + "+00:00"
        return iso

    def day_to_iso(self, day, ft = "%Y-%B-%d"):
        start_str = year + "-January-01"
        start = datetime.datetime.strptime(start_str, ft)
        date = start + datetime.timedelta(days=day)
        return date.isoformat() + "+00:00"

if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()