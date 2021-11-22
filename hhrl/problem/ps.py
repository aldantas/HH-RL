from hhrl.problem import HyFlexDomain


class PersonnelScheduling(HyFlexDomain):
    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'PS', instance_id, seed)
