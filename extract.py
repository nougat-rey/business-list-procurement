import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time

class WebDriver():
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="html.parser")

    def get_yellowpages_data(self):
        
        data = []
        try:
            base_url = "https://www.yellowpages.ca/locations/Ontario/Ottawa"
            self.get_url(base_url)
            
            links = []
            categories = []
            for a in self.soup.findAll("a", attrs={"class":"child categories-wrap__sub-item__link"}):
                links.append("https://www.yellowpages.ca"+unquote(unquote(a['href'])))
                categories.append(a.text.split(" Ottawa")[0])

            category_count = 1
            business_count = 1
            print("Extracting data from yellow pages...")
            for link in links:
                self.get_url(link)
                print("Category #: "+str(category_count))
                print(link) #debugging TODO Remove once done debugging
                for div in self.soup.findAll("div", attrs={"class":"listing listing--bottomcta"}):
                    temp = div.find("a", attrs={"class":"listing__logo--link sponsologolink"})['title'].split(" - ")
                    if len(temp) == 4:
                        print(temp) #debugging TODO Remove once done
                        name = temp[0]
                        type = temp[2]
                        phoneNum = temp[3]
                    elif len(temp) == 2:
                        if temp[1][0:3]=="613":
                            name = temp[0]
                            phoneNum = temp[1]
                            type = ""
                        else:
                            name = temp[0]
                            type = temp[1]
                            phoneNum = ""
                    elif len(temp) == 1: 
                        name = temp[0]
                    else:
                        name = temp[0]
                        type = temp[1]
                        phoneNum = temp[2]
                    if name is None: name = ""
                    if type is None: type = ""
                    if phoneNum is None: phoneNum = ""
                    
                    website = div.find("li", attrs={"class":"mlr__item mlr__item--website"})
                    address = div.find("span", attrs={"itemprop":"streetAddress"})
                    if address is None: address = ""
                    else: address = address.text
                    if website is None: website = ""
                    else:
                        website = website.find("a")['href'].split("redirect=")
                        if len(website) == 1: website = unquote(unquote(website[0])).encode('utf-8')
                        else: website = unquote(unquote(website[1])).encode('utf-8')

                    print("Business #: "+str(business_count))
                    business_count += 1
                    data.append([name, address, type, phoneNum, '=HYPERLINK("{}")'.format(website)])
                category_count += 1
                if category_count%50 == 0: self.reset_driver() #Resetting chromedriver after every 50 queries
        except Exception as error:
            print("Error extracting business listings from Yellow Pages: {}".format(error))
        return data


    def reset_driver(self):
        self.driver.close(); #close browser window
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

    def get_url(self, link):
        self.driver.get(link)
        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="html.parser")

class CSVManager():
    def __init__(self, filename):
        self.file = open(filename, "w")
        self.writer = csv.writer(self.file, delimiter=',')
        self.writer.writerow(['Name', 'Address', 'Category', 'Phone Number', 'Website', 
            'Size of Business', 'Product/Service', 'Clientel', 'Point of Contact',
            'Email', 'Host?', 'Advertiser?', 'What advertisements to host?',
            'What hosts to advertise at?', 'Description', 'Availability of space'
        ])

    def write_row(self, row):
        self.writer.writerow(row)

    def shutdown(self):
        self.file.close()

if __name__ == "__main__":
    start = time.time()
    myCSVManager = CSVManager("business_listings.csv")
    myWebDriver = WebDriver()
    data = myWebDriver.get_yellowpages_data()
    for row in data: myCSVManager.write_row(row)
    myCSVManager.shutdown()
    end = time.time()
    print('Execution Time: ' + str(end - start))
