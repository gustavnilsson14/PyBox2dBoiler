# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import numpy
from heapq import *
import time

class Path :
    
    def __init__( self, path ) :
        self.lifetime = 20
        self.path = path
        self.start = self.path[ 0 ]
        self.goal = self.path[ -1 ]
        self.computed = int( time.time() )
        
    def is_valid( self, current_time ) :
        if self.computed + self.lifetime > current_time :
            self.computed = int( time.time() )
            return self.path
        return False

class Pathfinder :
    
    def __init__( self, map ) :
        self.path_list = []
        self.map =  numpy.array( map )
        self.neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    def heuristic( self, a, b ) :
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    
    def match_path( self, start, goal ) :
        current_time = int( time.time() )
        for path in self.path_list :
            if path.is_valid( current_time ) == False :
                self.path_list.remove( path )
                continue
            if start[0] != path.start[0] or start[1] != path.start[1] :
                continue
            if goal[0] != path.goal[0] or goal[1] != path.goal[1] :
                continue
            return path
        return 0
    
    def find( self, start, goal ) :
        start = ( round( start[0] ), round( start[1] ) )
        goal = ( round( goal[0] ), round( goal[1] ) )
        
        if self.map[ goal[0] ][ goal[1] ].get( 'collision' ) != None :
            return 0
        
        old_path = self.match_path( start, goal )
        if old_path != 0 :
            return old_path.path[:]
        close_set = set()
        came_from = {}
        gscore = {start:0}
        fscore = {start:self.heuristic(start, goal)}
        oheap = []

        heappush(oheap, (fscore[start], start))
        
        while oheap:

            current = heappop(oheap)[1]

            if current == goal:
                data = []
                while current in came_from:
                    #PREPEND
                    data[:0] = [current]
                    current = came_from[current]
                data[:0] = [start]
                self.path_list.append( Path( data ) )
                return data[:]

            close_set.add(current)
            for i, j in self.neighbors:
                neighbor = current[0] + i, current[1] + j            
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)
                
                if 0 <= neighbor[ 0 ] < self.map.shape[ 0 ]:
                    if 0 <= neighbor[ 1 ] < self.map.shape[ 1 ]: 
                        if self.map[ neighbor[ 0 ] ][ neighbor[ 1 ] ].get( 'collision' ) != None :
                            continue
                        if i != 0 and j != 0 :
                            edge_neightbor_y = current[0], current[1] + j
                            edge_neightbor_x = current[0] + i, current[1]
                            if self.map[ edge_neightbor_y[ 0 ] ][ edge_neightbor_y[ 1 ] ].get( 'collision' ) != None :
                                continue
                            if self.map[ edge_neightbor_x[ 0 ] ][ edge_neightbor_x[ 1 ] ].get( 'collision' ) != None :
                                continue
                                
                    else:
                        # array bound y walls
                        continue
                else:
                    # array bound x walls
                    continue
                    
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                    
                if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(oheap, (fscore[neighbor], neighbor))
                    
        return 0
