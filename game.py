import argparse

class BaseGame:
	"""Don't modify this function, instead use Game.init()."""
	def __init__(self,screencontrol,argv):
		self.screencontrol = screencontrol
		self.ap = argparse.ArgumentParser(prog="pyfc")
		self.init()
		self.args = self.ap.parse_args(args=argv)
		self.handleArguments()

	"""Initialize game variables and handle arguments with self.ap"""
	def init(self):
		return

	"""Called after arguments have been handled. Results in self.args"""
	def handleArguments(self):
		return

	"""Called every update frame"""
	def update(self,events):
		return

	"""Called every frame."""
	def draw(self):
		self.screencontrol.fill((255,255,255))
		self.screencontrol.finishDraw()
