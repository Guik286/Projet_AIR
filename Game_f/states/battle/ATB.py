import pygame
from Data.settings import SCREENWIDTH, SCREENHEIGHT, lenATB, widATB



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




