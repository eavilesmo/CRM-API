# -------------------------
# IMPORTS
# -------------------------
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, DateField
from wtforms.validators import InputRequired, Email

# Creating an instance of Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "22_this_is_a_flask_test_22"

# -------------------------
# VARIABLES
# -------------------------
customers_dict = {}
len_dict = 0
radio_bt = [("Option 1", "Create new customer"),
            ("Option 2", "Get one customer"),
            ("Option 3", "Get all customers"),
            ("Option 4", "Update a customer"),
            ("Option 5", "Delete a customer")]
result_index = """<h2>Welcome to the CRM API!</h2><button type="button" onclick="window.location.href='/home'">Home</button>"""
result_create = """<h2>The customer was correctly created!<br> Name: {}<br> Surname: {}<br> Email: {}<br> Birthdate: {}.</h2>
                   <button type="button" onclick="window.location.href='/home'">Home</button>"""
result_getone = """<h2>Here are the results for your search! <br> Customer ID: {}<br> Name: {}<br> Surname: {}<br> Email: {}<br> Birthdate: {}</h2>
                   <button type="button" onclick="window.location.href='/home'">Home</button>"""
result_getall_empty  = """<h2>The list of customers is empty!</h2>
                          <button type="button" onclick="window.location.href='/home'">Home</button>"""
result_update = """<h2>The customer was correctly updated!<br> Customer ID: {}<br> Name: {}<br> Surname: {}<br> Email: {}<br> Birthdate: {}.</h2>
                   <button type="button" onclick="window.location.href='/home'">Home</button>"""
result_update_error = """<h2>The ID does not exist in the database. Please introduce an existing customer ID.</h2>
                         <button type="button" onclick="window.location.href='/update-customer'">Back</button>"""
result_delete = """<h2>Customer deleted! <br> The customer with ID {} was correctly deleted.</h2>
                   <button type="button" onclick="window.location.href='/home'">Home</button>"""
result_error_getone = """<h2>The ID does not exist in the database. Please introduce the ID again.</h2><br>
                         <button type="button" onclick="window.location.href='/getone-customer'">Back</button>"""
result_error_delete = """<h2>The ID does not exist in the database. Please introduce the ID again.</h2><br>
                         <button type="button" onclick="window.location.href='/delete-customer'">Back</button>"""

# -------------------------
# CLASSES
# -------------------------
class home_page(FlaskForm):
    radio_buttons = RadioField(choices = radio_bt)

class custom_create_form(FlaskForm):
    custom_name = StringField("Name: ", validators=[InputRequired()])
    custom_surname = StringField("Surname: ", validators=[InputRequired()])
    custom_email = StringField("Email: ", validators=[InputRequired(), Email()])
    custom_birthdate = DateField("Birthdate: ", validators=[InputRequired()])

class custom_getone_form(FlaskForm):
    custom_id = StringField("Customer ID: ", validators=[InputRequired()])

def get_dict(id=None):
    if id != None:
        return customers_dict.get(id)
    else:
        return customers_dict

class custom_update_form(FlaskForm):
    custom_id = StringField("Customer ID: ", validators=[InputRequired()])
    custom_name = StringField("Name: ", validators=[InputRequired()])
    custom_surname = StringField("Surname: ", validators=[InputRequired()])
    custom_email = StringField("Email: ", validators=[InputRequired(), Email()])
    custom_birthdate = DateField("Birthdate: ", validators=[InputRequired()])

class custom_delete_form(FlaskForm):
    custom_id = StringField("Customer ID: ", validators=[InputRequired()])

# -------------------------
# FUNCTIONS
# -------------------------
# Creating index page
@app.route("/", methods=["GET", "POST"])
def index():
    return result_index

# Creating home page
@app.route("/home", methods=["GET", "POST"])
def home():
    form = home_page()
    if form.validate_on_submit():
        if form.radio_buttons.data == "Option 1":
            return redirect(url_for("create_form"))
        elif form.radio_buttons.data == "Option 2":
            return redirect(url_for("get_one_form"))
        elif form.radio_buttons.data == "Option 3":
            return redirect(url_for("get_all_form"))
        elif form.radio_buttons.data == "Option 4":
            return redirect(url_for("update_form"))
        elif form.radio_buttons.data == "Option 5":
            return redirect(url_for("delete_form"))
    return render_template("home.html", form=form)

# Creating create-customer page
@app.route("/create-customer", methods=["GET", "POST"])
def create_form():
    global len_dict, customers_dict
    form = custom_create_form()
    if form.validate_on_submit():
        customers_dict[len_dict] = {"name": form.custom_name.data, 
                                    "surname": form.custom_surname.data, 
                                    "email": form.custom_email.data, 
                                    "birthdate": form.custom_birthdate.data}
        len_dict += 1
        return result_create.format(form.custom_name.data, form.custom_surname.data, 
                                    form.custom_email.data, form.custom_birthdate.data)
    return render_template("create_form.html", form=form)

# Creating getone-customer page
@app.route("/getone-customer", methods=["GET", "POST"])
def get_one_form():
    form = custom_getone_form()
    if form.validate_on_submit():
        try:
            id = int(form.custom_id.data)
        except ValueError:
            return result_error_getone
        dict = get_dict(id)
        if dict == None:
            return result_error_getone
        else:
            return result_getone.format(id, dict["name"], dict["surname"], 
                                            dict["email"], dict["birthdate"])
    return render_template("get_one_form.html", form=form)

# Creating getall-customer page
@app.route("/getall-customer", methods=["GET", "POST"])
def get_all_form():
    form = get_dict()
    if len(get_dict()) == 0:
        return result_getall_empty
    else:
        return render_template("get_all_form.html", form=form)

# Creating udpate-customer page
@app.route("/update-customer", methods=["GET", "POST"])
def update_form():
    global customers_dict
    form = custom_update_form()
    if form.validate_on_submit():
        try:
            id = int(form.custom_id.data)
        except ValueError:
            return result_error_delete
        if get_dict(id) == None:
            return result_update_error
        else:
            customers_dict[id] = {"name": form.custom_name.data, 
                              "surname": form.custom_surname.data, 
                              "email": form.custom_email.data, 
                              "birthdate": form.custom_birthdate.data}
            return result_update.format(form.custom_id.data, form.custom_name.data, 
                                    form.custom_surname.data, form.custom_email.data,
                                    form.custom_birthdate.data)
    return render_template("update_form.html", form=form)

# Creating delete-customer page
@app.route("/delete-customer", methods=["GET", "POST"])
def delete_form():
    global customers_dict
    form = custom_delete_form()
    if form.validate_on_submit():
        try:
            id = int(form.custom_id.data)
        except ValueError:
            return result_error_delete
        if id == None:
            return result_error_delete
        else:
            customers_dict.pop(id)
            return result_delete.format(form.custom_id.data)
    return render_template("delete_form.html", form=form)


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
