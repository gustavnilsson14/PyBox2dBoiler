from Unit import *
from Core import *
from Constants import *
import math
import random

class Pellet( Projectile ) :
    
    def __init__( self, scene, origin, offset = -0.8, speed = 500, lifetime = 150 ) :
        Projectile.__init__( self, scene, origin, -0.6, 750, 60 )
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

    def __init__( self, scene, pos = ( 0, 0 )  ) :
        ProjectileWeapon.__init__( self, scene, pos, 14, (0.3,0), 3 )
        self.pellet_amount = 10
        self.spread = 7
        self.types += [ "shotgun" ]

    def create_projectile( self ) :
        if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 6
        if self.body != 0 :
            for i in range(0, self.pellet_amount ) :
                transform = self.apply_spread()
		projectile = Pellet( self.scene, transform )
                self.scene.add_entity( projectile )

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_short_gun( self, self.scene, pos, 1, FILTER_WEAPON )
        return self.body
    
class Machinegun( ProjectileWeapon ) :

    def __init__( self, scene, pos = ( 0, 0 ) ) :
        ProjectileWeapon.__init__( self, scene, pos, 3, (0.4,0), 3 )
        self.spread = 1
        self.types += [ "machinegun" ]

    def create_projectile( self ) :
	if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 1
        if self.body != 0 :
            transform = self.apply_spread()
            projectile = Projectile( self.scene, transform )
            self.scene.add_entity( projectile )

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_long_gun( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/machinegun.png' )
        return self.body
