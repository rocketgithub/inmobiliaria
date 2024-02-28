# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID
import logging

class Lead(models.Model):
    _inherit = "crm.lead"

    parqueo_ids = fields.Many2many('product.product', string='Parqueo')
    numero_parqueos = fields.Integer('Numero de parqueos')
    total_parqueo = fields.Float('Total parqueo')

    inmueble_id = fields.Many2one('product.product', string='Inmueble')
    precio_por_metro_cuadrado = fields.Float('Precio mts.2') # precio_metros_cuadrados
    gastos_escrituracion = fields.Float('Gastos de escrituración')
    tasa_interes_anual = fields.Float('Tasa de interés anual')
    total_inmueble = fields.Float('Total inmueble')
    iva = fields.Float('IVA')
    total = fields.Float('Total mas impuestos')
    gran_total = fields.Float('Total mas escrituración')
    saldo_financiar = fields.Float('Saldo a financiar')
    unico_pago = fields.Float('Único pago')

    # Datos para la reserva
    reserva_total = fields.Float('Reserva') # reserva
    cuota_reserva = fields.Float('Cuota reserva') # es nuevo, pendiente calcular
    cantidad_cuotas_reserva = fields.Integer('Plazo meses pagar reserva') # es nuevo
    enganche_menos_reserva = fields.Float('Enganche sin reserva') # enganche_reserva

    # Datos para el enganche
    enganche_total = fields.Float('Enganche total')
    cuota_enganche = fields.Float('Cuota enganche')
    cantidad_cuotas_enganche = fields.Integer('Plazo meses pagar enganche') # plazo_meses

    #fecha_pactada_abonos = fields.Date('Fecha pactada de inicio de abonos')
    #bodega_id = fields.Many2one('product.product', string='Bodega')
    #precio_parqueo = fields.Float('Precio parqueo')
    #tipo_cambio = fields.Float('Tipo de cambio')

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
