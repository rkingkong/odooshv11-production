# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, api, fields, _
import json
from re import sub
from decimal import Decimal


import logging
_logger = logging.getLogger(__name__)


class generic_tax_report(models.AbstractModel):

    _inherit = 'account.generic.tax.report'

    def get_reports_buttons(self):
        return [{'name': _('Print Preview'), 'action': 'print_pdf'}, {'name': _('Export (XLSX)'), 'action': 'print_xlsx'},{'name': _('Pay Taxes'), 'action': 'pay_tax'}]

    


    def pay_tax(self, options):
        invoices = []
        action = self.env.ref('tax_pay_button.action_pay_tax_wizard').read()[0]
        ctx = self._context.copy()
        ctx.update({'options': options})
        action['context'] = ctx
        return action

class TaxPay(models.TransientModel):

    _name = 'tax.pay.wizard'

    def format_amount(self, value, currency=False):
        value = Decimal(sub(r'[^\d.]', '', value))
        # if self.env.context.get('no_format'):
        #     return value
        # currency_id = currency or self.env.user.company_id.currency_id
        # value = value.replace(currency_id.symbol,'').strip()
        # _logger.info('=========%r====%r',self._context.get('lang'),self.env.user.lang)
        # timezone = self._context.get('lang') or self.env.user.lang
        # if timezone == 'en_US':
        #     timezone += '.UTF-8'
        # locale.setlocale(locale.LC_ALL, timezone)
        # _logger.info('================%r',locale.atof(value))
        # return value

    @api.model
    def get_default_pay_journals(self):
        cr_type = self.env.ref('account.data_account_type_current_liabilities').id
        dr_type = self.env.ref('account.data_account_type_liquidity').id
        cr_account = self.env['account.account'].search([('user_type_id','=',cr_type)], limit=1)
        dr_account = self.env['account.account'].search([('user_type_id','=',dr_type)], limit=1)
        lines = self.env['account.generic.tax.report'].with_context(self._context.get('options').get('date')).get_lines(self._context.get('options'))
        amount = 0.0
        for line in lines:
            if line.get('caret_options'):
                tax = self.env['account.tax'].browse(line.get('id'))
                if tax and tax.type_tax_use == 'sale':
                    amount += float(self.format_amount(line.get('columns')[1].get('name')))
        return [(0,0,{'account_id':cr_account.id, 'type':'cr','amount':amount}),(0,0,{'account_id':dr_account.id, 'type':'dr','amount':amount})]

    tax_journal_ids = fields.One2many('tax.pay.journal', 'tax_id', string="Tax Payable Journal", default=get_default_pay_journals)
    
    @api.multi
    def post_journals(self):
        account_move = self.env['account.move']
        line_ids = []
        for journal in self.tax_journal_ids:
            line_ids.append((0,0,{'account_id':journal.account_id.id, 'credit':journal.amount if journal.type == 'cr' else 0.0,'debit':journal.amount if journal.type == 'dr' else 0.0}))
        vals = {'ref':'Tax Pay','journal_id':self.env['account.journal'].search([('type','=','general')], limit=1).id or False,'line_ids':line_ids}
        res = account_move.create(vals)
        res.post()
        return True


class TaxPay(models.TransientModel):
    
    _name = 'tax.pay.journal'

    account_id = fields.Many2one('account.account', string="Account")
    amount = fields.Float(string="Amount", required=True)
    type = fields.Selection([('cr','Cr'),('dr','Dr')], string="Amount Type")
    tax_id = fields.Many2one('tax.pay.wizard', string="Tax Pay")