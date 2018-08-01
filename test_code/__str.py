class std:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "hi " + self.name



test = std("zhangsan")

print (test)
print (test.__str__())
