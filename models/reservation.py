from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError
import random
import string
from datetime import datetime

class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _description = 'Hotel Reservation'

    room_id = fields.Many2one('hotel.room', string='Room', required=True)
    customer_id = fields.Many2one('hotel.customer', string='Customer', required=True)
    check_in_date = fields.Date(string='Check-In Date', required=True)
    check_out_date = fields.Date(string='Check-Out Date', required=True)
    adults = fields.Integer(string='Adults', default=1)
    children = fields.Integer(string='Children', default=0)
    service_ids = fields.Many2many('hotel.service', string='Services')
    status = fields.Selection([('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], string='Status', default='pending')
    reservation_code = fields.Char(string='Reservation Code', default=lambda self: self._generate_reservation_code(), readonly=True, required=True)
    reservation_type = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline')
    ], string='Reservation Type', required=True, default='offline')
    archived = fields.Boolean(string='Archived', default=False)
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    total_service_cost = fields.Float(string='Total Service Cost', compute='_compute_total_service_cost', store=True)

    @api.model
    def _generate_reservation_code(self):
        """Generates a unique reservation code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    @api.depends('service_ids')
    def _compute_total_service_cost(self):
        for reservation in self:
            total = sum(service.price for service in reservation.service_ids if not service.included_in_reservation)
            reservation.total_service_cost = total

    @api.depends('room_id', 'check_in_date', 'check_out_date', 'adults', 'children', 'total_service_cost')
    def _compute_total_cost(self):
        for reservation in self:
            if reservation.room_id and reservation.check_in_date and reservation.check_out_date:
                duration = (reservation.check_out_date - reservation.check_in_date).days
                room_cost = duration * reservation.room_id.price
                service_cost = reservation.total_service_cost
                total_cost = room_cost + service_cost
                reservation.total_cost = total_cost

    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for reservation in self:
            if reservation.check_in_date and reservation.check_out_date and reservation.check_out_date <= reservation.check_in_date:
                raise ValidationError("Check-out date must be after check-in date.")

    @api.constrains('adults', 'children', 'room_id')
    def _check_room_capacity(self):
        for reservation in self:
            if reservation.room_id:
                total_people = reservation.adults + reservation.children
                if total_people > reservation.room_id.capacity:
                    raise ValidationError("The total number of people exceeds the room capacity.")

    @api.onchange('check_in_date', 'check_out_date')
    def _onchange_dates(self):
        available_rooms = self._get_available_rooms()
        return {'domain': {'room_id': [('id', 'in', available_rooms.ids)]}}

    def _get_available_rooms(self):
        if self.check_in_date and self.check_out_date:
            query = """
                SELECT id FROM hotel_room WHERE id NOT IN (
                    SELECT room_id FROM hotel_reservation WHERE status = 'confirmed' AND (
                        (check_in_date <= %s AND check_out_date >= %s) OR
                        (check_in_date <= %s AND check_out_date >= %s)
                    )
                )
            """
            self.env.cr.execute(query, (self.check_out_date, self.check_in_date, self.check_in_date, self.check_out_date))
            room_ids = [row[0] for row in self.env.cr.fetchall()]
            return self.env['hotel.room'].browse(room_ids)
        return self.env['hotel.room']

    @api.model
    def create(self, values):
        reservation = super(HotelReservation, self).create(values)
        self._check_and_update_archived_status([reservation])
        self.env['hotel.room'].update_room_status()
        return reservation

    def write(self, values):
        result = super(HotelReservation, self).write(values)
        self._check_and_update_archived_status(self)
        self.env['hotel.room'].update_room_status()
        return result

    @api.model
    def _check_and_update_archived_status(self, reservations):
        today = fields.Date.today()
        for reservation in reservations:
            if reservation.status == 'canceled' or (reservation.check_out_date and reservation.check_out_date < today):
                if not reservation.archived:
                    reservation.write({'archived': True})
            else:
                if reservation.archived:
                    reservation.write({'archived': False})

    def send_confirmation_email(self):
        template = self.env.ref('gestion_hotel.email_template_hotel_reservation_confirmation')
        template.send_mail(self.id, force_send=True)

    def action_confirm_reservation(self):
        self.write({'status': 'confirmed'})
        self.room_id.update_room_status()

    def action_archive_reservation(self):
        self.write({'archived': True})

    def action_unarchive_reservation(self):
        self.write({'archived': False})
