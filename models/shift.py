from odoo import models, fields, api

class HotelShift(models.Model):
    _name = 'hotel.shift'
    _description = 'Hotel Shift'

    staff_ids = fields.Many2many('hotel.staff', string='Staff', required=True)
    date = fields.Date(string='Date', required=True)
    start_time = fields.Float(string='Start Time', required=True, help="Time in hours (e.g., 14.5 for 2:30 PM)")
    end_time = fields.Float(string='End Time', required=True, help="Time in hours (e.g., 16.0 for 4:00 PM)")
    staff_count = fields.Integer(string='Number of Staff', compute='_compute_staff')

    @api.depends('staff_ids')
    def _compute_staff(self):
        for shift in self:
            shift.staff_count = len(shift.staff_ids)

