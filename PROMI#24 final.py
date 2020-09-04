#PROMI Photomaton + Boulanger
#DUBOIS,DOS SANTOS,DONY

from tkinter import*
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import time


def boulanger(i,j,width,height):
    "Effectue la transfo du boulanger sur un pixel (i,j)"
    x,y = i // 2, 2 * j + i % 2 #étirement
    
    if y < width: #repliage si dans la deuxième moitié
        return x,y
    else:
        return height -1 - x , width - y -1


def photomaton(k,t):#k : coordonnée i ou j , t : self.width ou self.height
    "Effectue la transfo du photomaton sur UN SEUL élément de la coordonnée du pixel (i,j): (soit i soit j)"
    if k%2 == 0:
        return k//2
    else:
        return k//2 + t//2


def rgb_hex(r,g,b):
    '''Convert an RGB color tuple to hex coded color string.'''
    return "#{:02x}{:02x}{:02x}".format(r,g,b)


def extraction_rgb(img):
    "extrait les valeurs rgb d'une image et les mets dans une matrice"
    # get pixels ((r,g,b) tuples) from the image 
    matrix = [[img.get(x,y) for x in range(img.width())]
              for y in range(img.height())]

    # convert (r,g,b) tuples to hex string color codes
    matrix_hex = [[rgb_hex(r,g,b) for (r,g,b) in row] for row in matrix]
    return matrix_hex




