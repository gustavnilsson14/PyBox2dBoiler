from Unit import *

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