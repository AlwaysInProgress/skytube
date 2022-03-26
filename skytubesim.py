import numpy as np
import math


class SkyTubeSim:

	def __init__(self) -> None:
		self.resolution = 500
		self.initialHeight = 50
		self.gravity = 9.806 #m/s2
		self.impactTime = 30
		self.maxTime = 30
		self.initialVelocity = -53; #terminal velocity of a human in m/s
		self.dt = self.maxTime/self.resolution
		self.C_D = 1

		self.humanDensity = 985; #kg/m3
		self.humanMass = 100; #kg
		self.humanFrontalArea = 0.18; #m2
		self.humanVolume = 0.062; #m3


		# Mapping Functions
		self.accFunc = lambda x: 4 * math.exp(- x * .81) * self.gravity + self.gravity

		# Lists
		self.fluidDensity = np.zeros(self.resolution, dtype=float)
		self.x = np.linspace(0,self.initialHeight,self.resolution)
		self.desiredAcc = np.array([self.accFunc(i) for i in self.x])
		self.t = np.transpose(np.linspace(0,self.maxTime,self.resolution))
		self.height = np.zeros(self.resolution, dtype=float)
		self.velocity= np.zeros(self.resolution, dtype=float)
		self.acceleration = np.zeros(self.resolution, dtype=float)
		# Forces
		self.pressureDrag = np.zeros(self.resolution, dtype=float)
		self.buoyancyForce = np.zeros(self.resolution, dtype=float)
		self.gravityForce = self.gravity*self.humanMass #N

		# Initial Data
		self.height[0] = self.initialHeight
		self.velocity[0] = self.initialVelocity

		self.currentIndex = 1

	def step_human(self):
			i = self.currentIndex
			self.currentIndex += 1

			self.fluidDensity[i] = (self.gravityForce + self.humanMass*self.desiredAcc[i])/(self.humanVolume*self.gravity + 0.5*self.velocity[i-1]**2*self.humanFrontalArea*self.C_D)
			self.pressureDrag[i] = 0.5*self.fluidDensity[i]*self.velocity[i-1]**2*self.humanFrontalArea*self.C_D #N upward
			self.buoyancyForce[i] = self.fluidDensity[ i ]*self.humanVolume*self.gravity; #N upward
			dv = (self.pressureDrag[i] + self.buoyancyForce[i] - self.gravityForce)/self.humanMass*self.dt
			self.velocity[i] = self.velocity[i-1] + dv
			self.acceleration[i] = dv/self.dt/self.gravity
			self.height[i] = self.height[i-1] + self.velocity[i]*self.dt
			if self.height[i] <= 0 and self.height[i-1] > 0:
					impactTime = i*self.dt
					print("Impact Time(s):", self.impactTime)
					print("Impact Velocity (m/s): ",self.velocity[i])
					return True
			return False

	def currentHeight(self):
		return self.height[self.currentIndex-1]

	def run(self):
		while (True):
			print("Current Height", self.currentHeight())
			if self.step_human():
				break


