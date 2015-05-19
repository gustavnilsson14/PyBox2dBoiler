from Util import *
from time import sleep
from Core import *
from Body import *
from framework import *

class Unit() :
    
    def __init__( self, scene, pos ) :
        self.body_handler = Body()
        self.scene = scene
        self.current_path = 0
        self.current_tile = ()
        self.current_order = 0
        self.image = 0
        self.lifetime = 0
        self.vision_range = 0
        self.health = 0
        self.alive = True
        self.target = 0
        self.types = [ "unit" ]
        
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
                print "VISIBLE"
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
        self.move_along_path( new_pos )
        #self.move_towards_target( self.scene.target_unit, 1 )
        
    def stop( self ) :
        if self.body == 0 :
            return False
        self.body.linearVelocity = (0,0)
        #self.move_towards_target( self.scene.target_unit, 1 )
        
    def move_towards_target( self, target, final_distance ) :
        my_pos = self.body.transform.position
        target_pos = target.body.transform.position
        if get_distance_between_points( my_pos, target_pos ) > final_distance :
            radians_to_target = get_radians_between_points( my_pos, target_pos )
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
        movement_vector = get_movement_vector( radians_to_tile, self.speed )
        
        self.body.transform = [ self.body.transform.position, radians_to_tile ]
        self.body.linearVelocity = movement_vector
        
    def take_damage( self, origin, damage ) :
        if self.health > 0 :
            self.health -= damage
            if self.image != 0 :
                self.image.blink()
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
        self.speed = 4
        self.vision_range = 10
        self.health = 10
        self.body_handler.set_image_at( 'head', 'image.png' )
        
        self.body_handler.attach_item( "right_arm", ProjectileWeapon( scene ) )
        #self.body_handler.detach_item( "right_arm" )
        self.target = 0
        self.types += [ "character" ]
    
    def update( self, update ) :
        Unit.update( self, update )
        self.handle_item( update )
        
    def aim( self, target ) :
        if self.has_vision_of_point( target.body.transform.position ) :
            return True
        return False
        
    def handle_item( self, update ) :
        self.body_handler.use()
        
    def attack( self, target ) :
        weapon = self.body_handler.find_item( 'weapon' )
        if weapon :
            return weapon.use( target )
        return False
        
class Projectile( Unit ) :
    
    def __init__( self, scene, origin, offset = -0.8 ) :
        pos = origin.position + get_movement_vector( origin.angle, offset )
        Unit.__init__( self, scene, origin.position )
        self.body = self.body_handler.create_projectile( self, scene.world, pos, 0.5, FILTER_PROJECTILE )
        self.origin = origin
        self.speed = 50
        self.lifetime = 15
        vector = get_movement_vector( origin.angle, -self.speed )
        self.body.ApplyForce( vector, self.body.worldCenter, True)
        self.damage = 1
        self.body_handler.set_image_at( 'main', 'image.png' )
        self.types += [ "projectile" ]
    
    def update( self, update ) :
        pass
        #Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        if colliding_fixture.body.userData.get( 'owner' ).__class__.__name__ == "Block" :
            self.die( colliding_fixture.body.userData.get( 'owner' ) )
        if colliding_fixture.body.userData.get( 'owner' ).__class__.__name__ == "Character" :
            self.die( colliding_fixture.body.userData.get( 'owner' ) )
            self.deal_damage( colliding_fixture.body.userData.get( 'owner' ) )
            
    def deal_damage( self, target ) :
        if target.take_damage( self, self.damage ) == True :
            pass

class Item :
    
    def __init__( self, scene, cooldown = 0, local_anchor = (0,0) ) :
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
        if get_distance_between_points( self.body.transform.position, target.body.transform.position ) < self.attack_range :
            return True
        return False
            
class ProjectileWeapon( Weapon ) :
    
    def __init__( self, scene, cooldown = 5, local_anchor = (0.45,0), attack_range = 10 ) :
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
                density=0.00001
            )
        )
        return self.body

    def handle_collision( self, my_fixture, colliding_fixture ) :
        pass
