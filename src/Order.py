class Order :
    
    def __init__( self, unit_list ) :
        self.interruptable = True
        for unit in unit_list :
            if unit.set_order( self ) == False :
                unit_list.remove( unit )
        self.unit_list = unit_list
        
    def add_unit( self, unit ) :
        if self.unit_list.__contains__( unit ) :
            return False
        self.unit_list.append( unit )
        return True
        
    def remove_unit( self, unit ) :
        if self.interruptable == True :
            return False
        if self.unit_list.__contains__( unit ) :
            self.unit_list.remove( unit )
            return True
        return False
        
    def destroy( self ) :
        for unit in self.unit_list :
            unit.current_order = 0
        self.unit_list = 0
        
    def Step( self ) :
        pass
        
class MoveOrder( Order ) :
    
    def __init__( self, unit_list, goal ) :
        Order.__init__( self, unit_list )
        self.goal = goal
    
    def Step( self ) :
        Order.Step( self )
        for unit in self.unit_list :
            unit.move( self.goal )
