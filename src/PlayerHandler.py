from Util import *

class PlayerHandler :
	
	def __init__( self, game ) :
		self.game = game
		self.player_list = []
		self.input_list = []
		
	def update( self, keys ) :
		for player in self.player_list :
			player.update()
		for input in self.input_list :
			input.run( keys )
			
	def add_input( self, new_input ) :
		for input in self.input_list :
			if input.key == new_input.key :
				return False
		self.input_list += [ new_input ]
		return True
		
	def add_player( self, new_player ) :
		for player in self.player_list :
			if player.character == new_player.character :
				return False
		self.player_list += [ new_player ]
		
class Player :
	
	def __init__( self, game, character ) :
		self.game = game
		self.character = character
		
	def update( self ) :
		self.character.movement_vector = ( 0, 0 )
		return True
		
	def move_up( self ) :
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( current_vector[0], 1 )
			return True
		return False
		pass
		
	def move_down( self ) :
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( current_vector[0], -1 )
			return True
		return False
		
	def move_right( self ) :
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( 1, current_vector[1] )
			return True
		return False
		
	def move_left( self ) :
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( -1, current_vector[1] )
			return True
		return False
		
	def pickup( self ) :
		if self.character.alive == True :
			pos = self.character.body.transform.position
			for body in self.game.world.bodies :
				if body.userData == None :
					continue
				owner = body.userData.get( 'owner' )
				if owner == None :
					continue
				for item in self.character.body_handler.find_items() :
					if item.body == body :
						continue
					if 'item' in owner.types :
						if owner.holder != 0 :
							continue
						target = body.transform.position
						if get_distance_between_points( pos, target ) < 1 :
							print owner
							self.character.body_handler.attach_item( 'right_arm', owner )
							self.character.set_current_item( 'weapon' )
							return True
		return False
	
	def turn( self ) :
		if self.character.alive == True :
			mouse_pos = self.game.MousePos()
			mouse_pos = ( mouse_pos[0], convert_y_axis( mouse_pos[1], self.game.settings.screenSize[ 1 ] ) )
			abs_mouse_pos = ( mouse_pos[0] + self.game.viewOffset[0], mouse_pos[1] + self.game.viewOffset[1] )
			abs_mouse_pos = ( abs_mouse_pos[0] / self.game.viewZoom, abs_mouse_pos[1] / self.game.viewZoom )
			self.character.aim( abs_mouse_pos )
			return True
		return False
	
	def use_item( self ) :
		if self.character.alive == True :
			self.character.use_current_item( 0 )
			return True
		return False
		
class Input :
	
	def __init__( self, player, key, function, repeat = True ) :
		self.player = player
		self.key = key
		self.function = function
		self.repeat = repeat
		
	def run( self, keys ) :
		if self.key in keys :
			self.function()
			if self.repeat == False :
				self.player.game.pressed_keys.remove( self.key )
			return True
		return False
