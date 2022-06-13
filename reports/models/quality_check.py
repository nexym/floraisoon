from odoo import api, fields, models, _


class QualityCheck(models.Model):
    _inherit = "quality.check"

    date = fields.Date(default=lambda self: fields.Date.today(), string='Date')
    partner_id = fields.Many2one(related='picking_id.partner_id', string="Fournisseur")
    receipt_id = fields.Char(related='picking_id.name', string="Fich de réception N°")
    purchase_id = fields.Char(related='picking_id.purchase_id.name', string="Bon de commande N°")
    concordance = fields.Char(string="Concordance")
    condition = fields.Char(string="Condition de transport")
    comments = fields.Char(string="Commentaires")
    cleanliness = fields.Char(string="Propreté")
    machine_protection = fields.Char(string="Protection de l'engin")
    unwanted_elements = fields.Char(string="Présence d'éléments indiserables")
    driver_name = fields.Char(string="Nom du chauffeur")
    driver_behavior = fields.Char(string="Comportement du chauffeur")
    total = fields.Char(string="Total")
    product_id = fields.Many2one(
        string="Article",
        comodel_name="product.product",
        ondelete="cascade",
        required=True,
    )
    setting = fields.Text("Paramétres à contoler")
    etiquetage = fields.Char("Etiquetage")
    emballage = fields.Char("Intégrité de l'emballage")
    cleanliness2 = fields.Char("Propreté")
    ddm = fields.Char("DDM ( 3 mois après fabrication)")
    odeur = fields.Char("Odeur")
    color = fields.Char("Couleur")
    apparence = fields.Char("Apparence")
    texture = fields.Char("Texture")
    quality = fields.Char("Qualité de l'impression de l'étiquetage")
    total2 = fields.Char("Total par article")
