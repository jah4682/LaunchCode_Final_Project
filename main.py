# ---------------------- Final Project | Launch Code ----------------------
# --------------------------- TITLE: Split Me -----------------------------
# DESCRIPTION: A split restaurant bill tip cacluator.

# *******************
#   Imports
# *******************
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils_hash_n_salt import make_pw_hash, check_pw_hash
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

# ****************************** Database Connection ************************
# Database name: split-me
# User Account: split-me
# User Password: mybill
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://split-me:mybill@localhost:8889/split-me' 
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)   # variable to create database objects
app.secret_key = '123' # secret key

# ******************************  Setup Database Tables ************************
class User(db.Model):

    # create columns and specify its datatype.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    bills = db.relationship('Bills', backref='owner') # relationship: one-to-many, user has many bill history.

    # constructor
    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

class Bills(db.Model):
    # create columns and specify its datatype.
    id = db.Column(db.Integer, primary_key=True) # primary key, column constructor, unique integer. handled automatically by sqlalchemy
    bill_overall = db.Column(db.String(200))
    bill_ind = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # foreign key

    # constuctor
    def __init__(self, bill_overall, bill_ind, owner):
        self.bill_overall = bill_overall
        self.bill_ind = bill_ind
        self.owner = owner

################################# Functions ##############################
@app.route("/", methods=['GET'])
def index():
# Display homepage
    username = session['username']  # retrieving username that is stored in session
    return render_template('index.html',username=username)


# ***************************************************************************
@app.before_request
def require_login():
# Allowed Routes
    allowed_routes = ['login', 'registration']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')



# ***************************************************************************
@app.route('/login', methods=['POST', 'GET'])
def login():
# Login
    if request.method == 'POST':
        # Get parameters from post request
        username = request.form['username_form']
        password = request.form['password_form']
        user = User.query.filter_by(username=username).first()

        # Verify
        if user and check_pw_hash(password, user.pw_hash):  # does the user exist
            session['username'] = username  # if user exist save username in a session
            return redirect('/')
        else:
            flash('password is incorrect or user does not exist', 'error')  # if user does not exist give error message
    
    return render_template('login.html')



# ***************************************************************************
@app.route('/registration', methods=['POST', 'GET'])
def registration():
# Registration
    if request.method == 'POST':
        # Get parameters from post request
        username = request.form['username_form']
        password = request.form['password_form']
        verify = request.form['verify_form']

        # ------ BEGIN VALIDATION -------

        # validate password
        if password == '':  # if null
            flash('password must be filled in', 'error')
            return render_template('registration.html')
        elif ' ' in password:  # if space
            flash('password cannot contain a space', 'error')
            return render_template('registration.html')
        elif len(password) < 3 or len(password) > 20:  # if out of range 3 to 20
            flash('password must be between 3 and 20 characters long', 'error')
            return render_template('registration.html')

        # validate password confirmation
        elif password != verify:
            flash('your passwords do not match', 'error')
            return render_template('registration.html')

        # Validate Username
        user = User.query.filter_by(username=username).first()
        if user != None:  # if not in database skip inner if-statement to avoid error
            if user.username == username:  # if username exist
                flash('this username already exists')
                return render_template('registration.html')
        
        elif username == '':  # if field is left blank
            flash('username must be filled in')
            return render_template('registration.html')

        elif ' ' in username:  # if there is a space
            flash('username cannot contain a space')
            return render_template('registration.html')

        elif len(username) < 3 or len(username) > 20:  # if username is out of range. 
            flash('username must be between 3 and 20 characters long')
            return render_template('registration.html')

        # ------ END VALIDATION ------

        # if successful add new user to database and redirect user to newpost page
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
    
    return render_template('registration.html')



# ***************************************************************************
@app.route('/logout')
def logout():
# Logout
    del session['username'] # removing username from current session
    return redirect('/')    # redirect to index page (which will redirect to login page because username is not in a session)



# ***************************************************************************
@app.route("/page1", methods=['GET'])
def page1():
# Begin Tip/Split Calculator on page 1    
    return render_template('page1.html')


