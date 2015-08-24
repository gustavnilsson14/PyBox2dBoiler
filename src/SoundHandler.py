import pygame

class SoundHandler() :
    
    def __init__( self, settings ) :
        self.settings = settings
        self.sounds = {
            'fire': {
                'sound': pygame.mixer.Sound( 'res/sfx/fire.ogg' ),
                'volume': 1.0
            },
            'ice': {
                'sound': pygame.mixer.Sound( 'res/sfx/ice.ogg' ),
                'volume': 1.0
            },
            'bolt': {
                'sound': pygame.mixer.Sound( 'res/sfx/bolt.ogg' ),
                'volume': 0.05
            },
            'fireboom': {
                'sound': pygame.mixer.Sound( 'res/sfx/fireboom.ogg' ),
                'volume': 1.0
            },
            'iceicle': {
                'sound': pygame.mixer.Sound( 'res/sfx/iceicle.ogg' ),
                'volume': 1.0
            },
            'bigbolt': {
                'sound': pygame.mixer.Sound( 'res/sfx/bigbolt.ogg' ),
                'volume': 0.05
            },
            'holy': {
                'sound': pygame.mixer.Sound( 'res/sfx/holy.ogg' ),
                'volume': 1.0
            },
            'death': {
                'sound': pygame.mixer.Sound( 'res/sfx/death.ogg' ),
                'volume': 0.7
            },
            'pick_up': {
                'sound': pygame.mixer.Sound( 'res/sfx/pick_up.ogg' ),
                'volume': 1.0
            },
            'lvl_up': {
                'sound': pygame.mixer.Sound( 'res/sfx/lvl_up.ogg' ),
                'volume': 1.0
            }
        }
        self.music = {
            'default': {
                'sound': pygame.mixer.Sound( 'res/music/tikk.ogg' ),
                'volume' : 0.7
            },
            'demons_acecream' : {
                'sound': pygame.mixer.Sound( 'res/music/acecream_demoner.ogg' ),
                'volume' : 0.3
            }
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
        sfx = sound.get( 'sound' )
        sfx.play()
        sfx.set_volume( sound.get( 'volume' ) )
        return 1
        
    def play_music( self, key ) :
        #Run almost anywhere!
        #self.game.sound_handler.play_music('default')
        track = self.music.get( key )
        if track == None :
            return False
        if self.settings.sound == False :
            return 0
        sfx = track.get( 'sound' )
        sfx.play( -1 )
        sfx.set_volume( track.get( 'volume' ) )
        
    def stop_music( self, key = 0 ) :
        if key == 0 :
            for track in self.music :
                self.music.get( track ).stop()
            return True
        track = self.music.get( key )
        if track == None :
            return False
        track.get('sound').stop()
        return True