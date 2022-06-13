from odoo import fields, models,api
import base64


class SupplierSheet(models.Model):
    _name = "supplier.sheet"
    _description = "Fiche de sélection des fournisseur"


    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
    qr_code = fields.Char("QR Code", compute="_compute_qr_code")

    def _compute_qr_code(self):
        for rec in self:
            rec.qr_code = "Fiche de sélection des fournisseur"

    def print_report(self):
        self.ensure_one()
        return self.env.ref('reports.action_supplier_sheet').report_action(None)



class ReceptionControl(models.Model):
    _name = "reception.control"
    _description = "Controle à la réception"


    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
    qr_code = fields.Char("QR Code", compute="_compute_qr_code")

    def _compute_qr_code(self):
        for rec in self:
            rec.qr_code = "Controle à la réception"

    def print_report(self):
        self.ensure_one()
        return self.env.ref('reports.action_reception_control').report_action(None)

