class NETP:
    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        self.tools[name] = func

    def execute(self, name, *args, **kwargs):
        if name not in self.tools:
            raise ValueError("Tool not found")
        return self.tools[name](*args, **kwargs)
