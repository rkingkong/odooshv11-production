# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class InheritSaleOrderLineInstruction(models.Model):
    _inherit = 'sale.order.line'

    instruction = fields.Char("Instruction")

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        res = {}
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(
                _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos:
            account = fpos.map_account(account)

        res = {
            'name': self.name,
            'instruction': self.instruction,
            'sequence': self.sequence,
            'origin': self.order_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'layout_category_id': self.layout_category_id and self.layout_category_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
        }
        return res


class InheritStockPickingInstruction(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def create(self, vals):
        res = super(InheritStockPickingInstruction, self).create(vals)
        return res


class InheritAccountInvoiceLineInstruction(models.Model):
    _inherit = 'account.invoice.line'

    instruction = fields.Char("Instruction")


class InheritStockMove(models.Model):
    _inherit = 'stock.move'

    instruction = fields.Char("Instruction")

    @api.model
    def create(self, vals):
        origin = vals.get('origin')
        order = self.env['sale.order'].search([('name', '=', origin)])
        order_line = self.env['sale.order.line'].search([('order_id', '=', order.id),
                                                         ('product_id', '=', vals.get('product_id'))])
        instruction = order_line.instruction
        vals['instruction'] = instruction
        perform_tracking = not self.env.context.get('mail_notrack') and vals.get('picking_id')
        if perform_tracking:
            picking = self.env['stock.picking'].browse(vals['picking_id'])
            initial_values = {picking.id: {'state': picking.state}}
        vals['ordered_qty'] = vals.get('product_uom_qty')
        res = super(InheritStockMove, self).create(vals)
        if perform_tracking:
            picking.message_track(picking.fields_get(['state']), initial_values)
        return res
