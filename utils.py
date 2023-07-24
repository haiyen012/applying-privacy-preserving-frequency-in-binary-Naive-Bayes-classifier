import numpy as np

def split_data(data, num_parties, parties_collection):

    sizes = np.random.dirichlet(np.ones(num_parties), size=1)[0] * data.shape[0]
    sizes = np.round(sizes).astype(int)

    diff = data.shape[0] - np.sum(sizes)
    if diff > 0:
        sizes[:diff] += 1
    elif diff < 0:
        sizes[:abs(diff)] -= 1

    indices = np.cumsum(sizes)[:-1]

    dfs = np.split(data, indices)

    for party in parties_collection:
        party.receive_data(dfs[party.id])
        print(len(party.data))
    return dfs
