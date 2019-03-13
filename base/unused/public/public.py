from flask import Flask, render_template, url_for, session, redirect, request,flash
from werkzeug.datastructures import ImmutableOrderedMultiDict
#Sfrom MySQLdb import escape_string as escape
from datetime import datetime
import xml.etree.ElementTree
from urllib.request import urlopen
import requests
from .public_forms import AddressForm, ContactForm, CreateForm, ShippingForm
import time
from flask_mail import Mail, Message
import products
import logging
from ..utils import *
from ..tools import mail
from sm import app,c



@app.route('/')
def index():
     '''Render index template with banner, cart and contact details.'''

     return render_template('index.html',  lines = get_lines())

'''
Creator form display and submission.
'''
@app.route('/create',methods=["GET","POST"])
def create():
    '''Render collarcreator form and deal with form data'''
    createForm = CreateForm(csrf_enabled=False)
    text = ''

    default_collar()

    if createForm.is_submitted():

        collar_colour=session['collarcolour']
        text_colour = session['textcolour']
        image=session['icon']

        hardware = session['hardware']
        buckle = session['buckle']

        text = createForm.text.data
        width=createForm.width.data
        matching_leash = createForm.matching_leash.data
        neck = createForm.neck.data
        qty = 1

        custom =  {'text': text,'collar_colour': collar_colour,'text_colour': text_colour,
                                'image': image,'width': width,'neck': neck,
                                'hardware': hardware, 'buckle': buckle, 'matching_leash': matching_leash}

        if(not session.get('shipping')):
            add_shipping(products.default_shipping)

        price = get_price(custom)

        line = {'label': products.product_list[1][0], 'custom': custom, 'qty': qty,'price': price * qty}

        add_to_cart(line)

        return redirect(url_for('cart'))



    return render_template('collar_creator.html', lines = get_lines(), create = createForm, collardata = get_collars(), text = text, products=products,\
                        collarcolour=session['collarcolour'],\
                        icon = session['icon'],\
                        textcolour = session['textcolour'],\
                        ctext = session['text'],\
                        hardware = session['hardware'],\
                        buckle = session['buckle'])

@app.route('/info')
def info():
    '''Render info template'''
    return render_template('info.html', lines = get_lines(), text = 'text')

@app.route('/about')
def about():
    '''Render index template with banner, cart contact details and ABOUT text.'''

    text = ABOUT
    return render_template('about.html', lines = get_lines(), text = text)


@app.route('/contact', methods=["GET","POST"])
def contact():
    '''Render contact template with contact form and process submitted form data.'''
    contactForm = ContactForm(csrf_enabled=False)

    #if contact form submitted
    if contactForm.send.data:
        #Clean and verify input
        if contactForm.validate() == False:
            return render_template('contact.html', contactForm = contactForm,lines = get_lines())
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

            if not mail.send_email("Contact "+name,sender,[c['admin']],message,''):
                flash(c["messages"]['successful_contact'])
                return redirect(url_for('message'))
            else:
                flash(c["messages"]["contact_error"])
                return redirect(url_for('error'))

    return render_template('contact.html', contactForm = contactForm, lines = get_lines(), referrer = request.referrer)


@app.route('/cart', methods=["GET","POST"])
def cart():
    '''Render cart template to display shopping cart.'''
    cart = get_cart()
    total = get_total()
    shippingForm = ShippingForm(csrf_enabled=False)



    #If cart is empty, redirect to contact
    if not cart:
        flash(c['messages']['empty_cart'])
        return redirect(url_for('error'))

    if shippingForm.is_submitted():
        add_shipping(shippingForm.shipping.data)
        add_voucher(shippingForm.voucher.data)

        total = get_total()


    return render_template('cart.html',
                lines = get_lines(),\
                cart = cart,\
                total = get_total(),\
                gross = get_gross_total(),\
                shipping = get_shipping(),\
                voucher= get_voucher(),\
                discount = get_discount(),\
                shippingForm = shippingForm)

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
        flash(c["messages"]["line_not_found"])
        return redirect(url_for('error'))

    return redirect(redirect_url())


@app.route('/checkout', methods=["GET","POST"])
def checkout():
    '''Render checkout template and display cart and address forms.  Deal with submitted data.'''
    addressForm = AddressForm(csrf_enabled=False)
    shippingForm = ShippingForm(csrf_enabled=False)

    if(session.get('shipping')):
        shippingForm.update_shipping(session['shipping'])

    cart = get_cart()
    if not cart:
        flash(c['messages']['empty_cart'])
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
        newsletter = addressForm.newsletter.data

        session['address'] =  {'name': firstname,'surname': surname,'company': company,
                                'address1': address1,'address2': address2,'suburb': suburb,
                                'state': state,'postcode': postcode,'country':country,
                                'phone':phone,'email': email, 'newsletter': newsletter }

        if addressForm.validate() == False:
            logging.error(addressForm.errors)
            return render_template('cart.html',\
                lines = get_lines(),\
                cart = cart,\
                total = get_total(),\
                gross = get_gross_total(),\
                shipping = get_shipping(),\
                voucher= get_voucher(),\
                discount = get_discount(),\
                addressdata=get_address(),\
                shippingForm = shippingForm)
        else:

            return redirect(url_for('pay'))


    return render_template('cart.html',\
        lines = get_lines(),\
        cart = cart,\
        total = get_total(),\
        gross = get_gross_total(),\
        shipping = get_shipping(),\
        voucher= get_voucher(),\
        discount = get_discount(),\
        address = addressForm,\
        addressdata=get_address(),\
        shippingForm = shippingForm)

