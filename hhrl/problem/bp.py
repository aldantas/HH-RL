from hhrl.problem import HyFlexDomain


class BinPacking(HyFlexDomain):
    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'BP', instance_id, seed)
