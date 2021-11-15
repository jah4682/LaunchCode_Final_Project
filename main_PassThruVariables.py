# ---------------------- Final Project | Launch Code ----------------------
# --------------------------- TITLE: Split Me -----------------------------
# DESCRIPTION: A split restaurant bill tip cacluator.

# *******************
#   Imports
# *******************
from flask import Flask, request, redirect, render_template
import decimal
import math
import re
import cgi
import TipCalc_Func_Class

################################# Main Program ##############################

app = Flask(__name__)
app.config['DEBUG'] = True

global dishes
dishes = []                   # empty list for dish item collection for route "assignment"

# ***************************************************************************
@app.route("/", methods=['GET'])
def index():
# Display homepage
    return render_template('index.html')


# ***************************************************************************
@app.route("/numppl", methods=['GET','POST'])
def numppl():
# Number of people #

    if request.method == 'POST':
        num_ppl = request.form['num_ppl']
        num_ppl = int(num_ppl)
        return render_template('page2.html', num_ppl=num_ppl)
    else:
        # when back link is clicked
        num_ppl = request.args.get('num_ppl')
        num_ppl = int(num_ppl)
        return render_template('page2.html')

# ***************************************************************************
@app.route("/nameppl", methods=['GET','POST'])
def nameppl():
# Name of each person #

    if request.method == 'POST':
        global person
        person = []     # 'person' is a list of objects
        pError = []     # invalid name list

        # get a list of names from input text box
        Pnames = request.form.getlist('Pnames')


        for p in Pnames:
            matches = p.isalnum()   # validate alpha characters entered only
            if matches:
                person.append(TipCalc_Func_Class.Person(p))       # set the name of current Person object
            else:
                loop = True
                pError.append(p)

        if 'loop' in locals():
            return render_template("page2.html", Pnames=Pnames, error=loop, pError=pError)
        else:
            return render_template("page3.html")



# ***************************************************************************
@app.route("/subtotal", methods=['GET','POST'])
def subtotal():
# Subtotal #

    if request.method == 'POST':

        # get variables from Form
        subtotal = request.form['subtotal']

        regex = r'^[0-9]+([,.][0-9]{2})?$'    # Regular expression to be matched to
        matches = re.search(regex, subtotal)  # Validate only enter float numbers

        if subtotal == '0' or subtotal == '0.00':
            zero_div = "Bill cannot be zero"
            loop = True
            return render_template("page3.html", zero_div=zero_div, error=loop, subtotal=subtotal)

        if matches:
            # Type conversion
            subtotal = float(subtotal)
            return render_template("page4.html",  subtotal=subtotal) #person=person,

        else:
            loop = True
            return render_template("page3.html", error=loop, subtotal=subtotal)



# ***************************************************************************
@app.route("/tax", methods=['GET','POST'])
def tax():
# Tax #

    if request.method == 'POST':

        # get variables from Form
        #person = request.form.getlist('person')
        subtotal = request.form['subtotal']
        tax = request.form['tax']

        regex = r'^[0-9]+([,.][0-9]{2})?$'  # Regular expression to be matched to
        matches = re.search(regex, tax)     # Validate only enter float numbers

        if matches:
            # Type conversion
            tax = float(tax)
            subtotal = float(subtotal)
            tax_pct = round(tax/subtotal, 2)
            return render_template("page5.html", subtotal=subtotal, tax=tax, tax_pct=tax_pct) #person=person,
        
        else:
            loop = True
            return render_template("page4.html", error=loop, tax=tax)



# ***************************************************************************
@app.route("/inctip",  methods=['POST'])
def inctip():
# Included gratuity #

    if request.method == 'POST':

        # get variables from Form
        #person = request.form.getlist('person')
        subtotal = request.form['subtotal']
        tax = request.form['tax']
        tax_pct = request.form['tax_pct']
        inc_tip = request.form['inc_tip']


        regex = r'^[0-9]+([,.][0-9]{2})?$'  # Regular expression to be matched to
        matches = re.search(regex, inc_tip) # Validate only enter float numbers

        if matches:
            # Type conversion
            subtotal = float(subtotal)
            tax = float(tax)
            tax_pct = float(tax_pct)
            inc_tip = float(inc_tip)
            inc_tip_pct = round(inc_tip/(subtotal+tax), 2)

            # tip quick button dollar amount. returns tupil
            tipbtn = TipCalc_Func_Class.tip_btn(subtotal)


            return render_template("tipbtn.html", subtotal=subtotal, tax=tax, tax_pct=tax_pct, inc_tip=inc_tip, inc_tip_pct=inc_tip_pct, tipbtn=tipbtn) #person=person,
        else:
            loop = True
            return render_template("page5.html", error=loop, inc_tip=inc_tip)


