# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DailyMoWizard(models.TransientModel):
    _name = 'daily.mo.wizard'

    date_required = fields.Date(string='Required Date', required=True, default=fields.Date.today)

    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_required': self.date_required
            },
        }
        return self.env.ref('mo_daily_report.daily_mo_report_id').report_action(self,data=data)


class MrpPriduction(models.Model):
    _inherit = 'mrp.production'

    process_date = fields.Date(string='Date',default=fields.Date.today,required=True)

    @api.onchange('date_planned_start')
    def get_date(self):
        for rec in self:
            if rec.date_planned_start:
                rec.process_date = rec.date_planned_start.date()