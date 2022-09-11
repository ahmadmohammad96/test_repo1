import frappe
from frappe.model.naming import make_autoname


def sales_invoice_autoname(doc, method):
    if doc.items[0].sales_order:
        #Sample sales order name: AM-S-220600001 => splits to AM,S,220600001
        #Sample sales order name: AM-S-220600001-1
        sales_inv_suffix = doc.items[0].sales_order.split('-')
        invoice_number = '-'.join(sales_inv_suffix[2:])
        autoname = make_autoname('{}-SI-{}-'.format(sales_inv_suffix[0],invoice_number))
        doc.name = autoname[:-5]+autoname[-3:]
        # doc.name = make_autoname('RTSI-{}-{}'.format(sales_inv_suffix[-2],sales_inv_suffix[-1]))[:-5]

def purchase_invoice_autoname(doc, method):
    if doc.items[0].purchase_order:
        purchase_inv_suffix = doc.items[0].purchase_order.split('-')
        invoice_number = '-'.join(purchase_inv_suffix[2:])
        autoname = make_autoname('{}-PI-{}-'.format(purchase_inv_suffix[0],invoice_number))
        doc.name = autoname[:-5]+autoname[-3:]

def commission_shipment_autoname(doc, method):
    if doc.po_so_name_copy:
        #based on commission_po_so
        autoname = make_autoname('{}-'.format(doc.po_so_name_copy))
        doc.name = autoname[:-5]+autoname[-3:]
        