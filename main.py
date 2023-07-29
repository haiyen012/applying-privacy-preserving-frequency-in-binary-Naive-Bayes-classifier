import pandas as pd
import numpy as np
from party import Party
from miner import Miner
from utils import split_data, generation, processing_data
import tinyec.ec as ec
from tinyec import registry


curve = registry.get_curve('brainpoolP256r1')
num_parties = 10
np.random.seed(10)

raw_df = pd.read_csv('train.csv')
train_df, test_df = processing_data(raw_df)

# Category name of columns into class, nominal attribute, numeric attribute
class_name = 'Survived'
nominal_attribute_name = ['Pclass', 'Sex', 'Embarked']
numeric_attribute_name = ['Age', 'SibSp', 'Parch', 'Fare']

# Create new dataframe for class, nominal attribute, numeric attribute
class_df = train_df[class_name]
class_unique_values = class_df.unique()

nominal_df = train_df[nominal_attribute_name]
nominal_unique_values = {col: nominal_df[col].unique().tolist() for
                         col in nominal_df.columns}

numeric_df = train_df[numeric_attribute_name]

# Create miner and parties
miner, parties = generation(class_name, nominal_attribute_name, numeric_attribute_name,
                            class_unique_values, nominal_unique_values,
                            num_parties, curve)
split_data(train_df, miner, num_parties)

miner.sum_public_key()
miner.send_public_key()
miner.process_train_data()

print(f"Mean value: {miner.mean_value}")
print(f"Variance: {miner.var_value}")

x_record = {
    'Pclass': 2,
    'Sex': 'female',
    'Age': 25,
    'SibSp': 0,
    'Parch': 1,
    'Fare': 26,
    'Embarked': 'S'
}
print(miner.prob_class_nominal(x_record, 0))
print(miner.prob_class_numeric(x_record, 0))

print(miner.predict(x_record, 'Survived'))