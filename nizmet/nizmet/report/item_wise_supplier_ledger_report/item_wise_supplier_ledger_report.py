# Copyright (c) 2022, craft and contributors
# For license information, please see license.txt

import re
import frappe
from frappe import _
from frappe.utils import flt



def execute(filters=None):
	conditions = get_conditions(filters)
	invoice_sup_condition = get_invoice_sup_condition(filters)
	payment_sup_condition = get_payment_sup_condition(filters)
	columns, data = get_columns(filters), get_data(conditions,invoice_sup_condition,payment_sup_condition, filters)
	return columns, data


def get_columns(filters):
	columns = [
		{
			'label':_('Payment Entry'),
			'field_name':'payment_entry',
			'fieldtype':'Link',
			'options':'Payment Entry',
			'width':200
		},
		
		{
			'label':_('Item Code'),
			'field_name':'item_code',
			'fieldtype':'Link',
			'options':'Item',
			'width':200
		},
		{
			'label':_('Item Name'),
			'field_name':'item_name',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label':_('Invoice'),
			'field_name':'invoice',
			'fieldtype':'Link',
			'options':'Purchase Invoice',
			'width':200
		},
		{
			'label':_('Container'),
			'field_name':'container',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label':_('Posting Date'),
			'field_name':'posting_date',
			'fieldtype':'Date',
			'width':200
		},
		{
			'label':_('Supplier'),
			'field_name':'supplier',
			'fieldtype':'Link',
			'options':'Supplier',
			'width':200
		},
		{
			'label':_('Mode of Payment'),
			'field_name':'mode_of_payment',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label':_('Quantity'),
			'field_name':'quantity',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label':_('Stock UoM'),
			'field_name':'stock_uom',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label':_('Rate'),
			'field_name':'rate',
			'fieldtype':'Float',
			'width':200
		},
		{
			'label':_('Debit'),
			'field_name':'debit',
			'fieldtype':'Float',
			'width':200
		},
		{
			'label':_('Credit'),
			'field_name':'credit',
			'fieldtype':'Float',
			'width':200
		},
		{
			'label':_('Outstanding'),
			'field_name':'outstanding',
			'fieldtype':'Float',
			'width':200
		}
	]
	return columns

def get_data(conditions,invoice_sup_condition,payment_sup_condition, filters):
	# data = frappe.db.sql(
	# 	'''select pe.name, pii.item_code, pii.item_name, per.reference_name, pii.batch_no, pe.posting_date, pi.supplier_name, pe.mode_of_payment, pii.qty, pii.stock_uom, pii.rate, pe.paid_amount, pii.amount
	# 	from `tabPayment Entry` pe 
	# 	left join `tabPayment Entry Reference` per on pe.name = per.parent
	# 	left join `tabPurchase Invoice Item` pii on per.reference_name = pii.parent
	# 	left join `tabPurchase Invoice` pi on per.reference_name = pi.name where pe.name is not null {}
	# 	'''.format(conditions)
	# )
	data = []
	payment_entry = frappe.db.sql(
		'''
		select name, posting_date, party, mode_of_payment, paid_amount from `tabPayment Entry` where docstatus = 1 {} {} and payment_type='Pay' order by posting_date
		'''.format(conditions,payment_sup_condition), as_dict = 1
	)
	purchase_invoice = frappe.db.sql(
		'''
		select pii.item_code, pii.item_name, pii.parent,pi.supplier_name, batch_no, posting_date, pii.qty, stock_uom, rate, amount
		from `tabPurchase Invoice Item` pii left join `tabPurchase Invoice` pi on pii.parent = pi.name where pi.docstatus = 1 {} {} order by posting_date
		'''.format(conditions,invoice_sup_condition), as_dict = 1
	)
	credit_total = 0
	total_quantity = 0
	total_rate = 0
	total_debit = 0


	if filters.get('supplier') : 

		payment_entry = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
			'party': filters.get('supplier') , 
		},
	)
	

	elif  filters.get('company') : 
		payment_entry = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
			'company' : filters.get('company')
		},
	)

	elif filters.get('company') and filters.get('supplier') : 
		payment_entry = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
			'party': filters.get('supplier') , 
			'company' : filters.get('company')
		},
	)

	else : 
		payment_entry = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
		},
	)

		



	for i in payment_entry:
		take_payment = frappe.get_doc('Payment Entry' , i['name'])

		row = {
			'payment_entry':i['name'],
			'item_code':'',
			'item_name':'',
			'invoice':'',
			'container':'',
			'posting_date':take_payment.posting_date,
			'supplier':take_payment.party,
			'mode_of_payment':take_payment.mode_of_payment,
			'quantity':'',
			'stock_uom':'',
			'rate':'',
			'debit':take_payment.paid_amount,
			'credit':'',
			'debit_amount': take_payment.paid_amount,
			'credit_amount': 0,
		}
		credit_total += take_payment.paid_amount
		data.append(row)

		# modification 3 - deductions
		take_deduc = take_payment.deductions
		for jj in take_deduc : 

			row2 = {
				'payment_entry':i['name'],
				'item_code':'',
				'item_name':'',
				'invoice':'',
				'container':'',
				'posting_date':take_payment.posting_date,
				'supplier':take_payment.party,
				'mode_of_payment':take_payment.mode_of_payment,
				'quantity':'',
				'stock_uom':'',
				'rate':'',
				'debit':jj.amount,
				'credit':'',
				'debit_amount': jj.amount,
				'credit_amount': 0,

			}
			data.append(row2)
			
			










	if filters.get('supplier') : 

		purchase_invoice = frappe.db.get_list('Purchase Invoice',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'customer': filters.get('customer') , 
		},
	)
	

	elif  filters.get('company') : 
		purchase_invoice = frappe.db.get_list('Purchase Invoice',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'company' : filters.get('company')
		},
	)

	elif filters.get('company') and filters.get('customer') : 
		purchase_invoice = frappe.db.get_list('Purchase Invoice',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'party': filters.get('customer') , 
			'company' : filters.get('company')
		},
	)

	else : 
		purchase_invoice = frappe.db.get_list('Purchase Invoice',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
		},
	)

	
	



	
	j_ent = ''
	if  filters.get('company') : 
		j_ent = frappe.db.get_list('Journal Entry',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'company' : filters.get('company')
		},
	)

	
	else : 
		j_ent = frappe.db.get_list('Journal Entry',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
		},
	)


		



