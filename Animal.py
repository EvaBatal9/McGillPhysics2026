class Animal:
    name=None
    sound=None
    frequency=None
    image=None
    soundStrength=None
    location=None
    maze=None

    def __init__(self,name,sound,frequency,image,soundStrength,location,maze):
        self.name=name
        self.sound=sound
        self.frequency=frequency
        self.image=image
        self.soundStrength=soundStrength
        self.location=location
        self.maze=maze