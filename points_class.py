# n	40 * (n + 1)	100 * (n + 1)	300 * (n + 1)	1200 * (n + 1)
class Points:
    def __init__(self, lines, level):
        self.points = 0
        self.level = level
        self.lines = lines

    def clear(self):
        self.points += self.level

    def increment(self):
        lines_list = ((1, 40), (2,100), (3,300), (4,1200))
        for n in lines_list:
            if self.lines == n[0]:
                return(n[1])
