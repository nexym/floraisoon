from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    qr_code = fields.Char("QR Code", compute="_compute_qr_code")

    @api.depends("name", "state", "partner_id")
    def _compute_qr_code(self):
        for sale in self:
            if sale.partner_id:
                sale.qr_code = "name" + " " + sale.state + " " + sale.partner_id.name
            else:
                sale.qr_code = "name" + " " + sale.state
