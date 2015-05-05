from math import atan2, sqrt, cos, sin
import time

class Fov :
    
    def __init__( self, pos, radius, data ) :
        self.pos = ( pos[0], pos[1] )
        self.radius = radius
        self.data = data
        self.lifetime = 20
        self.computed = int( time.time() )

    def is_valid( self, time ) :
        if self.computed + self.lifetime > time :
            return self.data
        return False

class FovChecker :
    
    def __init__( self, map ) :
        self.map = map
        self.fov_list = []
    
    def clear_map( self ) :
        for row in map :
            for tile in row :
                tile[ 'visible' ] = False
    
    def match_fov( self, pos, radius ) :
        current_time = int( time.time() )
        for fov in self.fov_list :
            if fov.is_valid( current_time ) == False :
                self.fov_list.remove( fov )
                continue
            if fov.radius != radius :
                continue
            if fov.pos[0] != pos[0] :
                continue
            if fov.pos[1] != pos[1] :
                continue
            return fov
        return 0
        
    def check( self, pos, radius ) :
        old_fov = self.match_fov( pos, radius )
        if old_fov != 0 :
            return old_fov.data[:]
            
        visible_tiles = []
        i = 0
        while i < 360 :
            x=cos( float( i*0.01745 ) );
            y=sin( float( i*0.01745 ) );
            visible_tiles = visible_tiles + self.cast_ray( pos, radius, x, y )
            i = i + 10
        self.fov_list.append( Fov( pos, radius, visible_tiles ) )
        return visible_tiles[:]
        
    def cast_ray( self, pos, radius, x, y ) :
        ox = pos[0] + 0.5;
        oy = pos[1] + 0.5;
        visible_tiles = []
        i = 0
        while i < radius :
            visible_tiles.append( ( int( ox ), int( oy ) ) )
            if self.map[ int( ox ) ][ int( oy ) ].get( 'collision' ) != None :
                return visible_tiles
            i = i + 1
            ox+=x;
            oy+=y;
        return visible_tiles
