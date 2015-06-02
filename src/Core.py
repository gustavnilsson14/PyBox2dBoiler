import pygame
from pygame.sprite import *
import pygame.display
from Constants import *
import math

class Entity :
	
	def __init__( self, scene ) :
		self.scene = scene
		self.types = [ "entity" ]
		self.body_handler = 0
		
	def draw( self, screen ) :
		if self.body_handler == 0 :
			return False
		self.body_handler
		
class Image( DirtySprite ) :
	
	def __init__( self, image, align = ALIGN_BOTTOM_CENTER ) :
		DirtySprite.__init__( self )
		self.original_image = pygame.image.load( image )
		self.zoomed_image = self.original_image.copy()
		self.rotated_image = self.zoomed_image.copy()
		self.image = self.rotated_image.copy()
		self.rect = self.image.get_rect()
		self.align = align
		self.tint_duration = 0
		self.tint_color = 0
		self.current_angle = -1
		self.current_zoom = -1
		self.dirty = 1
		
	def blink( self, duration = 8, color = ( 64,64,64,255 ) ) :
		self.tint_duration = duration
		self.tint_color = color
		
	def scale_image( self, zoom ) :
		if self.current_zoom != zoom :
			self.current_zoom = zoom
			return pygame.transform.scale( self.original_image, ( int( self.original_image.get_width() * self.current_zoom ), int( self.original_image.get_height() * self.current_zoom ) ) )
		return self.zoomed_image
		
	def rotate_image( self, angle ) :
		angle = math.degrees( angle ) - 90
		if angle != self.current_angle :
			return pygame.transform.rotate( self.zoomed_image, int( self.current_angle ) )
		return self.rotated_image
		
	def clip_image( self, view_zoom, view_offset, default_zoom, settings ) :
		return self.rotated_image
		
	def update( self, position, angle, view_zoom, view_offset, default_zoom, settings ) :
		self.dirty = 1
		zoom = view_zoom/default_zoom/2
		
		self.zoomed_image = self.scale_image( zoom )
		self.rotated_image = self.rotate_image( angle )
		self.image = self.clip_image( view_zoom, view_offset, default_zoom, settings )
		
		if self.tint_duration > 0 :
			self.image = self.image.convert_alpha()
			tmp = pygame.Surface( self.image.get_size(), pygame.SRCALPHA, 32)
			tmp.fill( self.tint_color )
			self.image.blit(tmp, (0,0), self.image.get_rect(), pygame.BLEND_RGBA_MULT)
			self.tint_duration -= 1
		posX = ( position[0] * view_zoom ) - view_offset[0]
		posY = ( position[1] * view_zoom ) - view_offset[1]

		posY -= settings.screenSize[ 1 ]
		if posY < 0 :
			posY = math.fabs( posY )
		else :
			self.image = pygame.Surface((0,0))

		alignment = self.get_alignment( self.image, self.align )
		
		imgpos = ( posX + alignment[0], posY + alignment[1] )
		self.rect = self.image.get_rect()
		self.rect.x = imgpos[0]
		self.rect.y = imgpos[1]
		
	def get_alignment( self, image, align ) :
		if align == ALIGN_BOTTOM_CENTER :
			return ( -( image.get_width() / 2 ), -image.get_height() )
		elif align == ALIGN_CENTER_CENTER :
			return ( -( image.get_width() / 2 ), -( image.get_height() / 2 ) )
		elif align == ALIGN_TOP_CENTER :
			return ( -( image.get_width() / 2 ), -0 )
		elif align == ALIGN_TOP_LEFT :
			return ( -0, -0 )
		elif align == ALIGN_BOTTOM_RIGHT :
			return ( -image.get_width(), -image.get_height() )
		
		
