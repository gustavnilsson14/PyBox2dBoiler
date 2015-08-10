from Util import *
from Unit import *
import os, sys
import pygame

class PlayerHandler :
	
	def __init__( self, game ) :
		self.game = game
		self.player_list = []
		self.input_list = []
		self.joystick_list = []
		
	def update( self, keys ) :
		for player in self.player_list :
			player.update()
		for input in self.input_list :
			input.run( keys )
		self.check_player_opt_in( keys )
		
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
		new_player.character = PlayerCharacter( self.game.current_scene, self.game.current_scene.get_spawn_point() )
		self.game.current_scene.add_entity( new_player.character )
		self.game.current_scene.hud.add_player( new_player )
		self.game.current_scene.screen.focus_positions += [ new_player.character.body.transform.position ]
		
	def clear_input( self ) :
		while len( self.input_list ) != 0 :
			self.input_list.remove( self.input_list[0] )
	
	def add_keyboard_mouse_input( self, player ) :
		self.add_input( Input( player, Keys.K_m, player.change_scene ) )
		self.add_input( Input( player, Keys.K_RETURN, player.respawn ) )
		self.add_input( Input( player, Keys.K_w, player.move_up ) )
		self.add_input( Input( player, Keys.K_s, player.move_down ) )
		self.add_input( Input( player, Keys.K_a, player.move_left ) )
		self.add_input( Input( player, Keys.K_d, player.move_right ) )
		self.add_input( Input( player, Keys.K_e, player.pickup, False ) )
		self.add_input( Input( player, -100, player.turn ) )
		self.add_input( Input( player, -101, player.use_item ) )
	
	def add_joystick_input( self, player, joystick ) :
		self.add_input( Input( player, joystick.get_id() - 1000, player.joystick ) )
		self.game.pressed_keys += [joystick.get_id() - 1000]
		
	def check_player_opt_in( self, keys ) :
		if keys.__contains__( Keys.K_RETURN ) and self.keyboard_mouse_player_exists() == False :
			player = Player( self.game )
			self.add_player( player )
			self.add_keyboard_mouse_input( player )
		for joystick in self.joystick_list :
			start = joystick.get_button( JOYSTICK_BUTTON_START )
			if start == 1 and self.joystick_player_exists( joystick ) == False :
				player = Player( self.game, joystick )
				self.add_player( player )
				self.add_joystick_input( player, joystick )
	
	def keyboard_mouse_player_exists( self ) :
		for player in self.player_list :
			if player.input_type == INPUT_TYPE_KEYBOARD_MOUSE :
				return True
		return False
		
	def joystick_player_exists( self, joystick ) :
		for player in self.player_list :
			if player.input_type == joystick :
				return True
		return False
		
class Player :
	
	def __init__( self, game, input_type = INPUT_TYPE_KEYBOARD_MOUSE, character = 0 ) :
		self.input_type = input_type
		self.game = game
		self.character = character
		
	def update( self ) :
		if self.character != 0 :
			self.character.movement_vector = ( 0, 0 )
			return True
		return False
				
	def change_scene( self ) :
		self.game.change_scene( "res/maps/compiled_map1.js" )
					
	def move_up( self ) :
		if self.character == 0 :
			return False
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( current_vector[0], 1 )
			return True
		return False
		
	def move_down( self ) :
		if self.character == 0 :
			return False
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( current_vector[0], -1 )
			return True
		return False
		
	def move_right( self ) :
		if self.character == 0 :
			return False
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( 1, current_vector[1] )
			return True
		return False
		
	def move_left( self ) :
		if self.character == 0 :
			return False
		if self.character.alive == True :
			current_vector = self.character.movement_vector
			self.character.movement_vector = ( -1, current_vector[1] )
			return True
		return False
		
	def pickup( self ) :
		if self.character == 0 :
			return False
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
		if self.character == 0 :
			return False
		if self.character.alive == True :
			mouse_pos = self.game.MousePos()
			mouse_pos = ( mouse_pos[0], convert_y_axis( mouse_pos[1], self.game.settings.screenSize[ 1 ] ) )
			abs_mouse_pos = ( mouse_pos[0] + self.game.viewOffset[0], mouse_pos[1] + self.game.viewOffset[1] )
			abs_mouse_pos = ( abs_mouse_pos[0] / self.game.viewZoom, abs_mouse_pos[1] / self.game.viewZoom )
			self.character.aim( abs_mouse_pos )
			return True
		return False
	
	def use_item( self ) :
		if self.character == 0 :
			return False
		if self.character.alive == True :
			self.character.use_current_item( 0 )
			return True
		return False
		
	def respawn( self ) :
		if self.character.alive == True :
			return False
		self.character = PlayerCharacter( self.game.current_scene, self.game.current_scene.get_spawn_point() )
		self.game.current_scene.add_entity( self.character )
		
	def joystick( self ) :
		if self.character == 0 :
			return
		joystick = self.input_type
		if self.character.alive == True :
			movement_vector = ( joystick.get_axis( JOYSTICK_AXIS_HORIZONTAL_MOVE ), -joystick.get_axis( JOYSTICK_AXIS_VERTICAL_MOVE ) )
			self.character.movement_vector = (0,0)
			if movement_vector[ 0 ] > 0.4 or movement_vector[ 1 ] > 0.4 or movement_vector[ 0 ] < -0.4 or movement_vector[ 1 ] < -0.4 :
				self.character.movement_vector = movement_vector
				
			character_pos = self.character.body.transform.position
			angle_vector = ( joystick.get_axis( JOYSTICK_AXIS_HORIZONTAL_TURN ) + character_pos[0], -joystick.get_axis( JOYSTICK_AXIS_VERTICAL_TURN ) + character_pos[1])
			if angle_vector[ 0 ] > 0.4 or angle_vector[ 1 ] > 0.4 or angle_vector[ 0 ] < -0.4 or angle_vector[ 1 ] < -0.4 :
				self.character.aim( angle_vector )
			
			if joystick.get_button( JOYSTICK_BUTTON_USE ) == 1 :
				self.use_item()
			
			if joystick.get_button( JOYSTICK_BUTTON_PICKUP ) == 1 :
				self.pickup()
		else :
			if joystick.get_button( JOYSTICK_BUTTON_START ) == 1 :
				self.respawn()
			
		
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