# ***************************************************************************
@app.route("/addtip", methods=['POST'])
def addtip():
# Additonal tip or Regular tip #

    if request.method == 'POST':

        # get variables from Form
        #person = request.form.getlist('person')

        subtotal = request.form['subtotal']
        tax = request.form['tax']
        tax_pct = request.form['tax_pct']
        inc_tip = request.form['inc_tip']
        inc_tip_pct = request.form['inc_tip_pct']
        add_tip = request.form['add_tip'] # will be a number. validation is on client side web browser through buttons and slider.

        # Type conversion
        subtotal = float(subtotal)
        tax = float(tax)
        tax_pct = float(tax_pct)
        inc_tip = float(inc_tip)
        inc_tip_pct = float(inc_tip_pct)
        add_tip = float(add_tip)
        add_tip = TipCalc_Func_Class.tip(add_tip, subtotal) # Save the variable
        add_tip_pct = round(add_tip/subtotal, 2)


        if add_tip == 0: # if tip is zero skip round tip page.
            # for assignment page
            bill_so_far = subtotal
            return render_template("page8.html", subtotal=subtotal, tax=tax, tax_pct=tax_pct, inc_tip=inc_tip, inc_tip_pct=inc_tip_pct, add_tip=add_tip, add_tip_pct=add_tip_pct, bill_so_far=bill_so_far) #person=person,
        else:
            return render_template("page7.html", subtotal=subtotal, tax=tax, tax_pct=tax_pct, inc_tip=inc_tip, inc_tip_pct=inc_tip_pct, add_tip=add_tip, add_tip_pct=add_tip_pct) #person=person,



# ***************************************************************************
@app.route("/roundtip", methods=['POST'])
def roundtip():
# Rounding option (tip) #

    if request.method == 'POST':

        # get variables from Form
        #person = request.form.getlist('person')
        subtotal = request.form['subtotal']
        tax = request.form['tax']
        tax_pct = request.form['tax_pct']
        inc_tip = request.form['inc_tip']
        inc_tip_pct = request.form['inc_tip_pct']
        add_tip = request.form['add_tip']
        add_tip_pct = request.form['add_tip_pct']
        
        # deterimine if round type was skipped
        if "roundtype" in locals():
            roundtype = request.form['roundtype'] # up, down, closest
            print("roundtype = ",roundtype) #test
            percision = request.form['percision'] # dollar, half, quarter, tenth


        # Type conversion
        subtotal = float(subtotal)
        tax = float(tax)
        tax_pct = float(tax_pct)
        inc_tip = float(inc_tip)
        inc_tip_pct = float(inc_tip_pct)
        add_tip = float(add_tip)
        add_tip_pct = float(add_tip_pct)

        # Invoke Rounding Function
        if "roundtype" in locals():
            add_tip = TipCalc_Func_Class.round_option(add_tip, roundtype, percision)
            # Decimal point
            add_tip = round(add_tip,2)

        # for assignment page
        bill_so_far = subtotal

        # deterimine if round type was skipped
        if "roundtype" in locals():
            return render_template("page8.html", subtotal=subtotal, tax=tax, tax_pct=tax_pct, inc_tip=inc_tip, inc_tip_pct=inc_tip_pct, add_tip=add_tip, add_tip_pct=add_tip_pct, roundtype=roundtype, percision=percision, bill_so_far=bill_so_far) #person=person,
        else:
            return render_template("page8.html", subtotal=subtotal, tax=tax, tax_pct=tax_pct, inc_tip=inc_tip, inc_tip_pct=inc_tip_pct, add_tip=add_tip, add_tip_pct=add_tip_pct, bill_so_far=bill_so_far) #person=person,


