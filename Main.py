import sys
import os.path
import json
sys.path.append( 'lib' )
sys.path.append( 'src' )
from framework import *
from Scene import *

class Game (Framework):
    
    def __init__( self ) :
        self.defaultZoom = 20.0
        super(Game, self).__init__()
        self.current_scene = 0
        self.world.gravity = (0,0)
        self.change_scene( "res/maps/compiled_example.js" )
        self.reset_zoom()
        
    def change_scene( self, map_file ) :
        if self.current_scene != 0 :
            self.current_scene.destroy()
        if os.path.isfile( map_file ) == False :
            return False
        with open (map_file, "r") as myfile :
            map_data = myfile.read().replace('\n', '')
            self.current_scene = Scene( self, self.world, json.loads( map_data ) )

    def reset_zoom( self ) :
        #This property manages zoom level
        self.viewZoom = self.defaultZoom
        
    def Step(self, settings):
        super( Game, self ).Step( settings )
        
        if self.current_scene != 0 :
            self.current_scene.Step()
        
        #self.DrawStringAt(500, 100, "LULZLULZLULZLULZLULZLULZLULZLULZ", ( 255, 0, 0, 255 ) )
        #self.viewCenter = (self.car.position.x, 20)
        
if __name__=="__main__":
     main(Game)
