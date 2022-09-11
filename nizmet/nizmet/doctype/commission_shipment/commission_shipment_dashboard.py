from __future__ import unicode_literals

from frappe import _

def get_data():
	return {
		'fieldname': 'commission_shipment',
		'non_standard_fieldnames': {
			'Journal Entry': 'reference_name',
        }
    }