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
		
	def blink( self, duration = 8, color = ( 64,64,64,255 ) ) :
		self.tint_duration = duration
		self.tint_color = color
		
	def get_current_image( self, zoom, angle ) :
		image = pygame.transform.scale( self.current_image, ( int( self.current_image.get_width() * zoom ), int( self.current_image.get_height() * zoom ) ) )
		image = pygame.transform.rotate(image, angle)
		if self.tint_duration > 0 :
			image = image.convert_alpha()
			tmp = pygame.Surface( image.get_size(), pygame.SRCALPHA, 32)
			tmp.fill( self.tint_color )
			image.blit(tmp, (0,0), image.get_rect(), pygame.BLEND_RGBA_MULT)
			self.tint_duration -= 1
		return image
