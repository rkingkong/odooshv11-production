# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderMarkup(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('markup')
    def _markup_change(self):
        for line in self:
            if line.purchase_price != 0.0:
                line.price_unit = line.purchase_price * (1 + line.markup)
                try:
                    line.purchase_price = line.price_unit / (1 + line.markup)
                except ZeroDivisionError:
                    line.price_unit = 0.0

    @api.onchange('purchase_price')
    def _purchase_price_change(self):
        for line in self:
            if line.purchase_price != 0.0:
                line.price_unit = line.purchase_price * (1 + line.markup)
            try:
                line.markup = (line.price_unit / line.purchase_price) - 1
            except ZeroDivisionError:
                line.markup = 0.00

    @api.onchange('price_unit')
    def _price_unit_change(self):
        for line in self:
            try:
                line.markup = (line.price_unit / line.purchase_price) - 1
            except ZeroDivisionError:
                line.markup = 0.00
            if line.purchase_price != 0.0:
                try:
                    line.purchase_price = line.price_unit / (1 + line.markup)
                except ZeroDivisionError:
                    line.price_unit = 0.0

    markup = fields.Float('Markup')


class AccountInvoiceMarkup(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('markup')
    def _get_price_unit(self):
        for line in self:
            purchase_price = line.product_id.standard_price
            line.price_unit = purchase_price * (1 + line.markup)

    markup = fields.Float('Markup')
