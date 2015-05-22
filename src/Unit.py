from Util import *
from time import sleep
from Core import *
from Body import *
from framework import *

class Unit( Entity ) :
    
    def __init__( self, scene, pos ) :
        Entity.__init__( self, scene )
        self.body_handler = Body( scene )
        self.scene = scene
        self.current_path = 0
        self.current_tile = ()
        self.current_order = 0
        self.lifetime = 0
        self.vision_range = 0
        self.health = 0
        self.alive = True
        self.target = 0
        self.types += [ "unit" ]
        
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
                self.scene.remove_unit( self )
    
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
        self.current_tile = self.current_path.pop( 0 )
        self.move_to_tile( self.current_tile )
        #print self.current_path, self.body.transform.position
        
    def move_to_tile( self, tile ) :
        radians_to_tile = get_radians_between_points( self.body.transform.position, tile )
        self.body_handler.turn( radians_to_tile )
        movement_vector = get_movement_vector( radians_to_tile, self.speed )
        self.body.linearVelocity = movement_vector
        
    def take_damage( self, origin, damage ) :
        if self.health > 0 :
            self.health -= damage
            if self.body_handler != 0 :
                self.body_handler.blink()
            if self.health <= 0 :
                self.die( origin )
                return True
        return False
                
    def die( self, origin ) :
        if self.alive == False :
            return False
        self.scene.remove_unit( self )
        self.alive = False
        return True
        
class Character( Unit ) :
    
    def __init__( self, scene, pos ) :
        Unit.__init__( self, scene, pos )
        self.body = self.body_handler.create_humanoid( self, scene, pos, 0.3, FILTER_CHARACTER )
        self.speed = 1 * self.body.mass
        self.accuracy = 10
        self.current_accuracy = ( 0, float(self.accuracy/10.0) )
        self.vision_range = 40
        self.health = 100000
        self.body_handler.set_image_at( 'head', 'image.png' )
        self.current_item = 0
        self.body_handler.attach_item( "right_arm", ProjectileWeapon( scene ) )
        #self.body_handler.detach_item( "right_arm" )
        self.target = 0
        self.types += [ "character" ]
    
    def update( self, update ) :
        Unit.update( self, update )
        self.handle_accuracy()
        
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
    
    def __init__( self, scene, pos ) :
        Unit.__init__( self, scene, pos )
        self.body = self.body_handler.create_humanoid( self, scene, pos, 0.3, FILTER_CHARACTER )
        self.speed = 1 * self.body.mass
        self.accuracy = 2
        self.current_accuracy = ( 0, float(self.accuracy/10.0) )
        self.vision_range = 40
        self.health = 100000
        self.body_handler.set_image_at( 'head', 'image.png' )
        self.current_item = 0
        self.body_handler.attach_item( "right_arm", ProjectileWeapon( scene ) )
        #self.body_handler.detach_item( "right_arm" )
        self.target = 0
        self.types += [ "player_character" ]
        self.movement_vector = ( 0, 0 )
        self.set_current_item( 'weapon' )
    
    def update( self, update ) :
        self.body_handler.update( update )
        self.handle_accuracy()
        self.body.linearVelocity = ( self.movement_vector[0] * self.speed, self.movement_vector[1] * self.speed )
    
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
        if self.current_item == 0 :
            return False
        radians_to_target = get_radians_between_points( self.body.transform.position, target )
        self.body_handler.turn( radians_to_target )
        self.body_handler.aim( self.current_item, target, self.current_accuracy )
        return True
                
    def use_current_item( self, target ) :
        if self.current_item != 0 :
            return self.current_item.use( target )
        return False
        
    def take_damage( self, origin, damage ) :
        Unit.take_damage( self, origin, damage )
        self.scene.screen.shake_time = 1
        self.scene.game.pause_time = 5

class Projectile( Unit ) :
    
    def __init__( self, scene, origin, offset = -0.8 ) :
        pos = origin.position + get_movement_vector( origin.angle, offset )
        Unit.__init__( self, scene, origin.position )
        self.body = self.body_handler.create_projectile( self, pos, 0.1, FILTER_PROJECTILE )
        self.origin = origin
        self.speed = 500 * self.body.mass
        self.lifetime = 150
        vector = get_movement_vector( origin.angle, -self.speed )
        self.body.ApplyForce( vector, self.body.worldCenter, True)
        self.damage = 1
        self.body_handler.set_image_at( 'main', 'image.png' )
        self.types += [ "projectile" ]
    
    def update( self, update ) :
        Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )
            
    def deal_damage( self, target ) :
        if target.take_damage( self, self.damage ) == True :
            pass

class Item :
    
    def __init__( self, scene, cooldown = 0, local_anchor = ( 0, 0 ) ) :
        self.holder = 0
        self.scene = scene
        self.body = 0
        self.max_cooldown = cooldown
        self.cooldown = 0
        self.local_anchor = local_anchor
        self.types = [ "item" ]
        
    def update( self, update ) :
        if self.cooldown > 0 :
            self.cooldown -= 1
    
    def use( self ) :
        if self.cooldown == 0 :
            self.cooldown = self.max_cooldown
            return True
        return False
    
    def destroy_body( self ) :
        if self.body != 0 :
            self.scene.game.add_garbage_body( self.body )
            return True
        return False

class Weapon( Item ) :
    
    def __init__( self, scene, cooldown, local_anchor, attack_range ) :
        Item.__init__( self, scene, cooldown, local_anchor )
        self.attack_range = attack_range
        self.types += [ "weapon" ]

    def use( self, target ) :
        if target == 0 :
            return True
        if get_distance_between_points( self.body.transform.position, target.body.transform.position ) < self.attack_range :
            return True
        return False
            
class ProjectileWeapon( Weapon ) :
    
    def __init__( self, scene, cooldown = 5, local_anchor = (0.45,0), attack_range = 5 ) :
        Weapon.__init__( self, scene, cooldown, local_anchor, attack_range )
        self.attack_range = attack_range
        self.types += [ "projectile_weapon" ]
      
    def use( self, target ) :
        if Weapon.use( self, target ) :
            if Item.use( self ) :
                self.create_projectile()
                return True
            return True
        return False
            
    def create_projectile( self ) :
        if self.body != 0 :
            projectile = Projectile( self.scene, self.body.transform )
            self.scene.add_unit( projectile )
    
    def create_body( self, pos ) :
        self.body = self.scene.world.CreateDynamicBody(
            position = pos,
            fixedRotation=False,
            allowSleep=False,
            userData={
                'owner' : self
            },
            fixtures=b2FixtureDef(
                filter=b2Filter(
                    groupIndex = 0,
                    categoryBits = FILTER_WEAPON[0],
                    maskBits = FILTER_WEAPON[1]
                ),
                shape=b2PolygonShape(
                    box=(0.2, 0.03)
                ), 
                density=0.0001
            )
        )
        return self.body

    def handle_collision( self, my_fixture, colliding_fixture ) :
        pass
