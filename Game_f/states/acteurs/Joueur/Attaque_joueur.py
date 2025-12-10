
import os,sys
import json

#parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#sys.path.append(parent_dir)





class Attaque_joueur:

    

    attaque_id = ""
    attack_PA = ""
    attack_for = ""
    attack_effet = ""
    attack_cast = ""
    attack_CD = ""
    Portee = ""
    #Sprite =
    # attack_name,attack_PA,attack_for,attack_effet,attack_cast,attack_CD,Portee,
    
    def __init__(self,stat_file = "Data/statistique/Skill.json",index = 0):
        self.statistique = stat_file
        self.index = index
        

        self.get_data()
        self.names = []
        self.stat = {}
        self.PA = []

        for names in self.data['skills']:
            self.names.append(names['Nom'])
            self.stat[names['Nom']] = names['stat']

  
        
        

    def get_data(self):
        try :

            with open(self.statistique,'r') as file:
                self.data = json.load(file)
                

        except FileNotFoundError:
            print("le fichier d'Attaque du joueur n'a pas été trouvé")

    

    def print(self):
        print (f"Task({self.attack_name}, {self.attack_PA}, {self.attack_PA}, {self.attack_for})")
        return f"Task({self.attack_name}, {self.attack_PA}, {self.attack_PA}, {self.attack_for})"
    

    


    
    
    def to_json(self):
        """Converts the task to a JSON serializable dictionary."""
        return {
                   "Nom" : self.attack_name,
                   "PA":self.attack_PA,
                   "FOR": self.attack_for,
                   "effet" : self.attack_effet,
                   "Cas" : self.attack_cast,
                   "CD": self.attack_CD,
                   "Portee":self.Portee
                   #"sprite": ""
        }
    
    def from_json(json_data):
        """Creates a task instance from a JSON serializable dictionary."""
        attack = Attaque_joueur(json_data['Nom'], json_data['PA'],json_data["FOR"],json_data["effet"],json_data["Cas"],json_data["CD"],json_data["Portee"])
        attack.attack_id = json_data['task_id']
        
        attack.attack_id = json_data['index']
        return attack


