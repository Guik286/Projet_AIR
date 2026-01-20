import pygame
from Data.settings import SCREENWIDTH, SCREENHEIGHT, lenATB, widATB
from Game_f.mechs.logique.LogiqueCombat.Point2D import Acteur



class ATB:
    def __init__(self,Nom,length,width,color,x,y):
        self.Nom = Nom
        self.lenATB = length
        self.widATB = width
        self.color = pygame.Color(color)
        self.x = x
        self.y = y

        
    
    def draw_ATB(self,surface):

        
        
        pygame.Rect((self.x,self.y),(self.widATB,self.lenATB))
        pygame.draw.rect(surface,self.color,pygame.Rect((self.x,self.y),(self.widATB,self.lenATB))) 




### Parametres graphique :

Battle_screen = []


#Cooldown
ATBcd = pygame.Rect(((SCREENWIDTH/3)-widATB,5*lenATB/6),(widATB,lenATB/6))
ATBrflx = pygame.Rect(((SCREENWIDTH/3)-widATB,4* lenATB/6),( widATB, lenATB/6))
ATBurg = pygame.Rect(((SCREENWIDTH/3)-widATB,3*lenATB/6),(widATB,lenATB/6))
ATBcom = pygame.Rect(((SCREENWIDTH/3)-widATB,2*lenATB/6),(widATB,lenATB/6))
ATBreflechi = pygame.Rect(((SCREENWIDTH/3)- widATB,1* lenATB/6),( widATB, lenATB/6))
ATBreso = pygame.Rect(((SCREENWIDTH/3)- widATB,0),( widATB, lenATB/6))

Battle_screen.append(ATB("BarreATBtotale",lenATB,widATB,"black",(SCREENWIDTH/3)-widATB,0))
Battle_screen.append(ATB("Cooldown",lenATB/6,widATB,"gray",(SCREENWIDTH/3)-widATB,5*lenATB/6))
Battle_screen.append(ATB("Reflexe",lenATB/6,widATB,"red",(SCREENWIDTH/3)-widATB,4* lenATB/6))
Battle_screen.append(ATB("Urgence",lenATB/6,widATB,"orange",(SCREENWIDTH/3)-widATB,3*lenATB/6))
Battle_screen.append(ATB("Combat",lenATB/6,widATB,"lightblue",(SCREENWIDTH/3)-widATB,2*lenATB/6))
Battle_screen.append(ATB("Reflechir",lenATB/6,widATB,"blue",(SCREENWIDTH/3)- widATB,1* lenATB/6))
Battle_screen.append(ATB("Resolution",lenATB/6,widATB,"green",(SCREENWIDTH/3)- widATB,0))




### Je veux creer une classe ATB permettant de gerer les differentes phase de jeu des acteurs en combat

class ATBlogique:
    def __init__(self,Acteur,dt):
        ### On part sur un système à la Grandia dans un premier temps
        ## Cooldown : l'acteur ne peut que subir
        ## Action Acteur : l'acteur peut choisir son action, les points de PA se remplissent
        # au fur et à mesure, débloquant différentes actions en fonction du nombre de PA
        ## Resolution : l'acteur exécute son action, cette action peut être interrompue si l'acteur subit selon des paramètres à définir (CC, KB, etc..)
        self.Etat_Temporel = ["Cooldown","Action_Acteur","Resolution"]
        self.ET_Actuel = self.Etat_Temporel[0]
        self.chrono_CD = 0
        self.chrono_R = 0
        self.wait = False
        self.dt = dt
        self.acteur = Acteur
        self.seuil_resolution = 5 # à définir plus tard

        ## On divise en deux chronos distincts pour plus de clarté
        ## un Chrono pour le cooldown
        ## un Chrono pour la resolution de l'action
        # quand le chrono du cooldown atteint le max, on passe à la phase d'action acteur
        # l'acteur choisi son action, puis on passe à la phase de resolution
        # durant la phase de resolution, le chrono de resolution s'active (entre 0 et ) 



        ## Dans grandia on a une phase de cooldown, l'action du joueur quand le temps
        ## est egale à un certain seuil, et la resolution de l'action
        self.index_phase = 0

    def calcul_temps_CD(self,dt):
        
        
        ## Si un signal stop, le temps de l'acteur s'arrête
        if self.acteur.wait:
            pass
        elif self.chrono_CD >= self.acteur.Etats["tps_max"]:
            self.index_phase += 1
            self.ET_Actuel =self.Etat_Temporel[self.index_phase] # Action joueur
            self.chrono_CD = self.acteur.Etats["tps_max"]
            self.acteur.wait = True # on maintien le chrono au max entre le cooldown et la resolution

        ## Si on est durant le cooldown
        else:
            self.chrono_CD += self.dt * self.acteur.Etats["modif"] #(*une variable de contingence)
        

    def calcul_temps_resolution(self,dt):

        if self.acteur.wait or self.ET_Actuel != "Resolution":
            pass
        else:
            self.chrono_R += self.dt
            if self.chrono_R >= self.seuil_resolution:
                self.chrono_R = self.acteur.Etats["tps_max"]
                self.index_phase = 0
                self.chrono_CD = 0
                self.chrono_R = 0
                self.ET_Actuel =self.Etat_Temporel[self.index_phase] # Cooldown
                self.acteur.wait = False

        


        
          # Index de la phase actuelle




