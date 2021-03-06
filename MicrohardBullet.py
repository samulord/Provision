# Working script
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
import csv
import os
import re
import time


class configgerer():

    def connect(self, configURL, ip):
        self.configURL = configURL
        self.ip = ip
        p = webdriver.FirefoxProfile()
        #p.set_preference('webdriver.log.file','/tmp/firefox_console')
        self.driver = webdriver.Firefox(p)
        self.driver.get(self.configURL)
            
    
    def disconnect(self):
        self.driver.quit()

    def getMac(self):
        driver = self.driver
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-info.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        return(self.driver.find_element_by_xpath("/html/body/div/div[6]/div[3]/table[2]/tbody/tr/td[2]").text) 

    def getWifiMac(self):
        driver = self.driver
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-info.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        return(self.driver.find_element_by_xpath("/html/body/div/div[6]/div[5]/table[2]/tbody/tr[3]/td[1]").text) 

    def getPublicIP(self):
        driver = self.driver
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-info.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        return(self.driver.find_element_by_xpath("/html/body/div/div[6]/div[4]/table[3]/tbody/tr/td[2]").text)

    def getFirmware(self):
        driver = self.driver
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        return(self.driver.find_element_by_xpath("/html/body/div/form/div/div[1]/table[2]/tbody/tr[2]/td[3]").text)

    def checkPage(self):
        print(WebDriverWait(self.driver, 10).until(EC.title_contains("Summary")))

    def upgradeFirmware(self, firmware="/support/microhard/microhard_provision/1084-20.bin"):
        driver = self.driver
        print(firmware)
        #Move to Maintanence Page
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()

        #upload the file
        uploadButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("upgradefile"))
        uploadButtonEle.send_keys(firmware)

        #click upgrade 
        upgradeButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("upgrade"))
        upgradeButtonEle.click()

        element = WebDriverWait(driver, 900).until(EC.title_contains("Summary"))

        #sleep for 10 minutes while upgrade
        #time.sleep(600)

    def uploadConfig(self,configurationFilePath):
        driver = self.driver
        
        #go to Maintanence window
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        
        #upload the path to the file 
        uploadConfigButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("configfile"))
        uploadConfigButtonEle.send_keys(configurationFilePath)
        
        #click the "Restore" button
        uploadConfigConfirmButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("chkconfig"))
        uploadConfigConfirmButtonEle.click()
    
        #Reconfirming the "Restore" button 
        uploadConfigRestoreButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("instconfig"))
        uploadConfigRestoreButtonEle.click()

    def setHostname(self, name, desc):
        driver = self.driver
        hostname=name
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-settings.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        #Change Hostname Field
        hostnameFieldXpath = "//input[@name='hostname']"
        hostanmeFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(hostnameFieldXpath))
        hostanmeFieldElement.clear()
        hostanmeFieldElement.send_keys(hostname)
        
        fieldXpath = "//input[@name='description']"
        fieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(fieldXpath))
        fieldElement.clear()
        fieldElement.send_keys(desc)

        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()

    def setDesc(self, name):
        driver = self.driver
        desc=name
        print(desc)
        print("Change to the Settings tab in a Microhard")
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-settings.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        print("Change Hostname Field")
        fieldXpath = "//input[@name='description']"
        fieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(fieldXpath))
        fieldElement.clear()
        fieldElement.send_keys(desc)
        
        print("Submit the change, like a commit")
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()

    def setSSID(self, name):
        driver = self.driver
        ssid=name
        
        #Change to the Wireless tab
        wirelessButtonXpath = "Wireless"
        wirelessElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text(wirelessButtonXpath))
        wirelessElement.click()
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = "//a[@href='/cgi-bin/webif/wireless-wlan0.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        #Change Hostname Field
        ssidFieldXpath = "//*[@id='ssid_0']"
        ssidFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(ssidFieldXpath))
        ssidFieldElement.clear()
        ssidFieldElement.send_keys(ssid)
        
        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()

    def setRadiusID(self, name):
        driver = self.driver
        radiusID=name
        
        #Change to the Wireless tab
        wirelessButtonXpath = "Wireless"
        wirelessElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text(wirelessButtonXpath))
        wirelessElement.click()
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = "//a[@href='/cgi-bin/webif/coova-chilli.sh']" 
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        #Change Hostname Field
        radiusIDFieldXpath = "coova_chilli_coova_nasid" 
        radiusIDFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name(radiusIDFieldXpath))
        radiusIDFieldElement.clear()
        radiusIDFieldElement.send_keys(radiusID)
        
        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()

    def writeToLog(self, text):
        with open('log.txt', 'a') as logfile:
            logfile.write(text)