# ***************************************************************************
@app.route("/numppl", methods=['GET','POST'])
def numppl():
# Number of people #

    if request.method == 'POST':
        num_ppl = request.form['num_ppl']
        num_ppl = int(num_ppl)
        return render_template('page2.html', num_ppl=num_ppl)
    else:
        # when "back" link is clicked. "GET" Method
        num_ppl = request.args.get('num_ppl')
        num_ppl = int(num_ppl)
        return render_template('page2.html')



# ***************************************************************************
@app.route("/nameppl", methods=['GET','POST'])
def nameppl():
# Name of each person #

    if request.method == 'POST':

        global person   # make global variable
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
        global subtotal # make global variable

        # get variables from Form
        subtotal = request.form['subtotal']

        regex = r'^[0-9]+([,.][0-9]{2})?$'    # Regular expression to be matched to
        matches = re.search(regex, subtotal)  # Validate only enter float numbers

        if matches:
            # Type conversion
            subtotal = float(subtotal)
            return render_template("page4.html")
        elif subtotal == '0' or subtotal == '0.00':
            zero_div = "Subtotal cannot be zero"
            loop = True
            return render_template("page3.html", zero_div=zero_div, error=loop, subtotal=subtotal)
        else:
            loop = True
            return render_template("page3.html", error=loop, subtotal=subtotal)



# ***************************************************************************
@app.route("/tax", methods=['GET','POST'])
def tax():
# Tax #

    if request.method == 'POST':
        # make global variable
        global tax
        global tax_pct


        # get variables from Form
        tax = request.form['tax']

        regex = r'^[0-9]+([,.][0-9]{2})?$'  # Regular expression to be matched to
        matches = re.search(regex, tax)     # Validate only enter float numbers

        if matches:
            # Type conversion
            tax = float(tax)
            tax_pct = round(tax/subtotal, 2)
            return render_template("page5.html")
        else:
            loop = True
            return render_template("page4.html", error=loop, tax=tax)



# ***************************************************************************
@app.route("/inctip",  methods=['POST'])
def inctip():
# Included gratuity #

    if request.method == 'POST':
        # make global variable
        global inc_tip
        global inc_tip_pct


        # get variables from Form
        inc_tip = request.form['inc_tip']

        regex = r'^[0-9]+([,.][0-9]{2})?$'  # Regular expression to be matched to
        matches = re.search(regex, inc_tip) # Validate only enter float numbers

        if matches:
            # Type conversion
            inc_tip = float(inc_tip)
            inc_tip_pct = round(inc_tip/(subtotal+tax), 2)

            # tip quick button dollar amount. returns tupil
            tipbtn = TipCalc_Func_Class.tip_btn(subtotal)
            return render_template("tipbtn.html", inc_tip=inc_tip, tipbtn=tipbtn, subtotal=subtotal)
        else:
            loop = True
            return render_template("page5.html", error=loop, inc_tip=inc_tip)


# ***************************************************************************
@app.route("/addtip", methods=['POST'])
def addtip():
# Additonal tip or Regular tip #

    if request.method == 'POST':
        # make global variable
        global add_tip
        global add_tip_pct
        global bill_so_far


        # get variables from Form
        add_tip = request.form['add_tip'] # will be a number. validation is on client side web browser through buttons and slider.

        # Type conversion
        add_tip = float(add_tip)
        add_tip = TipCalc_Func_Class.tip(add_tip, subtotal) # Save the variable
        add_tip_pct = round(add_tip/subtotal, 2)


        if add_tip == 0: # if tip is zero skip round tip page 7.
            bill_so_far = subtotal  # for assignment page
            return render_template("page8.html", subtotal=subtotal, bill_so_far=bill_so_far)
        else:
            return render_template("page7.html", add_tip=add_tip)



# ***************************************************************************
@app.route("/roundtip", methods=['POST'])
def roundtip():
# Rounding option (tip) #


    if request.method == 'POST':

        answer = request.form['answer']

        # deterimine if round type was skipped
        if answer == 'y':

            # make global variable
            global roundtype
            global percision
            global add_tip

            # get variables from Form
            roundtype = request.form['roundtype'] # up, down, closest
            percision = request.form['percision'] # dollar, half, quarter, tenth


            # Invoke Rounding Function
            add_tip = TipCalc_Func_Class.round_option(add_tip, roundtype, percision)
            # Decimal point
            add_tip = round(add_tip, 2)


            bill_so_far = subtotal  # for assignment page 8
            return render_template("page8.html", subtotal=subtotal, bill_so_far=bill_so_far)
        else:
            bill_so_far = subtotal  # for assignment page 8
            return render_template("page8.html", subtotal=subtotal, bill_so_far=bill_so_far)


