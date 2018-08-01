from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def remove_taxes(self):
        self.ensure_one()
        if self.state not in ['draft','sent']:
            raise UserError(_('Remove taxes only from order(s) which are in draft or sent state.'))
        for line in self.order_line:
            line.tax_id = False
        return True