# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID
import logging

class Lead(models.Model):
    _inherit = "crm.lead"

    numero_parqueos = fields.Integer('Numero de parqueos')
    precio_metros_cuadrados = fields.Float('Precio mts.2')
    precio_parqueo = fields.Float('Precio parqueo')
    gastos_escrituracion = fields.Float('Gastos de escrituración')
    reserva = fields.Float('Reserva')
    #tipo_cambio = fields.Float('Tipo de cambio')
    tasa_interes_anual = fields.Float('Tasa de interés anual')
    plazo_meses = fields.Integer('Plazo meses')
    inmueble_id = fields.Many2one('product.product', string='Inmueble')
    parqueo_ids = fields.Many2many('product.product', string='Parqueo')
    total_inmueble = fields.Float('Total inmueble')
    total_parqueo = fields.Float('Total parqueo')
    iva = fields.Float('IVA')
    total = fields.Float('Total')
    gran_total = fields.Float('Gran total')
    enganche_reserva = fields.Float('Eganche reserva')
    enganche_total = fields.Float('Enganche total')
    cuota_enganche = fields.Float('Cuota enganche')
    saldo_financiar = fields.Float('Saldo a financiar')
    fecha_pactada_abonos = fields.Date('Fecha pactada de abonos')
    bodega_id = fields.Many2one('product.product', string='Bodega')
    unico_pago = fields.Float('Unico pago')

    @api.onchange('inmueble_id', 'parqueo_ids', 'gastos_escrituracion', 'reserva', 'tasa_interes_anual', 'plazo_meses')
    def onchange_total_inmueble(self):
        if self.inmueble_id:
            if self.inmueble_id.metros_cuadrados > 0:
                self.precio_metros_cuadrados = self.inmueble_id.list_price / self.inmueble_id.metros_cuadrados
            self.total_inmueble = self.inmueble_id.list_price
        if self.parqueo_ids:
            cantidad_parqueos = 0
            total_parqueo = 0
            for parqueo in self.parqueo_ids:
                cantidad_parqueos += 1
                total_parqueo += parqueo.list_price
            self.numero_parqueos = cantidad_parqueos
            self.total_parqueo = total_parqueo
        self.iva = (self.total_parqueo + self.total_inmueble) * 0.12
        self.total = self.iva + (self.total_parqueo + self.total_inmueble)
        if self.total and self.gastos_escrituracion:
            self.gran_total = self.gastos_escrituracion + self.total
        if self.reserva and self.gran_total:
            self.enganche_reserva = self.gran_total * 0.3 - self.reserva
            self.enganche_total = self.gran_total * 0.3
        if self.plazo_meses > 0:
            self.cuota_enganche = self.enganche_reserva / self.plazo_meses
        if self.gran_total and self.enganche_total:
            self.saldo_financiar = self.gran_total - self.enganche_total