class databaser():
    def readFile(self):
       self.book = {}
       with open('vancouvertaxi.csv') as csvfile:
           reader = csv.DictReader(csvfile)
           for row in reader:
               self.book[row['MAC']] = row
               print(row)

    def getDevice(self, mac):
        m = re.sub(r':','', mac) 
        dev = self.book[m]
        return dev


class logger():
    def openLog(self):
        self.log = {}

    def addToLog(self, type, item):
        self.log[type] = item

    def writeToLog(self, text):
        with open('log.txt', 'w') as logfile:
            logfile.write(text)


#class portListener(threading.Thread):

def run(ip, db):
    print("======== " + ip + " thread starting")
    i = 0
    while True:
        if i < 1:
# initial stage
            try:
# try to connect
                print("******** " + ip + " loading")
                configURL = 'http://admin:admin@' + ip + '/'
                device = configgerer()
                device.connect(configURL, ip)
                firmware = device.getFirmware()
            except:
                print("........ " + ip + " down ......... Retrying ........")
                continue
# try to upload firmware
            try:
                print("******** " + ip + firmware)
                #===============================================================
                # if firmware != "v1.1.0 build 1084-20":
                #     print("++++++++ UPLOADING FIRMWARE")
                #     device.upgradeFirmware()
                #     #timer for firmware upgrade is an implicit timer on the webDriverWait
                # if firmware != "v1.1.0 build 1084-20":
                #     print("XXXXXXXX " + ip + " FIRMWARE FAIL!!!")
                #     break
                #===============================================================
                i = 1
            except:
                print("XXXXXXXX " + ip  + " UPGRADE FAIL")
                continue
        if i < 2:
            try:
                print("++++++++ " + ip + " UPLOADING CONFIGURATION")
                device.uploadConfig("/support/microhard/microhard_provision/VancouverTaxi.config")
                print("******** " + ip + " SLEEPING FOR 2 MINUTES UNTIL CONFIG IS APPLIED")
                time.sleep(120)
                device.disconnect()
                i = 2
            except:
                print("XXXXXXXX " + ip + " CONFIGURATION FAIL")
                continue
        if i < 3:  
            try:
                configURL = 'http://admin:admin@' + ip + '/'
                device2 = configgerer()
                device2.connect(configURL, ip)
            
                #Gets Wifi Mac
                print("******** " + ip + " GETTING WIFI MAC")
                MAC = device2.getWifiMac()
                print("******** " + ip + " WIFI MAC ADDRESS = " + MAC)
                
                #Gets Eth Mac
                print("******** " + ip + " GETTING ETH MAC")
                EthMAC = device2.getMac()
                print("******** " + ip + " ETH MAC ADDRESS = " + EthMAC)
                
                #Gets Public IP
                print("******** " + ip + " GETTING PUBLIC IP")
                PubIP = device2.getPublicIP()
                print("******** " + ip + " PUBLIC IP = " + PubIP)
                
                #Gets Device info on the spreadsheet
                print("******** " + ip + " GETTING DEVICE INFO")
                devinfo = db.getDevice(MAC)
                print("******** " + ip + " HOSTNAME = " + devinfo["HOSTNAME"])
               

                devToStr = "******** "  + ip +  "  HOSTNAME = " + devinfo["HOSTNAME"] + " / PUBLIC IP = " + PubIP + " / WIFI MAC = " + MAC + " / ETH MAC = " + EthMAC + " / \n" 
                print(devToStr)
                #device2.writeToLog(devToStr)
            
                print("++++++++ " + ip + " " +  devinfo["HOSTNAME"] + " : " + ip + " : " + EthMAC + " ++++++++ Setting HOSTNAME = " + devinfo["HOSTNAME"] + " / DESCRIPTION = " + devinfo["DESCRIPTION"])
                        # Hostname & Description
                device2.setHostname(devinfo["HOSTNAME"], devinfo["DESCRIPTION"])
                time.sleep(120)
                        # SSID
                #device2.setSSID(devinfo["SSID"])
                #print("++++++++ " + devinfo["HOSTNAME"] + " : SSID")
                #time.sleep(150)
                        # NASID
                
                print("++++++++ " + ip + " " + devinfo["HOSTNAME"] + " : " + ip + " : " + EthMAC + " ++++++++ Setting NASID = " + devinfo["NASID"])        
                device2.setRadiusID(devinfo["NASID"])
                device2.disconnect()
                time.sleep(120)
                print("******** " + ip + " " +  devinfo["HOSTNAME"] + " : " + ip + " : " + EthMAC + " ******** Configuration Complete")   
                i = 3

            except:
                print("XXXXXXXX  " + ip + " SETTINGS FAIL")
                continue

        if i < 4:
            try:
                configCheckURL = 'http://admin:admin' + PubIP + '/'
                device3 = configgerer()
                device3.connect(configURL, ip)

                CheckEthMAC = device3.getMac()
                print("******** " + ip + " / Hostname: " + devinfo["HOSTNAME"]  +  " / Mac address = " + CheckEthMAC)
                CheckWifiMAC = device3.getWifiMac()
                print("******** " + ip + " / Hostname: " + devinfo["HOSTNAME"]  +  " / Wifi Mac address = " + CheckWifiMAC)
                device3.disconnect()
                print("******** " + ip + " testing complete.")
                print("******** " + ip + " / Hostname: " + devinfo["HOSTNAME"]  +  " is COMPLETED")
                print("------------------------------------------------------------------------------")
                i = 4
            except:
                print("XXXXXXXX  " + ip + " TESTING FAIL")
                continue


