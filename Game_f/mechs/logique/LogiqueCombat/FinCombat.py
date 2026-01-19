

#### Conditions de sortie vers Fin
def Defaite(level):
    if level.player.etat == "mort":
        level.next_state = "GAME_OVER"
        level.done = True

def Fin_Joueur(level):
    level.player.mort()
    Defaite(level)

#### fin adversaire

def Ennemi_out(level):
    for i in range(0,len(level.Ennemis),1):

        if level.Ennemis[i].lp <= 0:
            level.Ennemis[i].mort()
            level.Ennemis.pop(i)
            level.couleur_E.pop(i+1)
            level.Index_cible = 0
            
            break

### Conditions de sortie vers suite


def Victoire(level):

    if level.Ennemis == []:
        level.next_state = "Victoire"
        level.done = True
        #Recharge pour le niveau suivant
        
        level.player.experience += 1
        print("Exp +1 ! Total :",level.player.experience)

