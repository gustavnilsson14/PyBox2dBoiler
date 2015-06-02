from Map import *
from Unit import *
from Order import *
from PlayerHandler import *
from random import randint
import pygame
from Constants import *

class Scene :
    
    def __init__( self, game, world, scene_data ) :
        self.entity_list = []
        self.orders = []
        self.game = game
        self.world = world
        self.map = Map( self, world, scene_data.get( 'grid' ) )
        self.update_list = []
        self.screen = Screen( game )
        self.sprite_group = pygame.sprite.LayeredDirty()
        
        image = Image( "res/img/environment/default.png", ALIGN_BOTTOM_CENTER )
        self.sprite_group.add( image )
        #self.add_update( Update( self.screen.screen_shake, 250, 10, 2 ) )
        
        #unit.move( (23,20) )
        
        
        self.target_unit = PlayerCharacter( self, ( 44,40 ) )
        self.screen.center_position = self.target_unit.body.transform.position
        player1 = Player( self.game, self.target_unit )
        self.game.player_handler.add_player( player1 )
        self.game.player_handler.add_input( Input( player1, Keys.K_w, player1.move_up ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_s, player1.move_down ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_a, player1.move_left ) )
        self.game.player_handler.add_input( Input( player1, Keys.K_d, player1.move_right ) )
        self.game.player_handler.add_input( Input( player1, -100, player1.turn ) )
        self.game.player_handler.add_input( Input( player1, -101, player1.use_item ) )
        
        
        unit = Character( self, ( 40,25 ) )
        self.add_entity( unit )
        self.add_entity( self.target_unit )
        self.orders.append( AttackOrder( [ unit ], self.target_unit ) )
    
    def draw( self, view_zoom, view_offset, default_zoom, settings ) :
        rects = []
        for sprite in self.sprite_group :
            sprite.update( (20,20), 0, view_zoom, view_offset, default_zoom, settings )
        rects += self.sprite_group.draw( self.game.screen )
        for entity in self.entity_list :
            body = entity.body_handler
            if body != 0 :
                body.update_images( view_zoom, view_offset, default_zoom, settings )
                rects += body.sprite_group.draw( self.game.screen )
        pygame.display.update( rects )
        return
    
    def add_entity( self, entity ) :
        if self.entity_list.__contains__( entity ) :
            return False
        self.entity_list.append( entity )
        self.add_update( Update( entity, entity.update ) )
        
    def remove_entity( self, entity ) :
        if self.entity_list.__contains__( entity ) == False :
            print entity.__class__.__name__ + " ALREADY GONE"
            return False
        self.entity_list.remove( entity )
        for update in self.update_list :
            if update.owner == entity :
                self.remove_update( update )
        self.game.add_garbage_body( entity.body )
    
    def add_update( self, update ) :
        if update == None :
            return False
        if self.update_list.__contains__( update ) :
            return False
        self.update_list.append( update )
        return True
        
    def remove_update( self, update ) :
        if self.update_list.__contains__( update ) :
            self.update_list.remove( update )
            return True
        return False
        
    def Step( self ) :
        for update in self.update_list :
            update.run()
        self.screen.update_camera_center()
    
    def destroy( self ) :
        self.world.ClearForces()
        while len( self.world.bodies ) != 0 :
            self.world.destroyBody( self.world.bodies[0] )

class Screen :
    
    def __init__( self, game, shake_magnitude = 20 ) :
        self.game = game
        self.shake_offset = (0,0)
        self.shake_magnitude = shake_magnitude
        self.center_position = 0
        self.shake_time = 0
        
    def update_camera_center( self ) :
        self.game.setCenter( self.center_position )
        if self.shake_time > 0 :
            self.shake_offset = ( randint(-self.shake_magnitude,self.shake_magnitude), randint(-self.shake_magnitude,self.shake_magnitude) )
            self.game._viewOffset[ 0 ] += self.shake_offset[0]
            self.game._viewOffset[ 1 ] += self.shake_offset[1]
            self.shake_time -= 1
        
class Update :
    
    def __init__( self, owner, function, interval = 1, burst = 1, burst_interval = 1, looping = True ) :
        #This game_objects update function runs when interval is at 0, must be a GameObject
        self.owner = owner
        self.function = function
        
        #The function runs these many times when interval is at 0
        self.max_burst = burst
        self.burst = burst
        
        #Each consecutive run when interval is at 0 will be delayed be this much
        self.max_burst_interval = burst_interval
        self.burst_interval = 0
        
        #Before running the function waits this long
        self.max_interval = interval
        self.interval = interval
        
        #If this is true the update resets after burst and interval are both at 0
        self.looping = looping
        
    def run( self ) :
        if self.interval > 0 :
            self.interval = self.interval - 1
            return True
        if self.burst > 0 :
            if self.burst_interval > 0 :
                self.burst_interval = self.burst_interval - 1
                return True
            self.burst_interval = self.max_burst_interval
            self.burst = self.burst - 1
            self.function( self )
            return True
        if self.looping == True :
            self.interval = self.max_interval
            self.burst = self.max_burst
            self.burst_interval = 0
            return True
        return False
        
        
        
        
        
        
        
        
        
        
        
        
