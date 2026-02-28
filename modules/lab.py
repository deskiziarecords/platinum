class Lab:
    def __init__(self, letters):
        self.letters = letters

    def experiment(self, letter_name, value):
        letter = self.letters.get(letter_name)
        if not letter:
            return "Letter not found"
        return letter.execute(value)
