import fire

from .say_hello import say_hello


class Command:
    def say_hello(self, name: str="Mr X"):
        say_hello(name=name)
        
        
def run():
    fire.Fire(Command)
    