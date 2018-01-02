"""
Noah Hefner
Space Fight
Last Updated: 22 May 2017
"""

import math
import pygame
import random
from highscores import *

SCREEN_HEIGHT = 768
SCREEN_WIDTH = 1360

YELLOW = (255,255,  0)
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
GREEN = (  0,255,  0)
GREY = (105,105,105)
RED = (255,  0,  0)

def main():
	""" Entire program.

	"""

	class Player(pygame.sprite.Sprite):

		""" The player-controlled main character of the game.

		Args:
			image_string (str): Human readable name of the picture used to make
				the player sprite.

		Attributes:
			image (pygame image): Image used for the sprite.
			original (image): A copy of the original image. This image is rotated
				every update.
			rect (rect): Rect attributes for the player sprite.
			velx (int): The player's x axis velocity.
			vely (int): The player's y axis velocity.
			lives (int): Number of lives the player begins with.
			ammo (int): Number of bullets the player begins with.

		"""

		def __init__ (self,image_string):

			super(Player, self).__init__()

			self.image = pygame.image.load(image_string).convert()
			self.image.set_colorkey(BLACK)
			self.original = self.image
			self.rect = self.image.get_rect()
			self.rect.x = (SCREEN_WIDTH / 2) - (self.rect.width / 2)
			self.rect.y = (SCREEN_HEIGHT / 2) - (self.rect.height / 2)
			self.velx = 0
			self.vely = 0
			self.lives = 0
			self.ammo = 100
			self.speed = 5

		def change_speed(self,x,y):
			""" Adds an int value to the velx and vely attributes.

			Args:
				x (int): Amount to be added to the velx attribute.
				y (int): Amount to be added to the vely attribute.

			"""

			self.velx += x
			self.vely += y

		def update(self):
			""" Checks edge-of-screen collision, move and rotate player, and
			adjust the ammo counter color based on how many bullets we have.
			Check if the player is going off the screen. If they are,
			set the proper rect attribute to the corresponding side.
			Add the velx and vely to the rect.x and rect.y attributes,
			respectively. Rotate the player based on the formulas. Set the
			appropriate ammo counter color.

			"""

			if self.rect.x + self.rect.width >= SCREEN_WIDTH:

				self.rect.right = SCREEN_WIDTH

			if self.rect.x <= 0:

				self.rect.left = 0

			if self.rect.y <= 0:

				self.rect.top = 0

			if self.rect.y + self.rect.height >= SCREEN_HEIGHT:

				self.rect.bottom = SCREEN_HEIGHT

			self.rect.x += self.velx
			self.rect.y += self.vely

			(mouse_x, mouse_y) = pygame.mouse.get_pos()
			angle = 360 - (math.degrees(math.atan2(self.rect.center[1] - mouse_y,
			self.rect.center[0] - mouse_x)) + 180)

			self.image = pygame.transform.rotate(self.original, angle)
			self.rect = self.image.get_rect(center = self.rect.center)

			if self.ammo < 50 and self.ammo > 25:

				game.ammo_count_color = YELLOW

			elif self.ammo <= 25:

				game.ammo_count_color = RED

			else:

				game.ammo_count_color = GREEN

	class Alien(pygame.sprite.Sprite):

		""" Aliens that follow the player and explode.

		Attributes:
			image_string (str): Picture of the alien (corresponds to lives.)
			explode_sound (pygame mixer): Sound played when the alien has 0 lives.
			image (pygame sprite image): Sprite image.

			rect (pygame sprite rect): Rect attributes for sprite image.
			e1 (image): First image in explosion sequence.
			e2 (image): Second image in explosion sequence.
			e3 (image): Third image in explosion sequence.
			e4 (image): Fourth image in explosion sequence.
			e5 (image): Fifth image in explosion sequence.
			velx (int): Aliens x axis velocity.
			vely (int): Aliens y axis velocity.
			frame (int): Counter for number of frames in explosion.
			exp_num (int): Counter for the explosion image list.

			heart_drop (int): Random value for heart carrier.
			ammo_drop (int): Random value for ammo carrier.
			freeze_drop (int): Random value for freeze carrier.

			heart_dropped (bool): Has a heart carrier been killed.
			ammo_dropped (bool): Has an ammo carrir been killed.
			freeze_dropped (bool): Has a freeze carrier been killed.
			full_freeze (bool): Is there an active freeze.
			exploding (bool): Is the alien in the exploding loop.

			dropped_frames (int): Number of frames the alien has been dead for.
			lives (int): NUmber of lives the alien has (corresponds to image.)
			speed_multiplier (int): Multiply by to velx and vely to increase speed of approach.

		"""

		def __init__ (self):

			super(Alien, self).__init__()

			self.image_string = "Alien.png"
			self.explode_sound = pygame.mixer.Sound("explosion.ogg")
			self.image = pygame.image.load(self.image_string).convert()
			self.image.set_colorkey(BLACK)

			self.rect = self.image.get_rect()
			self.e1 = pygame.image.load("e1.png").convert()
			self.e2 = pygame.image.load("e2.png").convert()
			self.e3 = pygame.image.load("e3.png").convert()
			self.e4 = pygame.image.load("e4.png").convert()
			self.e5 = pygame.image.load("e5.png").convert()

			self.e1.set_colorkey(BLACK)
			self.e2.set_colorkey(BLACK)
			self.e3.set_colorkey(BLACK)
			self.e4.set_colorkey(BLACK)
			self.e5.set_colorkey(BLACK)

			lr = random.randrange(0,2)
			tb = random.randrange(0,2)

			if lr == 0:

				self.rect.x = random.randrange(-2100,-100)

			elif lr == 1:

				self.rect.x = random.randrange(SCREEN_WIDTH + 100, SCREEN_WIDTH + 2100)

			if tb == 0:

				self.rect.y = random.randrange(-2100,-100)

			elif tb == 1:

				self.rect.y = random.randrange(SCREEN_HEIGHT + 100, SCREEN_HEIGHT + 2100)

			self.velx = 0
			self.vely = 0
			self.frame = 0
			self.exp_num = 0

			self.heart_drop = random.randrange(0,40)
			self.ammo_drop = random.randrange(5,16)
			self.freeze_drop = random.randrange(0,30)
			self.coin_drop = random.randrange(10,20)

			self.heart_dropped = False
			self.ammo_dropped = False
			self.freeze_dropped = False
			self.coin_dropped = False
			self.full_freeze = False
			self.exploding = False

			self.dropped_frames = 0
			self.lives = 1
			self.speed_multiplier = 1

		def update(self):
			""" Stop motion if the alien has been shot. Set the other attributes
			as False to prevent dual-drop. Drop priorities: Ammo, heart, then
			freeze. Change the image to the corresponding drop image. Add one
			to dropped_frames. If the dropped_frames reaches the drop time
			threshold, reset it's attributes and tag it for explosion in the next
			update. Run collision detection with player to test of the player
			picks up the drop. If so, tag the alien for respawn and execute the
			respective drop effects (give ammo, freeze aliens, or give life.)
			If the alien is still alive, set the image to the corresponding life
			number. If there is an active freeze, stop movement. If there is not
			an active freeze, calculate the triange of trajectory towards the
			player and move along the hypotenuse of that triangle. Check for
			collision with player and bullet. If player collision, subtract from
			the players lives the corresponding aliens number of lives. If
			bullet collision, subtract one life from the alien. Revoke any lucky
			carrier attributes from the alien if there is a player collision. If
			the alien is exploding. Send it to the explode method.

			"""

			if self.ammo_dropped == True or self.heart_dropped == True or \
			self.freeze_dropped == True or self.coin_dropped == True:

				self.velx = 0
				self.vely = 0

				if self.ammo_dropped == True:

					self.freeze_dropped = False
					self.heart_dropped  = False
					self.coin_dropped = False
					self.freeze_drop = 0
					self.heart_drop = 0
					self.coin_drop = 0

				elif self.heart_dropped == True:

					self.freeze_dropped = False
					self.ammo_dropped = False
					self.coin_dropped = False
					self.freeze_drop = 0
					self.ammo_drop = 0
					self.coin_drop = 0

				elif self.freeze_dropped == True:

					self.heart_dropped = False
					self.ammo_dropped = False
					self.coin_dropped = False
					self.ammo_drop = 0
					self.heart_drop = 0
					self.coin_drop = 0

				elif self.coin_dropped == True:

					self.heart_dropped = False
					self.ammo_dropped = False
					self.freeze_dropped = False
					self.ammo_drop = 0
					self.heart_drop = 0
					self.freeze_drop = 0

				if self.ammo_dropped == True:

					self.image = pygame.image.load("ammo_drop.png").convert()

				elif self.heart_dropped == True:

					self.image = pygame.image.load("heart.png").convert()

				elif self.freeze_dropped == True:

					self.image = pygame.image.load("freeze_powerup.png").convert()

				elif self.coin_dropped == True:

					self.image = pygame.image.load("Coin.png")

				self.image.set_colorkey(BLACK)

				self.dropped_frames += 1

				if self.dropped_frames == 360:

					self.exploding = True
					self.freeze_drop = 0
					self.heart_drop = 0
					self.ammo_drop = 0
					self.coin_drop = 0
					self.exp_num = 0
					self.frame = 0


				player_collect = pygame.sprite.spritecollide(self,game.players,False)

				for pickup in player_collect:

					if self.ammo_dropped == True:

						game.player.ammo += 25
						self.ammo_drop = 0

					if self.heart_dropped == True:

						game.player.lives += 1
						self.heart_drop = 0

					if self.freeze_dropped == True:

						game.freeze_pickup = True
						self.freeze_drop = 0
						game.freeze_hit = True

					if self.coin_dropped == True:

						game.coins += 1
						self.coin_drop = 0

					self.respawn()

			elif self.ammo_dropped == False and self.freeze_dropped == False and \
			self.exploding == False and self.heart_dropped == False and \
			self.coin_dropped == False:

				if self.lives == 3:

					self.image = pygame.image.load("alien_level3.png").convert()
					self.image.set_colorkey(BLACK)

				elif self.lives == 2:

					self.image = pygame.image.load("alien_level2.png").convert()
					self.image.set_colorkey(BLACK)

				elif self.lives == 1:

					self.image = pygame.image.load("Alien.png").convert()
					self.image.set_colorkey(BLACK)

				if self.full_freeze == True:

					self.velx = 0
					self.vely = 0

				elif not self.full_freeze:

					speed = 2 * self.speed_multiplier

					x_diff = game.player.rect.center[0] - self.rect.center[0]
					y_diff = game.player.rect.center[1] - self.rect.center[1]
					angle = math.atan2( y_diff, x_diff )

					self.velx = math.cos(angle) * speed
					self.vely = math.sin(angle)  * speed

					self.rect.x += self.velx
					self.rect.y += self.vely

				bullet_alien_collision = pygame.sprite.spritecollide(self, game.bullets,True)
				player_alien_collision = pygame.sprite.spritecollide(self, game.players,False)

				for alien in  bullet_alien_collision:

					self.lives -= 1

					if self.lives <= 0:

						game.score += 1
						self.explode_sound.play()
						self.exploding = True

				for alien in player_alien_collision:

					self.explode_sound.play()

					self.heart_drop = 0
					self.ammo_drop = 0
					self.freeze_drop = 0
					self.coin_drop = 0

					game.player.lives -= self.lives

					self.exploding = True

			if self.exploding == True:

				self.explode()

		def respawn(self):
			""" The first four if statements don't respawn the alien. They
			check the alien for the lucky number and set the corresponding
			drop attribute to True if they match. If there is no active drop
			attributes, increase the speed multiplier and calculate a new,
			random a and y position. Set the image to the corresponding life
			number. Reset all the attributes.

			"""

			if self.heart_drop == 15:

				self.heart_dropped = True
				self.speed_multiplier *= 1.05

			if self.ammo_drop == 15:

				self.speed_multiplier *= 1.05
				self.ammo_dropped = True

			if self.freeze_drop == 15:

				self.speed_multiplier *= 1.05
				self.freeze_dropped = True

			if self.coin_drop == 15:

				self.speed_multiplier *= 1.05
				self.coin_dropped = True

			if self.heart_drop != 15 and self.ammo_drop != 15 and \
			self.freeze_drop != 15 and self.coin_drop != 15:

				lr = random.randrange(0,2)
				tb = random.randrange(0,2)

				self.speed_multiplier *= 1.05

				if lr == 0:

					self.rect.x = random.randrange(-2600,-100)

				elif lr == 1:

					self.rect.x = random.randrange(SCREEN_WIDTH + 100, SCREEN_WIDTH + 2600)

				if tb == 0:

					self.rect.y = random.randrange(-2600,-100)

				elif tb == 1:

					self.rect.y = random.randrange(SCREEN_HEIGHT + 100, SCREEN_HEIGHT + 2600)

				if game.score % 10 == 0:

					self.image = pygame.image.load("alien_level3.png").convert()
					self.lives = 3

				elif game.score % 3 == 0 and self.lives != 3:

					self.image = pygame.image.load("alien_level2.png").convert()
					self.lives = 2

				else:

					self.image = pygame.image.load("Alien.png").convert()
					self.lives = 1

				self.freeze_dropped = False
				self.dropped_frames = 0
				self.heart_dropped = False
				self.ammo_dropped = False
				self.coin_dropped = False
				self.freeze_drop = random.randrange(0, 30)
				self.heart_drop = random.randrange(0, 40)
				self.ammo_drop = random.randrange(0, 20)
				self.coin_drop = random.randrange(10, 20)
				self.exploding = False
				self.exp_num = 0
				self.frame = 0
				self.image.set_colorkey(BLACK)

		def explode(self):
			""" Stop movement. If the frame attribute reaches the explosion
			frame threshold, revoke the exploding attribute and tag it for
			respawn in the next update. If the frame attribute reaches the
			individual explosion frame threshold, move to the next frame.
			Always add one to frame attribute and set image to the corresponding
			explosion image for that frame number.

			"""

			exp_list = [self.e1,self.e2,self.e3,self.e4,self.e5]

			self.velx = 0
			self.vely = 0

			if self.frame == 25:

				self.exploding = False
				self.respawn()

			elif self.frame % 5 == 0:

				self.exp_num += 1

				if self.exp_num == 5:

					self.exp_num = 4

			if self.exploding == True:

				self.frame += 1
				self.image  = exp_list[self.exp_num]

	class Bullet(pygame.sprite.Sprite):

		""" Bullets that spawn from the player position and move towards the cursor.

		Args:
			image_string (str): Picture of the bullet (can change color).

		Attributes:
			image (pygame sprite): Pygame sprite image that uses the
			image_string arg.
			rect (pygame sprite rect): Rect attributes for sprite image.
			velx (int): Aliens x axis velocity.
			vely (int): Aliens y axis velocity.

		"""

		def __init__ (self, image_string):

			super(Bullet, self).__init__()

			self.image = pygame.image.load(image_string).convert()
			self.image.set_colorkey(BLACK)
			self.rect = self.image.get_rect()

			self.rect.x = 0
			self.rect.y = 0
			self.velx = 0
			self.vely = 0

		def update(self):
			""" Add the velx and vely attributes to the rect.x and rect.y
			positions, respectively. If the bullet goes off the screen, kill it.

			"""

			self.rect.y += self.vely
			self.rect.x += self.velx

			if self.rect.x + self.rect.width < 0 or self.rect.y + self.rect.height < 0:

				self.kill()

			elif self.rect.y > SCREEN_HEIGHT or self.rect.x > SCREEN_WIDTH:

				self.kill()

	class Cursor(pygame.sprite.Sprite):
		""" Cursor that is blitted in place of the windows cursor.

		Args:
			image_string (str): Image of the cursor.

		Attributes:
			image (pygame sprite): Pygame sprite image that uses the
			image_string arg.
			rect (pygame sprite rect): Rect attributes for sprite image.

		"""

		def __init__ (self,image_string):

			super(Cursor, self).__init__()

			self.image = pygame.image.load(image_string).convert()
			self.image.set_colorkey(BLACK)

			self.rect = self.image.get_rect()

		def update(self):
			""" Get the mouse position. Set the center of the cursor to that
			point.

			"""

			(mouse_x, mouse_y) = pygame.mouse.get_pos()
			self.rect.center = (mouse_x,mouse_y)

		def draw(self, screen):
			""" Blit the cursor to the screen.

			"""

			screen.blit(self.image, [self.rect.x, self.rect.y])

	class Text (pygame.sprite.Sprite):
		""" Turns text into a sprite.

		Args:
			text (str/int/float): The text to be converted into a sprite.
			font (font): The font used to create the text sprite.
			default_color (color): Default color of the text.
			highlight (bool): Boolean for weather or not the text should
			highlight when the cursor moves over it.

		Attributes:
			font (font): The font used to create the text sprite.
			color (color): The color the sprite is in the current frame.
			text (str/int/float): Puts str operator on the text arg to ensure
			it is a string.
			image (string image): Uses the text as image for sprite.
			rect (pygame sprite rect): Rect attributes for sprite image.
			highlight (bool): Boolean for weather or not the text should
			highlight when the cursor moves over it.

		"""

		def __init__ (self,text, font, default_color, highlight):

			super(Text, self).__init__()

			self.font = font
			self.color = default_color
			self.text = str(text)
			self.image = self.font.render(self.text, False, self.color)
			self.rect = self.image.get_rect()
			self.highlight = highlight

		def update(self):
			""" Update the image (in case of color change.)

			"""

			self.image = self.font.render(self.text, False, self.color)

		def draw(self,screen):
			""" Blit the text to the screen.

			"""

			screen.blit(self.image,[self.rect.x,self.rect.y])

	class Picture(pygame.sprite.Sprite):
		""" Turns images into sprites.

		Args:
			image_string (str): Image to be made into a sprite.

		Attributes:
			image (sprite image): Load image for the sprite.
			rect (pygame sprite rect): Rect attributes for sprite image.

		"""

		def __init__ (self, image_string):

			super(Picture, self).__init__()

			self.image = pygame.image.load(image_string).convert()
			self.image.set_colorkey(BLACK)

			self.rect = self.image.get_rect()

		def draw(self,screen):

			""" Draws the image to the screen.

			Args:
				screen (screen): Blit destinaiton.

			"""

			screen.blit(self.image, [self.rect.x, self.rect.y])

	class Star(pygame.sprite.Sprite):
		""" Star sprite images used for background.

		Args:
			image_string (str): Star image.

		Attribues:
			image (sprite image): Load image for the sprite.
			rect (pygame sprite rect): Rect attributes for sprite image.
			velx (int): Aliens x axis velocity.
			vely (int): Aliens y axis velocity.

		"""

		def __init__ (self, image_string):

			super(Star, self).__init__()

			self.image = pygame.image.load(image_string).convert()
			self.image.set_colorkey(BLACK)
			self.rect = self.image.get_rect()
			self.velx = 0
			self.vely = 0

		def update(self):
			""" Add the velx and vely attributes to the rect.x and rect.y
			positions, respectively. If the star goes off the top of the screen,
			reset the posiiton to the bottom of the screen.

			"""

			self.rect.x += self.velx
			self.rect.y += self.vely

			if self.rect.y + self.rect.height < 0:

				self.rect.y = SCREEN_HEIGHT

	class Game(object):
		""" Instance of the game.
		'04B_30_' is font name for windows. '04B' is font name for ubuntu.

		Important Attributes:
			Screen Booleans:
				title_screen: Screen that shows when the program is lanched.
				game_over: Screen that shows when the game is over and there
				is no new highscore.
				game: Screen that shows while playing the game.
				settings: Screen that shows when settings is selected from the
				main menu.
				paused: Screen that shows when the game is paused.
				player_select: Screen that shows when change player is selected
				from the settings menu.
				bullet_select: Screen that shows when change bullet is selected
				from the settings menu.
				cursor_select: Screen that shows when change cursor is selected
				from the settings menu.
				highscore_screen = Screen that shows when highscores is selected
				from the main menu.
				new_highscore_screen: Screen that shows when the game is over and
				the player achieves a top 5 score.
				enter_name_screen: Screen that shows when the player selects
				continue from the new highscore screen.
				upgrades_screen: Screen that shows when upgrades is selected
				from the settings screen.

			Lists and Groups:
				settings_screen_items (sprite group): Holds items for settings screen.
				change_bullet_items (sprite group): Holds items for bullet select screen.
				change_player_items (sprite group): Holds items for player select screen.
				change_cursor_items (sprite group): Holds items for cursor select screen.
				title_screen_items (sprite group): Holds items for title screen screen.
				game_over_items (sprite group): Holds items for game over screen.
				pause_items (sprite group): Holds items for paused screen.
				game_items (sprite group): Holds items for the game itself.
				new_highscore_items (sprite group): Holds items for new highscore screen.
				bullets (sprite group): Holds list of bullets.
				players (sprite group): Holds list of player(s).
				aliens (sprite group): Holds list pf aliens.
				highscore_items (sprite group): Holds items for highscores screen.
				highscore_name_items (sprite group): Holds list of names for highscore screen.
				keyboard (sprite group): Holds all keys on the keyboard.
				upgrade_screen_items (sprite group): Holds items for upgrade screen.

			Sprites:
				player (sprite): The player sprite.
				[All Picture Sprites] (sprite): Misc image sprites.
				[All Text Sprites] (sprite): Misc text sprites.

			Misc:
				score (int): Number of aliens the player has killed.
				ammo_number (int): Numerical value for corresponding ammo type.
				player_number (int): Numerical value for corresponding player type.
				main_music (audio): Main track for the game.
				shoot (audio): Sound that plays when a bulelt is fired.
				alphabet (list): A list of letters.

		"""

		def __init__ (self):

			self.title_screen = True
			self.game_over = False
			self.game = False
			self.settings = False
			self.paused = False
			self.player_select = False
			self.bullet_select = False
			self.cursor_select = False
			self.highscore_screen = False
			self.new_highscore_screen = False
			self.enter_name_screen = False
			self.upgrades_screen = False
			self.lives_with_upgrades = 3
			self.ammo_with_upgrades = 100

			self.score = 0
			self.coins = 0
			self.highscores_list = get_highscores()
			self.highscore_names = get_names()

			self.green_ammo = "green_ammo.png"
			self.red_ammo = "red_ammo.png"
			self.purple_ammo = "purple_ammo.png"
			self.blue_ammo = "blue_ammo.png"
			self.yellow_ammo = "yellow_ammo.png"
			self.ammo_number = 0

			self.player_number = 0

			self.ammo_type = self.green_ammo

			self.main_music = pygame.mixer.Sound("main_music.ogg")
			self.shoot = pygame.mixer.Sound("shoot_sound.ogg")

			self.freeze_pickup  = False
			self.freeze_hit = False
			self.frozen_frames  = 0

			menu_font_size = int(round(SCREEN_HEIGHT / 13.5))
			game_font_size = int(round(SCREEN_HEIGHT / 17.5))
			self.font = pygame.font.SysFont('04B_30_', menu_font_size, False, False)
			self.small_font = pygame.font.SysFont('04B_30_', game_font_size, False, False)
			self.universal_spacing_gap = 10

			self.settings_screen_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.change_bullet_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.change_player_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.change_cursor_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.title_screen_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.game_over_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.pause_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.game_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.new_highscore_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.bullets = pygame.sprite.Group()
			self.players = pygame.sprite.Group()
			self.aliens = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.highscore_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.highscore_name_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.keyboard = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])
			self.upgrade_screen_items = pygame.sprite.LayeredUpdates([pygame.sprite.Group()])

			""" - - - Create sprites - - - """

			self.player = Player("original.png")
			self.player.lives = self.lives_with_upgrades
			self.player.ammo = self.ammo_with_upgrades
			self.game_items.add(self.player)
			self.players.add(self.player)

			self.alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M" \
			,"N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

			for i in range(30):

				alien = Alien()
				self.aliens.add(alien)

			self.cursor = Cursor("red_cursor.png")

			self.blue_player_pic = Picture("big_blue.png")
			self.original_player_pic = Picture("big_original.png")
			self.yellow_player_pic = Picture("big_yellow.png")
			self.green_ammo_pic = Picture("green_ammo_big.png")
			self.red_ammo_pic = Picture("red_ammo_big.png")
			self.purple_ammo_pic = Picture("purple_ammo_big.png")
			self.yellow_ammo_pic = Picture("yellow_ammo_big.png")
			self.blue_ammo_pic = Picture("blue_ammo_big.png")
			self.title_pic = Picture("Title.png")
			self.big_red_cursor_pic = Picture("big_red_cursor.png")
			self.big_blue_cursor_pic = Picture("big_blue_cursor.png")
			self.big_green_cursor_pic = Picture("big_green_cursor.png")
			self.big_purple_cursor_pic = Picture("big_purple_cursor.png")
			self.big_yellow_cursor_pic = Picture("big_yellow_cursor.png")
			self.heart_pic = Picture("heart.png")
			self.coin_pic = Picture("Coin.png")
			self.coin_pic2 = Picture("Coin.png")
			self.speed_coin = Picture("Coin.png")
			self.life_coin = Picture("Coin.png")
			self.ammo_coin = Picture("Coin.png")

			self.player_select_arrow = Picture("selection_arrow.png")
			self.bullet_select_arrow = Picture("selection_arrow.png")

			self.paused_word = Text("PAUSED", self.font, WHITE, False)
			self.go_home_word = Text("GO HOME", self.font, WHITE, True)
			self.back_word = Text("BACK", self.font, WHITE, True)
			self.start_word = Text("START", self.font, WHITE, True)
			self.game_over_word = Text("GAME OVER!", self.font, WHITE, False)
			self.restart_word = Text("RESTART", self.font, WHITE, True)
			self.settings_word = Text("SETTINGS", self.font, WHITE, True)
			self.upgrades_word = Text("UPGRADES", self.font, WHITE, True)
			self.quit_word = Text("QUIT", self.font, WHITE, True)
			self.change_player_word = Text("PLAYER", self.font, WHITE, True)
			self.change_bullet_word = Text("BULLET", self.font, WHITE, True)
			self.change_cursor_word = Text("CURSOR", self.font, WHITE, True)
			self.score_word = Text("SCORE:", self.small_font, WHITE, False)
			self.highscore_word = Text("HIGHSCORES", self.font, WHITE, True)
			self.new_highscore_word = Text("NEW HIGHSCORE!", self.font, WHITE, False)
			self.increase_speed_word = Text("MOAR SPEED 10", self.font, WHITE, True)
			self.add_start_life_word = Text("MOAR LIFE 20", self.font, WHITE, True)
			self.ammo_upgrade_word = Text("MOAR AMMO 30", self.font, WHITE, True)
			self.coin_count_word = Text(str(self.coins), self.font, WHITE, False)
			self.coin_count_word2 = Text(str(self.coins), self.font, WHITE, False)
			self.new_highscore_score_word = Text(str(self.score), self.font, WHITE, False)
			self.entered_name_string = ""
			self.entered_name = Text(self.entered_name_string, self.font, WHITE, False)
			self.continue_word = Text("CONTINUE", self.font, WHITE, True)
			self.done_word = Text("DONE", self.font, WHITE, True)
			self.backspace_word = Text("BCKSPC", self.font, WHITE, True)
			self.number_score = Text(str(self.score), self.small_font, WHITE, False)
			self.ammo_counter = Text(str(self.player.ammo), self.small_font, GREEN, False)

			self.upgrade_screen_items.add(self.increase_speed_word)
			self.upgrade_screen_items.add(self.add_start_life_word)
			self.upgrade_screen_items.add(self.coin_pic2)
			self.upgrade_screen_items.add(self.coin_count_word2)
			self.upgrade_screen_items.add(self.ammo_upgrade_word)
			self.upgrade_screen_items.add(self.speed_coin)
			self.upgrade_screen_items.add(self.life_coin)
			self.upgrade_screen_items.add(self.ammo_coin)

			self.new_highscore_items.add(self.new_highscore_word)
			self.new_highscore_items.add(self.new_highscore_score_word)
			self.new_highscore_items.add(self.continue_word)

			self.change_player_items.add(self.blue_player_pic)
			self.change_player_items.add(self.original_player_pic)
			self.change_player_items.add(self.yellow_player_pic)

			self.change_cursor_items.add(self.big_red_cursor_pic)
			self.change_cursor_items.add(self.big_blue_cursor_pic)
			self.change_cursor_items.add(self.big_green_cursor_pic)
			self.change_cursor_items.add(self.big_purple_cursor_pic)
			self.change_cursor_items.add(self.big_yellow_cursor_pic)

			self.change_bullet_items.add(self.green_ammo_pic)
			self.change_bullet_items.add(self.red_ammo_pic)
			self.change_bullet_items.add(self.purple_ammo_pic)
			self.change_bullet_items.add(self.yellow_ammo_pic)
			self.change_bullet_items.add(self.blue_ammo_pic)

			self.settings_screen_items.add(self.change_cursor_word)
			self.settings_screen_items.add(self.change_bullet_word)
			self.settings_screen_items.add(self.change_player_word)
			self.settings_screen_items.add(self.upgrades_word)

			self.title_screen_items.add(self.title_pic)
			self.title_screen_items.add(self.start_word)
			self.title_screen_items.add(self.highscore_word)
			self.title_screen_items.add(self.settings_word)
			self.title_screen_items.add(self.quit_word)
			self.title_screen_items.add(self.coin_pic)
			self.title_screen_items.add(self.coin_count_word)

			self.game_over_items.add(self.game_over_word)
			self.game_over_items.add(self.restart_word)
			self.game_over_items.add(self.go_home_word)
			self.game_over_items.add(self.quit_word)

			self.pause_items.add(self.paused_word)
			self.pause_items.add(self.go_home_word)
			self.pause_items.add(self.quit_word)

			self.game_items.add(self.score_word)
			self.game_items.add(self.number_score)
			self.game_items.add(self.ammo_counter)
			self.game_items.add(self.player)

			self.highscore_items.add(self.highscore_word)

			for i in range(0,5):

				score = self.highscores_list[i]

				sprite_score = Text(score, self.font, WHITE, False)

				self.highscore_items.add(sprite_score)

			for i in range(0,5):

				name = self.highscore_names[i]

				sprite_name = Text(name, self.font, WHITE, False)

				self.highscore_name_items.add(sprite_name)

			for character in self.alphabet:

				letter = Text(character, self.font, WHITE, True)
				self.keyboard.add(letter)

		def spawn_bullet(self, mouse_x, mouse_y):
			""" Spawn a bullet from the player position and set its trajectory
			towards the cursor position.

			"""

			self.shoot.play()
			self.player.ammo -= 1

			bullet_speed = 20
			angle = math.atan2(self.player.rect.center[1]-mouse_y,
			self.player.rect.center[0]-mouse_x)
			x_vel = math.cos(angle) * (-1 * bullet_speed)
			y_vel = math.sin(angle)  * (-1 * bullet_speed)
			bullet = Bullet(self.ammo_type)
			bullet.rect.x = self.player.rect.center[0] - (bullet.rect.width / 2)
			bullet.rect.y = self.player.rect.center[1] - (bullet.rect.height / 2)
			bullet.velx = x_vel
			bullet.vely = y_vel

			self.game_items.add(bullet)
			self.bullets.add(bullet)

			return

		def update_changing_items(self):
			""" Update the items that need to refresh every frame.

			"""

			self.game_items.remove(self.number_score)
			self.game_items.remove(self.ammo_counter)

			self.number_score = Text(str(self.score), self.small_font, WHITE, False)
			self.ammo_counter = Text(str(self.player.ammo), self.small_font, GREEN, False)

			self.ammo_counter.rect.y = self.heart_pic.rect.y + self.heart_pic.rect.height + 10
			self.ammo_counter.rect.x = 10

			self.number_score.rect.x = self.score_word.rect.x + self.score_word.rect.width + 10
			self.number_score.rect.y = 10

			self.game_items.add(self.number_score)
			self.game_items.add(self.ammo_counter)

			return

		def draw_lives(self, screen):
			""" Draw the appropriate amount of lives.

			"""

			heart_x_offset = 0

			for i in range(self.player.lives):

				self.heart_pic.rect.x = 10 + heart_x_offset
				self.heart_pic.rect.y = self.score_word.rect.y + self.score_word.rect.height + 10
				self.heart_pic.draw(screen)

				heart_x_offset += self.heart_pic.rect.width + 10

			return

		def check_cursor_overlap(self, info):
			""" Check if the cursor is overlapping with the info arg. If so,
			return True. If not, return False.

			Args:
				info (sprite): The sprite to be checked for cursor overlapping.

			"""

			(mouse_x, mouse_y) = pygame.mouse.get_pos()

			if mouse_x in range(info.rect.x, info.rect.x + info.rect.width) \
			and mouse_y in range(info.rect.y, info.rect.y + info.rect.height):

				return True

			else:

				return False

		def highlight_cursor_text(self, item_list):
			""" Checks if the cursor is overlapping with all items in the item_list
			arg. If so, change the color of the text. If not, keep color white.

			Args:
				item_list (list): List to be checked for cursor overlap.

			"""

			for i in range(len(item_list)):

				item = pygame.sprite.LayeredUpdates.get_sprite(item_list, i)

				if Game.check_cursor_overlap(game, item) is True and isinstance(item, Text) == True:

					if hasattr(item, "highlight"):

						if item.highlight == True:

							item.color = RED

				else:

					item.color = WHITE

			return

		def highlight_cursor_word(self, word):
			""" Highlight the given word if the word is highlightable and the
			cursor is on that word.

			Args:
				word (sprite): The word to be highlighted.

			"""

			if Game.check_cursor_overlap(game, word) is True and isinstance(word, Text) == True:

				if hasattr(word, "highlight"):

					word.color = RED

			else:

				word.color = WHITE

			return

		def process_events(self):
			""" Handle user inputs.

			"""

			if self.player.lives <= 0 and self.game == True:

				self.new_highscore_items.remove(self.new_highscore_score_word)
				self.new_highscore_score_word = Text(str(self.score), self.font, WHITE, False)
				self.new_highscore_items.add(self.new_highscore_score_word)

				self.game = False

				if self.score > self.highscores_list[4]:

					self.new_highscore_screen = True

				else:

					self.game_over = True

			for event in pygame.event.get():

				if event.type == pygame.QUIT:

					return True

				if self.game:

					if self.paused == True:

						Game.highlight_cursor_text(game, self.pause_items)

				elif self.title_screen:

					Game.highlight_cursor_text(game, self.title_screen_items)

				elif self.settings:

					Game.highlight_cursor_text(game, self.settings_screen_items)
					Game.highlight_cursor_word(game, self.back_word)
					Game.highlight_cursor_text(game, self.upgrade_screen_items)

				elif self.highscore_screen:

					Game.highlight_cursor_word(game, self.back_word)

				elif self.game_over:

					Game.highlight_cursor_text(game, self.game_over_items)

				elif self.new_highscore_screen:

					Game.highlight_cursor_text(game, self.new_highscore_items)

				elif self.enter_name_screen:

					Game.highlight_cursor_text(game, self.keyboard)
					Game.highlight_cursor_word(game, self.backspace_word)
					Game.highlight_cursor_word(game, self.done_word)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

					(mouse_x, mouse_y) = pygame.mouse.get_pos()

					if self.game:

						if self.player.ammo > 0 and not self.paused:

							Game.spawn_bullet(game, mouse_x, mouse_y)

						if self.paused:

							if Game.check_cursor_overlap(game, self.go_home_word) is True:

								self.score = 0
								self.lives = 3
								self.game = False
								self.paused = False
								self.title_screen = True

								self.aliens.empty()

								for i in range(30):

									alien = Alien()
									self.aliens.add(alien)

								self.player.rect.x = (SCREEN_WIDTH / 2) - (self.player.rect.width / 2)
								self.player.rect.y = (SCREEN_HEIGHT / 2) - (self.player.rect.height / 2)

								self.paused_word.color = WHITE

								self.upgrade_screen_items.remove(self.coin_count_word2)
								self.title_screen_items.remove(self.coin_count_word)

								self.coin_count_word = Text(str(self.coins), self.font, WHITE, False)
								self.coin_count_word2 = Text(str(self.coins), self.font, WHITE, False)

								self.upgrade_screen_items.add(self.coin_count_word2)
								self.title_screen_items.add(self.coin_count_word)

					elif self.title_screen:

						if Game.check_cursor_overlap(game, self.start_word) is True:

							self.game = True
							self.highscore_screen = False
							self.title_screen = False
							self.start_word.color = WHITE
							self.bullets.empty()

						if Game.check_cursor_overlap(game, self.settings_word) is True:

							self.settings = True
							self.title_screen = False
							self.settings_word.color = WHITE

						if Game.check_cursor_overlap(game, self.highscore_word) is True:

							self.title_screen = False
							self.highscore_screen = True
							self.highscore_word.color = WHITE

						if Game.check_cursor_overlap(game, self.quit_word) is True:

							return True

					elif self.enter_name_screen:

						for i in range(len(self.keyboard)):

							item = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, i)

							if Game.check_cursor_overlap(game, item) is True:

								self.entered_name_string += item.text
								self.entered_name = Text(self.entered_name_string, self.font, WHITE, False)

						if Game.check_cursor_overlap(game, self.backspace_word) is True:

							self.entered_name_string = self.entered_name_string[0:len(self.entered_name_string) - 1]
							self.entered_name = Text(self.entered_name_string, self.font, WHITE, False)

						if Game.check_cursor_overlap(game, self.done_word) is True and \
						len(self.entered_name_string) > 1 and len(self.entered_name_string) < 10:

							name_index = insert_score(self.score)
							insert_name(self.entered_name_string, name_index)
							self.highscores_list = get_highscores()
							self.highscore_names = get_names()

							self.highscore_items.empty()
							self.highscore_name_items.empty()

							self.highscore_items.add(self.highscore_word)

							for i in range(0,5):

								score = self.highscores_list[i]

								sprite_score = Text(score, self.font, WHITE, False)

								self.highscore_items.add(sprite_score)

							for i in range(0,5):

								name = self.highscore_names[i]

								sprite_name = Text(name, self.font, WHITE, False)

								self.highscore_name_items.add(sprite_name)

							self.game = False
							self.enter_name_screen = False
							self.new_highscore_screen = False
							self.title_screen = False
							self.highscore_screen = True
							self.player.lives = self.lives_with_upgrades
							self.score = 0
							self.player.ammo = 100
							self.aliens.empty()

							for i in range(30):

								alien = Alien()
								self.aliens.add(alien)

							self.player.rect.x = (SCREEN_WIDTH / 2) - (self.player.rect.width / 2)
							self.player.rect.y = (SCREEN_HEIGHT / 2) - (self.player.rect.height / 2)

							self.entered_name_string = ""
							self.entered_name = Text(self.entered_name_string, self.font, WHITE, False)
							self.continue_word.color = WHITE

							self.upgrade_screen_items.remove(self.coin_count_word2)
							self.title_screen_items.remove(self.coin_count_word)

							self.coin_count_word = Text(str(self.coins), self.font, WHITE, False)
							self.coin_count_word2 = Text(str(self.coins), self.font, WHITE, False)

							self.upgrade_screen_items.add(self.coin_count_word2)
							self.title_screen_items.add(self.coin_count_word)
							self.done_word.color = WHITE

					elif self.settings:

						if Game.check_cursor_overlap(game, self.back_word) is True:

							if self.player_select:

								self.player_select = False

							elif self.bullet_select:

								self.bullet_select = False

							elif self.cursor_select:

								self.cursor_select = False

							elif self.upgrades_screen:

								self.upgrades_screen = False

							else:

								self.settings = False
								self.title_screen = True
								self.back_word.color = WHITE

							self.back_word.color = WHITE

						if self.player_select:

							if Game.check_cursor_overlap(game, self.original_player_pic) is True:

								self.game_items.remove(self.player)
								self.players.remove(self.player)
								self.player = Player("original.png")
								self.game_items.add(self.player)
								self.players.add(self.player)
								self.player_number = 0

							if Game.check_cursor_overlap(game, self.blue_player_pic) is True:

								self.game_items.remove(self.player)
								self.players.remove(self.player)
								self.player = Player("blue_ship.png")
								self.game_items.add(self.player)
								self.players.add(self.player)
								self.player_number = 1

							if Game.check_cursor_overlap(game, self.yellow_player_pic) is True:

								self.game_items.remove(self.player)
								self.players.remove(self.player)
								self.player = Player("yellow_ship.png")
								self.game_items.add(self.player)
								self.players.add(self.player)
								self.player_number = 2

							self.player.lives = self.lives_with_upgrades

						if self.bullet_select:

							if Game.check_cursor_overlap(game, self.green_ammo_pic) is True:

								self.ammo_type = self.green_ammo
								self.ammo_number = 0

							elif Game.check_cursor_overlap(game, self.red_ammo_pic) is True:

								self.ammo_type = self.red_ammo
								self.ammo_number = 1

							elif Game.check_cursor_overlap(game, self.purple_ammo_pic) is True:

								self.ammo_type = self.purple_ammo
								self.ammo_number = 2

							elif Game.check_cursor_overlap(game, self.blue_ammo_pic) is True:

								self.ammo_type = self.blue_ammo
								self.ammo_number = 3

							elif Game.check_cursor_overlap(game, self.yellow_ammo_pic) is True:

								self.ammo_type = self.yellow_ammo
								self.ammo_number = 4

						if self.cursor_select:

							if Game.check_cursor_overlap(game, self.big_red_cursor_pic) is True:

								self.cursor = Cursor("red_cursor.png")

							elif Game.check_cursor_overlap(game, self.big_green_cursor_pic) is True:

								self.cursor = Cursor("green_cursor.png")

							elif Game.check_cursor_overlap(game, self.big_blue_cursor_pic) is True:

								self.cursor = Cursor("blue_cursor.png")

							elif Game.check_cursor_overlap(game, self.big_purple_cursor_pic) is True:

								self.cursor = Cursor("purple_cursor.png")

							elif Game.check_cursor_overlap(game, self.big_yellow_cursor_pic) is True:

								self.cursor = Cursor("yellow_cursor.png")

						if self.upgrades_screen:

							if Game.check_cursor_overlap(game, self.increase_speed_word) is True and self.coins >= 10:

								self.player.speed += 1
								self.coins -= 10

								self.upgrade_screen_items.remove(self.coin_count_word2)
								self.title_screen_items.remove(self.coin_count_word)

								self.coin_count_word = Text(str(self.coins), self.font, WHITE, False)
								self.coin_count_word2 = Text(str(self.coins), self.font, WHITE, False)

								self.upgrade_screen_items.add(self.coin_count_word2)
								self.title_screen_items.add(self.coin_count_word)

							if Game.check_cursor_overlap(game, self.add_start_life_word) is True and self.coins >= 20:

								self.lives_with_upgrades += 1
								self.player.lives = self.lives_with_upgrades
								self.coins -= 20

								self.upgrade_screen_items.remove(self.coin_count_word2)
								self.title_screen_items.remove(self.coin_count_word)

								self.coin_count_word = Text(str(self.coins), self.font, WHITE, False)
								self.coin_count_word2 = Text(str(self.coins), self.font, WHITE, False)

								self.upgrade_screen_items.add(self.coin_count_word2)
								self.title_screen_items.add(self.coin_count_word)

							if Game.check_cursor_overlap(game, self.ammo_upgrade_word) is True and self.coins >= 30:

								self.ammo_with_upgrades += 20
								self.player.ammo = self.ammo_with_upgrades
								self.coins -= 30

								self.upgrade_screen_items.remove(self.coin_count_word2)
								self.title_screen_items.remove(self.coin_count_word)

								self.coin_count_word = Text(str(self.coins), self.font, WHITE, False)
								self.coin_count_word2 = Text(str(self.coins), self.font, WHITE, False)

								self.upgrade_screen_items.add(self.coin_count_word2)
								self.title_screen_items.add(self.coin_count_word)

						else:

							if Game.check_cursor_overlap(game, self.change_player_word) is True:

								self.player_select = True
								self.change_player_word.color = WHITE

							if Game.check_cursor_overlap(game, self.change_bullet_word) is True:

								self.bullet_select = True
								self.change_cursor_word.color = WHITE

							if Game.check_cursor_overlap(game, self.change_cursor_word) is True:

								self.cursor_select = True
								self.change_cursor_word.color = WHITE

							if Game.check_cursor_overlap(game, self.upgrades_word) is True:

								self.upgrades_screen = True
								self.upgrades_word.color = WHITE

					elif self.highscore_screen:

						if Game.check_cursor_overlap(game, self.back_word) is True:

							self.title_screen = True
							self.highscore_screen = False

					elif self.game_over:

						if Game.check_cursor_overlap(game, self.restart_word) is True:

							self.aliens.empty()

							for i in range(30):

								alien = Alien()
								self.aliens.add(alien)

							self.score = 0
							self.player.lives = self.lives_with_upgrades
							self.player.ammo = 100
							self.game = True
							self.game_over = False

						elif Game.check_cursor_overlap(game, self.quit_word) is True:

							self.game_over = False

							return True

						elif Game.check_cursor_overlap(game, self.go_home_word) is True:

							self.paused = False
							self.game = False
							self.game_over = False
							self.title_screen = True
							self.player.lives = self.lives_with_upgrades
							self.player.ammo = 100
							self.score = 0

							self.player.rect.x = (SCREEN_WIDTH / 2) - (self.player.rect.width / 2)
							self.player.rect.y = (SCREEN_HEIGHT / 2) - (self.player.rect.height / 2)

							self.aliens.empty()

							for i in range(30):

								alien = Alien()
								self.aliens.add(alien)

							self.upgrade_screen_items.remove(self.coin_count_word2)
							self.title_screen_items.remove(self.coin_count_word)

							self.coin_count_word = Text(str(self.coins), self.font, WHITE, False)
							self.coin_count_word2 = Text(str(self.coins), self.font, WHITE, False)

							self.upgrade_screen_items.add(self.coin_count_word2)
							self.title_screen_items.add(self.coin_count_word)

							self.restart_word.color = WHITE


					elif self.new_highscore_screen:

						if Game.check_cursor_overlap(game, self.continue_word) is True:

							self.enter_name_screen = True
							self.new_highscore_screen = False
							self.game_over = False

				if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_ESCAPE:

						return True

					elif event.key == pygame.K_w:

						self.player.change_speed(0,-1 * self.player.speed)

					elif event.key == pygame.K_a:

						self.player.change_speed(-1 * self.player.speed,0)

					elif event.key == pygame.K_s:

						self.player.change_speed(0,self.player.speed)

					elif event.key == pygame.K_d:

						self.player.change_speed(self.player.speed,0)

					elif event.key == pygame.K_p:

						if self.paused == True:

							self.paused = False

						elif self.game:

							self.paused = True

				if event.type == pygame.KEYUP:

					if event.key == pygame.K_w:

						self.player.change_speed(0,self.player.speed)

					elif event.key == pygame.K_a:

						self.player.change_speed(self.player.speed,0)

					elif event.key == pygame.K_s:

						self.player.change_speed(0,-1 * self.player.speed)

					elif event.key == pygame.K_d:

						self.player.change_speed(-1 * self.player.speed,0)

			return

		def run_res_math(self):
			""" Calculate the appropriate positions for everything in relaiton to the screen
			size.

			"""

			self.back_word.rect.x = self.universal_spacing_gap
			self.back_word.rect.y = self.universal_spacing_gap

			if self.title_screen:

				for i in range(len(self.title_screen_items)):

					item = pygame.sprite.LayeredUpdates.get_sprite(self.title_screen_items, i)

					if i == 0:

						item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width / 2)
						item.rect.y = 20

					elif i == 5:

						item.rect.x = (SCREEN_WIDTH - item.rect.width - self.universal_spacing_gap)
						item.rect.y = self.universal_spacing_gap

					elif i == 6:

						item.rect.x = (SCREEN_WIDTH - item.rect.width - 50 - self.universal_spacing_gap)
						item.rect.y = self.universal_spacing_gap - 3

					else:

						item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width / 2)
						item.rect.y = (i + 7.25) * (SCREEN_HEIGHT / (len(self.title_screen_items) + 6)) - (item.rect.height / 2)

			elif self.game:

				self.score_word.rect.x = self.universal_spacing_gap
				self.score_word.rect.y = self.universal_spacing_gap

				self.number_score.rect.x = self.score_word.rect.x + self.score_word.rect.width + self.universal_spacing_gap
				self.number_score.rect.y = self.universal_spacing_gap

				self.ammo_counter.rect.x = self.universal_spacing_gap
				self.ammo_counter.rect.y = self.heart_pic.rect.y + self.heart_pic.rect.height + self.universal_spacing_gap

				if self.paused:

					for i in range(len(self.pause_items)):

						item = pygame.sprite.LayeredUpdates.get_sprite(self.pause_items, i)

						item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width / 2)
						item.rect.y = (i + 1) * (SCREEN_HEIGHT / (len(self.pause_items) + 1)) - (item.rect.height / 2)

			elif self.highscore_screen:

				for i in range(len(self.highscore_items)):

					item = pygame.sprite.LayeredUpdates.get_sprite(self.highscore_items, i)
					item2 = pygame.sprite.LayeredUpdates.get_sprite(self.highscore_name_items, i - 1)

					if i == 0:

						item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width / 2)

					else:

						item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width + item2.rect.width / 2)

					item.rect.y = (i + 1) * (SCREEN_HEIGHT / (len(self.highscore_items) + 1)) - (item.rect.height / 2)

				for i in range(len(self.highscore_name_items)):

					item = pygame.sprite.LayeredUpdates.get_sprite(self.highscore_name_items, i)
					item2 = pygame.sprite.LayeredUpdates.get_sprite(self.highscore_items, i + 1)
					item.rect.x = item2.rect.x + item2.rect.width + 50
					item.rect.y = (i + 2) * (SCREEN_HEIGHT / (len(self.highscore_items) + 1)) - (item.rect.height / 2)

			elif self.new_highscore_screen:

				for i in range(len(self.new_highscore_items)):

					item = pygame.sprite.LayeredUpdates.get_sprite(self.new_highscore_items, i)
					item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width / 2)
					item.rect.y = (i + 1) * (SCREEN_HEIGHT / (len(self.new_highscore_items) + 1)) - (item.rect.height / 2)

			elif self.enter_name_screen:

				for i in range(8):

					key = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, i)
					key.rect.x = ((i + 1) * (SCREEN_WIDTH / 9)) - (key.rect.width / 2)
					key.rect.y = (2 * (SCREEN_HEIGHT / 6)) - (key.rect.height / 2)

				for i in range(8):

					key = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, i + 8)
					key.rect.x = ((i + 1) * (SCREEN_WIDTH / 9)) - (key.rect.width / 2)
					key.rect.y = (3 * (SCREEN_HEIGHT / 6)) - (key.rect.height / 2)

				for i in range(8):

					key = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, i + 16)
					key.rect.x = ((i + 1) * (SCREEN_WIDTH / 9)) - (key.rect.width / 2)
					key.rect.y = (4 * (SCREEN_HEIGHT / 6)) - (key.rect.height / 2)

				for i in range(2):

					key = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, i + 24)
					key.rect.x = ((i + 1) * (SCREEN_WIDTH / 9)) - (key.rect.width / 2)
					key.rect.y = (5 * (SCREEN_HEIGHT / 6)) - (key.rect.height / 2)

				backspace_x = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, 2)
				backsapce_y = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, 25)
				self.backspace_word.rect.x = backspace_x.rect.x
				self.backspace_word.rect.y = backsapce_y.rect.y

				done_x = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, 6)
				done_y = pygame.sprite.LayeredUpdates.get_sprite(self.keyboard, 25)
				self.done_word.rect.x = done_x.rect.x
				self.done_word.rect.y = done_y.rect.y

				self.entered_name.rect.x = (SCREEN_WIDTH / 2) - (self.entered_name.rect.width / 2)
				self.entered_name.rect.y = (SCREEN_HEIGHT / 6) - (key.rect.height / 2)

			elif self.game_over:

				for i in range(len(self.game_over_items)):

					item = pygame.sprite.LayeredUpdates.get_sprite(self.game_over_items, i)

					item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width / 2)
					item.rect.y = (i + 1) * (SCREEN_HEIGHT / (len(self.game_over_items) + 1)) - (item.rect.height / 2)

			elif self.settings:

				self.back_word.rect.x = self.universal_spacing_gap
				self.back_word.rect.y = self.universal_spacing_gap

				if self.player_select:

					for i in range(len(self.change_player_items)):

						item = pygame.sprite.LayeredUpdates.get_sprite(self.change_player_items, i)

						item.rect.x = (i + 1) * (SCREEN_WIDTH / (len(self.change_player_items) + 1)) - (item.rect.width / 2)
						item.rect.y = (SCREEN_HEIGHT / 2) - (item.rect.height / 2)

					if self.player_number == 0:

						self.player_select_arrow.rect.x = (self.original_player_pic.rect.x + (self.original_player_pic.rect.width / 2)) - \
						(self.player_select_arrow.rect.width / 2)
						self.player_select_arrow.rect.y = (self.original_player_pic.rect.y - self.player_select_arrow.rect.height - self.universal_spacing_gap)

					elif self.player_number == 1:

						self.player_select_arrow.rect.x = (self.blue_player_pic.rect.x + (self.blue_player_pic.rect.width / 2)) - \
						(self.player_select_arrow.rect.width / 2)
						self.player_select_arrow.rect.y = (self.blue_player_pic.rect.y - self.player_select_arrow.rect.height - self.universal_spacing_gap)

					elif self.player_number == 2:

						self.player_select_arrow.rect.x = (self.yellow_player_pic.rect.x + (self.yellow_player_pic.rect.width / 2)) - \
						(self.player_select_arrow.rect.width / 2)
						self.player_select_arrow.rect.y = (self.yellow_player_pic.rect.y - self.player_select_arrow.rect.height - self.universal_spacing_gap)

				elif self.bullet_select:

					for i in range(len(self.change_bullet_items)):

						item = pygame.sprite.LayeredUpdates.get_sprite(self.change_bullet_items, i)

						item.rect.x = (i + 1) * (SCREEN_WIDTH / (len(self.change_bullet_items) + 1)) - (item.rect.width / 2)
						item.rect.y = (SCREEN_HEIGHT / 2) - (item.rect.height / 2)

					if self.ammo_number == 0:

						self.bullet_select_arrow.rect.x = (self.green_ammo_pic.rect.x + (self.green_ammo_pic.rect.width / 2)) - \
						(self.bullet_select_arrow.rect.width / 2)
						self.bullet_select_arrow.rect.y = (self.green_ammo_pic.rect.y - self.bullet_select_arrow.rect.height - self.universal_spacing_gap)

					if self.ammo_number == 1:

						self.bullet_select_arrow.rect.x = (self.red_ammo_pic.rect.x + (self.red_ammo_pic.rect.width / 2)) - \
						(self.bullet_select_arrow.rect.width / 2)
						self.bullet_select_arrow.rect.y = (self.red_ammo_pic.rect.y - self.bullet_select_arrow.rect.height - self.universal_spacing_gap)

					if self.ammo_number == 2:

						self.bullet_select_arrow.rect.x = (self.purple_ammo_pic.rect.x + (self.purple_ammo_pic.rect.width / 2)) - \
						(self.bullet_select_arrow.rect.width / 2)
						self.bullet_select_arrow.rect.y = (self.purple_ammo_pic.rect.y - self.bullet_select_arrow.rect.height - self.universal_spacing_gap)

					if self.ammo_number == 3:

						self.bullet_select_arrow.rect.x = (self.blue_ammo_pic.rect.x + (self.blue_ammo_pic.rect.width / 2)) - \
						(self.bullet_select_arrow.rect.width / 2)
						self.bullet_select_arrow.rect.y = (self.blue_ammo_pic.rect.y - self.bullet_select_arrow.rect.height - self.universal_spacing_gap)

					if self.ammo_number == 4:

						self.bullet_select_arrow.rect.x = (self.yellow_ammo_pic.rect.x + (self.yellow_ammo_pic.rect.width / 2)) - \
						(self.bullet_select_arrow.rect.width / 2)
						self.bullet_select_arrow.rect.y = (self.yellow_ammo_pic.rect.y - self.bullet_select_arrow.rect.height - self.universal_spacing_gap)

				elif self.cursor_select:

					for i in range(len(self.change_cursor_items)):

						item = pygame.sprite.LayeredUpdates.get_sprite(self.change_cursor_items, i)

						item.rect.x = (i + 1) * (SCREEN_WIDTH / (len(self.change_cursor_items) + 1)) - (item.rect.width / 2)
						item.rect.y = (SCREEN_HEIGHT / 2) - (item.rect.height / 2)

				elif self.upgrades_screen:

					self.increase_speed_word.rect.x = (SCREEN_WIDTH / 2) - \
					(self.increase_speed_word.rect.width / 2)
					self.increase_speed_word.rect.y = (SCREEN_HEIGHT / 4) - \
					(self.increase_speed_word.rect.height / 2)

					self.add_start_life_word.rect.x = (SCREEN_WIDTH / 2) - \
					(self.add_start_life_word.rect.width / 2)
					self.add_start_life_word.rect.y = (2 * (SCREEN_HEIGHT / 4)) - \
					(self.add_start_life_word.rect.height / 2)

					self.ammo_upgrade_word.rect.x = (SCREEN_WIDTH / 2) - \
					(self.ammo_upgrade_word.rect.width / 2)
					self.ammo_upgrade_word.rect.y = (3 * (SCREEN_HEIGHT / 4)) - \
					(self.ammo_upgrade_word.rect.height / 2)

					self.coin_pic2.rect.x = SCREEN_WIDTH - self.coin_pic2.rect.width - \
					self.universal_spacing_gap
					self.coin_pic2.rect.y = self.universal_spacing_gap

					self.coin_count_word2.rect.x = SCREEN_WIDTH - self.coin_count_word2.rect.width - \
					self.coin_pic2.rect.width - (2 * self.universal_spacing_gap)
					self.coin_count_word2.rect.y = self.universal_spacing_gap - 3

					self.speed_coin.rect.x = self.increase_speed_word.rect.x + self.increase_speed_word.rect.width + \
					self.universal_spacing_gap
					self.speed_coin.rect.y = self.increase_speed_word.rect.y
					self.life_coin.rect.x = self.add_start_life_word.rect.x + self.add_start_life_word.rect.width + \
					self.universal_spacing_gap
					self.life_coin.rect.y = self.add_start_life_word.rect.y
					self.ammo_coin.rect.x = self.ammo_upgrade_word.rect.x + self.ammo_upgrade_word.rect.width + \
					self.universal_spacing_gap
					self.ammo_coin.rect.y = self.ammo_upgrade_word.rect.y

				else:

					for i in range(len(self.settings_screen_items)):

						item = pygame.sprite.LayeredUpdates.get_sprite(self.settings_screen_items, i)

						item.rect.x = (SCREEN_WIDTH / 2) - (item.rect.width / 2)
						item.rect.y = (i + 1) * (SCREEN_HEIGHT / (len(self.settings_screen_items) + 1)) - (item.rect.height / 2)

			return

		def run_logic(self):
			""" Update the items that need to be updated for the current screen.

			"""

			self.cursor.update()
			self.back_word.update()
			Game.run_res_math(game)

			if self.game:

				if self.paused == False:

					if not self.freeze_pickup:

						self.game_items.update()
						self.aliens.update()
						Game.update_changing_items(game)

					if self.freeze_pickup:

						for i in range(len(self.aliens)):

							item = pygame.sprite.LayeredUpdates.get_sprite(self.aliens, i)

							item.full_freeze = True

						self.frozen_frames += 1

						if self.frozen_frames < 200:

							self.game_items.update()
							self.update_changing_items()
							self.aliens.update()

							if self.freeze_hit:

								self.frozen_frames -= 400

						elif self.frozen_frames == 200:

							for i in range(len(self.aliens)):

								item = pygame.sprite.LayeredUpdates.get_sprite(self.aliens, i)

								item.full_freeze = False

							self.frozen_frames = 0
							self.freeze_pickup = False
							self.aliens.update()
							self.game_items.update()
							Game.update_changing_items(game)

					self.freeze_hit = False

				elif self.paused == True:

					self.pause_items.update()

			elif self.settings:

				self.settings_screen_items.update()
				self.change_bullet_items.update()
				self.change_player_items.update()
				self.change_cursor_items.update()
				self.back_word.update()
				self.player_select_arrow.update()
				self.bullet_select_arrow.update()
				self.upgrade_screen_items.update()

			elif self.title_screen:

				self.title_screen_items.update()

			if self.new_highscore_screen:

				self.new_highscore_items.update()

			if self.game_over:

				self.game_over_items.update()

			if self.highscore_screen:

				self.highscore_items.update()

			if self.enter_name_screen:

				self.keyboard.update()
				self.backspace_word.update()
				self.done_word.update()
				self.entered_name.update()

			return

		def display_frame(self,screen):
			""" Draw the items needed for the current screen.

			"""

			if self.game:

				if not self.paused:

					self.game_items.draw(screen)
					Game.draw_lives(game, screen)
					self.aliens.draw(screen)

				if self.paused:

					self.pause_items.draw(screen)
					self.aliens.draw(screen)

			elif self.title_screen:

				self.title_screen_items.draw(screen)

			elif self.settings:

				self.back_word.draw(screen)

				if self.player_select:

					self.change_player_items.draw(screen)
					self.player_select_arrow.draw(screen)

				elif self.bullet_select:

					self.change_bullet_items.draw(screen)
					self.bullet_select_arrow.draw(screen)

				elif self.cursor_select:

					self.change_cursor_items.draw(screen)

				elif self.upgrades_screen:

					self.upgrade_screen_items.draw(screen)

				else:

					self.settings_screen_items.draw(screen)

			elif self.highscore_screen:

				self.back_word.draw(screen)
				self.highscore_items.draw(screen)
				self.highscore_name_items.draw(screen)

			elif self.new_highscore_screen:

				self.new_highscore_items.draw(screen)

			elif self.enter_name_screen:

				self.keyboard.draw(screen)
				self.backspace_word.draw(screen)
				self.done_word.draw(screen)
				self.entered_name.draw(screen)

			elif self.game_over:

				self.game_over_items.draw(screen)

			self.cursor.draw(screen)

			return

	pygame.init()

	done   = False
	screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT], pygame.FULLSCREEN)
	clock  = pygame.time.Clock()
	pygame.mouse.set_visible(False)

	stars = pygame.sprite.Group()

	game = Game()

	for i in range(int(SCREEN_WIDTH / 2)):

		star = Star("star.png")

		star.rect.x = random.randrange(0,SCREEN_WIDTH)
		star.rect.y = random.randrange(0,SCREEN_HEIGHT)
		star.velx   = 0
		star.vely   = random.randrange(-5,-1)

		stars.add(star)

	game.main_music.play(-1)

	""" - - - Main Loop - - - """

	while not done:

		done = game.process_events()

		game.run_logic()

		if game.paused == False:

			stars.update()

		screen.fill(BLACK)
		stars.draw(screen)
		game.display_frame(screen)

		pygame.display.flip()

		clock.tick(60)

	pygame.quit()

if __name__ == "__main__":
	main()
