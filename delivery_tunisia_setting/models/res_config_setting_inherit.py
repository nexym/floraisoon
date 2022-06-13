from odoo import fields, models, api


class ModelName(models.TransientModel):
    _inherit = 'res.config.settings'

    module_delivery_tunisia_express = fields.Boolean("Tunisia Express Connector")
