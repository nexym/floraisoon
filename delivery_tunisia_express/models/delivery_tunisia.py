# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from base64 import b64encode

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from .tunisia_request import TunisiaRequest

TRACKING_REF_DELIM = ', '

class ProviderTunisia(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[
        ('tunisia', 'tunisia')
    ], ondelete={'tunisia': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})})
    # Fields required to configure
    tunisia_account_number = fields.Char(string="Tunisia Account Number", groups="base.group_system")
    tunisia_developer_password = fields.Char(string="Passphrase", groups="base.group_system")
    tunisia_delivery_nature = fields.Selection([('Domestic', 'Domestic'), ('International', 'International')],
                                             default='Domestic', required=True)
    tunisia_domestic_deliver_type = fields.Selection([('tunisia 24h Pro', 'Tunisia 24h Pro'),
                                                   ('tunisia 24h business', 'Tunisia 24h business'),
                                                   ('Tunisia Bus', 'Tunisia Bus')], default='tunisia 24h Pro')
    tunisia_international_deliver_type = fields.Selection([('tunisia World Express Pro', 'tunisia World Express Pro'),
                                                         ('tunisia World Business', 'tunisia World Business'),
                                                         ('tunisia Europe Business', 'tunisia Europe Business')], default='tunisia World Express Pro')
    tunisia_label_stock_type = fields.Selection([('A4', 'A4'), ('A6', 'A6')], default='A6')
    tunisia_label_format = fields.Selection([('PDF', 'PDF'), ('PNG', 'PNG')], default='PDF')
    tunisia_shipment_type = fields.Selection([('SAMPLE', 'SAMPLE'),
                                            ('GIFT', 'GIFT'),
                                            ('GOODS', 'GOODS'),
                                            ('DOCUMENTS', 'DOCUMENTS'),
                                            ('OTHER', 'OTHER')], default='SAMPLE')
    tunisia_parcel_return_instructions = fields.Selection([('ABANDONED', 'Destroy'),
                                                         ('RTA', 'Return to sender by air'),
                                                         ('RTS', 'Return to sender by road')])
    tunisia_saturday = fields.Boolean(string="Delivery on Saturday", help="Allow deliveries on Saturday (extra charges apply)")
    tunisia_default_package_type_id = fields.Many2one('stock.package.type', string='tunisia Default Package Type')

    user_name = fields.Char(string="Login Tunisia")
    destinataire = fields.Char(string="Name of Receiver")

    @api.depends('tunisia_delivery_nature')
    def _compute_can_generate_return(self):
        super(ProviderTunisia, self)._compute_can_generate_return()
        for carrier in self:
            if carrier.delivery_type == 'tunisia':
                if carrier.tunisia_delivery_nature == 'International':
                    carrier.can_generate_return = False
                else:
                    carrier.can_generate_return = True

    def tunisia_rate_shipment(self, order):
        tunisia = TunisiaRequest(self.prod_environment, self.log_xml)
        check_value = tunisia.check_required_value(order.partner_shipping_id, self.tunisia_delivery_nature, order.warehouse_id.partner_id, order=order)
        if check_value:
            return {'success': False,
                    'price': 0.0,
                    'error_message': check_value,
                    'warning_message': False}
        try:
            price = tunisia.rate(order, self)
        except UserError as e:
            return {'success': False,
                    'price': 0.0,
                    'error_message': e.args[0],
                    'warning_message': False}
        if order.currency_id.name != 'EUR':
            quote_currency = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)
            price = quote_currency._convert(price, order.currency_id, order.company_id, order.date_order or fields.Date.today())
        return {'success': True,
                'price': price,
                'error_message': False,
                'warning_message': False}

    def tunisia_send_shipping(self, pickings):
        res = []
        tunisia = TunisiaRequest(self.prod_environment, self.log_xml)
        for picking in pickings:
            check_value = tunisia.check_required_value(picking.partner_id, picking.carrier_id.tunisia_delivery_nature, picking.picking_type_id.warehouse_id.partner_id, picking=picking)
            if check_value:
                raise UserError(check_value)
            shipping = tunisia.send_shipping(picking, self, self.return_label_on_delivery)
            order = picking.sale_id
            company = order.company_id or picking.company_id or self.env.company
            order_currency = picking.sale_id.currency_id or picking.company_id.currency_id
            if order_currency.name == "EUR":
                carrier_price = shipping['price']
            else:
                quote_currency = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)
                carrier_price = quote_currency._convert(shipping['price'], order_currency, company, order.date_order or fields.Date.today())
            carrier_tracking_ref = TRACKING_REF_DELIM.join(shipping['main_label']['tracking_codes'])
            tracking_links = '<br/>'.join(self._tracking_link_element(code) for code in shipping['main_label']['tracking_codes'])
            logmessage = (_("Shipment created into tunisia <br/> <b>Tracking Links</b> <br/>%s") % (tracking_links))
            tunisia_labels = [('Labels-tunisia.%s' % self.tunisia_label_format, shipping['main_label']['label'])]
            if picking.sale_id:
                for pick in picking.sale_id.picking_ids:
                    pick.message_post(body=logmessage, attachments=tunisia_labels)
            else:
                picking.message_post(body=logmessage, attachments=tunisia_labels)

            if shipping['return_label']:
                carrier_return_label_ref = TRACKING_REF_DELIM.join(shipping['return_label']['tracking_codes'])
                logmessage = (_("Return labels created into tunisia <br/> <b>Tracking Numbers: </b><br/>%s") % (carrier_return_label_ref))
                picking.message_post(body=logmessage, attachments=[('%s-%s.%s' % (self.get_return_label_prefix(), 1, self.tunisia_label_format), shipping['return_label']['label'])])

            shipping_data = {'exact_price': carrier_price,
                             'tracking_number': carrier_tracking_ref}
            res = res + [shipping_data]
        return res

    def _tracking_link_element(self, tracking_code):
        return f'<a href="{self._generate_tracking_link(tracking_code)}" target="_blank" rel="noopener noreferrer">{tracking_code}</a>'

    def _generate_tracking_link(self, tracking_code):
        return f"http://track.bpost.be/btr/web/#/search?itemCode={tracking_code}&lang=en"

    def tunisia_get_tracking_link(self, picking):
        # Using similar trick done in easypost, which is supported in the main delivery module.
        # This looks simpler than in easypost because we don't need to make a request to the api,
        # we just use the tracking numbers saved in picking.carrier_tracking_ref to generate
        # the links.
        tracking_urls = []
        for tracking_code in picking.carrier_tracking_ref.split(TRACKING_REF_DELIM):
            tracking_code = tracking_code.strip()
            tracking_urls.append([tracking_code, self._generate_tracking_link(tracking_code)])
        return tracking_urls[0][1] if len(tracking_urls) == 1 else json.dumps(tracking_urls)

    def tunisia_cancel_shipment(self, picking):
        picking.message_post(body=_(u'Shipment #%s has been cancelled', picking.carrier_tracking_ref))
        picking.write({'carrier_tracking_ref': '',
                       'carrier_price': 0.0})

    def _tunisia_passphrase(self):
        self.ensure_one()
        if self.delivery_type != 'tunisia':
            raise UserError(_("You cannot compute a passphrase for non-tunisia carriers."))
        return b64encode(("%s:%s" % (self.tunisia_account_number, self.tunisia_developer_password)).encode()).decode()

    def _tunisia_convert_weight(self, weight):
        weight_uom_id = self.env['product.template']._get_weight_uom_id_from_ir_config_parameter()
        return weight_uom_id._compute_quantity(weight, self.env.ref('uom.product_uom_kgm'), round=False)

    @api.model
    def tunisia_get_return_label(self, pickings, tracking_number=None, origin_date=None):
        tunisia = TunisiaRequest(self.prod_environment, self.log_xml)
        check_value = tunisia.check_required_value(pickings.partner_id, pickings.carrier_id.tunisia_delivery_nature, pickings.picking_type_id.warehouse_id.partner_id, picking=pickings)
        if check_value:
            raise UserError(check_value)
        shipping = tunisia.send_shipping(pickings, self, False, is_return_label=True)
        order = pickings.sale_id
        company = order.company_id or pickings.company_id or self.env.company
        order_currency = pickings.sale_id.currency_id or pickings.company_id.currency_id
        if order_currency.name == "EUR":
            carrier_price = shipping['price']
        else:
            quote_currency = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)
            carrier_price = quote_currency._convert(shipping['price'], order_currency, company, order.date_order or fields.Date.today())
        carrier_tracking_ref = shipping['main_label']['tracking_codes']
        # bpost does not seem to handle multipackage
        logmessage = (_("Return shipment created into tunisia <br/> <b>Tracking Number : </b>%s") % (carrier_tracking_ref[0]))
        pickings.message_post(body=logmessage, attachments=[('%s-%s-%s.%s' % (self.get_return_label_prefix(), carrier_tracking_ref[0], 1, self.tunisia_label_format), shipping['main_label']['label'])])
