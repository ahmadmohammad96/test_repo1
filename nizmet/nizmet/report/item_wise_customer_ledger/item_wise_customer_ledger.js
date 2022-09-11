// Copyright (c) 2022, craft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item-wise Customer Ledger"] = {
	"filters": [
		{
			'fieldname':'from_date',
			'label':__('From Date'),
			'fieldtype':'Date',
			'default':frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			'width':100,
		},
		{
			'fieldname':'to_date',
			'label':__('To Date'),
			'fieldtype':'Date',
			'default':frappe.datetime.get_today(),
			'width':100,
		},
		{
			'fieldname':'customer',
			'label':__('Customer'),
			'fieldtype':'Link',
			'options':'Customer',
			'width':100,
		},

		{
			'fieldname':'company',
			'label':__('Company'),
			'fieldtype':'Link',
			'options':'Company',
			'width':100,
		}

	]
};
