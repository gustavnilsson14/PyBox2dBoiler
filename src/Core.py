import pygame
from pygame.sprite import *
import pygame.display
from Constants import *
import math
import random

def randint( min, max ) :
	return random.randint(min,max)

class Entity :

	def __init__( self, scene ) :
		self.scene = scene
		self.types = [ "entity" ]
		self.body_handler = 0

	def draw( self, screen ) :
		pass
		if self.body_handler == 0 :
			return False
		self.body_handler

	def destroy( self ) :
		if self.body_handler != 0 :
			self.body_handler.destroy()
		return False

class Damage :

	def __init__( self, value, type = DAMAGE_TYPE_PHYSICAL ) :
		self.value = value
		self.type = type

class Image( DirtySprite ) :

	def __init__( self, image, image_handler, align = ALIGN_BOTTOM_CENTER ) :
		DirtySprite.__init__( self )
		self.image_key = image
		self.image_handler = image_handler
		self.image = pygame.Surface((0,0))
		self.buffered_image = 0
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

	def rotate_image( self, image, angle ) :
		angle = math.degrees( angle ) - 90
		if angle != self.current_angle :
			image = image.copy()
			self.current_angle = angle
			self.buffered_image = pygame.transform.rotate( image, self.current_angle )
		return self.buffered_image
<<<<<<< HEAD


	def update( self, position, angle, view_zoom, view_offset, settings ) :
=======
		
		
	def update( self, position, angle, view_zoom, view_offset, settings, scene ) :
>>>>>>> d981e3dac4a0c18b3d7e00880a48bfcf4f3f7ca5
		self.dirty = 1
		posX = ( position[0] * view_zoom ) - view_offset[0]
		posY = ( position[1] * view_zoom ) - view_offset[1]
		posY -= settings.screenSize[ 1 ]
		image = self.image_handler.get_image( self.image_key )

		#Trim images outside of draw area
<<<<<<< HEAD

		if ( posY + (settings.screenSize[1]) ) < 0 :
=======
		if posY < ( image.get_height() / 2) :
			if posY > 0 :
				posY -= posY * 2
			else :
				posY = math.fabs( posY )
		else :
>>>>>>> d981e3dac4a0c18b3d7e00880a48bfcf4f3f7ca5
			self.image = pygame.Surface((0,0))
			return
			'''print posY
			self.image = pygame.Surface((0,0))
			return'''
		
		if posY - ( image.get_height() / 2) > settings.screenSize[1] :
			self.image = pygame.Surface((0,0))
			return
		if ( posX - image.get_width() ) > settings.screenSize[0] :
			self.image = pygame.Surface((0,0))
			return
		if ( posX + image.get_width() ) < 0 :
			self.image = pygame.Surface((0,0))
			return
<<<<<<< HEAD

		if posY < 0 :
			posY = math.fabs( posY )
		else :
			self.image = pygame.Surface((0,0))
			return

=======
		scene.drawn_images += 1
>>>>>>> d981e3dac4a0c18b3d7e00880a48bfcf4f3f7ca5
		if self.current_zoom != view_zoom :
			self.current_zoom = view_zoom
			self.current_angle = -1
			self.image = self.rotate_image( image, angle )
		else :
			self.image = self.rotate_image( image, angle )
		alignment = self.get_alignment( self.image, self.align )
		imgpos = ( posX + alignment[0], posY + alignment[1] )
		self.rect = self.image.get_rect()
		self.rect.x = imgpos[0]
		self.rect.y = imgpos[1]

		if self.tint_duration > 0 :
			tmp = pygame.Surface( self.image.get_size(), pygame.SRCALPHA, 32)
			tmp.fill( self.tint_color )
			self.image.blit(tmp, (0,0), self.image.get_rect(), pygame.BLEND_RGBA_MULT)
			self.tint_duration -= 1

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

class ImageHandler() :

	def __init__( self, game ) :
		self.original_images = {}
		self.zoomed_images = {}
		self.game = game

	def zoom_image( self, image ) :
		zoom = self.game.viewZoom/self.game.defaultZoom/2
		return pygame.transform.scale( image, ( int( image.get_width() * zoom ), int( image.get_height() * zoom ) ) )

	def zoom_images( self ) :
		for key in self.original_images :
			image = self.original_images.get( key )
			self.zoomed_images[ key ] = self.zoom_image( image.copy() )

	def get_image( self, key ) :
		if self.original_images.get( key ) == None :
			image = pygame.image.load( key )
			image = image.convert_alpha()
			self.original_images[ key ] = image
			self.zoomed_images[ key ] = self.zoom_image( image.copy() )
		image = self.zoomed_images.get( key )
		if image != None :
			return image
