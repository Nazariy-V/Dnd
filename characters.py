import pygame
import dnd_character
SHEET_SIZE=(384,256)
UNIT_SIZE=(32,32)
def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return
def get_standing(sheet,unit):
    return clip(pygame.image.load(f"assets/characters/{sheet}.png"),unit[0]*96,unit[1]*128,UNIT_SIZE[0],UNIT_SIZE[1])
def get_moving(sheet,unit,direction):#direction is clockwise from looking at player
    return [clip(pygame.image.load(f"assets/characters/{sheet}.png"),unit[0]*96+32,unit[1]*128+32*direction,UNIT_SIZE[0],UNIT_SIZE[1]),
            clip(pygame.image.load(f"assets/characters/{sheet}.png"),unit[0]*96+64,unit[1]*128+32*direction,UNIT_SIZE[0],UNIT_SIZE[1])]