# ***************************************************************************
@app.route("/assignment", methods=['POST'])
def assignment():
# Add Individual Items #

    if request.method == 'POST':
        
        # get variables from Form
        #person = request.form.getlist('person')
        subtotal = request.form['subtotal']
        tax = request.form['tax']
        tax_pct = request.form['tax_pct']
        inc_tip = request.form['inc_tip']
        inc_tip_pct = request.form['inc_tip_pct']
        add_tip = request.form['add_tip']
        add_tip_pct = request.form['add_tip_pct']

        # deterimine if round type was skipped
        if "roundtype" in locals():
            roundtype = request.form['roundtype']
            percision = request.form['percision']

        answer = request.form['answer']

        

        if answer == 'True':
            answer = True             # do-while loop condition

        while answer == True or answer == "3" or answer == "2" or answer == "1" or answer == "0":

            # When "itemized bill" is pressed render page 9.
            if answer == "0":
                return render_template("page9.html", subtotal=subtotal)


            # Form for name and price of dish
            if answer == "1":

                loop = True           # do-while loop condition

                while loop:

                    # Retreive from Form
                    item_Name = request.form['item_Name']
                    item_Price = request.form['item_Price']

                    regex = r'^[0-9]+([,.][0-9]{2})?$'      # Regular expression to be matched to
                    matchesP = re.search(regex, item_Price)  # Validate only enter float numbers
                    matchesN = item_Name.isalnum()           # Validate only alpha-numeric


                    if matchesP and matchesN:
                        # add item to running dishes list
                        item_Price = float(item_Price)
                        dishes.append(item_Price)
                        print("****** dishes=",dishes) #test
                        return render_template("page10.html", subtotal=subtotal, item_Name=item_Name, item_Price=item_Price, person=person)
                    else:
                        loop = True
                        return render_template("page9.html", error=loop, item_Name=item_Name, item_Price=item_Price)


            # Form for assignment of dish(es) to persons
            if answer == "2":

                shared_ordered_list = request.form.getlist('shared_ordered_list')
                item_Name = request.form['item_Name']
                item_Price = request.form['item_Price']
                #subtotal = request.form['subtotal']
                # type conversion
                subtotal = float(subtotal)
                item_Price = float(item_Price)

                # assign item to individual person
                # loop through list of objects. 'x' is the object, not a number.
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

                print("****** dishes=",dishes,type(dishes))#test
                bill_so_far = TipCalc_Func_Class.dish_total(subtotal, dishes)

                #return render_template("page8.html",)


            # Spliting the rest
            if answer == "3":
                # split bill
                item_Name = "Split Rest of Bill"

                if "bill_so_far" in locals():
                    item_Price = bill_so_far
                # if answer = 1 is skipped and answer = 2 comes first
                else:
                    subtotal = float(subtotal)
                    item_Price = subtotal


                # add item to running dishes list
                dishes.append(item_Price)

                # loop through object list.
                for x in person:
                    # create item description
                    food_item = item_Name + " (1/" + str(len(person)) + ")"
                    # divide price by number of people at table
                    prx = item_Price / len(person)
                    dic_item = {food_item:prx}
                    x.ItemColl.update(dic_item)

                # add up amount in dishes list
                bill_so_far = TipCalc_Func_Class.dish_total(subtotal, dishes)



            if bill_so_far == 0:
                return render_template("page11.html")
            else:
                # Render page 8: ask if user wants to split the rest of bill or continue itemizing
                return render_template("page8.html", bill_so_far=bill_so_far, subtotal=subtotal)


# needs to go somewhere?
    # **************************************************
    # split included tip, tax, additional tip
    # **************************************************

    # add to each person object
    for i in person:
        # percentage of bill calculation. multiply by x amount
        i.Pct =  i.SubBill() / subtotal
        i.Pct = round(i.Pct,2)
        i.Tax = round(tax * i.Pct, 2)
        i.IncTip = round(inc_tip * i.Pct, 2)
        i.Tip = round(add_tip * i.Pct, 2)


@app.route("/page9")
def page9():
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


@app.route("/page10")
def page10():
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



# needs to go somewhere?
    # ********************************************
    #   bill so far
    # ********************************************

    grandtotal = subtotal+tax+inc_tip+add_tip
    #must_pay = subtotal+tax+inc_tip


# needs to go somewhere?
    # ********************************************
    #   Extra penny test
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


@app.route("/page11")
def page11():
    #********************************
    # Display Bill Information
    #********************************
    print()
    print('Grand Total: ${:.2f}'.format(grandtotal))
    print('Subtotal: ${:.2f}'.format(subtotal))
    print('Tax: ${:.2f}'.format(tax))

    
    # display included gratuity if it has been entered
    if inc_tip != 0:    
        print('Included tip: ${0:.2f} {1:.0f}% on (subtotal + tax)'.format(inc_tip,inc_tip_pct*100))
    

    # display rounded tip
    if 'roundtype' in locals():   #TODO change answer_Rtip to roundtype in locals
        print('tip: ${0:.2f} (rounded {1} {2}) {3:.0f}% on subtotal'.format(add_tip,roundtype,answer_Rtip[1],add_tip_pct*100))  #TODO change answer_Rtip[1] to percision
        print("*****STOP*****")
    # display rounded tip and rounded total
    elif 'roundtype' in locals() and answer_Rtol:      #TODO change answer_Rtip to roundtype in locals
        print('tip: ${0:.2f} (includes difference from rounded total and rounded {1} {2} tip) {3:.0f}% original tip on subtotal'.format(add_tip,roundtype,answer_Rtip[1],add_tip_pct*100))  #TODO  change answer_Rtip[1] to percision
    
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
    app.run()