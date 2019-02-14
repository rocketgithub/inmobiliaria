# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class account_payment(models.Model):
    _inherit = "account.payment"

    sale_id = fields.Many2one('sale.order','Venta')
    descripcion = fields.Char('Descripcion')
    fecha_boleta = fields.Date('Fecha boleta')
    cheque = fields.Char('Cheque')
    boleta = fields.Char('Boleta')
