# Library for dealing with probabilities

# Probability class
class P :
    def __init__(self, x=0, p=0) :
        self.x = x
        self.p = float(p)

    def __repr__(self) :
        return str((self.x, self.p))

# Probability Mass Function class
class PMF :
    def __init__(self, size=0, pmf=None) :
        self.size = size
        if (pmf == None) :
            self.pmf = [P() for x in xrange(size)]
        else :
            self.pmf = pmf

    def __repr__(self) :
        return "s: " + str(self.size) + ", pmf: " + str(self.pmf)

    def __setitem__(self, index, value) :
        self.pmf[index] = value

    def __getitem__(self, index) :
        return self.pmf[index]

    def __len__(self) :
        return len(self.pmf)

    def append(self, p) :
        self.size += 1
        self.pmf.append(p)

    def normalize(self) :
        sum_p = 0
        for i in range(self.size) :
            sum_p += self.pmf[i].p 
        if (sum_p != 0) :
            for i in range(self.size) :
                self.pmf[i].p = float(self.pmf[i].p)/sum_p

    def clear (self) :
        self.__init__()
        #for i in range(self.size) :
        #    self.pmf[i].p = 0


