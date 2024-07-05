from odoo import models, fields, api

class HotelDashboard(models.TransientModel):
    _name = 'hotel.dashboard'
    _description = 'Hotel Dashboard'

    date = fields.Date(string='Date', default=fields.Date.today(), required=True)
    single_rooms = fields.Html(string='Single Rooms', compute='_compute_room_availability')
    double_rooms = fields.Html(string='Double Rooms', compute='_compute_room_availability')
    suite_rooms = fields.Html(string='Suite Rooms', compute='_compute_room_availability')

    @api.depends('date')
    def _compute_room_availability(self):
        for dashboard in self:
            single_rooms_html = '<div style="display: flex; flex-wrap: wrap;">'
            double_rooms_html = '<div style="display: flex; flex-wrap: wrap;">'
            suite_rooms_html = '<div style="display: flex; flex-wrap: wrap;">'

            single_rooms = self.env['hotel.room'].search([('room_type', '=', 'single')])
            double_rooms = self.env['hotel.room'].search([('room_type', '=', 'double')])
            suite_rooms = self.env['hotel.room'].search([('room_type', '=', 'suite')])

            for room in single_rooms:
                status = self._get_room_availability(room, dashboard.date)
                color = '#A1DD70' if status == 'available' else '#DD5746'  # Adjusted shades of green and red
                single_rooms_html += f'<div style="width: 100px; height: 100px; margin: 10px; background-color: {color}; text-align: center; display: flex; align-items: center; justify-content: center;"><span style="font-weight: bold; color: white;">{room.name}</span></div>'

            for room in double_rooms:
                status = self._get_room_availability(room, dashboard.date)
                color = '#A1DD70' if status == 'available' else '#DD5746'  # Adjusted shades of green and red
                double_rooms_html += f'<div style="width: 100px; height: 100px; margin: 10px; background-color: {color}; text-align: center; display: flex; align-items: center; justify-content: center;"><span style="font-weight: bold; color: white;">{room.name}</span></div>'

            for room in suite_rooms:
                status = self._get_room_availability(room, dashboard.date)
                color = '#A1DD70' if status == 'available' else '#DD5746'
                suite_rooms_html += f'<div style="width: 100px; height: 100px; margin: 10px; background-color: {color}; text-align: center; display: flex; align-items: center; justify-content: center;"><span style="font-weight: bold; color: white;">{room.name}</span></div>'

            single_rooms_html += '</div>'
            double_rooms_html += '</div>'
            suite_rooms_html += '</div>'

            dashboard.single_rooms = single_rooms_html
            dashboard.double_rooms = double_rooms_html
            dashboard.suite_rooms = suite_rooms_html

    def _get_room_availability(self, room, date):
        today = fields.Date.today()
        reservations = self.env['hotel.reservation'].search([
            ('room_id', '=', room.id),
            ('status', '=', 'confirmed'),
            '|',
            '&', ('check_in_date', '<=', date), ('check_out_date', '>=', date),
            '&', ('check_in_date', '<=', today), ('check_out_date', '>=', today),
            ('archived', '=', False)
        ])
        if reservations:
            return 'booked'
        else:
            return 'available'

