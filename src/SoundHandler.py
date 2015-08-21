import pygame

class SoundHandler() :
    
    def __init__( self ) :
        self.sounds = {
            'shoot': pygame.mixer.Sound( 'res/sfx/shoot.wav' )
        }
        pass
    
    def get_sound( self, key ) :
        return self.sounds.get( key )
    
    def play_sound( self, key ) :
        self.sounds.get( key ).play()