# -*- encoding: utf-8 -*-

from odoo import api, models, fields
import logging

class ReporteFha(models.AbstractModel):
    _name = 'report.inmobiliaria.reporte_fha'

    @api.model
    def get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids', []))

        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
