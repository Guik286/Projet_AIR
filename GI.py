import pygame




class GraphicInterface:
    def __init__(self, texte ,txt_index,rect_texte):
        self.texte  = texte
        self.index = txt_index
        self.rect_texte = rect_texte
        self.color = (0,0,0)
        self.rect = pygame.Rect((0,0),(0,0))
        self.font = pygame.font.Font(None, 50)
        



    def render_text(self,index):  
        self.color = pygame.Color("red") if index == self.index else pygame.Color("white")
        return self.font.render(self.texte[index], True, self.color)  
    
    def get_text_position(self,index):
        center = (self.rect_texte.centerx, self.rect_texte.top + 50 + (index * 100))
        return self.render_text(index).get_rect(center=center)
    
    def draw(self,surface):
        for index, option in enumerate(self.texte):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(index))
