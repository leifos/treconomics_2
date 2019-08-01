from functools import reduce


class RotationOrdering(object):
    """ creates ordering for lists with an attribute id

    """
    def __init__(self):
        pass

    def number_of_orderings(self, slist=None):
        return 1

    def get_ordering(self, slist, i=0):
        """ given a list (i.e. of pages, cats), return the ith ordering

        :param list with and id:
        :param i:
        :return: list of ids
        """

        id_list = []
        for p in slist:
            if p.id:
                id_list.append(p.id)

        from random import shuffle
        shuffle(id_list)
        #id_list = id_list[::-1]

        return id_list


class PermutatedRotationOrdering(RotationOrdering):

    def number_of_orderings(self, slist=None):
        return int(reduce(lambda x, y: x * y, range (1, len (slist) + 1), 1))

    def get_ordering(self, slist, i=0):
        return self.PermN(slist, i)

    def PermN (self, seq, index):
        "Returns the Nth permutation of (in proper order)"
        seqc = list(seq [:])
        #print(seqc)
        result = []
        fact = self.number_of_orderings(seq)
        #print(fact)
        index %= fact
        #print("index",index)

        while seqc:
            fact = fact / len(seqc)
            choice, index = divmod(index,fact)
            x =seqc.pop(int(choice))
            result += [x]

        return result




