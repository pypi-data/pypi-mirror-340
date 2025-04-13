
import secrets
import string
import ast
import os


#gizli not defteri  
class secretnotesmodule():

    def __init__(self):
        self.sfr= []
        if not os.path.exists("test2.txt"):    
            open ("test2.txt", "w").close()
        
        txt_sfrs= open("test2.txt")
        for txt_sfr in txt_sfrs:
            txt_sfr= txt_sfr.replace("\n","")
            txt_sfr= txt_sfr.strip('"')
            txt_sfr= txt_sfr.replace('[',"")
            txt_sfr= txt_sfr.replace(']',"")
            if txt_sfr:    
                temiz_tuple= ast.literal_eval(txt_sfr)
                self.sfr.append(temiz_tuple)

        if not os.path.exists("test1.txt"):
            open ("test1.txt","w").close()
    def secret_notes (self, Enter_your_title, Enter_your_secret, Enter_master_key):  
        """
        Enter_your_title= "title", Enter_your_secret="Secret", Enter_master_key=123
        """
        rasgele_dizi= ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20)) + "="
        liste=[(Enter_master_key, rasgele_dizi, Enter_your_secret)] 


        with open ("test1.txt", "a")as file:
            file.write(f"{Enter_your_title}\n")
            file.write(f"{rasgele_dizi}\n")


        with open ("test2.txt", "a")as file1:
            file1.write(f"{liste}\n")


    def decrypt(self, password, key):
        """
        password=123, key= "xidhmd9DqRl1sMrmoshf="
        """
        for s,k,i in self.sfr:
            if s == password:
                if k == key:
                    print(i)



def update_size(event,line):
    """
    line= "How many lines?"
    """
    secret_text= event.widget
    line_count = int(secret_text.index('end-1c').split('.')[0])
    if line_count > line:
        secret_text.config(height=line_count)
