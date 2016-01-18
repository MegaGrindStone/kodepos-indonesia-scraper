from bs4 import BeautifulSoup
import requests
import sys
import csv

def fetchDataInPage(soup, data):
    for i in range(1, 20):
        propinsi = soup.find(id="r" + str(i) + "_kodeposalamat").find(id="el" + str(i) + "_kodeposalamat_Propinsi").span.string.strip()
        kabupaten = soup.find(id="r" + str(i) + "_kodeposalamat").find(id="el" + str(i) + "_kodeposalamat_Kabupaten").span.string.strip()
        kecamatan = soup.find(id="r" + str(i) + "_kodeposalamat").find(id="el" + str(i) + "_kodeposalamat_Kecamatan").span.string.strip()
        kelurahan = soup.find(id="r" + str(i) + "_kodeposalamat").find(id="el" + str(i) + "_kodeposalamat_Kelurahan").span.string.strip()
        kodepos = soup.find(id="r" + str(i) + "_kodeposalamat").find(id="el" + str(i) + "_kodeposalamat_Kodepos").span.string.strip()
        if not propinsi in data:
            data[propinsi] = {}
        if not kabupaten in data[propinsi]:
            data[propinsi][kabupaten] = {}
        if not kecamatan in data[propinsi][kabupaten]:
            data[propinsi][kabupaten][kecamatan] = {}
        data[propinsi][kabupaten][kecamatan][kelurahan] = kodepos

def getTotalPage(soup):
    return soup.find_all("div", {"class":"ewPager"})[1].find_all("span")[5].string.strip().split( )[1]

def writeCSV(data):
    csvFile = open("result-kodepos-indonesia.csv", "wb")
    writer = csv.writer(csvFile)
    for propinsi in data:
        for kabupaten in data[propinsi]:
            for kecamatan in data[propinsi][kabupaten]:
                for kelurahan in data[propinsi][kabupaten][kecamatan]:
                    writer.writerow((propinsi, kabupaten, kecamatan, kelurahan, data[propinsi][kabupaten][kecamatan][kelurahan]))
    csvFile.close()

print "Counting page"
urlString = "http://kodepos.posindonesia.co.id/kodeposalamatlist.php?cmd=search&t=kodeposalamat&z_Propinsi=LIKE&x_Propinsi=%25%25%25%25&z_Kabupaten=LIKE&x_Kabupaten=%25%25%25%25&z_Kecamatan=LIKE&x_Kecamatan=%25%25%25%25&z_Kelurahan=LIKE&x_Kelurahan=&psearch=%25%25%25%25&recperpage=20&start="
page = requests.get(urlString)
soup = BeautifulSoup(page.text, 'html.parser')
totalPage = int(getTotalPage(soup))
print "Total Page : ", totalPage

data = {}
for i in range(1, totalPage):
    print "Scraping page ", i , " from " , totalPage , " pages          \r",
    sys.stdout.flush()
    page = requests.get(urlString + str(i))
    soup = BeautifulSoup(page.text, 'html.parser')
    fetchDataInPage(soup, data)

print ""
print "Generating CSV File"
writeCSV(data)
print "Fucking Done!"
