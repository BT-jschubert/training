from odoo.tests import common

class My_test(common.TransactionCase):
    def setUp(self):
        return super(My_test, self).setUp()

    def test_seats_updated(self):
        sessions_table = self.env['session']
        initial_seats = sessions_table[0].num_seats
        print(initial_seats)

        partner_table = self.env['res.partner']

        sessions_table[0].attendees |= partner_table[60]

        current_seats = sessions_table[0].num_seats
        print(current_seats)

        self.assertNotEqual(initial_seats, current_seats)