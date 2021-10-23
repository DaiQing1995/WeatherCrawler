import time
import requests
import re
import datetime

webheader = {
        'Accept': 'text/html, application/xhtml+xml, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'DNT': '1',
        'Connection': 'Keep-Alive',
}

def getPageRaw(url):
    resp = requests.post(url, headers=webheader)
    return resp.text

def regTimeTempHum(date, rawChars):
    timePattern = re.compile(r'h:"([0-9]{2}:[0-9]{2})')
    timeResult = timePattern.findall(rawChars)

    tempPattern = re.compile(r'"([0-9]+)&nbsp;°C"')
    tempResult = tempPattern.findall(rawChars)

    humPattern = re.compile(r'"([0-9]+)%"')
    humResult = humPattern.findall(rawChars)

    print("%s, datasize: %d %d %d" % (date, len(timeResult), len(tempResult), len(humResult)))

    counter = 0
    for i in range(0, len(timeResult)):
        file_handle.writelines("%s %s %s %s\n" % (date, timeResult[i], tempResult[i], humResult[i]))
        counter += 1

    while counter < 24:
        file_handle.writelines("qs qs qs qs\n")
        counter += 1

def handle(date, url):
    rawPage = getPageRaw(url)
    regTimeTempHum(date, rawPage)

def main():
    rawDate = datetime.date(year=2020, month=1, day=1)
    endDate = datetime.date(year=2021, month=10, day=23)

    url = "https://www.timeanddate.com/scripts/cityajax.php?n=china/chengdu&mode=historic&hd=20210101&month=1&year=2021&json=1"

    while rawDate < endDate:
        fullDate = rawDate.strftime('%Y%m%d')
        year = rawDate.strftime('%Y')
        month = rawDate.strftime('%#m')
        url = "https://www.timeanddate.com/scripts/cityajax.php?n=china/chengdu&mode=historic&hd=%s&month=%s&year=%s&json=1" % (fullDate, month, year)
        print(url)
        # handle(fullDate, url)
        print(fullDate)
        rawDate += datetime.timedelta(days=1)
        time.sleep(3)

file_handle = open('weather.txt', mode='w')
main()
file_handle.close()