class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.transfo = 0
        self.nb_itération = 0

    
    def bouton_p(self):
        "Lors de l'appui sur le bouton photomaton"
        self.new_transfo = photomaton
        self.start()
        
    def bouton_b(self):
        "Appui sur le bouton Boulanger"
        self.new_transfo = boulanger
        self.start()
        
    def choix_fichier(self):
        "Gestion du choix du fichier , création du canvas aux bonnes dimensions avec l'image de départ"
        try:
            self.cnv.delete(ALL)
        except:
            pass
        path = askopenfilename(filetypes=[('GIF FILES','*.gif')])
        self.matrix_hex = extraction_rgb(PhotoImage(file=path))
        self.width , self.height = len(self.matrix_hex[0]) , len(self.matrix_hex)
        self.WIDTH, self.HEIGHT = 8*self.width+6, 8*self.height+6
        self.cnv = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg='white',highlightthickness=0)
        self.cnv.grid(row = 2 , columnspan = 3)
        
        self.matrix_4 = [[x for x in range(self.width*4)] for y in range(self.height*4)]

        for i in range(self.height):
            for j in range(self.width):
                for k in range(4):
                    for l in range(4):
                        self.matrix_4[(i*4)+k][(j*4)+l] = self.matrix_hex[i][j]


        self.img = PhotoImage(width=self.width*4, height=self.height*4)
        self.img.put(data=self.matrix_4 , to=(0,0))   
        self.cnv.create_image(0, 0, image=self.img, anchor=NW)
        
    def initialisation_graphique(self):
        "Création et affichage de l'interface tkinter"
        
        self.txt1 = Label(self).grid(row = 0 , sticky = E)
        self.txt2 = Label(self, text = 'Nombre d\'itérations : ').grid(row = 1 , sticky = E)

        self.entr2 = Entry(self)
        self.entr2.grid(row = 1, column = 1, sticky = W)

        Button(self, text="Quitter", command=self.destroy).grid(row = 1 , column = 2 )
        Button(self, text="Photomaton", command=self.bouton_p).grid(row = 0 , column = 1, sticky = W)
        Button(self, text="Boulanger", command=self.bouton_b).grid(row = 0 , column = 2, sticky = W)
        Button(self, text="Choisir fichier (.gif)", command= self.choix_fichier).grid(row = 0 , sticky = W)
        
            
    def affichage_graphique(self):
        "Affiche l'image finale"
        if self.transfo == photomaton or self.transfo == boulanger:
            self.cnv.delete(ALL)
            self.imgf = PhotoImage(width=self.width*4, height=self.height*4)
            self.img = PhotoImage(width=self.width*4, height=self.height*4)
            
            self.matrix_hex4 = [[x for x in range(self.width*4)] for y in range(self.height*4)]
            self.matrix_4 = [[x for x in range(self.width*4)] for y in range(self.height*4)]
            
            for i in range(self.height):#Grossissement x4
                for j in range(self.width):
                    for k in range(4):
                        for l in range(4):
                            self.matrix_hex4[(i*4)+k][(j*4)+l] = self.matrix_hexf[i][j]
                            
            for i in range(self.height):
                for j in range(self.width):
                    for k in range(4):
                        for l in range(4):
                            self.matrix_4[(i*4)+k][(j*4)+l] = self.matrix_hex[i][j]

            self.img.put(data=self.matrix_4 , to=(0,0))   
            self.cnv.create_image(0, 0, image=self.img, anchor= NW)
            
            self.imgf.put(data=self.matrix_hex4, to=(0,0))
            self.cnv.create_image(self.WIDTH, 0, image=self.imgf, anchor=NE)
            self.cnv.bind('<Button-1>',self.click_handler)

    
    def start(self):
        "Effectue les calculs et les affichages nécessaires au lancement de la transformation"
        
        self.tps = time.clock()
        
        if self.new_transfo != self.transfo:
            self.transfo = self.new_transfo
            tps3 = time.clock()
            self.calcul_période()
            print("(",round(time.clock()-self.tps,2),"s)")
            self.affichage_orbites()
            print("orbites calculées en : ",round(time.clock()-tps3,2),"s")
            self.calcul_n_transfo()
            print(round(time.clock()-self.tps,2),"s")
            self.affichage_graphique()
            self.comparaison()
            print("")

            
        else:
            self.nb_itération = int(self.entr2.get())
            tps3 = time.clock()
            self.affichage_orbites()
            print("orbites calculées en : ",round(time.clock()-tps3,2),"s")
            tps2 = time.clock()
            self.calcul_n_transfo()
            print(round(time.clock()-tps2,2),"s")
            self.affichage_graphique()
            self.comparaison()
            print("")

    def click_handler(self,event):
        "Gestion du clic sur l'image de droite pour afficher les trajectoires"
        self.coord = []
        Trajectoire(self.cnv,self.coord).effacer()
        self.case_click = (event.y//4 , event.x//4)
        
        #Recherche de l'orbite du pixel cliqué
        for k in range(len(self.orbites)):
            if self.case_click in self.orbites[k]:
                print("Orbite du click ",self.case_click,"détectée , taille : ",len(self.orbites[k]))
                Trajectoire(self.cnv,self.orbites[k]).nouveau()
                break

    
    def comparaison(self):
        "Comparaison entre l'image de départ et celle d'arrivée"
        n = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix_hexf[i][j] == self.matrix_hex[i][j]:
                    n += 1

        p = (n*100)//(self.width*self.height)
        print('Pourcentage en commun ', p,"%")

    
    def calcul_n_transfo(self):
        "calcul de la transformation de chaque pixel grâce à son orbite et à la période de celle-ci"
        self.matrix_hexf = [[x+(y*self.width) for x in range(self.width)]for y in range(self.height)]
        print("Calcul de la ",self.nb_itération," ième itération..", end = " ")
        
        for k in range(len(self.orbites)):
            for n in range(len(self.orbites[k])):
                i = self.orbites[k][n][0] #Pour chaque pixel de chaque orbite dans la matrice de départ 
                j = self.orbites[k][n][1]
                x = self.orbites[k][(n+self.nb_itération)%self.période_orbite[i][j]][0] #On avance dans l'orbite de n%p
                y = self.orbites[k][(n+self.nb_itération)%self.période_orbite[i][j]][1] #Pour avoir le pixel d'arrivée
                self.matrix_hexf[x][y] = self.matrix_hex[i][j]


        
    def affichage_orbites(self):
        "Affichage des orbites et calcul des orbites pour photomaton"
        if self.transfo == photomaton:
            self.orbites = []
            self.période_orbite = [[x*0 for x in range(self.width)]for y in range(self.height)]
            for i in range(self.height):
                for j in range(self.width):
                    if self.période_orbite[i][j] == 0:
                        self.calcul_orbite(i,j)
        n = 0
        mini = 1
        maxi = 0
        if len(self.orbites) <= 20:
            for z in range(len(self.orbites)):
                n += 1
                print(self.orbites[z][0],"orbite N°",n,"de taille",len(self.orbites[z]))
        else:
            for z in range(len(self.orbites)):
                if maxi < len(self.orbites[z]):
                    maxi =len(self.orbites[z])
                if mini > len(self.orbites[z]):
                    mini = len(self.orbites[z])
                    
            print(len(self.orbites)," orbites de tailles allant de ",mini," à ",maxi)



    def pgcd(self,p,k):
        "calcul du pgcd de p et k"
        self.p , self.k = p,k
        if self.k==0:
            return self.p
        else:
            self.r=self.p%self.k
            return self.pgcd(self.k,self.r)

        
    def ppcm(self,p,k):
        "Calcul du ppcm de p et k"
        self.p , self.k = p,k
        return (self.p*self.k)//self.pgcd(self.p,self.k)

 
    def calcul_période(self):
        "Calcul de la période de la matrice complète"
        
        print("Image de taille :",self.width,"x",self.height,"(",self.width*self.height,"pixels)")
        if self.transfo == photomaton:
            print("Photomaton")
            self.période, t = 1, 2 #compteur du nombre de passage dans la boucle , t=2^n,
            #si on considère une image de taille hxL
            #il est prouvé dans la partie maths que la période de la transformation du photomaton
            #est le plus petit entier n pour lequel h−1 et L−1 divisent 2n−1.
            
            while (t-1)%(self.width-1) != 0 or (t-1)%(self.height-1) !=0:
                self.période += 1
                t *= 2

            print("La période est ",self.période, end = " ")
            
        else:
            print("Boulanger")
            print("Calcul des orbites..", end = " ")
            t = time.clock()
            self.période_orbite = [[x*0 for x in range(self.width)]for y in range(self.height)]
            self.orbites = []
            for i in range(self.height):
                for j in range(self.width):
                    if self.période_orbite[i][j] == 0: #Si le pixel n'est dans aucune orbite
                        self.calcul_orbite(i,j) #On calcule l'orbite et sa taille
            
            print(round(time.clock()-t,2),"s")
            print("Décomposition des périodes des orbites..")
            self.decomp_ppcm = [] #liste des décomposition des périodes
            #suppression des doublons dans self.orbite si il y en a
            for k in range(1,len(self.orbites)):
                self.orbite_sans_doubles = []
                for i in self.orbites[k]:
                    if i not in self.orbite_sans_doubles:
                        self.orbite_sans_doubles.append(i)

                #Décomposition de la longueur des orbites en produit de facteurs premiers
                for i in range(len(self.decomp_liste(len(self.orbite_sans_doubles)))):
                    self.decomp_ppcm.append((self.decomp_liste(len(self.orbite_sans_doubles))[i][0],self.decomp_liste(len(self.orbite_sans_doubles))[i][1]))
            
            print("Calcul de la période...")
            self.liste_facteurs = []
            self.liste_puissances = []
            #Décomposition du ppcm
            for i in range(len(self.decomp_ppcm)):#si facteur non présent ou (facteur présent et puissance supérieure)
                if self.decomp_ppcm[i][0] not in self.liste_facteurs:
                        self.liste_facteurs.append(self.decomp_ppcm[i][0])
                        self.liste_puissances.append(self.decomp_ppcm[i][1])
                else:
                    if self.decomp_ppcm[i][1] >= self.liste_puissances[self.liste_facteurs.index(self.decomp_ppcm[i][0])]:
                       self.liste_puissances[self.liste_facteurs.index(self.decomp_ppcm[i][0])] = self.decomp_ppcm[i][1]
            

            self.période = 1
            #Calcul de la période par la méthode du produit des décomposition du ppcm
            for i in range(len(self.liste_facteurs)):
                self.période *= self.liste_facteurs[i]**self.liste_puissances[i]

            print("La période est ",self.période)
            return self.orbites , self.période
            
            
    def calcul_orbite(self,i,j):
        "Permet de calculer l'orbite de i,j"
        self.orbite = []
        
        if self.transfo == boulanger:
            n = 1
            self.orbite.append((i,j))
            x1,y1 = self.transfo(i,j,self.width,self.height)
            if y1 < 0:
                    y1 += self.width 
            while (x1,y1) != (i,j): #Tant qu'on a pas fais le tour de l'orbite on continue
                n += 1 #On incrémente la taille de l'orbite
                if y1 < 0:
                    y1 += self.width
                self.orbite.append((x1,y1))
                x1,y1 = self.transfo(x1,y1,self.width,self.height)# on cherche les coordonnées du pixel suivant d l'orbite
                
            
            self.orbites.append(self.orbite)
            for z in self.orbite:#On associe la longueur/période de l'orbite à chaque pixel de celle-ci 
                (i,j) = z
                self.période_orbite[i][j] = n
                
        else:
            n = 1
            self.orbite.append((i,j))
            x1,y1 = self.transfo(i,self.height), self.transfo(j,self.width)
            while (x1,y1) != (i,j):
                n += 1 
                self.orbite.append((x1,y1)) 
                x1,y1 = self.transfo(x1,self.height) , self.transfo(y1,self.width)

            self.orbites.append(self.orbite)
            for z in self.orbite:#On associe la longueur/période de l'orbite à chaque pixel de celle-ci 
                (i,j) = z
                self.période_orbite[i][j] = n
            
            
    def decomp(self,n):
        "on décompose n (longueur de l'orbite) en produit de facteurs premiers"
        self.n = n
        self.a = 2
        while self.a**2 <= self.n: #On essaye les facteurs jusqu'à racine de n 
            if self.n%self.a == 0:
                return [self.a] + self.decomp(self.n//self.a)
            self.a += 1
        return [self.n]

    def decomp_liste(self,n):
        "Création d'une liste du type [(facteur0,puissance0),(facteur1,puissance1),....]"
        #sorted() tri la liste dans l'ordre , set() pareil ,
        #x.count(y) compte le nombre de fois ou y apparait dans x
        self.n = n
        self.l = self.decomp(self.n)
        return sorted(set((self.n,self.l.count(self.n)) for self.n in self.l))


    

class Trajectoire(Application):
    def __init__(self,cnv,coord):
        self.cnv , self.coord  = cnv , coord 
        
    def nouveau(self):
        "Affiche la trajectoire du pixel selectionné"
        for k in range(len(self.coord)-1) :
            j = self.coord[k][0]
            i = self.coord[k][1]
            y = self.coord[k+1][0]
            x = self.coord[k+1][1]
            self.cnv.create_line(4*i+2,4*j+2,4*x+2,4*y+2,width=1, fill = 'white',tag = 'ligne')
            self.cnv.create_oval(4*i ,4*j ,4*i+3,4*j+3,fill = 'white',outline ='white',tag = 'point')

        j = self.coord[-1][0] #On boucle l'orbite 
        i = self.coord[-1][1]
        y = self.coord[0][0]
        x = self.coord[0][1]
        self.cnv.create_line(4*i+2,4*j+2,4*x+2,4*y+2,width=1, fill = 'white',tag = 'ligne')


    def effacer(self):
        "Efface toutes les trajectoires précédentes "
        self.cnv.delete('ligne')
        self.cnv.delete('point')


        
app = Application()
app.initialisation_graphique()
app.mainloop()
