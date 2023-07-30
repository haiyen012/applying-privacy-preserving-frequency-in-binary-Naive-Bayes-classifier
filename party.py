import numpy as np
import random
import math


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


primes = []
for num in range(2, 1000):
    if is_prime(num):
        primes.append(num)


class Party:
    def __init__(self, id,
                 class_name,
                 class_unique_values, nominal_unique_values,
                 curve):
        self.id = id
        self.data = None
        self.class_name = class_name
        self.class_unique_values = class_unique_values
        self.nominal_unique_values = nominal_unique_values
        self.s = None

        # parameters for encryption
        self.curve = curve
        self.p = random.choice(primes)
        self.q = random.choice(primes)
        self.P = self.p * curve.g
        self.Q = self.q * curve.g
        self.P_sum = None
        self.Q_sum = None

    # FOR EXPERIMENT TARGET: Received divided dataset
    def receive_data(self, data):
        self.data = data

    def encrypt_messages(self, messages):
        return messages * self.curve.g + self.q * self.P_sum - self.p * self.Q_sum

    # For both
    def calculate_n(self):
        print(f"\t\t User {self.id} ENCRYPTION MESSAGE")
        n = {}
        for class_value in self.class_unique_values:
            temp_df = self.data[(self.data[self.class_name] == class_value)]
            n[class_value] = len(temp_df)
            n[class_value] = self.encrypt_messages(n[class_value])

        return n

    # Nominal Attributes
    def calculate_c(self, attribute_name):
        print(f"\t\t User {self.id} ENCRYPTION MESSAGE")
        c = {}

        for attribute_value in self.nominal_unique_values[attribute_name]:
            for class_value in self.class_unique_values:
                temp_df = self.data[(self.data[attribute_name] == attribute_value)
                                    & (self.data[self.class_name] == class_value)]
                encrypted_message = self.encrypt_messages(len(temp_df))
                c[(attribute_value, class_value)] = encrypted_message

        return c

    # Numeric Attributes
    def calculate_s(self, attribute_name):
        print(f"\t\t User {self.id} ENCRYPTION MESSAGE")
        s = {}
        for class_value in self.class_unique_values:
            temp_df = self.data[self.data[self.class_name] == class_value]
            temp_sum = np.sum(temp_df[attribute_name].astype(float).values)

            frac, whole = math.modf(temp_sum)
            print(f"\t\t\t Message: {frac, whole}")
            frac_encrypted_message = self.encrypt_messages(int(frac * 100))
            whole_encrypted_message = self.encrypt_messages(int(whole))
            s[class_value] = [frac_encrypted_message, whole_encrypted_message]
        return s

    def calculate_v(self, attribute_name, attribute_mean):
        print(f"\t\t User {self.id} ENCRYPTION MESSAGE")
        v = {}
        for class_value in self.class_unique_values:
            temp_df = self.data[self.data[self.class_name] == class_value]
            # Minus to the mean
            res = temp_df[attribute_name].astype(float).values - attribute_mean[class_value]
            res = np.sum(np.square(res))

            frac, whole = math.modf(res)
            print(f"\t\t\t Message: {frac, whole}")
            frac_encrypted_message = self.encrypt_messages(int(frac * 100))
            whole_encrypted_message = self.encrypt_messages(int(whole))
            v[class_value] = [frac_encrypted_message, whole_encrypted_message]
            # Calculate sum of square

        return v