def test(ip):
    configURL = 'http://admin:admin@' + ip + ':8081/'
    device = configgerer()
    device.connect(configURL, ip)
    device.upgradeFirmware()
    i = 0 
    while i != 600:
        time.sleep(1)
        i = i + 1
        print(i)
    
    firmware = device.getFirmware()
    print(firmware)
    print(device.getMac())
    print(device.checkPage())
    device.setHostname("John", "Test")
    time.sleep(30)
    device.setSSID("test")
    time.sleep(80)
    device.setRadiusID("test")
    device.disconnect()


def test2(ip):
    configURL = 'http://admin:admin@' + ip + ':8081/'
    device = configgerer()
    device.connect(configURL, ip)
    WifiMAC = device.getWifiMac()
    EthMAC = device.getMac()
    device.writeToLog("" + WifiMAC + "," + EthMAC)
   

def test3(ip):
    configURL = 'http://admin:YellowCabs2015!@' + ip + ':8081/'
    device2 = configgerer()
    device2.connect(configURL, ip)
    
    print("++++++++ UPLOADING CONFIGURATION")
    device.uploadConfig("/support/microhard/microhard_provision/YellowCabsConfig.config")
    time.sleep(300)
    print("Getting Wifi MAC")
    MAC = device2.getWifiMac()
    print("Getting Eth MAC")
    EthMAC = device2.getMac()
    print("Getting Device info")
    devinfo = db.getDevice(MAC)

def main():
    IPs = ["10.254.0.3","10.254.0.19"]
    #IPs = ["10.254.0.3","10.254.0.19","10.254.0.35","10.254.0.51","10.254.0.67","10.254.0.83","10.254.0.99","10.254.4.3","10.254.4.19","10.254.4.35","10.254.4.51","10.254.4.67", "10.254.4.83", "10.254.4.99"]
            
            #"10.254.4.3","10.254.4.19","10.254.4.35","10.254.4.51","10.254.4.67"]    
    ts = []
    db = databaser()
    db.readFile()
    

    #test3(IPs[0])

    for ip in IPs:
        t = Thread(target=run, args=(ip, db))
        ts.append(t)
        t.start()
        


if __name__=='__main__':main() 