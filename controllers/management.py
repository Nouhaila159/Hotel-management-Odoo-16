from odoo import http
from odoo.http import request

class HotelReservationController(http.Controller):

    @http.route('/confirm_reservation/<int:reservation_id>', type='http', auth='public', website=True)
    def confirm_reservation(self, reservation_id, **kwargs):
        reservation = request.env['hotel.reservation'].sudo().browse(reservation_id)
        if reservation.exists() and reservation.status == 'pending':
            reservation.action_confirm_reservation()
            return request.render('gestion_hotel.confirmation_thank_you', {'reservation': reservation})
        return request.render('gestion_hotel.confirmation_error')

