import pygame

class SoundHandler() :
    
    def __init__( self ) :
        self.sounds = {
            'shoot': pygame.mixer.Sound( 'res/sfx/shoot.wav' )
        }
    
    def get_sound( self, key ) :
        sound = self.sounds.get( key )
        if ( sound == None ) :
            return False
        return sound 
    
    def play_sound( self, key ) :
        #Run almost anywhere!
        #self.game.sound_handler.play_sound('shoot')
        sound = self.sounds.get( key )
        if ( sound == None ) :
            return False
        sound.play()
        return True