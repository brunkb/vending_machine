# Vending machine demonstrates transitions state Machine

from transitions import Machine

class VendingMachine(object):
    states = ['waiting', 'selection', 'processing']

    def __init__(self):
        # long term values
        self.orderCount = 0
        self.revenue = 0.0
        # code, (name, price, count)
        self.inventory = { 'A1': ('Doritos', 1.0, 5), 'A2': ("Lay's Original", .75, 2), 'A3': ("Chicklets", .5, 10) }

        # values reset each order
        self.amount = 0.0
        self.itemCode = None
        self.item = None

        self.machine = Machine(model=self, states=VendingMachine.states, initial='waiting')
        self.machine.add_transition(trigger='money_inserted', source='waiting', dest='selection', after='set_money')
        self.machine.add_transition(trigger='enter_code', source='selection', dest='processing', after='set_item')
        self.machine.add_transition(trigger='cancel_order', source='selection', dest='waiting', after=['print_refund_msg', 'reset_machine'])
        self.machine.add_transition(trigger='select_item', source='processing', dest='waiting', conditions=['check_funds', 'check_inventory'], after=['vend', 'make_change', 'decrement_inventory', 'reset_machine'])

    def reset_machine(self):
        self.amount = 0.0
        self.item = None
        self.itemCode = None

    def set_money(self, amount=0.0):
        print "money added {0:.2f}".format(amount)
        self.amount = amount

    def set_item(self, itemCode):
        print ("item selected {0:s}".format(itemCode))
        self.itemCode = itemCode
        self.item = self.inventory[itemCode]

    def vend(self):
        print "dropping item {0:s}".format(self.item[0])
        self.orderCount += 1
        self.revenue += self.amount

    def check_funds(self):
        print "checking funds"
        if (self.amount >= self.item[1]):
            return True

        return False

    def check_inventory(self):
        print "checking inventory"
        if (self.item[2] >= 1):
            return True  #todo

        return False

    def decrement_inventory(self):
        decrementedItem = (self.item[0], self.item[1], self.item[2] - 1)
        self.inventory[self.itemCode] = decrementedItem

    def make_change(self):
        change = self.amount - self.item[1]
        print "making change " + str(change)

    def print_refund_msg(self):
        print "Your money has been refunded " + str(self.amount)

candyMachine = VendingMachine()

print "first run, add money then refund"
candyMachine.money_inserted(amount=1.0)
candyMachine.cancel_order()

print "second run, full order"
candyMachine.money_inserted(amount=1.50)
candyMachine.enter_code(itemCode='A1')
candyMachine.select_item()
print "total orders: {0:d}".format(candyMachine.orderCount)


print candyMachine.inventory
