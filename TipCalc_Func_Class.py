import math

# ********************************************
#   Person Class
# ********************************************
class Person:

    # constructor
    def __init__(self, name):
        self.Name = name
        self.ItemColl = {}  # dictionary
        self.IncTip = 0
        self.Tax = 0
        self.Tip = 0
        self.Pct = 0
        self.Bday = 0
        self.extraPennies = 0
        self.rounddiff = 0

    # get value clause
    def get_Name(self):
        return self.Name

    def get_ItemColl(self):
        return self.ItemColl

    def get_IncTip(self):
        return self.IncTip

    def get_Tax(self):
        return self.Tax

    def get_Tip(self):
        return self.Tip

    def get_Pct(self):
        return self.Pct

    def get_Bday(self):
        return self.Bday

    def get_ExtraPenny(self):
        return self.extraPennies

    def get_rounddiff(self):
        return self.rounddiff

    # zero out their costs
    def Birthday(self):
        for i in self.get_ItemColl():
            self.ItemColl[i] = 0
        self.IncTip = 0
        self.Tip = 0
        self.Tax = 0
        self.Bday = 0
        self.rounddiff = 0
        return None


    # calculate subtotal and total
    def SubBill(self):
        #add optional parameter to add to this
        Sub_Bill = 0
        for i in self.ItemColl.values():
            Sub_Bill += i
        Sub_Bill = Sub_Bill + self.get_rounddiff()
        return Sub_Bill

    def TolBill(self):
        Tol_Bill = self.SubBill() + self.get_IncTip() + self.get_Tax() + self.get_Tip() + self.get_Bday() + self.get_ExtraPenny()
        return Tol_Bill

    # identify clause
    
    def __repr__(self):
        return self.Name + ": " + str(self.TolBill())
    
# ************************************************
#   Split the Rest Function for dictionary edition
# ************************************************
def split_bill(personlist, bill_so_far):

    split_the_rest = 0

    # loop through each person's subtotal
    for i in personlist:
        total_p_subtotal = i.SubBill()

    # minus individual orders from what is left to split
    split_the_rest = bill_so_far - total_p_subtotal

    # splitting calculation
    subtotal_per_person = round(split_the_rest / personlist.count(), 2)

    return subtotal_per_person


# ********************************************
#  Dish Total Function
# ********************************************
def dish_total(subtotal, dishes):
    # add up amount in dishes list
    dishes_total = 0
    for i in dishes:
        dishes_total += i
    # minus subtotal from dishes total
        bill_so_far = subtotal - dishes_total

    return bill_so_far


# ********************************************
#   Tip Button Function
# ********************************************
def tip_btn(sub):
    #print("\nEnter quick buttons or custom % amount or press enter to skip")

    #quick buttons
    ten_pct = round(sub * 0.10, 2)
    ten_pct = f"${ten_pct:.2f}"
    twelve_pct = round(sub * 0.12, 2)
    twelve_pct = f"${twelve_pct:.2f}"
    fifteen_pct = round(sub * 0.15, 2)
    fifteen_pct = f"${fifteen_pct:.2f}"
    eighteen_pct = round(sub * 0.18, 2)
    eighteen_pct = f"${eighteen_pct:.2f}"
    twenty_pct = round(sub * 0.20, 2)
    twenty_pct = f"${twenty_pct:.2f}"

    # Web Edition
    return (ten_pct, twelve_pct, fifteen_pct, eighteen_pct, twenty_pct)

    # Console Edition
    #print(f"10% {ten_pct} | 12% {twelve_pct} | 15% {fifteen_pct} | 18% {eighteen_pct} | 20% {twenty_pct}")

# ********************************************
#   Tip Calculation Function
# ********************************************
def tip(t, sub):

    rounded_tip = sub * t/100
    custom_tip = round(rounded_tip, 2)

    return custom_tip


# ********************************************
#   Rounding Button Function
# ********************************************
# Console Edition
def round_btn():
    print("Round button: Up, Down, Closest")
    round_type = input()
    print("To the next: 1.00, 0.50, 0.25, 0.10")
    print("button: dollar, half, quarter, tenth")
    round_decimal = input()

    return round_type, round_decimal


# ********************************************
#   Rounding Type Option Function
# ********************************************
def round_option(t, rt, rd):

    if str.lower(rt) == 'up':
        if str.lower(rd) == 'dollar':
            return math.ceil(t)
        elif str.lower(rd) == 'half':
            return math.ceil(t / .5) * .5
        elif str.lower(rd) == 'quarter':
            return math.ceil(t / .25) * .25
        elif str.lower(rd) == 'tenth':
            return math.ceil(t / .1) * .1
    elif str.lower(rt) == 'down':
        if str.lower(rd) == 'dollar':
            return math.floor(t)
        elif str.lower(rd) == 'half':
            return math.floor(t / .5) * .5
        elif str.lower(rd) == 'quarter':
            return math.floor(t / .25) * .25
        elif str.lower(rd) == 'tenth':
            return math.floor(t / .1) * .1
    elif str.lower(rt) == 'closest':
        if str.lower(rd) == 'dollar':
            return round(t)
        elif str.lower(rd) == 'half':
            return round(t / .5) * .5
        elif str.lower(rd) == 'quarter':
            return round(t / .25) * .25
        elif str.lower(rd) == 'tenth':
            n = round(t / .1) * .1
            if len(str(n).split('.')[1]) <= 2: # convert n into string. use split function at decimal. find the length of digits left of decimal. list[1] gives digits right of decimal. list[0] gives digits left of decimal.
                return n
            else:
                return round(math.floor(t / .1), 1) * .1  # if len right of decimal greater than 2 use this formula.  