@app.route('/pay')
def pay():
    '''Render pay template displaying cart and payment buttons.'''
    address = ''
    if order_ok():
        cart = get_cart()
        total = get_total()
        gross = get_gross_total()
        discount = get_discount()
        address = get_address()
        shippingForm = ShippingForm(csrf_enabled=False)
        log_order()
    else:
        flash(c["messages"]["order_error"])
        return redirect(url_for('error'))

    return render_template('pay.html', c = c,\
            lines = get_lines(),\
            address = address,\
            cart = cart,\
            total = total,\
            gross = gross,\
            discount = discount,\
            shipping=get_shipping(),\
            shippingForm = shippingForm)

@app.route('/error')
def error():
    '''Render error template displaing flashed() message.'''

    return render_template('error.html', lines = get_lines())

@app.route('/message')
def message():
    '''Render error template displaing flashed() message.'''

    return render_template('success.html', lines = get_lines(),message='')

@app.route('/success')
def success():
    '''Render success template displaying success or failure of order.'''
    if(order_ok()):
        send_order()
        save_order()
        log_order(c["messages"]["log_success"])

    else:
        send_error()
        log_order(c["messages"]["log_error"])
        flash(c["messages"]["return_error"])
        return redirect(url_for('error'))

    empty_cart()

    return render_template('success.html', lines=get_lines(),message=c["messages"]["successful_order"])


@app.route('/shipping')
def shipping():
    '''Render shipping template to display SHIPPING and TERMS from config file.'''
    shipping = c["messages"]["shipping"]
    terms = c["messages"]["terms"]
    return render_template('shipping.html', lines=get_lines(), shipping = shipping, terms = terms)


@app.route('/ipn',methods=['GET','POST'])
def ipn():
    '''Receive and process IPN details from paypal to verify correct payment and complete order or display error.'''
    try:
        arg = ''
        request.parameter_storage_class = ImmutableOrderedMultiDict
        values = request.form
        for x, y in values.items():
            arg += "&{x}={y}".format(x=x,y=y)

        validate_url = 'https://www.paypal.com' \
                       '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
                       .format(arg=arg)
        r = requests.get(validate_url)

        logging.debug(r.text)

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
                    log_order(c["messages"]["log_success"]+" " +payer_email)
                    return redirect(url_for('success'))

                else:
                    send_error()
                    log_order(c["messages"]["log_error"])
                    flash(c["messages"]["return_error"])
                    return redirect(url_for('error'))

                #['messages']['empty_cart']()


            except Exception as e:
                with open('ipnout.txt','a') as f:
                    data = 'ERROR WITH IPN DATA\n'+str(values)+'\n'
                    data += str(e)+'\n'
                    f.write(data)

            with open('ipnout.txt','a') as f:
                data = 'SUCCESS\n'+str(values)+'\n'
                f.write(data)

        #invalid response from paypal payment, send error email

        else:
            with open('ipnout.txt','a') as f:
                data = 'FAILURE\n'+str(values)+'\n'
                f.write(data)
            send_error()
            log_order(c["messages"]["log_error"])
            flash(c["messages"]["return_error"])

            return redirect(url_for('error'))

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
        flash(c["messages"]["line_not_found"])
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
        flash(c["messages"]["line_not_found"])
        return redirect(url_for('error'))

    return redirect(redirect_url())


@app.route('/ipn2',methods=['GET','POST'])
def ipn_sandbox():
    '''Receive and process IPN details from paypal to verify correct payment and complete order or display error.'''
    try:
        arg = ''
        request.parameter_storage_class = ImmutableOrderedMultiDict
        values = request.form
        for x, y in values.items():
            arg += "&{x}={y}".format(x=x,y=y)

        validate_url = 'https://ipnpb.sandbox.paypal.com' \
                       '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
                       .format(arg=arg)
        r = requests.get(validate_url)

        logging.debug(r.text)

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
                    log_order(c["messages"]["log_success"]+" " +payer_email)
                    return redirect(url_for('success'))

                else:
                    send_error()
                    log_order(c["messages"]["log_error"])
                    flash(c["messages"]["return_error"])
                    return redirect(url_for('error'))

                #['messages']['empty_cart']()


            except Exception as e:
                with open('ipnout.txt','a') as f:
                    data = 'ERROR WITH IPN DATA\n'+str(values)+'\n'
                    data += str(e)+'\n'
                    f.write(data)

            with open('ipnout.txt','a') as f:
                data = 'SUCCESS\n'+str(values)+'\n'
                f.write(data)

        #invalid response from paypal payment, send error email

        else:
            with open('ipnout.txt','a') as f:
                data = 'FAILURE\n'+str(values)+'\n'
                f.write(data)
            send_error()
            log_order(c["messages"]["log_error"])
            flash(c["messages"]["return_error"])

            return redirect(url_for('error'))

        return r.text
    except Exception as e:
        return str(e)
