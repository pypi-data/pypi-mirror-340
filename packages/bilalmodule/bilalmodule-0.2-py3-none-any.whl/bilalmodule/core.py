import secrets
import string
import ast
import os
from cryptography.fernet import Fernet
import base64

# Gizli not defteri modülü
class secretnotesmodule():

    def __init__(self):
        # Şifrelenmiş notlar için liste
        self.sfr = []
        
        # Şifreleme anahtarını kontrol et: Dosya yoksa yeni bir anahtar oluştur
        if not os.path.exists("crypto.key"):
            self.key = Fernet.generate_key()  # Yeni bir Fernet anahtarı oluştur
            with open("crypto.key", "wb") as key_file:
                key_file.write(self.key)  # Anahtarı dosyaya yaz
        else:
            # Anahtar dosyasını oku: Mevcut bir anahtarı kullan
            with open("crypto.key", "rb") as key_file:
                self.key = key_file.read()
        
        # Fernet nesnesi: Şifreleme işlemleri için anahtar kullanarak oluştur
        self.fernet = Fernet(self.key)
        
        # Şifrelenmiş notları dosyadan oku: Eğer dosya varsa ve veri içeriyorsa
        if os.path.exists("encrypted_notes.bin"):
            with open("encrypted_notes.bin", "rb") as f:
                encrypted_data = f.read()
                if encrypted_data:
                    try:
                        # Şifreli veriyi çöz ve Python listesine dönüştür
                        decrypted_data = self.fernet.decrypt(encrypted_data)
                        self.sfr = ast.literal_eval(decrypted_data.decode())
                    except:
                        # Hata durumunda boş liste kullan
                        self.sfr = []

        # test1.txt dosyasını oluştur: Dosya yoksa boş bir dosya yarat
        if not os.path.exists("test1.txt"):
            open("test1.txt", "w").close()

    def secret_notes(self, Enter_your_title, Enter_your_secret, Enter_master_key):  
        """
        Yeni bir gizli not oluştur ve şifrele.
        Enter_your_title: Notun başlığı
        Enter_your_secret: Gizli not içeriği
        Enter_master_key: Not için anahtar
        """
        # Rastgele bir kimlik dizisi oluştur: 20 karakter uzunluğunda
        rasgele_dizi = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20)) + "="
        # Notu anahtar, kimlik ve içerik ile birlikte listeye ekle
        self.sfr.append((Enter_master_key, rasgele_dizi, Enter_your_secret))

        # Şifrelenmiş veriyi dosyaya kaydet: Listeyi şifrele ve dosyaya yaz
        encrypted_data = self.fernet.encrypt(str(self.sfr).encode())
        with open("encrypted_notes.bin", "wb") as f:
            f.write(encrypted_data)

        # Başlık ve kimliği SecretNotes.txt dosyasına yaz
        with open("SecretNotes.txt", "a") as file:
            file.write(f"{Enter_your_title}\n")
            file.write(f"{rasgele_dizi}\n")

    def decrypt(self, password, key):
        """
        Şifrelenmiş notu çöz ve göster.
        password: Not için kullanılan anahtar
        key: Notun kimlik dizisi
        """
        found = False
        # Listeyi dolaşarak doğru anahtar ve kimlik eşleşmesini bul
        for s, k, i in self.sfr:
            if s == password and k == key:
                print(f"Gizli Not: {i}")  # Notu yazdır
                found = True
                break
        # Eşleşme bulunamazsa hata mesajı göster
        if not found:
            print("Not bulunamadı veya şifre/anahtar yanlış!")

def update_size(event, line=3):
    """
    Metin kutusunun yüksekliğini satır sayısına göre güncelle.
    event: Metin kutusu için olay nesnesi
    line: Maksimum satır sayısı (varsayılan 3)
    """
    secret_text = event.widget
    line_count = int(secret_text.index('end-1c').split('.')[0])
    # Satır sayısını kontrol et ve gerekirse yükseklik ayarla
    if line_count > line:
        secret_text.config(height=line_count)
