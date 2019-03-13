@app.route('/order/<int:product_id>',methods=["GET","POST"])
   def order(product_id):
       '''Render order template displaying order form and process submitted form data'''

       search_term =''
       product = None
       total = 0
       qty = 1


       line = {'type': '','label': products.product_list[product_id][0],'qty': qty,'price': products.product_list[product_id][1] * qty}
       #line = [adapter_type, products.product_list[adapter_type][0], qty,products.product_list[adapter_type][3] * qty]
       add_to_cart(line)



       return redirect(url_for('cart'))


  @app.route('/products')
  def product_list():
      '''render page with list of products'''
      return render_template('about.html', banner = BANNER, contact=get_contact(), lines = get_lines(), text = 'text')

  @app.route('/emptysearch')
  def empty_search():
      '''Empty element14 product ordering_service list'''
      total = 0
      if session.get('ordering_service'):
          total = session['ordering_service']['cost']
          session['subtotal'] = session['subtotal'] - total

      session['ordering_service'] = None

      return redirect(url_for('index'))

  def get_e14(search_term):
      '''Use element14 API to get the details of the product searched'''
      product = 0
      ns = '{http://pf.com/soa/services/v1}'
      api_call = API_BASE + API_KEY + search_term

      try:
          e = xml.etree.ElementTree.parse(urllib2.urlopen(api_call)).getroot()
      except Exception:
          return 0

      results = 0

      #if there are some results, populate the dictionary
      if e.find(ns+'numberOfResults') != None:
          results = int(e.find(ns+'numberOfResults').text )

          if results == 1:

              for product in e.findall(ns+'products'):
                  name = ''
                  e14id = 0
                  partNumber = ''
                  new = False
                  package = ''
                  totalStock = 0
                  intStock = 0
                  stock = 0
                  price = 0

                  if product.find(ns+'sku') != None:
                      e14id = int(escape(product.find(ns+'sku').text))

                  if product.find(ns+'displayName') != None:
                      name = escape(product.find(ns+'displayName').text)

                  if product.find(ns+'translatedManufacturerPartNumber') != None:
                      partNumber = escape(product.find(ns+'translatedManufacturerPartNumber').text)

                  if product.find(ns+'stock/'+ns+'level') != None:
                      totalStock = int(escape(product.find(ns+'stock/'+ns+'level').text))

                  if product.find(ns+'inventoryCode') != None:
                      if escape(product.find(ns+'inventoryCode').text) == 2:
                          new = True

              #loop through all stock locations and get the AU stock
                  for s in product.findall(ns+'stock/'+ns+'breakdown'):
                      if s.find(ns+'region').text == 'AU':
                          stock = int(escape(s.find(ns+'inv').text))

                  #loop through all price breaks and get the highest
                  for p in product.findall(ns+'prices'):
                      if p.find(ns+'from').text == '1':
                          price = float(escape(p.find(ns+'cost').text))

                  if totalStock >=0  and stock >=0:
                      intStock = totalStock - stock

      #dictionary of product details
      product = {'e14id': e14id, 'name': name,'part':partNumber,'austock':stock, 'intstock':intStock, 'cost':price}


      return product

  def display_cart():
      '''Unused'''
      lines = []

      '''
      if session.get('cart'):
          for l in session['cart']:

              try:
                  pid = int(l[0])
              except ValueError:
                  pid = None

              if l[1]:
                  qty = int(l[1])
              else:
                  qty = 1

              part_cost = 0.0

              if len(l) == 3:
                  part_cost = l[2]

              #if an adapter line
              elif pid > 0:
                  description = products.product_list[pid][0:3]
                  description = description[0]+' to ' +description[1]+' ' + str(description[2])+ ' pins'
                  price = products.product_list[pid][3]
                  lines.append((description,qty,price))

              #assembly line
              if pid == -1:
                  lines.append(("Assembly", qty,l[4])) #assembly charge

        '''
      return lines


  def get_part():
      '''Return the element14 part ID from the session'''
      part = None

      if session.get('ordering_service'):
          part = session.get('ordering_service')

      return part
