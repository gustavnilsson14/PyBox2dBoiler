import pygame

class SoundHandler() :
    
    def __init__( self, settings ) :
        self.settings = settings
        self.sounds = {
            'shoot': pygame.mixer.Sound( 'res/sfx/shoot.wav' )
        }
        self.music = {
            'default': pygame.mixer.Sound( 'res/music/tikk.ogg' )
        }
    
    def get_sound( self, key ) :
        sound = self.sounds.get( key )
        if sound == None :
            return 0
        return sound 
    
    def play_sound( self, key ) :
        #Run almost anywhere!
        #self.game.sound_handler.play_sound('shoot')
        sound = self.sounds.get( key )
        if sound == None :
            return 0
        if self.settings.sound == False :
            return 0
        sound.play()
        return 1
        
    def play_music( self, key ) :
        #Run almost anywhere!
        #self.game.sound_handler.play_music('default')
        track = self.music.get( key )
        if track == None :
            return False
        if self.settings.sound == False :
            return 0
        track.play()
        
    def stop_music( self, key = 0 ) :
        if key == 0 :
            for track in self.music :
                self.music.get( track ).stop()
            return True
        track = self.music.get( key )
        if track == None :
            return False
        track.stop()
        return True