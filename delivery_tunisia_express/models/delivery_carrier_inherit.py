from odoo import fields, models, api


class ChooseDeliveryCarrierInherit(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    display_price = fields.Float(string='Cost')
