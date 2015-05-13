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
        self.handle_fov( update )
        if self.current_order != 0 :
            if self.current_order.Step() == False :
                return False
    
    def attach_weapon( self, weapon ) :
        self.weapon = weapon
        
        joint = b2RevoluteJointDef(
            bodyA=weapon.body,
            bodyB=self.body,
            localAnchorA=(-0.7,0),
            localAnchorB=(0,0),
            motorSpeed=10,
            maxMotorTorque=100,
            enableMotor=False,
            collideConnected=False
        )
        self.weapon_joint = self.scene.world.CreateJoint(joint)
       
    def handle_fov( self, update ) :
        return False
        if self.vision_range > 0 :
            if self.scene.map.fov.is_pos_visible( self.body.transform.position, (5+13,5+4), self.vision_range ) :
                pass
                #print "I C U"
    
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
                print next_tile_distance, ( 0.3 * self.speed )
                if next_tile_distance < ( 0.3 * self.speed ) :
                    self.current_tile = self.current_path.pop( 0 )
                    self.move_to_tile( self.current_tile )
                    #self.scene.map.get_visible_tiles( self.body.transform.position )
                    if len( self.current_path ) == 0 :
                        self.current_path = 0
                        self.body.linearVelocity = ( 0, 0 )
                        return False
                    return True
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
        #self.body.setTransform( self.body.transform.position, radians_to_tile )
        self.body.linearVelocity = movement_vector
        
    def shoot( self, update ) :
        pass
    
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
        print self.__class__.__name__ + " died"
        self.scene.remove_unit( self )
        self.alive = False
        return True
        
class Character( Unit ) :
    
    def __init__( self, scene, pos ) :
        Unit.__init__( self, scene, pos )
        self.body = self.body_handler.create_humanoid( self, scene.world, pos, 0.5, FILTER_CHARACTER )
        self.speed = 2
        self.vision_range = 10
        self.health = 10
        #self.image = Image( 'image.png' )
        
        weaponbody = scene.world.CreateDynamicBody(
            position = pos,
            fixedRotation=False,
            allowSleep=False,
            fixtures=b2FixtureDef(
                filter=b2Filter(
                    groupIndex = 0,
                    categoryBits = FILTER_WEAPON[0],
                    maskBits = FILTER_WEAPON[1]
                ),
                shape=b2PolygonShape(
                    box=(0.4, 0.05)
                ), 
                density=0.00001
            ),
        )
        self.body_handler.attach_item( Weapon( scene, weaponbody ) )
    
    def update( self, update ) :
        Unit.update( self, update )
        self.handle_weapon( update )
        self.aim()
        
    def aim( self ) :
        pass
        '''if self.weapon != 0 and self.target != 0 :
            angle = get_radians_between_points( self.body.transform.position, self.target.body.transform.position )
            vector = get_movement_vector(angle, 0.0000001)
            self.weaponbody2.ApplyForce(vector, self.weaponbody2.worldCenter, True)'''
    
    def handle_weapon( self, update ) :
        self.body_handler.update( update )
        #PLACEHOLDER
        self.body_handler.use()
        
        
class Projectile( Unit ) :
    
    def __init__( self, scene, origin ) :
        #HACK, WEAPONS ARE TO BE IMPLEMENTED
        pos = origin.position + get_movement_vector( origin.angle, 0.7 )
        Unit.__init__( self, scene, origin.position )
        self.body = self.body_handler.create_projectile( self, scene.world, pos, 0.4, FILTER_PROJECTILE )
        self.origin = origin
        self.speed = 50
        self.lifetime = 15
        vector = get_movement_vector( origin.angle, self.speed )
        self.body.ApplyForce( vector, self.body.worldCenter, True)
        self.damage = 1
    
    def update( self, update ) :
        pass
        #Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        if colliding_fixture.body.userData.__class__.__name__ == "Block" :
            self.die( colliding_fixture.body.userData )
        if colliding_fixture.body.userData.__class__.__name__ == "Character" :
            self.die( colliding_fixture.body.userData )
            self.deal_damage( colliding_fixture.body.userData )
            
    def deal_damage( self, target ) :
        if target.take_damage( self, self.damage ) == True :
            pass

class Weapon :
    
    def __init__( self, scene, body, cooldown = 10, owner = 0 ) :
        self.owner = owner
        self.scene = scene
        self.body = body
        self.max_cooldown = cooldown
        self.cooldown = 0
        
    def update( self, update ) :
        if self.cooldown > 0 :
            self.cooldown -= 1
    
    def shoot( self ) :
        if self.cooldown == 0 :
            self.cooldown = self.max_cooldown
            self.create_projectile()
            
    def create_projectile( self ) :
        if self.body != 0 :
            projectile = Projectile( self.scene, self.body.transform )
            self.scene.add_unit( projectile )
    
    def create_body( self, pos ) :
        pass
        
    def destroy_body( self ) :
        pass
