from scipy.stats import norm
import numpy as np


class Miner:
    def __init__(self, nominal_attribute_name, numeric_attribute_name, column_unique_values):
        self.parties = []
        self.n = None
        self.p = {}
        self.column_unique_values = column_unique_values
        self.nominal_attribute_name = nominal_attribute_name
        self.numeric_attribute_name = numeric_attribute_name
        self.mean_value = {}
        self.var_value = {}

    # For both
    def cal_sum_n(self, class_name):
        self.n = None
        for party in self.parties:
            party_n = party.calculate_n(self.column_unique_values, class_name)
            if self.n is None:
                self.n = party_n.copy()
            else:
                for key, value in party_n.items():
                    self.n[key] += value

        return self.n

    # For nominal attributes
    def cal_sum_c(self, attribute_name, class_name):
        c = None
        for party in self.parties:  # nhét giao thức PPFC vào đây
            party_c = party.calculate_c(self.column_unique_values, attribute_name, class_name)
            if c is None:
                c = party_c.copy()
            else:
                for key, value in party_c.items():
                    c[key] += value

        return c

    def cal_p(self, attribute_name, class_name):
        c = self.cal_sum_c(attribute_name, class_name)
        temp_p = {}
        for key_c, value_c in c.items():
            for key_n, value_n in self.n.items():
                if (key_c[1] == key_n):
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
        for class_value in self.column_unique_values[class_name]:
            temp_prob = self.prob_class_nominal(x_records, class_value) * self.prob_class_numeric(x_records, class_value)
            if temp_prob > max_prob:
                predict_class = class_value
                max_prob = temp_prob

        # print(f"Person who embarked is {x['Embarked']} and {x['Sex']} was {predict_name}")
        return class_dict[predict_class]

    # For numeric attributes:
    def cal_sum_s(self, attribute_name, class_name):
        s = None
        for party in self.parties:  # nhét giao thức PPFC vào đây
            party_s = party.calculate_s(self.column_unique_values, attribute_name, class_name)
            if s is None:
                s = party_s.copy()
            else:
                for key, value in party_s.items():
                    s[key] += value

        return s

    def cal_mean(self, attribute_name, class_name):
        s = self.cal_sum_s(attribute_name, class_name)
        temp_mean_value = {}
        for key_s, value_s in s.items():
            temp_mean_value[key_s] = value_s / self.n[key_s]

        self.mean_value[attribute_name] = temp_mean_value

        return temp_mean_value

    def cal_sum_v(self, attribute_name, class_name):
        v = None

        for party in self.parties:  # nhét giao thức PPFC vào đây
            party_v = party.calculate_v(self.column_unique_values,
                                        attribute_name, class_name,
                                        self.mean_value[attribute_name])

            if v is None:
                v = party_v.copy()
            else:
                for key, value in party_v.items():
                    v[key] += value

        return v

    def cal_var(self, attribute_name, class_name):
        v = self.cal_sum_v(attribute_name, class_name)
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