# ***************************************************************************
@app.route("/assignment", methods=['POST'])
def assignment():
# Add Individual Items #

    if request.method == 'POST':

        # get variables from Form
        answer = request.form['answer']


        # When "itemized bill" is pressed render page 9.
        if answer == "0":
            if not 'bill_so_far' in locals():
                bill_so_far = subtotal
            return render_template("page9.html", subtotal=subtotal, bill_so_far=bill_so_far)


        # Form for Name and Price of dish
        if answer == "1":

            # Retreive from Form
            item_Price = request.form['item_Price']
            item_Name = request.form['item_Name']

            regexP = r'^[0-9]+([,.][0-9]{2})?$'       # Regular expression to be matched to
            matchesP = re.search(regexP, item_Price)  # Validate only enter float numbers
            regexN = r'^[a-z\d\-_\s]+$'               # Regular expression to be matched to
            matchesN = re.search(regexN, item_Name)   # Validate only alpha, numeric, space


            if matchesP and matchesN:
                # add item to running dishes list
                item_Price = float(item_Price)
                dishes.append(item_Price)
                return render_template("page10.html", item_Name=item_Name, item_Price=item_Price, person=person) # subtotal=subtotal,
            else: # Error handeling
                if matchesP == None: # Price has error
                    loopP = True
                    return render_template("page9.html", errorP=loopP, item_Name=item_Name, item_Price=item_Price)
                elif matchesN == None: # Name has error
                    loopN = True
                    return render_template("page9.html", errorN=loopN, item_Name=item_Name, item_Price=item_Price)
                else: # Name and Price error
                    loopN = True
                    loopP = True
                    return render_template("page9.html", errorN=loopN, errorP=loopP, item_Name=item_Name, item_Price=item_Price)


        # Form for assignment of dish to person(s)
        if answer == "2":

            shared_ordered_list = request.form.getlist('shared_ordered_list')
            item_Name = request.form['item_Name']
            item_Price = request.form['item_Price']

            # type conversion
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
            bill_so_far = TipCalc_Func_Class.dish_total(subtotal, dishes)


        # Spliting the rest
        if answer == "3":
            # split bill
            item_Name = "Split Rest of Bill"

            # split whatever is remaining of bill
            if not "bill_so_far" in locals() or bill_so_far == subtotal:
                # split entire bill
                item_Price = subtotal
            else:
                item_Price = bill_so_far

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
            # split included tip, tax, & additional tip then add to each person object
            for i in person:
                # percentage of bill calculation.
                i.Pct = i.SubBill() / subtotal
                i.Pct = round(i.Pct, 2)
                # percentage multiply by x amount
                i.Tax = round(tax * i.Pct, 2)
                i.IncTip = round(inc_tip * i.Pct, 2)
                i.Tip = round(add_tip * i.Pct, 2)

            bill_so_far = ''
            return render_template("page11.html", person=person)
        else:
            # Render page 8: ask if user wants to split the rest of bill or continue itemizing
            return render_template("page8.html", bill_so_far=bill_so_far, subtotal=subtotal)




# ***************************************************************************
@app.route("/roundtotal", methods=['POST'])
def roundtotal():
# Round option (total of per person) function #

    global answer_Rtol

    answer = request.form['answer']

    if answer == 'y':
        # get each persons subbill total
        for i in person:
            old_sub_total = i.SubBill()                                                  # retain old subtotal
            new_sub_total = TipCalc_Func_Class.round_option(i.SubBill(), "up", "dollar") # new rounded sub total
            diff = new_sub_total - old_sub_total                                         # get difference between old and new subtotals
            i.Tip += diff                                                                # add difference to the tip
            i.rounddiff = diff                                                           # add difference to subbill calculation

        answer_Rtol = True                                                               # boolean to display correct display info
        return render_template("page12.html", person=person)
    else:
        answer_Rtol = False
        return render_template("page12.html", person=person)



