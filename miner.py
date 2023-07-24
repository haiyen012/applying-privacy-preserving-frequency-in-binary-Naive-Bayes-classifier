class Miner:
    def __init__(self, column_unique_values):
        self.parties = []
        self.c = None
        self.n = None
        self.column_unique_values = column_unique_values

    def calculate_sum_c(self, attribute_name, class_name):
        for party in self.parties:
            party_c = party.calculate_c(self.column_unique_values, attribute_name, class_name)
            if self.c is None:
                self.c = party_c.copy()
            else:
                for key, value in party_c.items():
                    self.c[key] += value

        return self.c

    def calculate_sum_n(self, class_name):
        for party in self.parties:
            party_n = party.calculate_n(self.column_unique_values, class_name)
            if self.n is None:
                self.n = party_n.copy()
            else:
                for key, value in party_n.items():
                    self.n[key] += value

        return self.n