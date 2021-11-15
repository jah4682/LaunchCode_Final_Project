# ---------------------- Final Project | Launch Code ----------------------
# --------------------------- TITLE: Split Me -----------------------------
# DESCRIPTION: A split restaurant bill tip cacluator.

# *******************
#   Imports
# *******************
import decimal
import math
import re
import TipCalc_Func_Class

################################# Main Program ##############################

def main():
    # ********************************************
    #   Number of people
    # ********************************************

    # TODO drop-down list. 1-10. use for loop to generate numbers.
    num_ppl = int(input("How many people? 1-10: "))



    # ********************************************
    #   Name of each person
    # ********************************************

    person = []                                                   # 'person' is a list of objects

    for p in range(num_ppl):
        x = str(p+1)                                              # begin with string x = 1
        loop = True                                               # validate alpha characters entered only
        while loop:
            Pname = input("\nName of person "+x+": ")             # ask for name of current person
            matches = Pname.isalpha()
            if matches:
                person.append(TipCalc_Func_Class.Person(Pname))   # set the name of current Person object
                loop = False
            else:
                loop = True



    # ********************************************
    #   Subtotal
    # ********************************************

    loop = True

    while loop:                                                   # Validate only enter float numbers
        subtotal = input("\nEnter Subtotal (before tax and tip): ")
        regex = r'^[0-9]+([,.][0-9]{2})?$'
        matches = re.search(regex, subtotal)
        if matches:
            subtotal = float(subtotal)
            loop = False
        else:
            loop = True



    # ********************************************
    #   Tax
    # ********************************************

    loop = True
    while loop:                                                   # Validate only enter float numbers
        tax = input("\nEnter tax: ")
        regex = r'^[0-9]+([,.][0-9]{2})?$'
        matches = re.search(regex, tax)
        if matches:
            tax = float(tax)
            tax_pct = round(tax/subtotal, 2)
            loop = False
        else:
            loop = True



    # ********************************************
    #   Included gratuity
    # ********************************************

    answer_G = input("\nIs gratuity included in this bill. (Type 'y' or press enter to skip): ")

    if answer_G == 'y':
        loop = True
        while loop:                                               # Validate only enter float numbers
            inc_tip = input("\nEnter included tip: ")
            regex = r'^[0-9]+([,.][0-9]{2})?$'
            matches = re.search(regex, inc_tip)
            if matches:
                inc_tip = float(inc_tip)
                inc_tip_pct = round(inc_tip/(subtotal+tax), 2)
                loop = False
            else:
                loop = True
    else:
        inc_tip = 0



    # ********************************************
    #   Additonal tip or Regular tip
    # ********************************************
    
    # if answer_G has a string inside, assumes user said yes to additional tipping, proceed to asking additonal tip, else ask user for a regular tip
    if answer_G == 'y':
        # Additional Tip
        answer_AT = input("\nAdd an additonal tip? (Type 'y' or press enter to skip): ")
        if answer_AT == 'y':
            TipCalc_Func_Class.tip_btn(subtotal)                  # Display tipping options
            loop = True
            while loop:                                           # Validate only enter float numbers
                t = input()                                       # input from user
                regex = r'^[0-9]+([,.][0-9]{2})?$'
                matches = re.search(regex, t)
                if matches:                                       # Validatin passes
                    t = float(t)                                  
                    add_tip = TipCalc_Func_Class.tip(t, subtotal) # Save the variable
                    loop = False
                else:                                             # Validation fails
                    loop = True
        else:
            add_tip = 0
    else:
        # Regular Tip
        t = input("\nAdd a tip to this bill? (Type 'y' or press 'enter' to skip without adding a tip): ")
        
        if t == 'y':                                               # if a tip is entered, not null
            TipCalc_Func_Class.tip_btn(subtotal)                   # Display tipping options
            loop = True
            while loop:                                            # Validate only enter float numbers
                t = input()
                regex = r'^[0-9]+([,.][0-9]{2})?$'
                matches = re.search(regex, t)
                if matches:
                    t = float(t)                                  
                    add_tip = TipCalc_Func_Class.tip(t, subtotal)  # Save the variable
                    loop = False
                else:
                    loop = True
        else:                                                      # if a tip is skipped
            add_tip = 0

    add_tip_pct = round(add_tip/subtotal, 2)



    # ********************************************
    #   Rounding option (tip)
    # ********************************************

    if add_tip != 0:                                              # if there is a tip
        answer = input(f"\nTip is ${add_tip:.2f} Do you want to round this tip? (Type 'y' or press enter to skip) ")
    else:                                                         # if tip is 0
        answer = ''

    if answer == 'y':
        answer_Rtip = TipCalc_Func_Class.round_btn()              # function returns a tupil for rounding tip

        add_tip = TipCalc_Func_Class.round_option(add_tip, answer_Rtip[0], answer_Rtip[1])



    # ********************************************
    #   bill so far
    # ********************************************

    grandtotal = subtotal+tax+inc_tip+add_tip
    must_pay = subtotal+tax+inc_tip



    # ********************************************
    #   Add Individual item
    # ********************************************

    dishes = []                                                   # empty list for dish item collection
    answer = True                                                 # do-while loop condition

    while answer == True or answer == "2" or answer == "1":
        if answer == True:
            answer = input("\nEnter bill items (enter 1) or Split the rest equally (enter 2)?: ")

        # Itemized dishes
        if answer == "1":
            #name of item
            item_Name = input("\nNickname for this item?: ")
            loop = True
            while loop:                                           # Validate only enter float numbers
                #price of item
                item_Price = input("\nEnter a cost for this item?: ")
                regex = r'^[0-9]+([,.][0-9]{2})?$'
                matches = re.search(regex, item_Price)
                if matches:
                    # add item to running dishes list
                    item_Price = float(item_Price)
                    dishes.append(item_Price)
                    loop = False
                else:
                    loop = True
            # who shared this item?
            print("\n\nEnter the name of person(s) who ordered or shared "+item_Name+"\n(For mulitple people type a comma in between their name without spaces. Ex: jason,joe):")
            # list people's name
            for i in person:
                print(i.Name, end=",\t")
            item_Shared = input("\n") # extra space
            # test if more than one person shared
            shared_ordered_list = item_Shared.split(",")

            # assign item to individual person
            # loop through object list. 'x' is the object, not a number.
            for x in person:
                # loop through shared_order list. list of names.
                for i in shared_ordered_list:
                    # matching object name with name in shared list
                    if x.Name == i:
                        # if shared list is greater than one add (1/x) to item name
                        if len(shared_ordered_list) > 1:
                            food_item = item_Name + " (1/" + str(len(shared_ordered_list)) + ")"
                        else:
                            food_item = item_Name
                        # divide price by number of people in shared list
                        prx = item_Price / len(shared_ordered_list)
                        dic_item = {food_item:prx}
                        # add price and nickname to object's item collection
                        x.ItemColl.update(dic_item)

            # add up amount in dishes list
            bill_so_far = TipCalc_Func_Class.dish_total(subtotal, dishes)


        # Spliting the rest
        if answer == "2":
            # split bill
            item_Name = "Rest of Bill"

            if "bill_so_far" in locals():
                item_Price = bill_so_far
            # if answer = 1 is skipped and answer = 2 comes first
            else:
                item_Price = subtotal


            # add item to running dishes list
            dishes.append(item_Price)

            # loop through object list.
            for x in person:
                # create item discription
                food_item = item_Name + " (1/" + str(len(person)) + ")"
                # divide price by number of people at table
                prx = item_Price / len(person)
                dic_item = {food_item:prx}
                x.ItemColl.update(dic_item)

            # add up amount in dishes list
            bill_so_far = TipCalc_Func_Class.dish_total(subtotal, dishes)


        if bill_so_far == 0:
            answer = False
        else:
            # print out what's left of the bill and ask if split or continue itemizing
            print(f"\n${bill_so_far:.2f} left in bill\n")
            # ask to split the rest after each entered item.
            answer = input("\nTo continue entering items enter 1, to split the rest enter 2: ")



    # **************************************************
    # split included tip, tax, additional tip
    # **************************************************

    # add to each person object
    for i in person:
        # percentage of bill calculation. muliply by x amount
        i.Pct =  i.SubBill() / subtotal
        i.Pct = round(i.Pct,2)
        i.Tax = round(tax * i.Pct, 2)
        i.IncTip = round(inc_tip * i.Pct, 2)
        i.Tip = round(add_tip * i.Pct, 2)


    # **********************************************
    #   Round option (total of per person) function
    # **********************************************
    
    # show each person's total
    for i in person:  # list people's name
        print(i.Name,str(round(i.SubBill(),2)),sep=": ")

    answer = input("\nDo you want to round up each person's total?\nThis will add the difference to the tip. (Type 'y' or press enter to skip): ")
    if answer == 'y':

        # get each persons subbill total
        for i in person:
            old_sub_total = i.SubBill()                                                  # retain old subtotal
            new_sub_total = TipCalc_Func_Class.round_option(i.SubBill(), "up", "dollar") # new rounded sub total
            diff = new_sub_total - old_sub_total                                         # get difference between old and new subtotals
            i.Tip += diff                                                                # add difference to the tip.

        answer_Rtol = True                                                               # boolean to display correct display info
    else:
        answer_Rtol = False



    # ********************************************
    #   Birthday Person
    # ********************************************
    answer = input("\nIs there a birthday person? (Type 'y' or press enter to skip): ")

    if answer == 'y':
        #TODO multi-selection box. <select name="cars" multiple> cars=saab&cars=opel => cars[]
        print("\n\nWho is the birthday person? \n\n")
        
        # list people's name
        for p in person:
            print(p.Name,end="\t")
        
        bday_persons = input("\n(For multiple people type a comma in between their name without spaces. Ex: jason,joe):\n")

        bday_person_list = bday_persons.split(",")  #take string input and convert into a list

        bday_total = 0

        # for persons in the birthday list
        for p in person:
            for i in bday_person_list:
                if p.Name == i:
                    # add up bday total
                    bday_total += p.TolBill()
                    # zero out this person's cost
                    p.Birthday()

        bday_share = round(bday_total, 2) / (len(person)-len(bday_person_list))         # calculate birthday share for each person: divide total birthday share by everyone not include persons on birthday list


        non_birthday_list = []

        # Find out who is not on the birthday list and add birthday share. 
        for p in person:
            for akey in bday_person_list:
                if not p.Name == akey:
                    p.Bday = bday_share
                    non_birthday_list.append(p)                                         # list for extra penny test


    # ********************************************
    #   Does extra penny test
    # ********************************************

    extra_penny_test = 0

    # loop through person list, excluding birthday persons
    # add totals of each person
    if 'non_birthday_list' in locals():
        for p in non_birthday_list:
            extra_penny_test += round(p.TolBill(), 2)
    else:
        for p in person:
            extra_penny_test += round(p.TolBill(), 2)

    # extra penny test
    if extra_penny_test < grandtotal:
        deficit = int(round(grandtotal - extra_penny_test, 2) * 100)

        for i in range(deficit):
            i = i % deficit # in case deficit is more than number of people in list, cycle back around to 0
            # add one penny to each person's total until deficit is complete
            if 'non_birthday_list' in locals():
                non_birthday_list[i].extraPennies += 1
            else:
                person[i].extraPennies += 0.01


    #********************************
    # Display Bill Information
    #********************************
    print()

    # calculations to get correct number of people to multiple grand total with. substract number of birthday people.
    """
    if 'bday_person_list' in locals():
        ptlength = len(person) - len(bday_person_list)
        ptlength = ptlength * #tol_per_person
    else:
        ptlength = len(person)
        ptlength = ptlength * #tol_per_person
    """


    print('Grand Total: ${:.2f}'.format(grandtotal))
    print('Subtotal: ${:.2f}'.format(subtotal))
    print('Tax: ${:.2f}'.format(tax))

    
    # display included gratuity if it has been entered
    if inc_tip != 0:    
        print('Included tip: ${0:.2f} {1:.0f}% on (subtotal + tax)'.format(inc_tip,inc_tip_pct*100))
    

    # display rounded tip
    if 'answer_Rtip' in locals():   
        print('tip: ${0:.2f} (rounded {1} {2}) {3:.0f}% on subtotal'.format(add_tip,answer_Rtip[0],answer_Rtip[1],add_tip_pct*100))
        print("*****STOP*****")
    # display rounded tip and rounded total
    elif 'answer_Rtip' in locals() and answer_Rtol:     
        print('tip: ${0:.2f} (includes difference from rounded total and rounded {1} {2} tip) {3:.0f}% original tip on subtotal'.format(add_tip,answer_Rtip[0],answer_Rtip[1],add_tip_pct*100))
    
    # display rounded total and unrounded tip
    elif answer_Rtol:   
        print('tip: ${0:.2f} (includes difference from rounded total) {1:.0f}% original tip on subtotal'.format(add_tip,add_tip_pct*100))
    
    # display unrounded tip
    elif add_tip == 0:
        print('tip: ${0:.2f}'.format(add_tip))
    
    else:   
        print('tip: ${0:.2f} ({1:.0f}% on subtotal)'.format(add_tip,add_tip_pct*100))
    
    print()
    #********************************
    # Person's Details
    #********************************

    for p in person:
        print(p.Name+':')
        print(f'Total: ${p.TolBill():.2f}')
        print(f'Sub Total: ${p.SubBill():.2f}')
        for k,v in p.ItemColl.items():
            print(f"   {k}: ${v:.2f}")
        if inc_tip != 0:
            print(f'included gratuity: ${p.IncTip:.2f}')
        print(f'tax: ${p.Tax:.2f}')
        if add_tip != 0:
            print(f'tip: ${p.Tip:.2f}')
        if 'bday_share' in locals():      #TODO this needs fixing. giving value of zero
            print(f'birthday share ${p.Bday:.2f}')
        print()

#********************************
if __name__ == "__main__":
    main()