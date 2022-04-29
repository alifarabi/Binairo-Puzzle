## each cell in puzzle
class Cell:
    def __init__(self,x,y,domain=['w','b'],value='_') :
        self.x=x
        self.y=y
        self.domain = domain
        self.value=value
    
    def isEmpty(self):
        return self.value == '_'

    def __str__(self) -> str:
        return f"☣️x: {self.x} ☣️y: {self.y} 🧞d: {'-'.join(self.domain)} 🚂v: {self.value}"