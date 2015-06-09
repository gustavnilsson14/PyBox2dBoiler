from Unit import *
from Core import *
from Constants import *
from framework import *
import math
import random

class Pellet( Projectile ) :
    
    def __init__( self, scene, origin, offset = -0.8, speed = 500, lifetime = 150 ) :
        Projectile.__init__( self, scene, origin, -0.6, 450, 30 )
        self.damage = 1
        self.body_handler.set_image_at( 'main', 'res/img/effect/default_bullet.png' )
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
            
    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.1, FILTER_PROJECTILE )

class Shotgun( ProjectileWeapon ) :

    def __init__( self, scene ) :
        ProjectileWeapon.__init__( self, scene, 14, (0.3,0), 3 )
        self.pellet_amount = 10
        self.types += [ "shotgun" ]

    def create_projectile( self ) :
        if self.body != 0 :
            for i in range(0, self.pellet_amount ) :
                angle = math.radians( math.degrees( self.body.transform.angle ) + random.randint( -7, 7 ) )
                rotation = b2Rot( angle )
                transform = b2Transform( self.body.transform.position, rotation )
                projectile = Pellet( self.scene, transform )
                self.scene.add_entity( projectile )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_short_gun( self, self.scene, pos, 1, FILTER_WEAPON )
        return self.body
        
class Machinegun( ProjectileWeapon ) :

    def __init__( self, scene ) :
        ProjectileWeapon.__init__( self, scene, 3, (0.4,0), 3 )
        self.types += [ "machinegun" ]

    def create_body( self, pos ) :
        self.body = self.body_handler.create_long_gun( self, self.scene, pos, 1, FILTER_WEAPON )
        return self.body
