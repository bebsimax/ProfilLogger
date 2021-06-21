import os
class ProfilLogger:
    """Stop it, get some help"""
    def __init__(self):
        self.log_level = "WARNING"

    def info(self, msg):
        open("log.log", "a")

