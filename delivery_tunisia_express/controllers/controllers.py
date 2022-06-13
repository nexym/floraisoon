# -*- coding: utf-8 -*-
# from odoo import http


# class DeliveryTunisiaExpress(http.Controller):
#     @http.route('/delivery_tunisia_express/delivery_tunisia_express', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_tunisia_express/delivery_tunisia_express/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_tunisia_express.listing', {
#             'root': '/delivery_tunisia_express/delivery_tunisia_express',
#             'objects': http.request.env['delivery_tunisia_express.delivery_tunisia_express'].search([]),
#         })

#     @http.route('/delivery_tunisia_express/delivery_tunisia_express/objects/<model("delivery_tunisia_express.delivery_tunisia_express"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_tunisia_express.object', {
#             'object': obj
#         })
