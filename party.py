class Party:
    def __init__(self, id):
        self.id = id    #ID
        self.c = None   #số mẫu có nhãn y, mang thuộc tính z
        self.n = None   #số mẫu có nhãn y
        self.data = None

    def calculate_c(self, column_unique_values, attribute_name, class_name):
        self.c = {}
        for class_value in column_unique_values[class_name]:
            for attribute_value in column_unique_values[attribute_name]:
                temp_df = self.data[(self.data[class_name] == class_value) & (self.data[attribute_name] == attribute_value)]
                self.c[(class_value, attribute_value)] = len(temp_df)

        return self.c

    def calculate_n(self, column_unique_values, class_name):
        self.n = {}
        for class_value in column_unique_values[class_name]:
            temp_df = self.data[self.data[class_name] == class_value]
            self.n[(class_value)] = len(temp_df)

        return self.n

    def receive_data(self, data):
        self.data = data