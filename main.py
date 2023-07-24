import pandas as pd
import numpy as np
from party import Party
from miner import Miner
from utils import split_data

num_parties = 3
np.random.seed(10)
train_df = pd.read_csv('train.csv')

y_data = train_df['Survived']
attribute = train_df['Embarked']

new_df = train_df[['Survived', 'Embarked']]

print(new_df)
column_unique_values = {col: new_df[col].unique().tolist() for col in new_df.columns}

print(column_unique_values)
miner = Miner(column_unique_values)
parties_collection = []

def generate_parties(num_parties):
    for id in range(0, num_parties):
        party_obj = Party(id)
        miner.parties.append(party_obj)
        parties_collection.append(party_obj)

generate_parties(num_parties)
split_data(new_df, num_parties, parties_collection)

for party in parties_collection:
    print(party.calculate_c(column_unique_values, 'Embarked', 'Survived'))
    print(party.calculate_n(column_unique_values, 'Survived'))

miner.calculate_sum_c('Embarked', 'Survived')
miner.calculate_sum_n('Survived')

pri