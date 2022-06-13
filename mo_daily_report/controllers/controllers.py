# -*- coding: utf-8 -*-
# from odoo import http


# class MoDailyReport(http.Controller):
#     @http.route('/mo_daily_report/mo_daily_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mo_daily_report/mo_daily_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mo_daily_report.listing', {
#             'root': '/mo_daily_report/mo_daily_report',
#             'objects': http.request.env['mo_daily_report.mo_daily_report'].search([]),
#         })

#     @http.route('/mo_daily_report/mo_daily_report/objects/<model("mo_daily_report.mo_daily_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mo_daily_report.object', {
#             'object': obj
#         })
