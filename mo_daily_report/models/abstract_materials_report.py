# -*- coding: utf-8 -*-

from odoo import models, api


class ReportMoDailyMaterials(models.AbstractModel):
    _name = 'report.mo_daily_report.mo_daily_template_id'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_required = data['form']['date_required']
        domain = [('process_date', '=', data['form']['date_required'])]
        mrp_orders = self.env['mrp.production'].search(domain)
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        print(mrp_orders)
        docs = []
        for order in mrp_orders:
            for line in order.move_raw_ids:
                docs.append({
                    'product_id': line.product_id.name,
                    'default_code': line.product_id.default_code,
                    'location_id': line.location_id.location_id.name + "/" + line.location_id.name,
                    'product_uom_qty': line.product_uom_qty
                })
        print(docs)
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs': docs,
            'date_required': date_required
        }
