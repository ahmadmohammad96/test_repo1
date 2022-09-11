# Copyright (c) 2022, craft and contributors
# For license information, please see license.txt

from itertools import count

from numpy import take
import frappe
from frappe import _
from datetime import datetime
from datetime import time

def execute(filters=None):
	conditions = get_conditions(filters)
	invoice_cus_conditions = get_invoice_cus_conditions(filters)
	payment_cus_conditions = get_payment_cus_conditions(filters)
	columns, data = get_columns(filters), get_data(conditions,invoice_cus_conditions, payment_cus_conditions,filters)
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
			'options':'Sales Invoice',
			'width':200
		},
		{
			'label':_('Container'),
			'field_name':'container',
			'fieldtype':'Data',
			'width':100
		},
		{
			'label':_('Posting Date'),
			'field_name':'posting_date',
			'fieldtype':'Date',
			'width':100
		},
		{
			'label':_('Customer'),
			'field_name':'customer',
			'fieldtype':'Link',
			'options':'Customer',
			'width':200
		},
		{
			'label':_('Mode of Payment'),
			'field_name':'mode_of_payment',
			'fieldtype':'Data',
			'width':100
		},
		{
			'label':_('Quantity'),
			'field_name':'quantity',
			'fieldtype':'Data',
			'width':100
		},
		{
			'label':_('Stock UoM'),
			'field_name':'stock_uom',
			'fieldtype':'Data',
			'width':100
		},
		{
			'label':_('Rate'),
			'field_name':'rate',
			'fieldtype':'Float',
			'width':100
		},
		{
			'label':_('Debit'),
			'field_name':'debit',
			'fieldtype':'Float',
			'width':100
		},
		{
			'label':_('Credit'),
			'field_name':'credit',
			'fieldtype':'Float',
			'width':100
		},
		{
			'label':_('Outstanding'),
			'field_name':'outstanding',
			'fieldtype':'Float',
			'width':100
		},
	]
	return columns

