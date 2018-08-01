config = {}

config["SERVER"] = "192.168.134.99"
config["USERNAME"] = "root"
config["PASSWORD"] = "JcatPass0197"
class Testbed(object):
    def __init__(self):
        self.config = {}
        self.entities = {}

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        """setting"""
        self._config = value

    @property
    def entities(self):
        return self._entities

    @entities.setter
    def entities(self, value):
        """setting"""
        self._entities = value

    def to_config_string(self):
        s = ["#" * 90,
             "Testbed Configuration:",
             "*" * 90]
        s1 = s + ["   {}: {}".format(m, self.config[m])
              for m in sorted(self.config.keys())]
        s2 = s1 + ["=" * 90]
        #print("\n".join(s2))
        return "\n".join(s2)

    def to_entities_string(self):
        s = ["|" * 79,
             "Testbed Entities:",
             "=" * 79]
        s += ["   {}: {}".format(k, self.entities[k])
              for k in sorted(self.entities.keys())]
        s += ["=" * 79]
        return "\n".join(s)

    def __str__(self):
        return "\n".join([self.to_config_string(),
                         self.to_entities_string()])




def get():
    return k

if __name__ == "__main__":
    k = Testbed()
    k.config.update(config)  # k is init object,so the config = {} at beginning
    # k.config = config
    #print(k.config)
    print(k.__str__())


