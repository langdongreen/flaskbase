from flask import Flask, render_template, url_for, session, redirect, request,flash
from werkzeug.datastructures import ImmutableOrderedMultiDict
from MySQLdb import escape_string as escape
from datetime import datetime
import xml.etree.ElementTree
from urllib.request import urlopen
import requests
from forms import AddressForm, ContactForm, CreateForm
import time
from flask_mail import Mail, Message
import products
from config import ADMIN, SKYPE, ORDER_EMAIL
from config import VALIDATION_FAIL, EMPTY_CART, LINE_NOT_FOUND, ORDER_ERROR, RETURN_ERROR
from config import LOG_SUCCESS, LOG_ERROR, SUCCESSFUL_ORDER
from config import HOME, BANNER, ABOUT, TERMS, SHIPPING
from config import API_BASE, API_KEY
import logging
from utils import *

logging.basicConfig(filename='debug.log',level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

app = Flask(__name__)

app.config.from_object('config')
mail = Mail(app)



@app.route('/')
def index():
     '''Render index template with banner, cart and contact details.'''
     logging.info("test")
     return render_template('index.html', banner = BANNER, lines = get_lines(),contact=get_contact())



@app.route('/create',methods=["GET","POST"])
def create():
    '''Render collarcreator form and deal with form data'''
    createForm = CreateForm(csrf_enabled=False)

    if createForm.is_submitted():
        text = createForm.text.data
        collar_colour = createForm.collar_colour.data
        text_colour = createForm.text_colour.data
        image = createForm.image.data
        width = createForm.width.data
        neck = createForm.neck.data
        hardware = createForm.hardware.data
        matching_leash = createForm.matching_leash.data

        custom =  {'text': text,'collar_colour': collar_colour,'text_colour': text_colour,
                                'image': image,'width': width,'neck': neck,
                                'hardware': hardware,'matching_leash': matching_leash}
        qty = 1
        price = get_price(custom)

        line = {'label': products.product_list[1][0], 'custom': custom, 'qty': qty,'price': price * qty}

        add_to_cart(line)

        '''if createForm.validate() == False:
            return render_template('collar_creator.html', banner = BANNER, contact = get_contact(), lines = get_lines(), create = createForm, collardata = get_collars(), text = 'text')
        else:
            return redirect(url_for('cart'))'''

        return redirect(url_for('cart'))

    text = ''

    return render_template('collar_creator.html', banner = BANNER, contact = get_contact(), lines = get_lines(), create = createForm, collardata = get_collars(), text = text)

@app.route('/info')
def info():
    '''Render info template'''
    return render_template('info.html', banner = BANNER, contact = get_contact(), lines = get_lines(), text = 'text')

@app.route('/about')
def about():
    '''Render index template with banner, cart contact details and ABOUT text.'''

    text = ABOUT
    return render_template('about.html', banner = BANNER, contact=get_contact(), lines = get_lines(), text = text)


@app.route('/contact', methods=["GET","POST"])
def contact():
    '''Render contact template with contact form and process submitted form data.'''
    contactForm = ContactForm(csrf_enabled=False)

    #if contact form submitted
    if contactForm.send.data:
        #Clean and verify input
        if contactForm.validate() == False:
            return render_template('contact.html', contactForm = contactForm, contact=get_contact(), lines = get_lines())
        else:
            try:
                name = contactForm.name.data
            except:
                name = ''

            try:
                sender = contactForm.email.data
            except:
                sender = ''

            try:
                message = contactForm.message.data
            except:
                message = ''

            html = render_template(email_order.html,banner = BANNER, contact=get_contact(),lines = get_lines(), address = address, cart = cart, total = total, shipping=get_shipping())
            if send_email("Contact "+name,sender,[ADMIN],message,html):
                return redirect(url_for('success'))
            else:
                return redirect(url_for('error'))

    return render_template('contact.html', banner = BANNER, contact=get_contact(), contactForm = contactForm, lines = get_lines(), referrer = request.referrer)


@app.route('/cart')
def cart():
    '''Render cart template to display shopping cart.'''
    cart = get_cart()
    total = get_total()

    #If cart is empty, redirect to contact
    if not cart:
        flash(EMPTY_CART)
        return redirect(url_for('error'))

    return render_template('cart.html', banner = BANNER, contact=get_contact(), lines = get_lines(), cart = cart, total = total, shipping = get_shipping())

@app.route('/empty')
def empty():
    '''Empty shopping cart list and redirect to order page.'''
    empty_cart()
    return redirect(url_for('index'))

@app.route('/cart/delete/<int:row_id>')
def remove_row(row_id):
    '''Remove one row of shopping cart list.'''
    cart = get_cart()

    if cart and row_id < len(cart):
        del cart[row_id]
        session['cart'] = cart
    else:
        flash(LINE_NOT_FOUND)
        return redirect(url_for('error'))

    return redirect(url_for('cart'))

@app.route('/checkout', methods=["GET","POST"])
def checkout():
    '''Render checkout template and display cart and address forms.  Deal with submitted data.'''
    addressForm = AddressForm(csrf_enabled=False)
    cart = get_cart()
    if not cart:
        flash(EMPTY_CART)
        return redirect(url_for('error'))
    #Address form submitted, save to session and redirect to payment page
    elif addressForm.is_submitted() and cart:
        firstname = addressForm.firstname.data
        surname = addressForm.surname.data
        company = addressForm.company.data
        address1 = addressForm.address1.data
        address2 = addressForm.address2.data
        suburb = addressForm.suburb.data
        state = addressForm.state.data
        country = addressForm.country.data
        email = addressForm.email.data
        phone = addressForm.phone.data
        postcode = addressForm.postcode.data

        session['address'] =  {'name': firstname,'surname': surname,'company': company,
                                'address1': address1,'address2': address2,'suburb': suburb,
                                'state': state,'postcode': postcode,'country':country,
                                'phone':phone,'email': email }

        if addressForm.validate() == False:
              return render_template('cart.html', banner = BANNER, contact=get_contact(), lines = get_lines(), address = addressForm, total=get_total(), cart= cart, shipping = get_shipping(), addressdata=get_address())
        else:

            return redirect(url_for('pay'))


    return render_template('cart.html',banner = BANNER, contact=get_contact(), lines = get_lines(), address = addressForm, total=get_total(), cart= cart, shipping = get_shipping(), addressdata=get_address())

@app.route('/pay')
def pay():
    '''Render pay template displaying cart and payment button.'''
    address = ''
    cart = get_cart()
    total = get_total()
    address = get_address()

    if(not order_ok()):
        flash(ORDER_ERROR)
        return redirect(url_for('error'))


    return render_template('pay.html', banner = BANNER, contact=get_contact(),lines = get_lines(), address = address, cart = cart, total = total, shipping=get_shipping())

@app.route('/error')
def error():
    '''Render error template displaing flashed() message.'''

    return render_template('error.html', banner = BANNER, contact=get_contact(),lines = get_lines())

@app.route('/success')
def success():
    '''Render success template displaying success or failure of order.'''
    if(order_ok()):
        send_order()
        log_order(LOG_SUCCESS)

    else:
        send_error()
        log_order(LOG_ERROR)
        flash(RETURN_ERROR)
        return redirect(url_for('error'))

    empty_cart()

    return render_template('success.html', banner = BANNER, contact=get_contact(),lines=get_lines(),message=SUCCESSFUL_ORDER)


@app.route('/shipping')
def shipping():
    '''Render shipping template to display SHIPPING and TERMS from config file.'''
    shipping = SHIPPING
    terms = TERMS
    return render_template('shipping.html', banner = BANNER, contact=get_contact(),lines=get_lines(), shipping = shipping, terms = terms)


@app.route('/ipn',methods=['GET','POST'])
def ipn():
    '''Receive and process IPN details from paypal to verify correct payment and complete order or display error.'''
    try:
        arg = ''
        request.parameter_storage_class = ImmutableOrderedMultiDict
        values = request.form
        for x, y in values.iteritems():
            arg += "&{x}={y}".format(x=x,y=y)

        validate_url = 'https://www.sandbox.paypal.com' \
                       '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
                       .format(arg=arg)
        r = requests.get(validate_url)


        if r.text == 'VERIFIED':

            try:
                payer_email =  escape(request.form.get('payer_email'))
                unix = int(time.time())
                payment_date = escape(request.form.get('payment_date'))
                username = escape(request.form.get('custom'))
                last_name = escape(request.form.get('last_name'))
                payment_gross = escape(request.form.get('payment_gross'))
                payment_fee = escape(request.form.get('payment_fee'))
                payment_net = float(payment_gross) - float(payment_fee)
                payment_status = escape(request.form.get('payment_status'))
                txn_id = escape(request.form.get('txn_id'))

                if(order_ok()):
                    send_order()
                    log_order(LOG_SUCCESS)

                else:
                    send_error()
                    log_order(LOG_ERROR)
                    flash(RETURN_ERROR)
                    return redirect(url_for('error'))

                empty_cart()


            except Exception as e:
                with open('ipnout.txt','a') as f:
                    data = 'ERROR WITH IPN DATA\n'+str(values)+'\n'
                    f.write(data)

            with open('ipnout.txt','a') as f:
                data = 'SUCCESS\n'+str(values)+'\n'
                f.write(data)

        #successful payment, send order email

        else:
             with open('/tmp/ipnout.txt','a') as f:
                data = 'FAILURE\n'+str(values)+'\n'
                f.write(data)

        return r.text
    except Exception as e:
        return str(e)


@app.route('/cart/add/<int:row_id>')
def add(row_id):
    '''Add 1 to the qty of row_id in cart list'''

    cart = get_cart()

    if cart and row_id < len(cart):
        cart[row_id]['qty'] += 1
        session['cart'] = cart
    else:
        flash(LINE_NOT_FOUND)
        return redirect(url_for('error'))

    return redirect(redirect_url())

@app.route('/cart/minus/<int:row_id>')
def minus(row_id):
    '''Remove 1 from the qnty of row_id in cart list or remove entirely'''
    cart = get_cart()

    if cart and row_id < len(cart):
        if cart[row_id]['qty'] > 0:
            cart[row_id]['qty'] -= 1
        else:
            del cart[row_id]

        session['cart'] = cart
    else:
        flash(LINE_NOT_FOUND)
        return redirect(url_for('error'))

    return redirect(redirect_url())
