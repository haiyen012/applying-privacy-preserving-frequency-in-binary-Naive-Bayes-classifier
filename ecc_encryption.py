import tinyec.ec as ec
from tinyec import registry


class EccEncryption:
    def __init__(self, nb_client, mtx_size) -> None:
        curve = registry.get_curve('brainpoolP256r1')

