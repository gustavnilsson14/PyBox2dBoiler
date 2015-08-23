from Unit import *
from Item import *
import random

class FireMage( Character ) :

    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_FIRE ]
        self.speed = 0.7 * self.body.mass
        self.accuracy = 5
        item = FireOrb( scene )
        self.body_handler.attach_item( "spell_orb", item )
        self.scene.add_entity( item )
        self.types += [ self.__class__.__name__ ]

    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/fire_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/fire_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/fire_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/fire_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/enemies/fire_blob.png' )

class IceMage( Character ) :

    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_ICE ]
        self.speed = 0.7 * self.body.mass
        self.accuracy = 5
        item = IceOrb( scene )
        self.body_handler.attach_item( "spell_orb", item )
        self.scene.add_entity( item )
        self.types += [ self.__class__.__name__ ]

    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/enemies/ice_blob.png' )

class BoltMage( Character ) :

    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_LIGHTNING ]
        self.speed = 0.7 * self.body.mass
        self.accuracy = 5
        item = BoltOrb( scene )
        self.body_handler.attach_item( "spell_orb", item )
        self.scene.add_entity( item )
        self.types += [ self.__class__.__name__ ]

    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/enemies/storm_blob.png' )

class WhiteMage( Character ) :

    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_LIGHTNING ]
        self.speed = 1.4 * self.body.mass
        self.accuracy = 5
        self.set_health( 40 )
        item = WhiteOrb( scene )
        self.body_handler.attach_item( "spell_orb", item )
        self.scene.add_entity( item )
        self.types += [ self.__class__.__name__ ]

    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/holy_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/holy_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/holy_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/holy_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/body/holy_head.png' )

class ColorMage( Character ) :

    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_FIRE ]
        self.speed = 1 * self.body.mass
        self.switch_time = 500
        self.accuracy = 5
        self.set_health( 35 )
        self.reset_orbs()
        item = FireOrb( scene )
        self.body_handler.attach_item( "spell_orb", item )
        self.scene.add_entity( item )
        self.types += [ self.__class__.__name__ ]

    def reset_orbs( self ) :
        self.available_orbs = [ FireOrb, IceOrb, BoltOrb ]
        random.shuffle( self.available_orbs )
    
    def switch_orb( self ) :
        self.switch_time = randint( 200, 1800 )
        if len( self.available_orbs ) == 0 :
            self.reset_orbs()
        orb = self.available_orbs.pop()
        item = orb( self.scene )
        item.picked( self, 0 )
        print self.immunities
        self.body_handler.attach_item( "spell_orb", item )
        self.set_current_item( 'weapon' )
        self.scene.add_entity( item )
    
    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/holy_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/holy_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/holy_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/holy_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/body/holy_head.png' )
        
    def update( self, update ) :
        Character.update( self, update )
        if self.scene.game.time % self.switch_time == 0 :
            self.switch_orb()
            
