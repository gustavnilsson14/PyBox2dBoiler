from Util import *
from time import sleep
from Core import *
from Body import *
from framework import *
import math

class Unit( Entity ) :

    def __init__( self, scene, pos ) :
        Entity.__init__( self, scene )
        self.body_handler = Body( scene )
        self.scene = scene
        self.immunities = []
        self.current_path = 0
        self.current_tile = ()
        self.current_order = 0
        self.lifetime = 0
        self.vision_range = 0
        self.max_health = 0
        self.health = 0
        self.alive = True
        self.target = 0
        self.types += [ "unit" ]

    def set_body_images( self ) :
        pass

    def set_health( self, health ) :
        self.max_health = health
        self.health = health

    def set_target( self, target ) :
        self.target = target

    def handle_collision( self, my_fixture, colliding_fixture ) :
        pass
        #self.scene.world.DestroyBody( colliding_fixture.body )

    def set_order( self, order ) :
        if self.current_order == 0 :
            self.current_order = order
            return True
        if self.current_order.remove_unit( self ) == True :
            self.current_order = order
            return True
        return False

    def update( self, update ) :
        self.last_update = update
        self.handle_lifetime( update )
        self.body_handler.update( update )
        if self.current_order != 0 :
            if self.current_order.Step() == False :
                return False

    def has_vision_of_point( self, pos ) :
        if self.vision_range > 0 :
            if self.scene.map.fov.is_pos_visible( self.body.transform.position, pos, self.vision_range ) :
                return True
        return False

    def handle_lifetime( self, update ) :
        if self.lifetime > 0 :
            self.lifetime -= 1
            if self.lifetime == 0 :
                self.scene.remove_entity( self )

    def move( self, new_pos ) :
        if self.body == 0 :
            self.pos = new_pos
            return True
        if self.has_vision_of_point( new_pos ) == False :
            self.move_along_path( new_pos )
            return True
        self.move_towards_target( new_pos, 1 )
        return True

    def stop( self ) :
        if self.body == 0 :
            return False
        self.current_path = 0
        self.body.linearVelocity = (0,0)
        #self.move_towards_target( self.scene.target_unit, 1 )

    def move_towards_target( self, target, final_distance ) :
        my_pos = self.body.transform.position
        self.current_path = 0
        if get_distance_between_points( my_pos, target ) > final_distance :
            radians_to_target = get_radians_between_points( my_pos, target )
            movement_vector = get_movement_vector( radians_to_target, self.speed )
            self.body.linearVelocity = movement_vector
            return False
        self.body.linearVelocity = (0,0)
        return True

    def move_along_path( self, new_pos ) :
        if self.current_path != 0 :
            if len( self.current_path ) != 0 :
                next_tile_distance = get_distance_between_points( self.body.transform.position, self.current_tile )
                if next_tile_distance < ( 0.3 * self.speed ) :
                    self.current_tile = self.current_path.pop( 0 )
                    self.move_to_tile( self.current_tile )
                    #self.scene.map.get_visible_tiles( self.body.transform.position )
                    if len( self.current_path ) == 0 :
                        self.current_path = 0
                        self.body.linearVelocity = ( 0, 0 )
                        return False
                    return True
                self.move_to_tile( self.current_tile )
                return True
            return True
        self.current_path = self.scene.map.find_path( self.body.transform.position, new_pos )
        if self.current_path == 0 :
            self.stop()
            return False
        self.current_tile = self.current_path.pop( 0 )
        self.move_to_tile( self.current_tile )

    def move_to_tile( self, tile ) :
        radians_to_tile = get_radians_between_points( self.body.transform.position, tile )
        self.body_handler.turn( radians_to_tile )
        movement_vector = get_movement_vector( radians_to_tile, self.speed )
        self.body.linearVelocity = movement_vector

    def take_damage( self, origin, damage ) :
        if self.immunities.__contains__( damage.type ) :
            return True
        if self.health > 0 :
            self.health -= damage.value
            if self.body_handler != 0 :
                self.body_handler.blink()
            if self.health <= 0 :
                self.die( origin )
                return True
        return False

    def die( self, origin ) :
        if self.alive == False :
            return False
        self.scene.remove_entity( self )
        self.alive = False
        return True

    def pickup( self, item, slot, key, body ) :
        if slot.item != 0 :
            if slot.item.body == body :
                return 0
        if item.picked( self, slot ) == True :
            return True
        self.body_handler.attach_item( key, item )
        self.set_current_item( 'weapon' )
        return True

class Character( Unit ) :

    def __init__( self, scene, pos ) :
        Unit.__init__( self, scene, pos )
        self.body = self.body_handler.create_humanoid( self, scene, pos, 0.3, FILTER_CHARACTER )
        self.speed = 1 * self.body.mass
        self.accuracy = 10
        self.current_accuracy = ( 0, float(self.accuracy/10.0) )
        self.vision_range = 40
        self.set_health( 10 )
        self.set_body_images()
        self.current_item = 0
        #self.body_handler.detach_item( "right_arm" )
        self.target = 0
        self.types += [ "character" ]

    def update( self, update ) :
        Unit.update( self, update )
        self.handle_accuracy()

    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/body/default_head2.png' )

    def set_current_item( self, type ) :
        self.current_item = self.body_handler.find_item( type )
        return True

    def handle_accuracy( self ) :
        self.current_accuracy = ( self.current_accuracy[0] + self.current_accuracy[1], self.current_accuracy[1] )
        if self.current_accuracy[0] > self.accuracy :
            self.current_accuracy = ( self.accuracy, -(self.accuracy/10.0) )
        if self.current_accuracy[0] < -self.accuracy :
            self.current_accuracy = ( -self.accuracy, (self.accuracy/10.0) )

    def aim( self, target ) :
        if self.current_item == 0 :
            return False
        if self.has_vision_of_point( target ) == False :
            return False
        radians_to_target = get_radians_between_points( self.body.transform.position, target )
        self.body_handler.turn( radians_to_target )
        self.body_handler.aim( self.current_item, target, self.current_accuracy )
        return True

    def use_current_item( self, target ) :
        if self.current_item != 0 :
            return self.current_item.use( 0 )
        return False

