class nation:
    def __init__(self, name, population, nukes):
        self.name = name
        self.population = population
        self.nukes = nukes

    def __str__(self):
        return f'{self.name}, {self.population}, {self.nukes}'

    def strike(self, target, number):
        print(f'Initiating strike on {target.name}...')
        print(f'{target.name} initial population: {target.population}')
        print(f'{target.name} initial nukes: {target.nukes}')
        self.nukes -= 1
        target.population *= 0.9**number
        target.nukes += 5
        print(f'{target.name} final population: {target.population}')
        print(f'{target.name} final nukes: {target.nukes}')