# modification - MR.index 0_0 - journal entries  
	all_j_entries = j_ent
	counter = 0 
	all_doc = list()
	final_dict =list()
	accounts_list = list()
	final_list = list()
	data_copy = data 
	while counter < len(all_j_entries) :
		counter2 = 0 
		final_dict.append({ all_j_entries[counter]['name'] : (frappe.get_doc('Journal Entry' , all_j_entries[counter]['name'])).accounts })
		counter +=1 
	
	for i in final_dict : 
		for j,k in i.items():

			take_his_list = k
			for j2 in take_his_list : 
				if j2.debit :
						
					data.append({
						'payment_entry':j,
						'item_code':'',
						'item_name':'',
						'invoice':'',
						'container':'',
						'posting_date':(frappe.get_doc('Journal Entry' , j )).posting_date,
						'supplier':(j2.party).upper(),
						'mode_of_payment':'',
						'quantity':'',
						'stock_uom':'',
						'rate':'',
						'debit':j2.debit,
						'credit':j2.credit,
						'debit_amount':j2.debit,
						'credit_amount': j2.credit

					})	



	# modification 2 - seperate the items in a sales invoice 
	take_all_invoices  = frappe.get_list('Purchase Invoice' )
	for i in take_all_invoices : 
		take_name = i['name']
		take_doc = frappe.get_doc('Purchase Invoice' , take_name)
		take_items = take_doc.items
		for j in take_items : 

			data.append({
							'payment_entry':'' , 
							'item_code':'',
							'item_name':j.item_name,
							'invoice':take_name,
							'container':j.batch_no,
							'posting_date':take_doc.posting_date,
							'supplier':(take_doc.supplier),
							'mode_of_payment':'',
							'quantity':'',
							'stock_uom':'',
							'rate':'',
							'debit':j.amount,
							'credit':0,
							'debit_amount':j.amount,
							'credit_amount': 0

						})	

		 

	#sort combined data based on posting_date
	sorted_data = sorted(data, key = lambda i: i['posting_date'])

	outstanding_amount = 0
	final_data = []
	for row in sorted_data:
		outstanding_amount = outstanding_amount + row['credit_amount'] - row['debit_amount']
		new_row = {
			'payment_entry':row['payment_entry'],
			'item_code':row['item_code'],
			'item_name':row['item_name'],
			'invoice':row['invoice'],
			'container':row['container'],
			'posting_date':row['posting_date'],
			'supplier':row['supplier'],
			'mode_of_payment':row['mode_of_payment'],
			'quantity':row['quantity'],
			'stock_uom':row['stock_uom'],
			'rate':row['rate'],
			'debit':row['debit'],
			'credit':row['credit'],
			'outstanding':outstanding_amount
		}
		final_data.append(new_row)

	final_data.append(
		{
			'payment_entry':'Total',
			'quantity':total_quantity,
			'rate':total_rate,
			'debit':total_debit,
			'credit':credit_total,
			'outstanding':outstanding_amount
			}
		)
	return final_data

def get_conditions(filters):
	conditions = ''
	if filters.get('from_date') and filters.get('to_date'):
		conditions += 'and posting_date between "{}" and "{}"'.format(filters.get('from_date'), filters.get('to_date'))

	return conditions

def get_invoice_sup_condition(filters):
	sup_cond = ''
	if filters.get('supplier'):
		sup_cond += 'and pi.supplier_name = "{}"'.format(filters.get('supplier'))
	return sup_cond

def get_payment_sup_condition(filters):
	sup_cond = ''
	if filters.get('supplier'):
		sup_cond += 'and party = "{}"'.format(filters.get('supplier'))

	return sup_cond
