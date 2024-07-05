from odoo import models, fields

class HotelCustomer(models.Model):
    _name = 'hotel.customer'
    _description = 'Hotel Customer'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    document = fields.Binary(string='Document', attachment=True)

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique.'),
    ]
