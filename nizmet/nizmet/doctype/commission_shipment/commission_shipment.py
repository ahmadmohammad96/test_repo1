# Copyright (c) 2022, craft and contributors
# For license information, please see license.txt

# from cmath import pi
# import imp
# from pprint import pp

from itertools import count
import frappe
from frappe.model.document import Document
from frappe.model.rename_doc import get_link_fields
from erpnext.accounts.party import get_party_account
from erpnext.accounts.general_ledger import (
	make_gl_entries,
	make_reverse_gl_entries,
)

class CommissionShipment(Document):
	def delete_gl_entries_on_cancel(self):
		frappe.db.sql("""delete from `tabGL Entry` where voucher_type = '{}' 
		and voucher_no = '{}'
		""".format(self.doctype, self.name))

	def on_cancel(self):
		self.delete_gl_entries_on_cancel()

	def on_submit(self):
		self.create_gl(self, self.name)
		self.create_customer_gl(self, self.name)
		self.create_purchase_gl(self,self.name)
		self.create_sales_gl(self, self.name)

	def calculate_amount(self, doc, handler = None):
		self.total = 0
		for i in doc.items:
			i.amount = i.net_weight * i.invoice_price
			# i.base_amount = i.net_weight * i.base_rate
			self.total += i.net_weight

		return self.total

	def calculate_purchase_price(self,doc,handler=None):
		self.pp = 0
		for i in doc.items:
			self.pp += i.purchase_price

		return self.pp

	def calculate_sales_price(self,doc,handler = None):
		self.sp = 0
		for i in doc.items:
			self.sp += i.sales_price
		
		return self.sp

	def calculate_invoice_price(self,doc,handler=None):
		self.ip = 0
		for i in doc.items:
			self.ip += i.invoice_price

		return self.ip

	def account_type(self):
		self.account_type_1 = frappe.get_value("Account",self.commission_income_account_name,"account_type")
		self.account_type_2 = frappe.get_value("Account",self.commission_expense_account_name,'account_type')

		return self.account_type_1, self.account_type_2

	def default_commission(self,doc):
		self.default_commission_income = frappe.get_value('Company',doc.company,'default_commission_income')
		self.default_commission_expense = frappe.get_value('Company',doc.company,'default_commission_expense')

		return self.default_commission_income, self.default_commission_expense

	def account_name(self):
		# frappe.get_value('Account',{'account_type':'Cost of Goods Sold'},'name')
		# frappe.get_value('Account',{'account_type':'Sales Account'},'name')
		self.purchase_account_name = frappe.get_list('Account' , filters={'account_type' :'Cost of Goods Sold' })
		self.sales_account_name = frappe.get_list('Account' , filters={ 'account_type' : 'Sales Account'} )

		return self.purchase_account_name, self.sales_account_name

	def create_gl(self, doc, handler=None):

		print('.....................' ,   self.default_commission(doc)[0])
		print('.....................' ,   self.default_commission(doc)[1])

		self.commission_income_account_name = doc.commission_income_account_name
		self.commission_expense_account_name = doc.commission_expense_account_name
		
		if self.account_type()[0] == 'Commission Receivable':
			
			# if 'Creditors - NF' in  self.default_commission(doc)[0] or 'Cost of Goods Sold - NF' in self.default_commission(doc)[0]  :
			# 	pass 
			# else :

			# 	print('inside 1 ')

			self.gl = frappe.new_doc("GL Entry")
			self.gl.posting_date = doc.date
			self.gl.account = self.default_commission(doc)[0]
			self.gl.credit = self.calculate_amount(doc) * doc.commission_income_rate
			# self.gl.account_currency = doc.currency
			self.gl.against = doc.supplier
			self.gl.voucher_type = 'Commission Shipment'
			self.gl.voucher_no = doc.name
			self.gl.cost_center = doc.cost_center
			self.gl.company = doc.company
			self.gl.flags.ignore_permissions = 1

			self.gl_2 = frappe.new_doc("GL Entry")
			self.gl_2.posting_date = doc.date
			self.gl_2.account = self.commission_income_account_name
			self.gl_2.debit = self.calculate_amount(doc) * doc.commission_income_rate
			# self.gl_2.account_currency = doc.currency
			self.gl_2.against = doc.supplier
			self.gl_2.voucher_type = 'Commission Shipment'
			self.gl_2.voucher_no = doc.name
			self.gl_2.cost_center = doc.cost_center
			self.gl_2.company = doc.company
			self.gl_2.flags.ignore_permissions = 1
			
			if self.gl.credit != 0 and self.gl_2.debit != 0:
				self.gl.save()
				self.gl_2.save()
			else:
				pass
		else:
			frappe.throw('Please Set Account Type as "Commission Receivable" for {}'.format(self.commission_income_account_name))
			return False

		if self.account_type()[1] == 'Commission Payable':

			# if 'Creditors - NF' in  self.default_commission(doc)[1] or 'Cost of Goods Sold - NF' in self.default_commission(doc)[1]  :
			# 	pass 
			# else :
			# 	print('inside 1 ')

			self.gl = frappe.new_doc("GL Entry")
			self.gl.posting_date = doc.date
			self.gl.account = self.default_commission(doc)[1]
			self.gl.debit = self.calculate_amount(doc) * doc.commission_expense_rate
			# self.gl.account_currency = doc.currency
			self.gl.against = doc.supplier
			self.gl.voucher_type = 'Commission Shipment'
			self.gl.voucher_no = doc.name
			self.gl.cost_center = doc.cost_center
			self.gl.company = doc.company
			self.gl.flags.ignore_permissions = 1

			self.gl_2 = frappe.new_doc("GL Entry")
			self.gl_2.posting_date = doc.date
			self.gl_2.account = self.commission_expense_account_name
			self.gl_2.credit = self.calculate_amount(doc) * doc.commission_expense_rate
			# self.gl_2.account_currency = doc.currency
			self.gl_2.against = doc.supplier
			self.gl_2.voucher_type = 'Commission Shipment'
			self.gl_2.voucher_no = doc.name
			self.gl_2.cost_center = doc.cost_center
			self.gl_2.company = doc.company
			self.gl_2.flags.ignore_permissions = 1
			
			if self.gl.debit != 0 and self.gl_2.credit != 0:
				self.gl.save()
				self.gl_2.save()
			else:
				pass
			
		else:
			frappe.throw('Please Set Account Type as "Commission Payable" for {}'.format(self.commission_expense_account_name))
			return False


	def create_customer_gl(self,doc, handler = None):
		print('.....................' ,   self.default_commission(doc)[0])
		print('.....................' ,   self.default_commission(doc)[1])


		self.commission_income_customer_account_name = doc.commission_income_customer_account_name
		self.commission_expense_customer_account_name = doc.commission_expense_customer_account_name

		if self.account_type()[0] == 'Commission Receivable':

			# if 'Creditors - NF' in  self.default_commission(doc)[0] or 'Cost of Goods Sold - NF' in self.default_commission(doc)[0]  :
			# 	pass 
			# else :
			# 	print('inside 1 ')

			self.cgl = frappe.new_doc("GL Entry")
			self.cgl.posting_date = doc.date
			self.cgl.account = self.default_commission(doc)[0]
			self.cgl.credit = self.calculate_amount(doc) * doc.commission_income_customer_rate
			# self.cgl.account_currency = doc.currency
			self.cgl.against = doc.customer
			self.cgl.voucher_type = 'Commission Shipment'
			self.cgl.voucher_no = doc.name
			self.cgl.cost_center = doc.cost_center
			self.cgl.company = doc.company
			self.cgl.flags.ignore_permissions = 1

			self.cgl_2 = frappe.new_doc("GL Entry")
			self.cgl_2.posting_date = doc.date
			self.cgl_2.account = self.commission_income_customer_account_name
			self.cgl_2.debit = self.calculate_amount(doc) * doc.commission_income_customer_rate
			# self.cgl_2.account_currency = doc.currency
			self.cgl_2.against = doc.customer
			self.cgl_2.voucher_type = 'Commission Shipment'
			self.cgl_2.voucher_no = doc.name
			self.cgl_2.cost_center = doc.cost_center
			self.cgl_2.company = doc.company
			self.cgl_2.flags.ignore_permissions = 1

			if self.cgl.credit != 0 and self.cgl_2.debit != 0:
				self.cgl.save()
				self.cgl_2.save()
			else:
				pass
			
		else:
			frappe.throw('Please Set Account Type as "Commission Receivable" for {}'.format(self.commission_income_customer_account_name))
			return False

		if self.account_type()[1] == 'Commission Payable':

			# if 'Creditors - NF' in  self.default_commission(doc)[0] or 'Cost of Goods Sold - NF' in self.default_commission(doc)[0]  :
			# 	pass 
			# else :

			# 	print('inside 1 ')


			self.cgl = frappe.new_doc("GL Entry")
			self.cgl.posting_date = doc.date
			self.cgl.account = self.default_commission(doc)[1]
			self.cgl.debit = self.calculate_amount(doc) * doc.commission_expense_customer_rate
			# self.cgl.account_currency = doc.currency
			self.cgl.against = doc.supplier
			self.cgl.voucher_type = 'Commission Shipment'
			self.cgl.voucher_no = doc.name
			self.cgl.cost_center = doc.cost_center
			self.cgl.company = doc.company
			self.cgl.flags.ignore_permissions = 1

			self.cgl_2 = frappe.new_doc("GL Entry")
			self.cgl_2.posting_date = doc.date
			self.cgl_2.account = self.commission_expense_customer_account_name
			self.cgl_2.credit = self.calculate_amount(doc) * doc.commission_expense_customer_rate
			# self.cgl_2.account_currency = doc.currency
			self.cgl_2.against = doc.supplier
			self.cgl_2.voucher_type = 'Commission Shipment'
			self.cgl_2.voucher_no = doc.name
			self.cgl_2.cost_center = doc.cost_center
			self.cgl_2.company = doc.company
			self.cgl_2.flags.ignore_permissions = 1
			if self.cgl.debit != 0 and self.cgl_2.credit != 0:
				self.cgl.save()
				self.cgl_2.save()
			else:
				pass
		else:
			frappe.throw('Please Set Account Type as "Commission Payable" for {}'.format(self.commission_expense_customer_account_name))
			return False

	def create_purchase_gl(self,doc,handler = None):
		pass

		print('..........111111111111111111111111111111...........' ,   self.account_name())
		print('???????????????????????????????????'  , self.company)
		# by Mr.index 0_0
		take_docs = []
		final_account = ''
		for i in self.account_name()[0]: 
			take_docs.append(frappe.get_doc('Account' , i['name']))

		print(take_docs) 
		counter = 0 
		while counter < len(take_docs) : 
			if take_docs[counter].company == self.company : 
				print('found the account ')
				final_account = self.account_name()[0][counter]['name']
				print('--------------------------->>>>' , final_account)

			counter +=1 

		self. credit_to = get_party_account("Supplier",self.supplier, self.company)

		# if 'Creditors - NF' in  self.account_name()[0] or 'Cost of Goods Sold - NF' in self.account_name()[0]  :
		# 		pass 
		# else :
		# 	print('inside 1 ')

		self.gl = frappe.new_doc('GL Entry')
		self.gl.posting_date = doc.date
		self.gl.account =final_account
		self.gl.debit = (self.calculate_purchase_price(doc)-self.calculate_invoice_price(doc))*self.calculate_amount(doc)
		self.gl.against = doc.supplier
		self.gl.voucher_type = 'Commission Shipment'
		self.gl.voucher_no = doc.name
		self.gl.cost_center = doc.cost_center
		self.gl.company = doc.company
		self.gl.flags.ignore_permissions = 1

		self.gl_2 = frappe.new_doc('GL Entry')
		self.gl_2.posting_date = doc.date
		self.gl_2.account = self.credit_to
		self.gl_2.party_type = 'Supplier'
		self.gl_2.party = self.supplier
		self.gl_2.credit = (self.calculate_purchase_price(doc)-self.calculate_invoice_price(doc))*self.calculate_amount(doc)
		self.gl_2.against = doc.supplier
		self.gl_2.voucher_type = 'Commission Shipment'
		self.gl_2.voucher_no = doc.name
		self.gl_2.cost_center = doc.cost_center
		self.gl_2.company = doc.company
		self.gl_2.flags.ignore_permissions = 1

		if self.gl.debit != 0 and self.gl_2.credit != 0:
			self.gl.save()
			self.gl_2.save()
		else:
			pass

	def create_sales_gl(self,doc,handler = None):
		pass 
		print('.....................' ,   self.account_name()[1])
		# by Mr.index 0_0
		take_docs = []
		final_account = ''
		for i in self.account_name()[1]: 
			take_docs.append(frappe.get_doc('Account' , i['name']))

		print(take_docs) 
		counter = 0 
		while counter < len(take_docs) : 
			if take_docs[counter].company == self.company : 
				print('found the account ')
				final_account = self.account_name()[1][counter]['name']
				print('--------------------------->>>>' , final_account)

			counter +=1 

		self. debit_to = get_party_account("Customer",self.customer, self.company)

		# if 'Creditors - NF' in  self.account_name()[1] or 'Cost of Goods Sold - NF' in self.account_name()[1]  :
		# 		pass 
		# else :
		# 	print('inside 1 ')
	
		self.gl = frappe.new_doc('GL Entry')
		self.gl.posting_date = doc.date
		self.gl.account = final_account
		self.gl.debit = (self.calculate_sales_price(doc)-self.calculate_invoice_price(doc))*self.calculate_amount(doc)
		self.gl.against = doc.customer
		self.gl.voucher_type = 'Commission Shipment'
		self.gl.voucher_no = doc.name
		self.gl.cost_center = doc.cost_center
		self.gl.company = doc.company
		self.gl.flags.ignore_permissions = 1

		self.gl_2 = frappe.new_doc('GL Entry')
		self.gl_2.posting_date = doc.date
		self.gl_2.account = self.debit_to
		self.gl_2.party_type = 'Customer'
		self.gl_2.party = self.customer
		self.gl_2.credit = (self.calculate_sales_price(doc)-self.calculate_invoice_price(doc))*self.calculate_amount(doc)
		self.gl_2.against = doc.customer
		self.gl_2.voucher_type = 'Commission Shipment'
		self.gl_2.voucher_no = doc.name
		self.gl_2.cost_center = doc.cost_center
		self.gl_2.company = doc.company
		self.gl_2.flags.ignore_permissions = 1

		if self.gl.debit != 0 and self.gl_2.credit != 0:
			self.gl.save()
			self.gl_2.save()
		else:
			pass