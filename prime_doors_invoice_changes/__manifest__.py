# -*- coding: utf-8 -*-
{
    'name': 'Prime Doors Invoice Changes',
    'version': '11.0.1.0.0',
    'summary': '',
    'category': 'Accounting',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'account_invoicing', 'prime_doors_external_layout'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'views/invoice_slip_view.xml',
        'views/inherit_sale_invoice_inherit_address.xml'
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
