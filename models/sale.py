# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import uuid

from itertools import groupby
from datetime import datetime, timedelta
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = "sale.order"

    lead_id = fields.Many2one('crm.lead','Oportunidad')
    banco_id = fields.Many2one('account.journal','Banco')
    fecha_inicio = fields.Date('Fecha de inicio')

    @api.onchange('lead_id')
    def check_change(self):
        if self.lead_id or self.lead_id.parqueo_ids:
            lineas = []
            for oportunidad in self.lead_id:
                lineas.append((0,_,{'product_id': oportunidad.inmueble_id.id,'name': oportunidad.inmueble_id.name,'product_uom':oportunidad.inmueble_id.product_tmpl_id.uom_id ,'product_uom_qty': 1,'price_unit':  oportunidad.inmueble_id.list_price}))
                if oportunidad.parqueo_ids:
                    for parqueo in oportunidad.parqueo_ids:
                        lineas.append((0,0,{'product_id': parqueo.id ,'name': parqueo.name,'product_uom':parqueo.product_tmpl_id.uom_id,'product_uom_qty': 1,'price_unit': parqueo.list_price}))
            self.update({'order_line':lineas})
