from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    price = fields.Integer("Prix")
    delais = fields.Integer("Delai Livrasion")
    quality = fields.Integer("Qualité")

    production_capacity = fields.Integer("Capacité de production")
    location = fields.Integer("Localisation géographique")
    technical_capacity = fields.Integer("Capacité technique")

    management_organization = fields.Integer("Gestion et organisation")
    reputation_position = fields.Integer("Réputation et Postion dans l'industrie")
    financial_situation = fields.Integer("Situation financiére")

    assistance = fields.Integer("Assistance")
    communication_systeme = fields.Integer("Systeme de communication")
    impression = fields.Integer("Impression")

    do_business = fields.Integer("Désir de faire des affaires")
    sap = fields.Integer("Garantie et SAP")
    condition = fields.Integer("Conditionde paiement")

    total = fields.Integer("Score Total", readonly=1)
    qr_code = fields.Char("QR Code", compute="_compute_qr_code")

    @api.onchange("price", "delais", "quality", "production_capacity", "location",
                  "technical_capacity", "management_organization", "reputation_position",
                  "financial_situation", "assistance", "communication_systeme", "impression",
                  "do_business", "sap", "condition")
    def _onchange_criteria(self):
        self.total = self.price + self.delais + self.quality + self.production_capacity + self.location + self.technical_capacity + self.management_organization + self.reputation_position + self.financial_situation + self.assistance + self.communication_systeme + self.impression + self.do_business + self.sap + self.condition

    def _compute_qr_code(self):
        for rec in self:
            rec.qr_code = "Score Total de " + str(self.name) + " et " + str(self.total)

    def print_report(self):
        self.ensure_one()
        return self.env.ref('reports.action_supplier_sheet').report_action(None)
