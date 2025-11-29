

class toto:
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
    
class arene:
    def __init__(self):
        self.tab = [[None] * 3  for i in range(3)]


    def print_arene(self):
        for row in self.tab:
            print("-------------------------")
            a = ""
            for col in row:
                
                a += "|"
                if col :
                    a += col.name
                    
                else:
                    a += "00"
            print(a + "|")


toto1 = toto(1,1,"t1")
toto2 = toto(2,2,"t2")


arena = arene()
arena.tab[1][1] = toto1
arena.tab[2][2] = toto2
arena.print_arene()


