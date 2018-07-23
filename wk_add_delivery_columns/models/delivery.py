# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class StockMove(models.Model):
    _inherit = 'stock.move'

    purchase_order_id = fields.Many2one('purchase.order',
        'Purchase Order', ondelete='set null', compute="get_latest_purchase_order", store=True, index=True, readonly=True, copy=False)
    date_order = fields.Datetime(string='Scheduled Date', related='purchase_order_id.date_planned',)
    
    @api.multi
    @api.depends('origin')
    def get_latest_purchase_order(self):
        for obj in self:
            obj.purchase_order_id = self.env['purchase.order.line'].search([('product_id','=',obj.product_id.id)], limit=1, order="id desc").order_id.id

class SaleOrderLine(models.Model):
    
    _inherit ="sale.order.line"

    purchase_order_id = fields.Many2one('purchase.order',
        'Purchase Order', ondelete='set null', related="move_ids.purchase_order_id", store=True, index=True, readonly=True, copy=False)
        
        