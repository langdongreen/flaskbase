from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField, IntegerField, SubmitField,TextAreaField, validators,HiddenField
from wtforms.validators import DataRequired, Email,Required
import products
from sm import c

class CreateForm(Form):
    colours = ('','Red','Blue','Black','Pink','Purple')
    thread_colours = ('','White', 'Red', 'Blue', 'Lt Blue', 'Black', 'Pink', 'Purple', 'Orange', 'Green', 'Glow in the dark +$1')
    sizes = ('','19mm','25mm')
    buckle = ('Plastic','Zinc')
    material = ('Zinc','Brass')
    images = ('','Bone', 'Crown', 'Paw', 'Star', 'Skull', 'Heart')

    productid = StringField('productid')
    text = StringField('Text')
    collar_colour = SelectField('Collar Colour', choices=[(v,v) for v in colours])
    text_colour = SelectField('Text Colour', choices=[(v,v) for v in thread_colours])
    image = SelectField('Image +$1', choices=[(v,v) for v in images])
    width = SelectField('Width', choices=[('19mm','19mm'),('25mm', '25mm +$5')])
    neck = StringField('Neck (cm)',[validators.Required("Please enter your pets size")])
    hardware = SelectField('Hardware', choices = [('Chrome','Chrome'),('Brass','Brass +$3')])
    buckle_material = SelectField('Buckle Material', choices = [('Acetel Plastic','Acetel Plastic'),('Zinc','Zinc +$3.50')])
    matching_leash = SelectField('Matching Leash', choices = [('',''),('Leash','Yes +$11'),('No','No')])
    qty = SelectField('Qty', choices=[(i,i) for i in range(1,10)])
    add = SubmitField('Add To Cart')


class ShippingForm(Form):
    ship = ('No Tracking', 'Tracking', 'Express')
    shipping = SelectField('Shipping', choices = [(v,v) for v in ship])
    voucher = StringField('Voucher')
    add = SubmitField('Save')

    def update_shipping(self,value):
        self.shipping.data = value
        self.process()



class AddressForm(Form):
    firstname = StringField('firstName',[validators.Required("Please enter your first name")])
    surname = StringField('surname',[validators.Required("Please enter your surname")])
    company = StringField('company')
    address1 = StringField('address1',[validators.Required("Please enter your street")])
    address2 = StringField('address2')
    suburb = StringField('suburb',[validators.Required("Please enter your suburb")])
    state = StringField('state',[validators.Required("Please enter your state")])
    postcode = StringField('postcode',[validators.Required("Please enter your postcode")])
    country = StringField('country')
    email = StringField('email',[validators.Required("Please enter an email address")])
    #email = StringField('email')
    phone = StringField('phone')
    newsletter = BooleanField('newsletter')
    pay = SubmitField('Payment')

class ContactForm(Form):
    name = StringField('name',[validators.Required("Please enter your name")])
    email = StringField('email',[validators.Required("Please enter an email address"), validators.Email("Valid email address required")])
    message = TextAreaField('message',[validators.Required("Please enter a message")])
    gotcha = StringField('blank',[validators.Length(max=0)])
    valid = StringField('valid',[validators.Regexp(c['contact']['validator'])],default=c['contact']['validator'])
    send = SubmitField('Send')
