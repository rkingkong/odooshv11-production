# -*- coding: utf-8 -*-
{
    'name': 'Prime Doors Delivery Slip',
    'version': '11.0.1.0.0',
    'summary': '',
    'category': 'Inventory',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'account_invoicing', 'stock', 'sale_management', 'prime_doors_external_layout'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'views/delivery_slip_view.xml',
        'views/sale_order_line_inherit.xml',
        'views/invoice_line_inherit.xml',
        'views/stock_picking_inherit_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
