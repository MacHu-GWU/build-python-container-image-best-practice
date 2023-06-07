import fire

from .show_deps import show_deps
from .say_hello import say_hello


class Command:
    def show_deps(self):
        show_deps()
        
    def say_hello(self, name: str="Mr X"):
        say_hello(name=name)
        
        
def run():
    fire.Fire(Command)
    