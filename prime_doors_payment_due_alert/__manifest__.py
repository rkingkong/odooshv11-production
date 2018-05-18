# -*- coding: utf-8 -*-
{
    'name': 'Prime Doors Payment Due Alert',
    'version': '11.0.1.0.0',
    'summary': 'This Module generate email alert for vendor payment before 3 days from due date',
    'category': 'Accounting',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'account_invoicing', 'mail'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'views/alert_mail_template.xml',
        'views/due_alert_cron_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
