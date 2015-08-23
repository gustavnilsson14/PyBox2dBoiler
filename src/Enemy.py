from Unit import *
from Item import *

class FireMage( Character ) :
    
    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_FIRE ]
        self.speed = 0.4 * self.body.mass
        self.accuracy = 5
        item = FireOrb( scene )
        self.body_handler.attach_item( "spell_orb", item )
        self.scene.add_entity( item )
        self.types += [ self.__class__.__name__ ]
        
    def set_body_images( self ) :
        Unit.set_body_images( self )
        self.body_handler.set_image_at( 'right_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'left_arm', 'res/img/body/default_arm.png' )
        self.body_handler.set_image_at( 'right_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'left_shoulder', 'res/img/body/default_shoulder.png' )
        self.body_handler.set_image_at( 'head', 'res/img/effect/fireball.png' )
        
class IceMage( Character ) :
    
    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_ICE ]
        self.speed = 0.4 * self.body.mass
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
        self.body_handler.set_image_at( 'head', 'res/img/body/default_head2.png' )
        
class BoltMage( Character ) :

    def __init__( self, scene, pos ) :
        Character.__init__( self, scene, pos )
        self.immunities = [ DAMAGE_TYPE_LIGHTNING ]
        self.speed = 0.4 * self.body.mass
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
        self.body_handler.set_image_at( 'head', 'res/img/body/default_head2.png' )