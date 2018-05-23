# -*- coding: utf-8 -*-
import datetime
from datetime import date
from odoo import models, api


class VendorDueEmailAlert(models.Model):
    _name = 'due.alert'

    @api.multi
    def invoice_email_alert(self):
        ''' This function automatically send email alert when the vendor bill due date becomes expire before 3 days '''
        invoice_ids = self.env['account.invoice'].search([('type', '=', 'in_invoice'), ('state', '=', 'open')])
        for invoice in invoice_ids:
            if invoice.date_due:
                date_today = datetime.date.today()
                date_string = invoice.date_due
                due_date = date(*map(int, date_string.split('-')))
                diff = due_date - date_today
                if diff.days is 3:
                    ir_model_data = self.env['ir.model.data']
                    template_id = ir_model_data.get_object_reference('prime_doors_payment_due_alert', 'email_template_vendor_due_alert')[1]
                    mail_template = self.env['mail.template'].browse(template_id)
                    mail_template.send_mail(invoice.id, force_send=True)
