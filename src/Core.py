import pygame
import pygame.display
from Constants import *

class Entity :
	
	def __init__( self, scene ) :
		self.scene = scene
		self.types = [ "entity" ]

class Image :
	
	def __init__( self, image, align = ALIGN_BOTTOM_CENTER ) :
		self.current_image = pygame.image.load( image )
		self.align = align
		self.tint_duration = 0
		self.tint_color = 0
		
	def blink( self, duration = 2, color = ( 255,255,255,255 ) ) :
		self.tint_duration = duration
		self.tint_color = color
		
	def get_current_image( self, zoom ) :
		image = pygame.transform.scale( self.current_image, ( int( self.current_image.get_width() * zoom ), int( self.current_image.get_height() * zoom ) ) )
		
		if self.tint_duration > 0 :
			image = image.convert_alpha()
			tmp = pygame.Surface( image.get_size(), pygame.SRCALPHA, 32)
			tmp.fill( (255,0,0,255) )
			image.blit(tmp, (0,0), image.get_rect(), pygame.BLEND_RGBA_MULT)
			self.tint_duration -= 1
			#self.tint_duration = self.tint_duration - 1
			#image.fill((10,10,10), pygame.BLEND_ADD_RGB)
			
			#inv = pygame.Surface(image.get_rect().size, pygame.SRCALPHA)
			#inv.fill((255,255,255,255))
			#image.blit(inv, (0,0), None, pygame.BLEND_RGB_SUB)
			
			#tint_image.fill( self.tint_color )
			#image.blit( tint_image, (0,0) )
		return image
