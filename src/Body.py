from framework import *
from Core import *
from Constants import *

class Body :
	
	def __init__( self ) :
		self.main_body = 0
		self.all_bodies = []
		self.item_slots = []
		self.joints = []
		
	def create_humanoid( self, owner, scene, pos, size, filter ) :
		head = scene.world.CreateDynamicBody(
			position=pos,
			userData={
				'owner' : owner
			},
			fixedRotation=True,
			fixtures=[
				b2FixtureDef(
					shape=b2CircleShape(radius=0.3*size),
					density=10,
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					)
				)
			]
		)
		l_s_pos = ( pos[0], pos[1] + 0.4*size )
		left_shoulder = scene.world.CreateDynamicBody(
			position = l_s_pos,
			userData={
				'owner' : owner
			},
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.15*size, 0.15*size)
				), 
				density=5 * size
			),
		)
		left_shoulder_joint = scene.world.CreateWeldJoint(
			bodyA=head,
			bodyB=left_shoulder,
			anchor=l_s_pos,
		)
		r_s_pos = ( pos[0], pos[1] - 0.4*size )
		right_shoulder = scene.world.CreateDynamicBody(
			position = r_s_pos,
			userData={
				'owner' : owner
			},
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.15*size, 0.15*size)
				), 
				density=5 * size
			),
		)
		right_shoulder_joint = scene.world.CreateWeldJoint(
			bodyA=head,
			bodyB=right_shoulder,
			anchor=r_s_pos,
		)
		
		l_a_pos = ( pos[0] + 0.2*size, pos[1] + 0.5*size )
		left_arm = scene.world.CreateDynamicBody(
			position = l_a_pos,
			userData={
				'owner' : owner
			},
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.2*size, 0.1*size)
				), 
				density=5 * size
			),
		)
		left_arm_joint = scene.world.CreateRevoluteJoint(
			bodyA=left_shoulder,
			bodyB=left_arm,
            localAnchorA=(0,0),
            localAnchorB=(0.15*size,0),
            lowerAngle=210.0 * b2_pi / 180.0,
            upperAngle=150.0 * b2_pi / 180.0,
            enableLimit=True,
		)
		r_a_pos = ( pos[0] + 0.2*size, pos[1] - 0.5*size )
		right_arm = scene.world.CreateDynamicBody(
			position = r_a_pos,
			userData={
				'owner' : owner
			},
			fixtures=b2FixtureDef(
				filter=b2Filter(
					groupIndex = 0,
					categoryBits = filter[0],
					maskBits = filter[1]
				),
				shape=b2PolygonShape(
					box=(0.2*size, 0.1*size)
				), 
				density=5 * size
			),
		)
		right_arm_joint = scene.world.CreateRevoluteJoint(
			bodyA=right_shoulder,
			bodyB=right_arm,
            localAnchorA=(0,0),
            localAnchorB=(0.15*size,0),
            lowerAngle=210.0 * b2_pi / 180.0,
            upperAngle=150.0 * b2_pi / 180.0,
            enableLimit=True,
		)
		
		self.main_body = head
		self.all_bodies = { 
			"head": head, 
			"right_shoulder": right_shoulder, 
			"left_shoulder": left_shoulder, 
			"right_arm": right_arm, 
			"left_arm": left_arm 
		}
		self.item_slots = {
			"right_arm": ItemSlot( scene, right_arm, ( 0.2*size, 0 ) ), 
			"left_arm": ItemSlot( scene, left_arm, ( 0.2*size, 0 ) ) 
		}
		self.joints = { 
			"right_shoulder_joint": right_shoulder_joint, 
			"left_shoulder_joint": left_shoulder_joint, 
			"right_arm_joint": right_arm_joint, 
			"left_arm_joint": left_arm_joint 
		}
		return self.main_body
	
	def create_projectile( self, owner, world, pos, size, filter ) :
		main = world.CreateDynamicBody(
			position=pos,
			userData={
				'owner' : owner
			},
			fixtures=[
				b2FixtureDef(
					shape=b2CircleShape(radius=0.3*size),
					density=1,
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					)
				)
			]
		)
		self.all_bodies = { 
			"main": main
		}
		self.main_body = main
		return self.main_body
		
	def set_image_at( self, body_part, image ) :
		body = self.all_bodies.get( body_part )
		body.userData[ 'image' ] = Image( image, ALIGN_CENTER_CENTER )
		
	def attach_item( self, body_part, item ) :
		slot = self.item_slots.get( body_part )
		if slot == None :
			return False
		slot.detach_item()
		slot.attach_item( item )
		
	def detach_item( self, body_part ) :
		slot = self.item_slots.get( body_part )
		if slot == None :
			return False
		slot.detach_item()
		
	def use( self ) :
		pass
		
	def update( self, update ) :
		for key in self.item_slots :
			self.item_slots.get( key ).update( update )
	
	def find_items( self, type ) :
		item_list = []
		for key in self.item_slots :
			slot = self.item_slots.get( key )
			if slot.item == 0 :
				continue
			if type in slot.item.types :
				item_list += [ slot.item ]
		return item_list
				
	def find_item( self, type ) :
		for key in self.item_slots :
			slot = self.item_slots.get( key )
			if slot.item == 0 :
				continue
			if type in slot.item.types :
				return slot.item
		return False
	
class ItemSlot :
	
	def __init__( self, scene, body, local_anchor ) :
		self.scene = scene
		self.body = body
		self.local_anchor = local_anchor
		self.joint = 0
		self.item = 0
		
	def attach_item( self, item ) :
		body = item.create_body( self.body.transform.position + self.local_anchor )
		self.joint = self.scene.world.CreateWeldJoint(
			bodyA=self.body,
			bodyB=body,
            localAnchorA=self.local_anchor,
            localAnchorB=item.local_anchor,
		)
		self.item = item
		self.item.holder = self
		
	def detach_item( self ) :
		if self.joint != 0 :
			self.scene.game.add_garbage_joint( self.joint )
			self.joint = 0
			self.item = 0

	def update( self, update ) :
		if self.item != 0 :
			self.item.update( update )
