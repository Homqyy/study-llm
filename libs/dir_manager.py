import os

class DirManager:
    def __init__(self):
        self.libsDir = os.path.abspath(__file__)
        self.projectDir = os.path.join(self.libsDir, '../')
