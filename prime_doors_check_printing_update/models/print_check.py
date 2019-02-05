# -*- coding: utf-8 -*-

from odoo import models
from odoo.tools.translate import _
from odoo.tools.misc import formatLang, format_date

import logging
_logger = logging.getLogger(__name__)


LINE_FILLER = '*'
INV_LINES_PER_STUB = 9

class report_print_check(models.Model):
    _inherit = 'account.payment'

    def make_stub_line(self, invoice):
        result = super(report_print_check,self).make_stub_line(invoice)
        discount = 0.0
        for line in invoice.invoice_line_ids:
            discount += line.price_unit *(line.discount or 0.00) / 100.0
        result['discount'] = formatLang(self.env, discount, currency_obj=invoice.currency_id)
        _logger.info('========dis==%r',discount)
        return result