from odoo import models, fields

class HotelService(models.Model):
    _name = 'hotel.service'
    _description = 'Hotel Service'

    name = fields.Char(string='Service Name', required=True)
    price = fields.Float(string='Price', required=True)
    included_in_reservation = fields.Boolean(string='Included in Reservation', default=False)
    category = fields.Selection([
        ('room', 'Room Service'),
        ('restaurant', 'Restaurant Service'),
        ('spa', 'Spa Service'),
        ('other', 'Other Service')
    ], string='Category', required=True)
    availability = fields.Selection([
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ], string='Availability', required=True, default='available')
