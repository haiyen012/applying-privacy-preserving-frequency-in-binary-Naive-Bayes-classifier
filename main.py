import pandas as pd
import numpy as np
from party import Party
from miner import Miner
from utils import split_data, generation, processing_data

num_parties = 10
np.random.seed(10)
raw_df = pd.read_csv('train.csv')
train_df, test_df = processing_data(raw_df)


nominal_df = train_df[['Pclass', 'Sex', 'Embarked', 'Survived']]
nominal_attribute_name = ['Pclass', 'Sex', 'Embarked']
column_unique_values = {col: nominal_df[col].unique().tolist() for
                        col in nominal_df.columns}

numeric_attribute_name = ['Age', 'SibSp', 'Parch', 'Fare']
numeric_df = train_df[['Age', 'SibSp', 'Parch', 'Fare']]

miner, parties = generation(nominal_attribute_name, numeric_attribute_name, column_unique_values, num_parties)
split_data(train_df, miner, num_parties)

miner.cal_sum_n('Survived')

miner.cal_sum_c('Embarked', 'Survived')
miner.cal_p('Embarked', 'Survived')

miner.cal_sum_c('Sex', 'Survived')
miner.cal_p('Sex', 'Survived')

miner.cal_sum_c('Pclass', 'Survived')
miner.cal_p('Pclass', 'Survived')


miner.cal_sum_s('Fare', 'Survived')
miner.cal_mean('Fare', 'Survived')

miner.cal_sum_s('Age', 'Survived')
miner.cal_mean('Age', 'Survived')

miner.cal_sum_s('SibSp', 'Survived')
miner.cal_mean('SibSp', 'Survived')

miner.cal_sum_s('Parch', 'Survived')
miner.cal_mean('Parch', 'Survived')

miner.cal_sum_v('Fare', 'Survived')
miner.cal_var('Fare', 'Survived')

miner.cal_sum_v('Age', 'Survived')
miner.cal_var('Age', 'Survived')

miner.cal_sum_v('SibSp', 'Survived')
miner.cal_var('SibSp', 'Survived')

miner.cal_sum_v('Parch', 'Survived')
miner.cal_var('Parch', 'Survived')

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