# ***************************************************************************
@app.route("/birthday", methods=['POST'])
def birthday():
# Birthday Person #

    answer = request.form['answer']

    if answer == 'y':
        
        bday_person_list = request.form.getlist('bday_person_list')

        # Error Test: If all persons are selected to be the birthday person. At least one person must not be the birthday person.
        if len(bday_person_list) == len(person):
            loop = True
            errorMsg = "Sorry, someone is gonna have to pick up the tab."
            return render_template("page12.html", error=loop, errorMsg=errorMsg, person=person)

        bday_total = 0
        non_birthday_list = []

        # for persons in the birthday list
        for p in person:
            for i in bday_person_list:
                if p.Name == i:
                    # add up bday total
                    bday_total += p.TolBill()
                    # zero out this person's cost
                    p.Birthday()
                else:
                    non_birthday_list.append(p)        # list for extra penny test

        # calculate birthday share for each person: divide total birthday share by everyone not including persons on birthday list
        bday_total = round(bday_total, 2)
        bday_share = bday_total / (len(person)-len(bday_person_list))
        
        for p in person:
            for i in non_birthday_list:
                if p.Name == i:
                    p.Bday = bday_share
                    print("person bday",p.Bday)
                    print("bdayshare",bday_share)


    # ********************************************
    #  bill so far
    grandtotal = subtotal + tax + inc_tip + add_tip

    # ********************************************
    #   Extra penny test
    # ********************************************

    extra_penny_test = 0
    extra_penny_tax = 0

    # if there is a birthday, loop through person list, excluding birthday persons
    if 'non_birthday_list' in locals():
        list_index = len(non_birthday_list) # for list indexing
        for p in non_birthday_list:
            # add totals of each person
            extra_penny_test += round(p.TolBill(), 2)
            # add totals of tax divided by number in party
            extra_penny_tax += round(tax / len(non_birthday_list), 2)
    else:
        list_index = len(person) # for list indexing
        for p in person: # if birthday page was skipped, loop through all persons at the table.
            extra_penny_test += round(p.TolBill(), 2)
            # add totals of tax divided by number in party
            extra_penny_tax += round(tax / len(person), 2)

    # limit these variables to two decimal places
    extra_penny_test = round(extra_penny_test, 2)
    extra_penny_tax = round(extra_penny_tax ,2)
    grandtotal = round(grandtotal, 2)


    # extra penny TAX test
    if extra_penny_tax < tax:
        tax_deficit = tax - extra_penny_tax
        tax_deficit = round(tax_deficit, 2)

        tax_deficit_str = str(tax_deficit)
        tax_deficit_str = tax_deficit_str.split(".")
        test_length = len(tax_deficit_str[1])

        if test_length == 2:
            tax_deficit = tax_deficit * 100
        else:
            tax_deficit = tax_deficit * 10
        
        tax_deficit = int(tax_deficit)

        for i in range(tax_deficit):
            i = i % list_index
            if 'non_birthday_list' in locals():
                non_birthday_list[i].Tax += 0.01
            else:
                person[i].Tax += 0.01

    # extra penny TOTAL test
    if extra_penny_test < grandtotal:
        deficit = grandtotal - extra_penny_test
        deficit = round(deficit, 2)

        # convert deficit to string 
        deficit_str = str(deficit)
        deficit_str = deficit_str.split(".")
        # count how many digits after decimal spot (second spot in list)
        test_length = len(deficit_str[1])


        # Which to multiply by to get to single digit
        if test_length == 2:
            deficit = deficit * 100
        else:
            deficit = deficit * 10
        
        # convert float to integer for For-Loop
        deficit = int(deficit)
        

        # add a pennies to each person in list until loop is finished.
        for i in range(deficit):
            i = i % list_index # in case deficit is more than number of people in list, cycle back around to 0

            # add one penny to each person's total until deficit is complete
            if 'non_birthday_list' in locals():
                non_birthday_list[i].extraPennies += 0.01
            else:
                person[i].extraPennies += 0.01


    # Prepare string for database insersion
    # Overall Bill
    bill_overall = "Grandtotal: $" + str(f'{grandtotal:.2f}') + ","
    bill_overall = bill_overall + "Subtotal: $" + str(f'{subtotal:.2f}') + ","
    bill_overall = bill_overall + "Tax: $" + str(f'{tax:.2f}') + ","
    if inc_tip != 0:
        bill_overall = bill_overall + "Included Gratuity: $" + str(f'{inc_tip:.2f}') + " " + str(f'{inc_tip_pct*100:.0f}') + "% on (subtotal + tax),"
    if 'roundtype' in globals():
        bill_overall = bill_overall + "Tip: $" + str(f'{add_tip:.2f}') + " (rounded " + roundtype + " " + percision + ") " + str(f'{add_tip_pct*100:.0f}') + "% on subtotal"
    elif 'roundtype' in globals() and answer_Rtol:
        bill_overall = bill_overall + "Tip: $" + str(f'{add_tip:.2f}') + " (includes difference from rounded total and rounded " + roundtype + " " + percision + " tip) " + str(f'{add_tip_pct*100:.0f}') + "% original tip on subtotal"
    elif answer_Rtol:
        bill_overall = bill_overall + "Tip: $" + str(f'{add_tip:.2f}') + " (includes difference from rounded total) " + str(f'{add_tip_pct*100:.0f}') + "% original tip on subtotal"
    elif add_tip == 0:
        bill_overall = bill_overall + "Tip: $" + str(f'{add_tip:.2f}')
    else:
        bill_overall = bill_overall + "Tip: $" + str(f'{add_tip:.2f}') + "(" + str(f'{add_tip_pct*100:0.0f}') + "% on subtotal)"


    # Individual's Bill
    bill_ind = ""
    count = 0  # for conditional
    for i in person:
        bill_ind = bill_ind + i.Name + ",Individual Total: $" + str(f'{i.TolBill():0.2f}') + ","
        bill_ind = bill_ind + "Sub Total: $" + str(f'{i.SubBill():0.2f}') + ","
        for k, v in i.ItemColl.items():
            bill_ind = bill_ind + k + ": $" + str(f'{v:0.2f}') + ","
        bill_ind = bill_ind + "Tax: $" + str(f'{i.Tax:0.2f}') + ","
        bill_ind = bill_ind + "Tip: $" + str(f'{i.Tip:0.2f}') + ","
        bill_ind = bill_ind + "Included Gratuity: $" + str(f'{i.IncTip:0.2f}') + ","
        bill_ind = bill_ind + "Birthday Share: $" + str(f'{i.Bday:0.2f}')
        if count < len(person)-1:
            # conditional statement so comma is not placed at the end of the looping list
            bill_ind = bill_ind + ","
            count += 1


    # Insert this bill's data into database
    owner = User.query.filter_by(username=session['username']).first()        # if user is logged in get username from session object and apply to filter find out username's database id
    new_bill = Bills(bill_overall, bill_ind, owner)
    db.session.add(new_bill)
    db.session.commit()

    # Render Page 13
    if 'roundtype' in globals():
        return render_template("page13.html", person=person, grandtotal=grandtotal, subtotal=subtotal, tax=tax, inc_tip=inc_tip, inc_tip_pct=inc_tip_pct, add_tip=add_tip, add_tip_pct=add_tip_pct, answer_Rtol=answer_Rtol, roundtype=roundtype, percision=percision)
    else:
        return render_template("page13.html", person=person, grandtotal=grandtotal, subtotal=subtotal, tax=tax, inc_tip=inc_tip, inc_tip_pct=inc_tip_pct, add_tip=add_tip, add_tip_pct=add_tip_pct, answer_Rtol=answer_Rtol)



# ***************************************************************************
@app.route("/history", methods=['GET'])
def history():
    # Bills History #

    username = session['username']  # retrieve username from login session
    user = User.query.filter_by(username=username).first() # use username to retrieve its primary key id within the database
    history = Bills.query.filter_by(owner_id=user.id).all() # retrieve user_id's bill history information

    return render_template("history.html", history=history)


# ################################### END ####################################
if __name__ == "__main__":
    app.run()