class PlayerCharacter( Unit ) :

    def __init__( self, scene, pos, player ) :
        Unit.__init__( self, scene, pos )
        self.player = player
        self.body = self.body_handler.create_humanoid( self, scene, pos, 0.3, FILTER_CHARACTER )
        self.speed = 1.5 * self.body.mass
        self.accuracy = 2
        self.health = player.max_health
        self.power = 0
        self.orbs = 0
        self.current_accuracy = ( 0, float(self.accuracy/10.0) )
        self.vision_range = 40
        self.set_body_images()
        self.current_item = 0
        self.target = 0
        self.types += [ "player_character" ]
        self.movement_vector = ( 0, 0 )
        self.super_bullet_amount = 0
        self.super_bullet_mode = 0

    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/body/default_head.png' )

    def update( self, update ) :
        self.body_handler.update( update )
        self.handle_accuracy()
        self.fire_super_bullets()
        self.body.linearVelocity = ( self.movement_vector[0] * self.speed, self.movement_vector[1] * self.speed )

    def pickup( self, item, slot, key, body ) :
        if Unit.pickup( self, item, slot, key, body ) == True :
            item.fire_rate_multiplier = self.player.firerate
        
    def handle_accuracy( self ) :
        self.current_accuracy = ( self.current_accuracy[0] + self.current_accuracy[1], self.current_accuracy[1] )
        if self.current_accuracy[0] > self.accuracy :
            self.current_accuracy = ( self.accuracy, -(self.accuracy/10.0) )
        if self.current_accuracy[0] < -self.accuracy :
            self.current_accuracy = ( -self.accuracy, (self.accuracy/10.0) )

    def set_current_item( self, type ) :
        self.current_item = self.body_handler.find_item( type )
        return True

    def aim( self, target ) :
        radians_to_target = get_radians_between_points( self.body.transform.position, target )
        self.body_handler.turn( radians_to_target )
        if self.current_item == 0 :
            return False
        self.body_handler.aim( self.current_item, target, self.current_accuracy )
        return True

    def super_attack( self ) :
        if self.power < 6 :
            return
        if self.power < 20 :
            self.super_bullet_amount = self.power
            self.super_bullet_mode = 0
        elif self.power < 40 :
            self.super_bullet_amount = self.power * 1.5
            self.super_bullet_mode = 1
        elif self.power < 60 :
            self.super_bullet_amount = self.power * 2
            self.super_bullet_mode = 2
        self.power = 0
            
    def fire_super_bullets( self ) :
        from Item import *
        if self.super_bullet_amount <= 0 :
            return
        if self.super_bullet_mode == 2 :
            offset = math.radians( randint( 0, 360 ) )
            for i in range(0,19) :
                self.super_bullet_amount -= 1
                angle = math.radians( i*20 ) + offset
                transform = b2Transform( self.body.transform.position, b2Rot( angle ) )
                projectile = SuperBall( self, self.scene, transform )
                self.scene.add_entity( projectile )
            return
        if self.super_bullet_mode == 1 :
            for i in range(-1,2) :
                self.super_bullet_amount -= 1
                angle = self.body_handler.all_bodies.get('head').transform.angle
                position = self.body.transform.position
                if i != 0 :
                    diff = 90
                    theta = math.radians( math.degrees( angle ) + diff )
                    deltax = (i*cos(theta))/3
                    deltay = (i*sin(theta))/3
                    position = (self.body.transform.position[0] + deltax,self.body.transform.position[1] + deltay )
                transform = b2Transform( position, b2Rot( angle ) )
                projectile = SuperBall( self, self.scene, transform )
                self.scene.add_entity( projectile )
            return
        #mode 0
        self.super_bullet_amount -= 1
        angle = math.radians( randint( 0, 360 ) )
        transform = b2Transform( self.body.transform.position, b2Rot( angle ) )
        projectile = SuperBall( self, self.scene, transform )
        self.scene.add_entity( projectile )

    def use_current_item( self, target ) :
        if self.current_item != 0 :
            return self.current_item.use( target )
        return False

    def take_damage( self, origin, damage ) :
        Unit.take_damage( self, origin, damage )
        if self.immunities.__contains__( damage.type ) == 0 :
            self.scene.screen.shake_time = 1
            #self.scene.game.pause_time = 3'
        else:
            self.power += 0.2
            if self.power > self.player.max_power:
                self.power = self.player.max_power
                
    def die( self, origin ) :
        Unit.die( self, origin )
        self.scene.defeat( DEFEAT_GROUP_PLAYERS )
            
class Mage( PlayerCharacter ) :

    def __init__( self, scene, pos ) :
        item = GreyOrb( scene )
        self.body_handler.attach_item( "spell_orb", item )

from Item import *
