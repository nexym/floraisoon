# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mo_daily_report(models.Model):
#     _name = 'mo_daily_report.mo_daily_report'
#     _description = 'mo_daily_report.mo_daily_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
