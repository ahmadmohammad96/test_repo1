from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('Dashboard Information'),
		'fieldname': 'commission_po_so',
		'non_standard_fieldnames': {
			'Commission Shipment': 'commission_po_so',
		},
		# 'dynamic_links': {
		# 	'party_name': ['Customer', 'quotation_to']
		# },
		'transactions': [
			{
				'label': _('Commission Shipment'),
				'items': ['Commission Shipment']
			},
        ]
    }