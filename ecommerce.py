from Application import db


class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String(80))
  s_name = db.Column(db.String(80))
  email = db.Column(db.String(120), unique=True)
  created_at = db.Column(db.Date)

  def __init__(self, f_name, s_name, email, created_at):
    self.f_name = f_name
    self.s_name = s_name
    self.email = email
    self.created_at = created_at


class ShipAddr(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String)
  s_name = db.Column(db.String)
  line_one = db.Column(db.String)
  line_two = db.Column(db.String)
  city = db.Column(db.String)
  state = db.Column(db.String)
  zip_code = db.Column(db.String)
  uid = db.Column(db.Integer, db.ForeignKey('customer.id'))
  customer = db.relationship('Customer', backref=db.backref('addr_ship', lazy='dynamic'))

  def __init__(self, f_name, s_name, line_one, line_two, city, state, zip_code, customer):
    self.f_name = f_name
    self.s_name = s_name
    self.line_one = line_one
    self.line_two = line_two
    self.city = city
    self.state = state
    self.zip_code = zip_code
    self.customer = customer


class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120))
  desc = db.Column(db.Text)
  price = db.Column(db.Integer)
  length = db.Column(db.Float)
  height = db.Column(db.Float)
  depth = db.Column(db.Float)

  def __init__(self, title, desc, price, width, height, depth):
    self.title = title
    self.desc = desc
    self.price = price
    self.width = width
    self.height = height
    self.depth = depth


class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nonce = db.Column(db.String)
  status = db.Column(db.String(48))
  date = db.Column(db.Date)
  discount_rate = db.Column(db.Integer)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
  customer = db.relationship('Customer', backref=('orders'))
  ship_addr_id = db.Column(db.Integer, db.ForeignKey('ship_addr.id'))
  ship_addr = db.relationship('ShipAddr')

  order_statuses = [
      'incomplete'
    , 'invalid'
    , 'unfulfilled'
    , 'fulfilled'
    ]

  def __init__(self, nonce, status, date, customer, ship_addr, discount_rate=0):
    self.nonce = nonce
    self.status = status
    self.date = date
    self.customer = customer
    self.ship_addr = ship_addr
    self.discount_rate = discount_rate

  @property 
  def subtotal(self):
    from functools import reduce
    lines_total = reduce(lambda l1, l2: l1.total + l2.total, self.lines)
    discount_multiplier = (100 - self.discount_rate) / 100
    new_price = lines_total * discount_multiplier
    return int(new_price)

  @property
  def total(self):
    tax_multiplier = (100 + self.tax_rate) / 100
    new_price = self.subtotal * tax_multiplier
    return int(new_price)



class Line(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  quantity = db.Column(db.Integer)
  order_id = db.Column(db.ForeignKey('order.id'))
  order = db.relationship('Order', backref='lines')
  product_id = db.Column(db.ForeignKey(Product.id))
  product = db.relationship('Product', backref='lines')
  tax_rate = db.Column(db.Integer)
  discount_rate = db.Column(db.Integer)

  @property
  def subtotal(self):
    discount_multiplier = (100 - self.discount_rate) / 100
    new_price = self.product.price * discount_multiplier
    return int(new_price)

  @property
  def total(self):
    tax_multiplier = (100 + self.tax_rate) / 100
    new_price = self.subtotal * tax_multiplier
    return int(new_price)

  def __init__(self, quantity, order, product, tax_rate, discount_rate=0):
    self.quantity = quantity
    self.order = order
    self.product = product
    self.tax_rate = tax_rate
    self.discount_rate = discount_rate
