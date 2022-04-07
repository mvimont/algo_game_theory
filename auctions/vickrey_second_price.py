from random import uniform, randint
from numpy import average


class Bidder:
    def __init__(self, id, w, manipulation=False):
        self.id = id
        self.willingess_to_pay = w
        self.manipulation = manipulation
        if self.manipulation:
            self.reported_willingness_to_pay = self.willingess_to_pay - (self.willingess_to_pay * uniform(0, 1))
        else:
            self.reported_willingness_to_pay = self.willingess_to_pay
        self.utility = None

    def calculate_utility(self, won=False, cost=0):
        if won:
            self.utility = self.willingess_to_pay - cost
        else:
            self.utility = 0
    
class SecondHighestAuction:
    def __init__(self, number_of_bidders, manipulation=False):
        self.bidders = dict()
        for i in range(number_of_bidders):
            if manipulation:
                bidder_manipulates = randint(0, 1)
            else:
                bidder_manipulates = 0
            self.bidders[i] = Bidder(id=i, w=randint(0, 100), manipulation=bidder_manipulates)
        self.winner = None
        self.cost = 0
        self.find_winner()
    
    def find_winner(self):
        # for simplicity's sake, if a later bidder has an identical
        # bid as a former bidder, they replace that bidder
        result_dict = {bidder.reported_willingness_to_pay : bidder.id for bidder in self.bidders.values()}
        bids = list(result_dict.keys())
        bids.sort(reverse=True)
        self.winner = self.bidders[result_dict[bids[0]]]
        self.cost = bids[1]
        self.winner.calculate_utility(won=True, cost=self.cost)
    
    def get_winner_utility(self):
        return self.winner.utility

if __name__=="__main__":
    summary_no_manip = list()
    summary_manip = list()
    for i in range(1000):
        #no_manip_auction = SecondHighestAuction(100, manipulation=False)
        manip_auction = SecondHighestAuction(100, manipulation=True)
        if not manip_auction.winner.manipulation:
            summary_no_manip.append(manip_auction.winner.utility)
        else:
            summary_manip.append(manip_auction.winner.utility)
    print(f"No Manipulation Mean Utility: {sum(summary_no_manip) / len(summary_no_manip)}")
    print(f"Manipulation Mean Utility: {sum(summary_manip) / len(summary_manip)}")
