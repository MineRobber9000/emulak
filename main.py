import pygame,core,sys
# change this to load different setup
gameclass = core.Emulak
# initialize game engine
if __name__=="__main__":
	pygame.init()
	basetitle = "Emulak v0.1b"
	# set screen width/height and caption
	size = [640, 480]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption(basetitle)
	# initialize clock. used later in the loop.
	clock = pygame.time.Clock()

	# initialize frame count
	framecount = 0

class FakeSurface:
	def __init__(self):
		self.fake = True

	def blit(self,*args):
		return

	def fill(self,*args):
		return

	def set_at(self,*args):
		return

# screen control class so the game doesn't have to do anything relating to pygame

class ScreenControl:
	def __init__(self,screen=None,size=(640,480)):
		self.screen = screen
		self.size = size

	def fill(self,color):
		if self.screen:
			self.screen.fill(color)

	def fillRect(self,x,y,w,h,color):
		if self.screen:
			pygame.draw.rect(self.screen,color,pygame.Rect(x,y,w,h))

	def finishDraw(self):
		if self.screen:
			pygame.display.update()

	def setTitle(self,t):
		if self.screen:
			pygame.display.set_caption("{} - {}".format(t,basetitle))

	def newSurface(self,w,h):
		if self.screen:
			return pygame.Surface((w,h),0,self.screen)
		else:
			return FakeSurface()

	def blitSurface(self,s,x,y):
		if self.screen and (not hasattr(s,"fake")):
			self.screen.blit(s,(x,y))

	def getFont(self,font,size=32):
		if self.screen:
			return pygame.font.SysFont(font,size)

if __name__=="__main__":

	# Pass argv to game class
	argv = [i for i in sys.argv]
	argv.pop(0)

	game = gameclass(ScreenControl(screen,size),argv)

	# Loop until the user clicks close button
	done = False
	events = []
	while done == False:
	    # write event handlers here
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            done = True
		else:
	            events.append(event)
	    # write game logic here
	    framecount += 1
	    framecount = framecount % 2
	    if framecount==0:
		game.update(events)
		while len(events):
			events.pop()

	    # clear the screen before drawing
	    # screen.fill((255, 255, 255))
	    # write draw code here
	    game.draw()

	    # display what's drawn. this might change.
	    pygame.display.update()
	    # run at 60 fps
	    clock.tick(60)

	# close the window and quit
	pygame.quit()
