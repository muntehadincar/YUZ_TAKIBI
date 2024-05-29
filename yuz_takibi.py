#!/usr/bin/env python
# coding: utf-8

# In[1]:


import serial
import time
import cv2


# In[ ]:


# Arduino ile seri iletişim kuralım.
arduino = serial.Serial(port='COM11', baudrate=9600, timeout=.1)  

# OpenCV'nin ön eğitilmiş yüz tanıma modelini yükleyelim.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kameradan görüntü alalım.
cap = cv2.VideoCapture(0)

# Önceki karedeki yüz konumu
prev_face_pos = None

# Hareket algılama aralığı ve süresi
movement_interval = 10  # Her 10 karede bir hareket kontrolü yap
movement_duration = 5   # Hareket algılama süresi (karelerde)

# Hareket için eşik değeri 20 olarak belirledim.
movement_threshold = 20

# Hareket sayacı ve yönü
movement_counter = 0
movement_direction = None
display_counter = 0
display_duration = 50  # Metni göstereceğimiz süre 

def send_command_to_arduino(command):
    arduino.write(command.encode())
    time.sleep(0.1)

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()

    # Kameradaki aynalamayı düzelt 
    frame = cv2.flip(frame, 1)

    # Kareyi griye dönüştür (yüz tanıma algoritması gri tonlamalı görüntülerle daha iyi çalışır)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Hareketi algıla
    movement_counter += 1
    if movement_counter % movement_interval == 0:
        # Yüzleri tespit et
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            x, _, w, _ = faces[0]  # İlk tespit edilen yüzün konumunu al

            # Önceki karede yüz varsa, hareketi hesapla
            if prev_face_pos is not None:
                prev_x, _, _, _ = prev_face_pos
                movement = x - prev_x

                # Hareket yönüne göre işlem yapma
                if abs(movement) > movement_threshold:
                    if movement > 0:
                        movement_direction = 'R'
                    elif movement < 0:
                        movement_direction = 'L'

                    # Hareket algılama süresi boyunca yönü sakla
                    display_counter = display_duration
                    send_command_to_arduino(movement_direction)

        # Şu anki yüz konumunu önceki konum olarak kaydedelim.
        if len(faces) > 0:
            prev_face_pos = (x, _, w, _)

    # Metni göstermek için sayaç kullanalım
    if display_counter > 0:
        cv2.putText(frame, movement_direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        display_counter -= 1

    # Tespit edilen yüzleri çerçeve içine alma
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Sonuçları gösterme
    cv2.imshow('Face Detection', frame)

    # 'q' tuşuna basarak çıkış yapmak
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kullanılan kaynakları serbest bırakma ve pencereleri kapatma
cap.release()
cv2.destroyAllWindows()

#hareket yönünü belirlendikten sonra movement_direction değişkenine atanır.
#ve display_counter'ı display_duration kadar ayarlar.
#Her karede display_counter azalır
#ve display_counter sıfırdan büyük olduğu sürece hareket yönü ekranda gösterilir.
#Bu sayede metin daha uzun süre ekranda kalır.

