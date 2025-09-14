import tkinter
import random

velikost_pole = 15 
velikost_ctverce = 40
hrac_X = "X"
hrac_pocitac = "O"

class hra:
    def __init__(self, okno):           #vytvoření hracího okna pomací knihovny tkinter
        self.okno = okno 
        self.okno.title("Piškvorky")
        self.canvas = tkinter.Canvas(okno, width=velikost_ctverce*velikost_pole, height= velikost_pole*velikost_ctverce)
        self.canvas.pack()

        self.mrizka = [["" for _ in range(velikost_pole)] for _ in range(velikost_pole)]    #vytvoření seznamu seznamů, sloužícího pro
        self.aktualni_hrac = hrac_X                                                         #ukladání aktuálního stavu hry
        self.vytvorit_mrizku()
        self.canvas.bind("<Button-1>", self.kliknuti)                                       # nastavení praveho tlacítka jako funkci "kliknuti"
    
    def vytvorit_mrizku(self):                                                              #vytvoření čtvercové mrížky na hracím poli
        for radek in range(velikost_pole):
            for sloupcec in range(velikost_pole):
                x1 = sloupcec * velikost_ctverce
                y1 = radek * velikost_ctverce
                x2 = x1 + velikost_ctverce
                y2 = y1 + velikost_ctverce
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def kresleni_symbol(self, radek, sloupec,symbol):                               #funkce pro nakreslení symbolu do čtvercové mřížky
         x = sloupec * velikost_ctverce + velikost_ctverce // 2
         y = radek * velikost_ctverce + velikost_ctverce // 2
         self.canvas.create_text(x, y, text=symbol, font=("Arial", 30), fill="red")
    def kliknuti(self, akce):                                           #nastavení funkce kliknutí, která pomocí výpočtu souřadnic nakreslí symbol
        sloupec = akce.x // velikost_ctverce                             #do hracího okna a uložího taky do pomocného seznamu. Zaroveň zkontroluje pomoci
        radek = akce.y // velikost_ctverce                               #funkce kontrola, zda jsi nevyhral a spustí tah počítače

        if self.plna_mrizka():
            self.canvas.create_text(280,280,text=f" remíza",font=("Arial", 70), fill="green")
            self.canvas.unbind("<Button-1>")
            return
        if self.mrizka[radek][sloupec] == "":
            self.mrizka[radek][sloupec] = self.aktualni_hrac
            self.kresleni_symbol(radek, sloupec, self.aktualni_hrac)
            if self.kontrola(radek,sloupec,hrac_X,5):
                self.canvas.create_text(280,280,text=f" vyhrál si!!!",font=("Arial", 70), fill="green")
                self.canvas.unbind("<Button-1>")
                return

        self.protihrac()

    def kontrola(self, radek, sloupec,symbol,pocet_symbolu_k_vyhre,pocet_vedlejsich_symbolu = False):
        smery=[[1,0], [0,1], [1,1], [1,-1]]         #funkce kontroluje všechny směry od zadaného čtverce a počítá počet symbolů v řadě
        r = radek
        s = sloupec                 #parametr"pocet_vedlejsich_symbolu" vrací nejvetší počet symbolů v řadě pro dané políčko
    
        for smer in smery:
            pocet = 1
            while 0 <=radek + smer[0] < velikost_pole and 0 <= sloupec + smer[1] < velikost_pole and self.mrizka[radek + smer[0]][sloupec + smer[1]] == symbol:
                radek = radek + smer[0]
                sloupec = sloupec + smer[1]
                pocet += 1
            radek = r
            sloupec = s
            while 0 <=radek - smer[0] < velikost_pole and 0 <= sloupec - smer[1] < velikost_pole and self.mrizka[radek - smer[0]][sloupec - smer[1]] == symbol:
                radek = radek - smer[0]
                sloupec = sloupec - smer[1]
                pocet += 1
               
            if pocet >= pocet_symbolu_k_vyhre:
                return True
        if pocet_vedlejsich_symbolu:
            return pocet
        else:
            return False
    def protihrac(self):                      #nastavení hry počítače
        if self.plna_mrizka():                #na začátku hry počítač náhodně položí symbol vedle tebou položeného symbolu
            self.canvas.create_text(280,280,text=f" remíza",font=("Arial", 70), fill="green")
            self.canvas.unbind("<Button-1>")
            return
        
        if self.zacatek_hry():              
            for r in range(velikost_pole):
                for s in range(velikost_pole):
                    if self.mrizka[r][s]=="X":
                        tahy = [[1,0],[0,1],[1,1],[-1,-1],[1,-1],[-1,1],[-1,0],[0,-1]]
                        tah = random.choice(tahy)
                        r = r + tah[0]
                        s = s + tah[1]
                        self.mrizka[r][s] = "O"
                        self.kresleni_symbol(r, s, "O")
                        return

        for r in range(velikost_pole):      #počítač zde kontrouje zda nemůže jedním tahem vyhrát
            for s in range(velikost_pole):
                if self.mrizka[r][s] == "":
                    self.mrizka[r][s] = "O"
                    if self.kontrola(r,s,"O",5):
                        self.kresleni_symbol(r, s, "O")
                        self.canvas.unbind("<Button-1>")
                        self.canvas.create_text(280,280,text=f"prohrál jsi",font=("Arial", 70), fill="green")
                        return
                    self.mrizka[r][s] = ""
        
        for r in range(velikost_pole):          #zde se kontroluje zda hráč nemá v řadě 3 a víc symbolů, pokud ano, počítač se pokusí
            for s in range(velikost_pole):      #tuto řadu zkazit
                if self.mrizka[r][s] == "":
                    self.mrizka[r][s] = "X"
                    if self.kontrola(r,s,"X",4) or self.kontrola(r,s,"X",5):
                        self.kresleni_symbol(r,s,"O")
                        self.mrizka[r][s] = "O"
                        return
                    self.mrizka[r][s] = ""
        
        
        nejlepsi_tah1 = (0,0)               #zde program prochazí všechny políčka a pomocí MinMaxu hledá nejlepší, v případě že žádné nenajde
        nejlepsi_tah2 = (0,0)               #tak zvolí políčko s nejvíce symboly v řadě
        nej_skore1= -float("inf")
        nej_skore2 = -float("inf")
        for r in range(velikost_pole):
            for s in range(velikost_pole):
                if self.mrizka[r][s] == "":
                    if self.kontrola_okoli(r,s):        #nemá cenu vyhnocovat políčka co jsou daleko od symbolu
                        self.mrizka[r][s] = "O"
                        skore1, skore2 = self.min_max(False,3 ,"X",r,s)
                        self.mrizka[r][s] = ""
                        if skore1 > nej_skore1:
                            nej_skore = skore1
                            nejlepsi_tah1 = (r,s)
                        if skore2 > nej_skore2:
                            nej_skore = skore1
                            nejlepsi_tah2 = (r,s)

        if nej_skore1 == 0:                
            r,s = nejlepsi_tah2
            self.kresleni_symbol(r,s,"O")
            self.mrizka[r][s] = "O"
        else:
            r,s = nejlepsi_tah1
            self.kresleni_symbol(r,s,"O")
            self.mrizka[r][s] = "O"      
                    
    def min_max(self,max_hrac,hloubka,symbol,r,s):          #MinMax projde vsechny možnosti do hloubky 2 a pomocí konečného stavu oboduje políčko
        if self.kontrola(r,s,symbol,5) and symbol == "O":
            return 10,-float("inf")
        elif self.kontrola(r,s,symbol,5) and symbol == "X":
            return -10,-float("inf")
        elif hloubka == 0 or self.plna_mrizka():
            return 0, self.kontrola(r,s,symbol,5,True)
        
        if max_hrac:
            max_skore = -float("inf")
            for r in range(velikost_pole):
                for s in range(velikost_pole):
                    if self.mrizka[r][s] == "":
                        if self.kontrola_okoli(r,s):
                            self.mrizka[r][s] = symbol
                            skore1,skore2 = self.min_max(False,hloubka - 1,"O",r,s)
                            self.mrizka[r][s] = ""
                            max_skore = max(max_skore,skore1)
            return max_skore,0
        else: 
            min_skore = float("inf")
            for r in range(velikost_pole):
                for s in range(velikost_pole):
                    if self.mrizka[r][s] == "":
                        if self.kontrola_okoli(r,s):
                            self.mrizka[r][s] = symbol
                            skore1, skore2 = self.min_max(True,hloubka - 1,"X",r,s)
                            self.mrizka[r][s] = ""
                            min_skore = min(min_skore,skore2)
            return min_skore,0


    def plna_mrizka(self):          #jednoduchá funkce pro kontrolu, zda je mřížka plná
        for r in self.mrizka:
            if "" in r:
                return False
        return True
    
    def kontrola_okoli(self,r,s):       #kontroluje okolní políčka, zda na nich je symbol
        tahy = [[1,0],[0,1],[1,1],[-1,-1],[1,-1],[-1,1],[-1,0],[0,-1]]
        for tah in tahy:
            if 0 <= r + tah[0] < velikost_pole and 0 <= s + tah[1] < velikost_pole and self.mrizka[r+tah[0]][s+tah[1]] == "O":
                return True
        return False

    def zacatek_hry(self):          #zjišťuje, zda je na hracím poli jen jeden symbol
         pocet = 0
         for r in range(velikost_pole):
             for s in range(velikost_pole):
                 if self.mrizka[r][s] != "":
                     pocet +=1
         if pocet == 1:
             return True
         else:
             return False      
        
okno = tkinter.Tk()
game = hra(okno)
okno.mainloop()      
        








        

