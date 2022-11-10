import cv2 as cv
import mediapipe as mp       #Gerekli kütüphanelerin import edilmesi.
import goruntuislemeproje2

yukari=0  #Yapılan el hareketinde baş parmağın yukarda mı aşağıda mı olduğunu tespit etmek için kullandığım iki değişken.
asagi=0
browser=goruntuislemeproje2.Browser() #İkinci py dosyamdaki Browser classından bir instance oluşturdum.
mphands=mp.solutions.hands # Eldeki noktaların çizimi için kullanılıyor.
hands=mphands.Hands() # Resimdeki eli tarıyor.
mpdraw=mp.solutions.drawing_utils # Elde edilmiş noktaları resime basmak için kullanılıyor.
like=False  #Videonun ne zaman beğenileceğini tespit etmek için 2 boolean değişkeni kullandım.
dislike=False

kameram=cv.VideoCapture(0)#Kameradaki görüntüyü gösteriyor.
while True: # Sonsuz döngü
 if browser.buttonexist() and not browser.buttonsdef(): #Eğer basılacak bir buton mevcut ve buton tanımlı değilse tanımlıyoruz.
     browser.defbuttons()

 a,image=kameram.read()#Kameradaki o anki yakalanan görüntüyü image değişkenine atıyorum.
 image=cv.flip(image,1)#Kameradaki görüntünün ayna görüntüsünü veriyor.
 rgbimg=cv.cvtColor(image,cv.COLOR_BGR2RGB)#Kameradan yakalanan görüntüyü bgr'den rgb'ye dönüştürüyorum.
 hlms=hands.process(rgbimg)#Yolladığım görüntüdeki eli taraması için işlem başlatıyorum.
 if(hlms.multi_hand_landmarks):#Eğer görüntüde el yakalandıysa
     for handlandmarks in hlms.multi_hand_landmarks:#Tespit edilen el sayısı kadar döngü çalışıyor
        for num,landmark in enumerate(handlandmarks.landmark): #Eldeki nokta sayısı kadar yani 21 kez döngü çalışıyor.
         mpdraw.draw_landmarks(image,handlandmarks,mphands.HAND_CONNECTIONS) #Görüntü üzerinde eldeki noktaları birleştip çizdiriyor.
         if(num>4 and landmark.y<handlandmarks.landmark[2].y):# num eldeki noktanın id'si olmuş oluyor 1'den 4'e kadar olan noktalar
             asagi+=1                                     # baş parmağı temsil etmekte 4'den yüksek olduğu için diğer noktaları alıyor
                            # ve bu noktaları 2.nokta ile kıyaslıyoruz eğer ikinci nokta daha aşağıda ise asagi değişkenini 1 arttırdım.

         else :  #eğer ki 4'den büyük olan nokta 2.noktadan daha aşağıda kalıyorsa yani değeri daha büyükse bu sefer yukari değişkeni artıyor.
             yukari+=1

 cv.imshow("cam", image) #kameradaki görüntüye yukarıdaki işlemler gerçekleştirildikten sonra görüntülüyoruz.

 if yukari==21:  #yukari değişkeni alabileceği max değere ulaşmışsa benim 2.noktam diğer noktalardan(4'den büyük) daha yukarıda demektir.
     like=True   #baş parmağımı yukarı kaldırıp onay işaretini yaptığımı bu şekilde tespit ettikten sonra like değerini true yapıyorum.
 if asagi==16:   #aynı şekilde eğer tam tersiyse yani 2.noktam diğer noktalardan daha aşağıda ise dislike değerini true yapıyorum.
     dislike=True

 if like and browser.buttonexist() :#like işareti yapılmışsa ve sayfada istediğimiz buton var ise çalışıyor.
     browser.like()#videoyu beğenme fonksiyonu çalışıyor.
     like=False #tekrar tekrar beğenme butonuna basmaması için burda like değişkenini tekrar false haline getirdim.
 if dislike and browser.buttonexist():#buradada aynı şekilde dislike durumu kontrol ediliyor.
     browser.dislike()
     dislike=False
 asagi = 0 #Yukarıda kullanmış olduğum  16 ve 21 eşitliğinin doğru çalışması için her döngü sonunda değişkenleri sıfırlamamız gerekiyor.
 yukari = 0 #Sıfırlanmazsa sadece ilkinde if bloğu çalışıp diğerlerinde değerler sonsuza gideceği için çalışmayacaktır.
 if(cv.waitKey(1) & 0xFF==ord("q")):# Klavyeden q tuşuna basılınca while döngüsünü bitirip programı sonlandırıyor.
     break