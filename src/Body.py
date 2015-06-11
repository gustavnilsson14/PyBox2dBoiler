from framework import *
from Core import *
from Constants import *
from Util import *
import math
import time
import pygame

class Body :
	
	def __init__( self, scene ) :
		self.main_body = 0
		self.sprite_group = pygame.sprite.LayeredDirty()
		self.all_bodies = []
		self.item_slots = []
		self.joints = []
		self.scene = scene
		self.aimdelay = 10
		self.dexterity = 2
		
	def create_humanoid( self, owner, scene, pos, size, filter ) :
		main_body = self.scene.world.CreateDynamicBody(
			position=pos,
			userData={
				'owner' : owner
			},
			fixedRotation=True,
			fixtures=[
				b2FixtureDef(
					shape=b2CircleShape(radius=0.3*size),
					density=100,
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					)
				)
			]
		)
		head = self.scene.world.CreateDynamicBody(
			position=pos,
			userData={
				'owner' : owner
			},
			fixtures=[
				b2FixtureDef(
					shape=b2CircleShape(radius=0.3*size),
					density=100,
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					)
				)
			]
		)
		main_body_joint = self.scene.world.CreateRevoluteJoint(
			bodyA=main_body,
			bodyB=head,
			localAnchorA=(0,0),
			localAnchorB=(0,0),
			enableLimit=True,
			#lowerAngle=1230.0 * b2_pi / 180.0,
            #upperAngle=2230.0 * b2_pi / 180.0
		)
		l_s_pos = ( pos[0], pos[1] + 0.4*size )
		left_shoulder = self.scene.world.CreateDynamicBody(
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
				density=100 * size
			),
		)
		left_shoulder_joint = self.scene.world.CreateWeldJoint(
			bodyA=head,
			bodyB=left_shoulder,
			anchor=l_s_pos,
		)
		r_s_pos = ( pos[0], pos[1] - 0.4*size )
		right_shoulder = self.scene.world.CreateDynamicBody(
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
				density=100 * size
			),
		)
		right_shoulder_joint = self.scene.world.CreateWeldJoint(
			bodyA=head,
			bodyB=right_shoulder,
			anchor=r_s_pos,
		)
		
		arm_joint_lower_angle=130.0 * b2_pi / 180.0
		arm_joint_upper_angle=230.0 * b2_pi / 180.0
		l_a_pos = ( pos[0] + 0.2*size, pos[1] + 0.5*size )
		left_arm = self.scene.world.CreateDynamicBody(
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
				density=100 * size
			),
		)
		left_arm_joint = self.scene.world.CreateRevoluteJoint(
			bodyA=left_shoulder,
			bodyB=left_arm,
            localAnchorA=(0,0),
            localAnchorB=(0.15*size,0),
            lowerAngle=-arm_joint_lower_angle,
            upperAngle=-arm_joint_upper_angle,
            userData={
				"lowerAngle":arm_joint_lower_angle,
				"upperAngle":arm_joint_upper_angle,
			},
            enableLimit=True,
		)
		r_a_pos = ( pos[0] + 0.2*size, pos[1] - 0.5*size )
		right_arm = self.scene.world.CreateDynamicBody(
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
				density=100 * size
			),
		)
		right_arm_joint = self.scene.world.CreateRevoluteJoint(
			bodyA=right_shoulder,
			bodyB=right_arm,
            localAnchorA=(0,0),
            localAnchorB=(0.15*size,0),
            lowerAngle=arm_joint_lower_angle,
            upperAngle=arm_joint_upper_angle,
            userData={
				"lowerAngle":arm_joint_lower_angle,
				"upperAngle":arm_joint_upper_angle,
			},
            enableLimit=True,
		)
		
		self.main_body = main_body
		self.main_body_joint = main_body_joint
		self.all_bodies = {
			"main_body": main_body,
			"head": head, 
			"right_shoulder": right_shoulder, 
			"left_shoulder": left_shoulder, 
			"right_arm": right_arm, 
			"left_arm": left_arm 
		}
		self.item_slots = {
			"right_arm": ItemSlot( scene, right_arm, right_arm_joint, ( 0.2*size, 0 ) ), 
			"left_arm": ItemSlot( scene, left_arm, right_arm_joint, ( 0.2*size, 0 ) ) 
		}
		self.joints = { 
			"main_body_joint": main_body_joint,
			"right_shoulder_joint": right_shoulder_joint, 
			"left_shoulder_joint": left_shoulder_joint, 
			"right_arm_joint": right_arm_joint, 
			"left_arm_joint": left_arm_joint 
		}
		return self.main_body
	
	def create_projectile( self, owner, pos, size, filter ) :
		main = self.scene.world.CreateDynamicBody(
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
	
	def create_pellet( self, owner, pos, size, filter ) :
		main = self.scene.world.CreateDynamicBody(
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

	def create_short_gun( self, owner, scene, pos, size, filter ) :
		main = self.scene.world.CreateDynamicBody(
            position = pos,
            fixedRotation=False,
            allowSleep=False,
            userData={
                'owner' : owner
            },
            fixtures=[
				b2FixtureDef(
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					),
					shape=b2PolygonShape(
						box=(0.15 * size, 0.05 * size)
					), 
					density=0.0001
				)
            ]
        )
		self.all_bodies = { 
			"main": main
		}
		self.main_body = main
		return self.main_body
	
	def create_long_gun( self, owner, scene, pos, size, filter ) :
		main = self.scene.world.CreateDynamicBody(
            position = pos,
            fixedRotation=False,
            allowSleep=False,
            userData={
                'owner' : owner
            },
            fixtures=[
				b2FixtureDef(
					filter=b2Filter(
						groupIndex = 0,
						categoryBits = filter[0],
						maskBits = filter[1]
					),
					shape=b2PolygonShape(
						box=(0.2 * size, 0.03 * size)
					), 
					density=0.0001
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
		image = Image( image, self.scene.game.image_handler, ALIGN_CENTER_CENTER )
		self.sprite_group.add( image )
		body.userData[ 'image' ] = image
		
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
		
	def update( self, update ) :
		for key in self.item_slots :
			self.item_slots.get( key ).update( update )
	
	def find_items( self, type = 'item' ) :
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
		
	def turn( self, radians ) :
		main_joint = self.joints.get( "main_body_joint" )
		self.turn_joint( main_joint, radians, None, 2 )
		
	def aim( self, item, target, accuracy ) :
		joint = item.holder.body_joint
		main_joint = self.joints.get( "main_body_joint" )
		if joint == 0 :
			return False
		desired_angle = get_radians_between_points( target,item.body.transform.position )
		
		desired_angle -= main_joint.angle
		desired_angle = math.radians( ( math.degrees( desired_angle ) + accuracy[0] ) % 360 )
		
		limits = ( joint.userData.get( "upperAngle" ), joint.userData.get( "lowerAngle" ) )
		joint.SetLimits( desired_angle, desired_angle )
		
	def turn_joint( self, joint, desired_angle, limits = None, speed = 1 ) :
		turn_per_timestep = ( math.radians(160. * ( speed * self.dexterity ) ) / 60.0 )
		angle_now = joint.angle
		
		angle_to_turn = ( ( 180 + math.degrees( desired_angle - angle_now ) ) % 360 ) - 180
		
		if angle_to_turn < -10:
			angle_to_turn = -turn_per_timestep
		elif angle_to_turn > 10:
			angle_to_turn = turn_per_timestep
		else :
			angle_to_turn = math.radians( angle_to_turn )
		new_angle = angle_now + angle_to_turn
		
		joint.SetLimits( new_angle, new_angle )
		return True
		
	def blink( self ) :
		for body in self.all_bodies :
			image = self.all_bodies.get( body ).userData.get( "image" )
			if image != None :
				image.blink()
	
	def update_images( self, view_zoom, view_offset, settings ) :
		for key in self.all_bodies :
			image = self.all_bodies.get( key ).userData.get( "image" )
			if image == None :
				continue
			body = self.all_bodies.get( key )
			image.update( body.transform.position, body.transform.angle, view_zoom, view_offset, settings )
	
	def destroy( self ) :
		for j in self.joints :
			joint = self.all_bodies.get( j )
			self.scene.game.add_garbage_joint( joint )
		for b in self.all_bodies :
			body = self.all_bodies.get( b )
			self.scene.game.add_garbage_body( body )
		self.all_bodies = {}
			

class ItemSlot :
	
	def __init__( self, scene, body, body_joint, local_anchor ) :
		self.scene = scene
		self.body = body
		self.body_joint = body_joint
		self.local_anchor = local_anchor
		self.joint = 0
		self.item = 0
		
	def attach_item( self, item ) :
		body = item.create_body( self.body.transform.position + self.local_anchor )
		body.transform = [ body.transform.position, self.body.transform.angle ]
		self.joint = self.scene.world.CreateWeldJoint(
			bodyA=self.body,
			bodyB=body,
            localAnchorA=self.local_anchor,
            localAnchorB=item.local_anchor,
		)
		self.item = item
		self.item.holder = self
		
	def get_owner_types( self ) :
		owner = self.body.userData.get( 'owner' )
		if owner == None :
			return []
		return owner.types
		
	def detach_item( self ) :
		if self.joint != 0 :
			self.scene.game.add_garbage_joint( self.joint )
			self.joint = 0
			self.item.holder = 0
			main_body = self.body.userData.get( 'owner' ).body
			self.item.body.transform = [ main_body.transform.position, main_body.transform.angle ]
			self.item.body.linearVelocity = ( 0, 0 )
			self.item.body.angularVelocity = 0
			self.item = 0

	def update( self, update ) :
		if self.item != 0 :
			self.item.update( update )
