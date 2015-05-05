from math import atan2, sqrt, cos, sin

class Fov :
    def __init__( self, map ) :
        self.map = map
    
    def clear_map( self ) :
        for row in map :
            for tile in row :
                tile[ 'visible' ] = False
    
    def check( self, pos ) :
        visible_tiles = []
        i = 0
        while i < 360 :
            x=cos( float( i*0.01745 ) );
            y=sin( float( i*0.01745 ) );
            visible_tiles = visible_tiles + self.cast_ray( pos, x, y )
            i = i + 2
        return visible_tiles
        
    def cast_ray( self, pos, x, y ) :
        ox = pos[0] + 0.5;
        oy = pos[1] + 0.5;
        visible_tiles = []
        i = 0
        while i < 4 :
            visible_tiles.append( ( int( ox ), int( oy ) ) )
            if self.map[ int( ox ) ][ int( oy ) ].get( 'collision' ) != None :
                return visible_tiles
            i = i + 1
            ox+=x;
            oy+=y;
        return visible_tiles
