from odoo import models, fields

class HotelStaff(models.Model):
    _name = 'hotel.staff'
    _description = 'Hotel Staff'

    name = fields.Char(string='Name', required=True)
    role = fields.Selection([
        ('receptionist', 'Receptionist'),
        ('housekeeper', 'Housekeeper'),
        ('manager', 'Manager'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter')
    ], string='Role', required=True)
    hire_date = fields.Date(string='Hire Date', required=True)
    contact_info = fields.Char(string='Contact Info')
    salary = fields.Float(string='Salary')
    shift_ids = fields.Many2many('hotel.shift', string='Shifts')
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active')
