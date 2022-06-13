from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    qr_code = fields.Char("QR Code", compute="_compute_qr_code")

    @api.depends("name", "state", "partner_id")
    def _compute_qr_code(self):
        for purchase in self:
            if purchase.partner_id:
                purchase.qr_code = "name" + " " + purchase.state + " " + purchase.partner_id.name
            else:
                purchase.qr_code = "name" + " " + purchase.state
