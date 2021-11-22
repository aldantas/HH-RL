from hhrl.problem import HyFlexDomain


class VehicleRouting(HyFlexDomain):
    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'VRP', instance_id, seed)
