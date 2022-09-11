import imp
import frappe
from frappe.utils import money_in_words

# def calculate_amount(doc, handler = None):
#     total_nt_wt = 0
#     total_amount = 0
#     for i in doc.items:
#         i.qty = i.gross_weight-i.tare_weight
        # i.amount = i.net_weight * i.rate
        # i.base_amount = i.net_weight * i.base_rate
        # total_amount += i.amount
        # total_nt_wt += i.net_weight
    # doc.total_net_weight = total_nt_wt
    # doc.total = total_amount
    # doc.net_total = doc.total-doc.discount_amount
    # doc.grand_total = doc.total-doc.discount_amount
    # doc.in_words = money_in_words(doc.grand_total)
    # doc.outstanding_amount = (doc.grand_total-doc.write_off_amount)-doc.paid_amount


# def calculate_net_weight(doc, handler = None):
#     for i in doc.items:
#         i.net_weight = i.gross