# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api


class SaleOrderMarkup(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('markup')
    def _get_price_unit(self):
        for line in self:
            line.price_unit = line.purchase_price * (1 + line.markup)

    markup = fields.Float('Markup')


class AccountInvoiceMarkup(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('markup')
    def _get_price_unit(self):
        for line in self:
            purchase_price = line.product_id.standard_price
            line.price_unit = purchase_price * (1 + line.markup)

    markup = fields.Float('Markup')
