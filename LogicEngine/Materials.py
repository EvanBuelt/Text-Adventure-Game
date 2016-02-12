__author__ = 'Evan'
import random


class Quality:
    Junk = 0
    Common = 1
    Fine = 2
    Rare = 3
    Legendary = 4

    value = {0: "Junk", 1: "Common", 2: "Fine", 3: "Rare", 4: "Legendary",
             "Junk": 0, "Common": 1, "Fine": 2, "Rare": 3, "Legendary": 4}

    def __init__(self, probabilities=None):
        random.seed()
        if probabilities is None:
            self.probabilities = [0.30,  # Junk
                                  0.50,  # Common
                                  0.15,  # Fine
                                  0.04,  # Rare
                                  0.01]  # Legendary

        elif len(probabilities) is not 5:
            self.probabilities = [0.30,  # Junk
                                  0.50,  # Common
                                  0.15,  # Fine
                                  0.04,  # Rare
                                  0.01]  # Legendary
        else:
            self.probabilities = probabilities

        self._set_probabilities()

    def _set_probabilities(self):
        # Normalize the sum of probabilities to length 1
        probability_sum = 0
        for num in self.probabilities:
            probability_sum += num

        for i in range(0, len(self.probabilities)):
            self.probabilities[i] /= probability_sum

        # Update probabilities to make it a range instead of a single number
        min_value = 0
        max_value = self.probabilities[0]

        new_probabilities = []
        for i in range(0, len(self.probabilities)):
            new_probabilities.append((min_value, max_value))
            min_value += self.probabilities[i]
            max_value += self.probabilities[(i+1) % len(self.probabilities)]

        self.probabilities = list(new_probabilities)

    def get_quality(self):
        x = random.random()
        for i in range(0, len(self.probabilities)):
            item = self.probabilities[i]
            min_range = item[0]
            max_range = item[1]

            if min_range <= x <= max_range:
                return self.value[i]

        return 0


class Resource:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class Ore(Resource):
    def __init__(self, name, amount):
        Resource.__init__(self, name, amount)


class Metal(Resource):
    def __init__(self, name, probabilities=None):
        Resource.__init__(self, name, 1)
        self._quality = Quality(probabilities)
        self.quality = self._quality.get_quality()


class Wood(Resource):
    def __init__(self, name, amount):
        Resource.__init__(self, name, amount)

if False:
    print Metal.__class__.__name__
