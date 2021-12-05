import pygame


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

class Message(object):
    def __init__(self, text, x=0, y=0, width=100, height=50):
        self.text = text
        
        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(BLACK)
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        font = pygame.font.SysFont("constantia", 30)
        
        text_image = font.render(text, True, WHITE)
        text_rect = text_image.get_rect(center = self.rect.center)
        self.image_normal.blit(text_image, text_rect)

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)

    def update(self):
    
        self.image = self.image_normal
        
    def draw(self, surface):

        surface.blit(self.image, self.rect)