from scipy.stats import norm
import numpy as np
import time


class Miner:
    def __init__(self, class_name, nominal_attribute_name, numeric_attribute_name,
                 class_unique_values, nominal_unique_values,
                 curve):
        self.parties = []
        self.n = None
        self.p = {}

        self.class_name = class_name
        self.nominal_attribute_name = nominal_attribute_name
        self.numeric_attribute_name = numeric_attribute_name

        self.class_unique_values = class_unique_values
        self.nominal_unique_values = nominal_unique_values

        self.mean_value = {}
        self.var_value = {}

        # Sum public keys
        self.P_sum = None
        self.Q_sum = None

        self.curve = curve

    def sum_public_key(self):
        for party in self.parties:
            if self.P_sum is None:
                self.P_sum = party.P
            else:
                self.P_sum = self.P_sum + party.P

            if self.Q_sum is None:
                self.Q_sum = party.Q
            else:
                self.Q_sum = self.Q_sum + party.Q

    def send_public_key(self):
        for party in self.parties:
            party.P_sum = self.P_sum
            party.Q_sum = self.Q_sum

    def find_sum_value(self, M_sum, max_range=3000000):
        num_parties = len(self.parties)
        res = None
        for v in range(max_range):
            if v * self.curve.g == M_sum:
                res = v
                break
        return res

    def process_train_data(self):
        self.cal_sum_n()
        for attribute_name in self.nominal_attribute_name:
            self.cal_p(attribute_name)

        for attribute_name in self.numeric_attribute_name:
            self.cal_mean(attribute_name)
            self.cal_var(attribute_name)

    # For both
    def cal_sum_n(self):
        print(f"[INFO] Miner calculates sum of n")
        self.n = None
        party_n_list = []

        start_time = time.process_time()
        for party in self.parties:
            party_n = party.calculate_n()
            party_n_list.append(party_n)
        end_time = time.process_time()
        print(f"Time for all users encrypt is: {end_time - start_time}")

        print(f"DECRYPTION MESSAGE")
        start_time = time.process_time()
        for party_n in party_n_list:
            if self.n is None:
                self.n = party_n.copy()
            else:
                for class_value in self.class_unique_values:
                    self.n[class_value] = self.n[class_value] + party_n[class_value]

        for class_value in self.class_unique_values:
            self.n[class_value] = self.find_sum_value(self.n[class_value])
        end_time = time.process_time()
        print(f"Time for miner decrypt is: {end_time - start_time}")
        print('-' * 100)

        print(self.n)
        return self.n

    # For nominal attributes
    def cal_sum_c(self, attribute_name):
        print(f"[INFO] Miner calculates sum of c for {attribute_name}")
        c = None
        party_c_list = []

        start_time = time.process_time()
        for party in self.parties:  # nhét giao thức PPFC vào đây
            party_c = party.calculate_c(attribute_name)
            party_c_list.append(party_c)

        end_time = time.process_time()
        print(f"Time for all users encrypt {attribute_name} is: {end_time - start_time}")

        print(f"DECRYPTION MESSAGE")
        start_time = time.process_time()
        for party_c in party_c_list:
            if c is None:
                c = party_c.copy()
            else:
                for key, value in party_c.items():
                    c[key] += value

        for attribute_value in self.nominal_unique_values[attribute_name]:
            for class_value in self.class_unique_values:
                c[(attribute_value, class_value)] = self.find_sum_value(c[(attribute_value, class_value)])

        end_time = time.process_time()
        print(f"Time for miner decrypt {attribute_name} is: {end_time - start_time}")
        print('-' * 100)
        print()

        return c

    def cal_p(self, attribute_name):
        c = self.cal_sum_c(attribute_name)
        temp_p = {}

        for key_c, value_c in c.items():
            for key_n, value_n in self.n.items():
                if key_c[1] == key_n:
                    temp_p[key_c] = c[key_c] / value_n

        self.p.update(temp_p)

    def prob_class_nominal(self, x_records, y_class):
        """
      x_records: dictionary, key is attribute name, value is attribute value
      y_class: class value
    """
        prob_nominal_res = 1
        for attribute_name in self.nominal_attribute_name:
            # print(attribute_name)
            x_attribute_value = x_records[attribute_name]
            prob_nominal_res = prob_nominal_res * self.p[(x_attribute_value, y_class)]

        return prob_nominal_res * self.n[y_class]

    def predict(self, x_records, class_name):
        class_dict = {
          0: "Unsurvived", 1: "Survived"
        }
        predict_class = None
        max_prob = 0
        for class_value in self.class_unique_values:
            temp_prob = self.prob_class_nominal(x_records, class_value) * self.prob_class_numeric(x_records, class_value)
            if temp_prob > max_prob:
                predict_class = class_value
                max_prob = temp_prob

        # print(f"Person who embarked is {x['Embarked']} and {x['Sex']} was {predict_name}")
        return class_dict[predict_class]

    # For numeric attributes:
    def cal_sum_s(self, attribute_name):
        print(f"[INFO] Miner calculates sum of s for {attribute_name}")

        s = None
        party_s_list = []
        start_time = time.process_time()
        for party in self.parties:  # nhét giao thức PPFC vào đây
            party_s = party.calculate_s(attribute_name)
            party_s_list.append(party_s)
        end_time = time.process_time()

        print(f"Time for all users encrypt {attribute_name} is: {end_time - start_time}")

        print(f"DECRYPTION MESSAGE")
        start_time = time.process_time()
        for party_s in party_s_list:
            if s is None:
                s = party_s.copy()
            else:
                for key, value in party_s.items():
                    s[key][0] = s[key][0] + value[0]
                    s[key][1] = s[key][1] + value[1]

        for class_value in self.class_unique_values:
            frac_decrypt = self.find_sum_value(s[class_value][0])
            whole_decrypt = self.find_sum_value(s[class_value][1])
            s[class_value] = frac_decrypt / 100 + whole_decrypt
            print(s[class_value])

        end_time = time.process_time()
        print(f"Time for miner decrypt {attribute_name} is: {end_time-start_time}")
        print('-'*100)
        print()
        return s

    def cal_mean(self, attribute_name):
        s = self.cal_sum_s(attribute_name)
        temp_mean_value = {}
        for key_s, value_s in s.items():
            temp_mean_value[key_s] = value_s / self.n[key_s]

        self.mean_value[attribute_name] = temp_mean_value

        return temp_mean_value

    def cal_sum_v(self, attribute_name):
        print(f"[INFO] Miner calculates sum of v for {attribute_name}")
        v = None
        party_v_list = []

        start_time = time.process_time()
        for party in self.parties:  # nhét giao thức PPFC vào đây
            party_v = party.calculate_v(attribute_name, self.mean_value[attribute_name])
            party_v_list.append(party_v)
        end_time = time.process_time()
        print(f"Time for all users encrypt {attribute_name} is: {end_time - start_time}")

        print(f"DECRYPTION MESSAGE")
        start_time = time.process_time()
        for party_v in party_v_list:
            if v is None:
                v = party_v.copy()
            else:
                for key, value in party_v.items():
                    v[key][0] = v[key][0] + value[0]
                    v[key][1] = v[key][1] + value[1]

        for class_value in self.class_unique_values:
            frac_decrypt = self.find_sum_value(v[class_value][0])
            whole_decrypt = self.find_sum_value(v[class_value][1])
            v[class_value] = frac_decrypt / 100 + whole_decrypt
            print(v[class_value])
        end_time = time.process_time()
        print(f"Time for miner decrypt {attribute_name} is: {end_time - start_time}")
        print('-' * 100)
        print()
        return v

    def cal_var(self, attribute_name):
        v = self.cal_sum_v(attribute_name)
        temp_var_value = {}
        for key_v, value_v in v.items():
            temp_var_value[key_v] = value_v / (self.n[key_v] - 1)

        self.var_value[attribute_name] = temp_var_value

        return temp_var_value

    def prob_class_numeric(self, x_records, y_class):
        prob_numeric_res = 1
        for attribute_name in self.numeric_attribute_name:
            attribute_std_value = np.sqrt(self.var_value[attribute_name][y_class])
            x_attribute_value = x_records[attribute_name]
            prob_numeric_res = prob_numeric_res * norm.pdf(x_attribute_value, self.mean_value[attribute_name][y_class], attribute_std_value)

        return prob_numeric_res
