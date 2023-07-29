# FOR EXPERIMENT TARGET: SPLIT DATASET FOR PARTIES
import pandas as pd
import numpy as np
from miner import Miner
from party import Party


# tạo ra miner và các parties
def generation(class_name, nominal_attribute_name, numeric_attribute_name,
               class_unique_values, nominal_unique_values,
               num_parties, curve):

    miner = Miner(class_name, nominal_attribute_name, numeric_attribute_name,
                  class_unique_values, nominal_unique_values,
                  curve)
    for id in range(num_parties):
        miner.parties.append(Party(id, class_name, class_unique_values, nominal_unique_values, curve))
    return miner, miner.parties


def split_data(data, miner, num_parties):
    np.random.seed(10)
    # chia data ra num_parties phần có số hàng ngẫu nhiên
    sizes = np.random.dirichlet(np.ones(num_parties), size=1)[0] * data.shape[0]
    sizes = np.round(sizes).astype(int)

    diff = data.shape[0] - np.sum(sizes)  # chênh lệch giữa số hàng của bảng ban
    # đầu và tổng số hàng của các bảng mới chia
    if diff > 0:  # chênh lệch > 0 thì hàng của bảng đầu tiên +1
        sizes[:diff] += 1
    elif diff < 0:
        sizes[:abs(diff)] -= 1

    indices = np.cumsum(sizes)[:-1]
    dfs = np.split(data, indices)

    for party in miner.parties:  # chia phần tương ứng cho party
        party.receive_data(dfs[party.id])
        # print(len(party.data))
    return dfs


def processing_data(data):
    data.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)  # bỏ các cột
    data['Age'] = data['Age'].fillna(data['Age'].mean()).round()  # xử lý cột Age thiếu bằng mean
    data.dropna(inplace=True)  # bỏ các hàng có nan ở cột Embarked

    data.to_csv('clean_data.csv')
    df = pd.read_csv('clean_data.csv')
    train_df = df[:880]
    test_df = df[880:889]

    return train_df, test_df



