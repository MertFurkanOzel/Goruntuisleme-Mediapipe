from selenium import webdriver
import os
import subprocess
from selenium.common import NoSuchElementException, ElementNotInteractableException #Gerekli kütüphanelerin import edilmesi.
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.chdir("C:\Program Files\Google\Chrome\Application") #Youtube'da bir videoyu beğenmek için hesap açılması gerekiyor ve biz bu kod aracılığı ile
subprocess.Popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\debugger"')#chrome'da sayfa açtığımız için hesabımıza giriş yapmamıza izin vermiyor.
#Bu yüzden chrome'u debug modda açmamız gerekiyor.Yukarıdaki ilk satır kodu chrome'nin dizinine gitmemizi sağlıyor.
#İkinci kod ise cmd üzerinden kod çalıştırmamızı sağlıyor burada çalıştırdığımız kod ile port açıp bir klasör veriyoruz artık programı
#çalıştırdığımız zaman debug modda çalışmış olacak ve dosyalar verdiğimiz klasörde oluşturulacak.


class Browser:#Browser classının tanımı
    def __init__(self):#Yapıcı fonksiyonumuzu tanımlıyoruz.
        self.options=Options()#Webdrivera gönderilecek ayarlar.
        self.options.add_experimental_option("debuggerAddress","localhost:9222")#debuggerAddress'e portumuzu gönderip ayar yapmış olduk.
        self.driver=webdriver.Chrome(options=self.options,executable_path="C:\chromedriver\chromedriver.exe")#Webdrivera yaptığımız ayarları verip konumunu söylüyoruz ve son olarak driverımızı oluşturuyoruz.
        self.likebutton=None #like ve dislike butonlarını none olarak tanımladım.
        self.dislikebutton=None

    def buttonexist(self):#açılan sayfada like ve dislike butonu olup olmadığını tespit eden bir fonksiyon.
        if "watch" in self.driver.current_url: #Eğer driverımızdaki url'nin içinde watch geçiyorsa yani Youtube'da bir videodaysak.
            try:#Hata aldığımızda programın sonlanmaması için try bloğu oluşturdum.
                #self.driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[1]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-icon-button/button")
                self.driver.find_element(By.CSS_SELECTOR,"div.style-scope.ytd-video-primary-info-renderer div div#menu-container div#menu button")
            except NoSuchElementException:#Yukarıda like butonunu css selector ile buluyoruz.Eğer bulunmazsa false döndürüyor.
                return False
            return  True

    def buttonsdef(self):# Eğer butonlar tanımlıysa true ,değilse false döndüren bir fonksiyon.
        return self.likebutton is not None and self.dislikebutton is not None

    def defbuttons(self):#Butonları tanımlayan fonksiyon.Yine css selector ile butonları bulup tanımlıyoruz.
        self.likebutton=self.driver.find_element(By.CSS_SELECTOR,
                                 "div.style-scope.ytd-video-primary-info-renderer div div#menu-container div#menu button")
        self.dislikebutton=self.driver.find_element(By.CSS_SELECTOR,"div.style-scope.ytd-video-primary-info-renderer div div#menu-container div#menu ytd-toggle-button-renderer:nth-child(2) button")

    def like(self):#video beğenme fonksiyonu
        try:
            if(self.buttonsdef()) and self.likebutton.get_attribute("aria-pressed") == "false": #Butonlar tanımlı ve butona daha önce basılmamış ise.
                self.likebutton.click()#like butonunun click eventini tetikle.
        except ElementNotInteractableException:#bir şekilde buton olduğu halde basılamıyorsa print ile yazdırıyorum.
            print("butona basılamıyor")

    def dislike(self):# video beğenme fonksiyonunun aynısı sadece dislike butonu için aynı şeyleri yazdım.
        try:
            if(self.buttonsdef()) and self.dislikebutton.get_attribute("aria-pressed") == "false":
                self.dislikebutton.click()
        except ElementNotInteractableException:
            print("butona basılamıyor")