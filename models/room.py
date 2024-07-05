from odoo import models, fields, api
from datetime import date

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char(string='Room Name', required=True)
    room_type = fields.Selection([('single', 'Single'), ('double', 'Double'), ('suite', 'Suite')], string='Room Type', required=True)
    price = fields.Float(string='Price', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    status = fields.Selection([('available', 'Available'), ('booked', 'Booked')], string='Status', required=True, default='available')
    image = fields.Image("Room Image")

    _sql_constraints = [
        ('check_capacity', 'CHECK(capacity >= 1)', 'The capacity must be at least 1.')
    ]

    @api.model
    def update_room_status(self):
        today = fields.Date.today()
        rooms = self.search([])
        for room in rooms:
            reservations = self.env['hotel.reservation'].search([
                ('room_id', '=', room.id),
                ('status', '=', 'confirmed'),
                ('check_in_date', '<=', today),
                ('check_out_date', '>=', today),
                ('status', '!=', 'canceled')  # Exclude canceled reservations
            ])
            if reservations:
                room.status = 'booked'
            else:
                room.status = 'available'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        self.update_room_status()
        return super(HotelRoom, self).search_read(domain, fields, offset, limit, order)