def get_data(conditions,invoice_cus_conditions,payment_cus_conditions,filters):
	#select name,party,posting_date,mode_of_payment,paid_amount from `tabPayment Entry`;
	#select sii.item_code,sii.item_name,si.name,sii.batch_no,si.posting_date,si.customer_name,sii.qty,sii.stock_uom,sii.rate,sii.amount from `tabSales Invoice Item` sii left join `tabSales Invoice` si on sii.parent = si.name;

	data = []

	paymentEntries = frappe.db.sql(
		'''
		select name,party,posting_date,mode_of_payment,paid_amount from `tabPayment Entry` where docstatus = 1 {} {} and payment_type='Receive' order by posting_date;
		'''.format(conditions, payment_cus_conditions),as_dict=1
	)

	salesInvoices = frappe.db.sql(
		'''
		select sii.item_code,sii.item_name,sii.parent,sii.batch_no,si.posting_date,si.customer_name,sii.qty,sii.stock_uom,sii.rate,sii.amount from `tabSales Invoice Item` sii left join `tabSales Invoice` si on sii.parent = si.name where si.docstatus = 1 {} {} order by si.posting_date;
		'''.format(conditions, invoice_cus_conditions),as_dict = 1
	)

	total_credit = 0
	total_quantity = 0
	total_rate = 0
	total_debit = 0
	paymentEntries = ''

	if filters.get('customer') : 

		paymentEntries = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
			'party': filters.get('customer') , 
		},
	)
	

	elif  filters.get('company') : 
		paymentEntries = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
			'company' : filters.get('company')
		},
	)

	elif filters.get('company') and filters.get('customer') : 
		paymentEntries = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
			'party': filters.get('customer') , 
			'company' : filters.get('company')
		},
	)

	else : 
		paymentEntries = frappe.db.get_list('Payment Entry',
	
	
		filters={
			'status': 'Submitted' ,
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'payment_type' : 'Receive'  , 
		},
	)

		

	for i in paymentEntries:
		take_payment = frappe.get_doc('Payment Entry' , i['name'])
		

		row = {
			'payment_entry':i['name'],
			'item_code':'',
			'item_name':'',
			'invoice':'',
			'container':'',
			'posting_date':take_payment.posting_date,
			'customer':take_payment.party,
			'mode_of_payment':take_payment.mode_of_payment,
			'quantity':'',
			'stock_uom':'',
			'rate':'',
			'debit':take_payment.paid_amount,
			'credit':'',
			'debit_amount': take_payment.paid_amount,
			'credit_amount': 0,
		}
		total_debit += take_payment.paid_amount
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
				'customer':take_payment.party,
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

		

	if filters.get('customer') : 

		salesInvoices = frappe.db.get_list('Sales Invoice',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'customer': filters.get('customer') , 
		},
	)
	

	elif  filters.get('company') : 
		salesInvoices = frappe.db.get_list('Sales Invoice',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'company' : filters.get('company')
		},
	)

	elif filters.get('company') and filters.get('customer') : 
		salesInvoices = frappe.db.get_list('Sales Invoice',
	
	
		filters={
			'posting_date' : ['>=' , filters.get('from_date') ] , 
			'posting_date' : ['<=' , filters.get('to_date')] , 
			'party': filters.get('customer') , 
			'company' : filters.get('company')
		},
	)

	else : 
		salesInvoices = frappe.db.get_list('Sales Invoice',
	
	
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


	# modification MR.index 0_0 - journal entries  
	all_j_entries =j_ent
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
			print(take_his_list)
			for j2 in take_his_list : 
				if j2.credit:
					
					data.append({
						'payment_entry':j,
						'item_code':'',
						'item_name':'',
						'invoice':'',
						'container':'',
						'posting_date':(frappe.get_doc('Journal Entry' , j )).posting_date,
						'customer':(j2.party).upper(),
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
	take_all_invoices  = salesInvoices
	for i in take_all_invoices : 
		take_name = i['name']
		take_doc = frappe.get_doc('Sales Invoice' , take_name)
		take_items = take_doc.items
		for j in take_items : 

			data.append({
							'payment_entry':'' , 
							'item_code':'',
							'item_name':j.item_name,
							'invoice':take_name,
							'container':j.batch_no,
							'posting_date':take_doc.posting_date,
							'customer':(take_doc.customer),
							'mode_of_payment':'',
							'quantity':j.stock_qty,
							'stock_uom':'',
							'rate':j.rate,
							'debit':0,
							'credit':j.amount,
							'debit_amount':0,
							'credit_amount': j.amount

						})	


			total_credit += j.amount
			total_quantity += j.stock_qty
			total_rate += j.rate




	print(data)		 
	#sort combined data based on posting_data
	sorted_data = sorted(data, key = lambda i : i['posting_date'])

	#calculate and add outstanding amount column
	outstanding_amount = 0
	global final_data
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
			'customer':row['customer'],
			'mode_of_payment':row['mode_of_payment'],
			'quantity':row['quantity'],
			'stock_uom':row['stock_uom'],
			'rate':row['rate'],
			'debit':row['debit'],
			'credit':row['credit'],
			'outstanding':outstanding_amount
		}
		final_data.append(new_row)

	final_data.append({
		'payment_entry':'Total',
		'quantity':total_quantity,
		'rate':total_rate,
		'debit':total_debit,
		'credit':total_credit,
		'outstanding':outstanding_amount
	})

	print('__________________________---------------------------' , final_data)
	
	return final_data

def get_conditions(filters):
	conditions = ''
	if filters.get('from_date') and filters.get('to_date'):
		conditions += 'and posting_date between "{}" and "{}"'.format(filters.get('from_date'),filters.get('to_date'))
	return conditions

def get_invoice_cus_conditions(filters):
	invoice_cus_conditions = ''
	if filters.get('customer'):
		print( 'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM', filters.get('customer') ,filters.customer )
		invoice_cus_conditions += 'and si.customer = "{}"'.format(filters.customer)
	return invoice_cus_conditions

def get_payment_cus_conditions(filters):
	payment_cus_conditions = ''
	if filters.get('customer'):
		payment_cus_conditions += 'and party = "{}"'.format(filters.customer)
	return payment_cus_conditions

