import numpy as np

class Party:
  def __init__(self, id):
    self.id = id
    self.n = None
    self.s = None
    self.v = None
    self.data = None

#FOR EXPERIMENT TARGET: Received divided dataset
  def receive_data(self, data):
    self.data = data

#For both
  def calculate_n(self, column_unique_values, class_name):
    self.n = {}
    for class_value in column_unique_values[class_name]:
      temp_df = self.data[(self.data[class_name] == class_value)]
      self.n[class_value] = len(temp_df)

    return self.n

#Nominal Attributes
  def calculate_c(self, column_unique_values, attribute_name, class_name):
    c = {}
    for attribute_value in column_unique_values[attribute_name]:
      for class_value in column_unique_values[class_name]:
        temp_df = self.data[(self.data[attribute_name] == attribute_value)
        & (self.data[class_name] == class_value)]
        c[(attribute_value, class_value)] = len(temp_df)

    return c

#Numeric Attributes
  def calculate_s(self, column_unique_values, attribute_name, class_name):
    self.s = {}
    for class_value in column_unique_values[class_name]:
      temp_df = self.data[self.data[class_name] == class_value]
      self.s[class_value] = np.sum(temp_df[attribute_name].astype(float).values)

    return self.s


  def calculate_v(self, column_unique_values, attribute_name, class_name, attribute_mean):
    print(attribute_mean)
    self.v = {}
    for class_value in column_unique_values[class_name]:
      temp_df = self.data[self.data[class_name] == class_value]
      # Minus to the mean
      res = temp_df[attribute_name].astype(float).values - attribute_mean[class_value].astype(float)
      # print(res)
      res = np.sum(np.square(res))

      self.v[class_value] = res
      # Calculate sum of square

    return self.v