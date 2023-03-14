# from wsgiref import validate
from . import __version__ as _app_version

app_name = "nizmet"
app_title = "Nizmet"
app_publisher = "craft"
app_description = "Nizmet Trading"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@craftinteractive.ae"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nizmet/css/nizmet.css"
# app_include_js = "/assets/nizmet/js/nizmet.js"

# include js, css files in header of web template
# web_include_css = "/assets/nizmet/css/nizmet.css"
# web_include_js = "/assets/nizmet/js/nizmet.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "nizmet/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	# "doctype" : "public/js/doctype.js"
	'Purchase Order':'public/js/buying/purchase_order.js',
	'Purchase Receipt':'public/js/buying/purchase_receipt.js',
	'Purchase Invoice':'public/js/buying/purchase_invoice.js',
	'Sales Order':'public/js/selling/sales_order.js',
	'Sales Invoice':'public/js/selling/sales_invoice.js',
	# 'Commission PO_SO':'public/js/commission_po_so.js',
	# 'Commission Shipment':'public/js/commission_shipment.js',
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "nizmet.install.before_install"
# after_install = "nizmet.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "nizmet.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
	"Sales Invoice":{
		"on_submit":"nizmet.events.sales_invoice_gl_entry.create_gl",
		# "validate":'nizmet.events.sales_invoice.calculate_amount',
		# 'onload':[
		# 	'nizmet.events.naming.sales_invoice_autoname',
		# ]
		'autoname':'nizmet.events.naming.sales_invoice_autoname',
	},
	"Purchase Invoice":{
	"on_submit":"nizmet.events.purchase_invoice_gl_entry.create_gl",
	'autoname':'nizmet.events.naming.purchase_invoice_autoname',
	},
	"Commission Shipment":{
		"autoname":"nizmet.events.naming.commission_shipment_autoname"
	}
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"nizmet.tasks.all"
# 	],
# 	"daily": [
# 		"nizmet.tasks.daily"
# 	],
# 	"hourly": [
# 		"nizmet.tasks.hourly"
# 	],
# 	"weekly": [
# 		"nizmet.tasks.weekly"
# 	]
# 	"monthly": [
# 		"nizmet.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "nizmet.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "nizmet.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "nizmet.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"nizmet.auth.validate"
# ]

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", 
			[

				#Purchase Order
				'Purchase Order-shipment_due_date',
				'Purchase Order-section_break_16',
				'Purchase Order-shipping_term',
				'Purchase Order-port_of_loading',
				'Purchase Order-final_destination',
				'Purchase Order-packing',
				'Purchase Order-item_description',
				'Purchase Order-column_break_21',
				'Purchase Order-origin',
				'Purchase Order-port_of_discharge',
				'Purchase Order-purchased_by',
				'Purchase Order-allocation',
				'Purchase Order Item-purchase_order_qty',
				# 'Purchase Order-section_break_24',
				# 'Purchase Order-column_break_28',
				'Purchase Order-commission',
				'Purchase Order-commission_income',
				'Purchase Order-commission_income_account_name',
				'Purchase Order-commission_income_rate',
				'Purchase Order-commission_expense',
				'Purchase Order-commission_expense_account_name',
				'Purchase Order-commission_expense_rate',
				'Purchase Order-bl_details',
				'Purchase Order-shipper',
				'Purchase Order-shipper_address',
				'Purchase Order-notify',
				'Purchase Order-notify_address',
				'Purchase Order-bl_description',
				'Purchase Order-column_break_43',
				'Purchase Order-consignee',
				'Purchase Order-consignee_address',
				'Purchase Order-bank',
				'Purchase Order-bank_details',
				'Purchase Order-supplier_so_no',
				#'Purchase Order-cost_center',
				'Purchase Order-naming_series-options',
				'Purchase Order-naming_series-default',
				'Purchase Order-container_type',
				'Purchase Order-forwarder',
				'Purchase Order-detailed_payment_term',


				#Purchase Invoice 
				'Purchase Invoice commission_column_break',
				'Purchase Invoice purchase_order',
				'Purchase Invoice-shipping_term_column_break',
				'Purchase Invoice-shipping_term_column_break_2',
				'Purchase Invoice-shipping_term_column_break_3',
				'Purchase Invoice-item_description',
				'Purchase Invoice-commission',
				#'Purchase Invoice-cost_center',
				'Purchase Invoice-accounting_dimensions_section',
				'Purchase Invoice-supplier_invoice_details',
				'Purchase Invoice-shipping_line',
				'Purchase Invoice-shipping_details',
				'Purchase Invoice-bl_no',
				'Purchase Invoice-etd',
				'Purchase Invoice-shipping_details_column_1',
				'Purchase Invoice-eta',
				# 'Purchase Invoice-bl_status',
				'Purchase Invoice-vessel_voyage_name_pending',
				'Purchase Invoice-schedule_date',
				'Purchase Invoice-supplier_so_no',
				'Purchase Invoice-shipping_term',
				'Purchase Invoice-origin',
				'Purchase Invoice-port_of_loading',
				'Purchase Invoice-port_of_discharge',
				'Purchase Invoice-final_destination',
				'Purchase Invoice-purchased_by',
				'Purchase Invoice-packing',
				'Purchase Invoice-allocation',
				'Purchase Invoice-item_description',
				'Purchase Invoice-commission',
				'Purchase Invoice-commission_income',
				'Purchase Invoice-commission_income_account_name',
				'Purchase Invoice-commission_income_rate',
				'Purchase Invoice-commission_expense',
				'Purchase Invoice-commission_expense_account_name',
				'Purchase Invoice-commission_expense_rate',
				'Purchase Invoice-naming_series-options',
				'Purchase Invoice-naming_series-default',
				'Purchase Invoice-bl_status',
				'Purchase Invoice-forwarder',
				'Purchase Invoice-detailed_payment_term',
				#Purchase Invoice Item
				'Purchase Invoice Item-tare_weight',
				'Purchase Invoice Item-net_weight',
				'Purchase Invoice Item-gross_weight',
				'Purchase Invoice Item-purchase_order_qty',

				#Purchase Receipt
				'Purchase Receipt-supplier_so_no',
				'Purchase Receipt-shipment_due_date',
				'Purchase Receipt-section_break_18',
				'Purchase Receipt-shipping_term',
				'Purchase Receipt-port_of_loading',
				'Purchase Receipt-final_destination',
				'Purchase Receipt-packing',
				'Purchase Receipt-item_description',
				'Purchase Receipt-column_break_24',
				'Purchase Receipt-origin',
				'Purchase Receipt-port_of_discharge',
				'Purchase Receipt-purchased_by',
				'Purchase Receipt-allocation',
				'Purchase Receipt-commission',
				'Purchase Receipt-commission_income',
				'Purchase Receipt-commission_income_account_name',
				'Purchase Receipt-commission_income_rate',
				'Purchase Receipt-commission_expense',
				'Purchase Receipt-commission_expense_account_name',
				'Purchase Receipt-commission_expense_rate',
				'Purchase Receipt-bl_details',
				'Purchase Receipt-shipper',
				'Purchase Receipt-shipper_address',
				'Purchase Receipt-notify',
				'Purchase Receipt-notify_address',
				'Purchase Receipt-bl_description',
				'Purchase Receipt-column_break_73',
				'Purchase Receipt-consignee',
				'Purchase Receipt-consignee_address',
				'Purchase Receipt-bank',
				'Purchase Receipt-bank_details',
				
				#Sales Order
				'Sales Order-shipment_due_date',
				'Sales Order-section_break_18',
				'Sales Order-shipping_term',
				'Sales Order-port_of_loading',
				'Sales Order-final_destination',
				'Sales Order-packing',
				'Sales Order-item_description',
				'Sales Order-column_break_24',
				'Sales Order-origin',
				'Sales Order-port_of_discharge',
				'Sales Order-sold_by',
				'Sales Order-allocation',
				'Sales Order-commission',
				'Sales Order-commission_income',
				'Sales Order-commission_income_account_name',
				'Sales Order-commission_income_rate',
				'Sales Order-commission_expense',
				'Sales Order-commission_expense_account_name',
				'Sales Order-commission_expense_rate',
				'Sales Order-bl_details',
				'Sales Order-shipper',
				'Sales Order-shipper_address',
				'Sales Order-notify',
				'Sales Order-notify_address',
				'Sales Order-bl_description',
				'Sales Order-column_break_73',
				'Sales Order-consignee',
				'Sales Order-consignee_address',
				'Sales Order-bank',
				#'Sales Order-cost_center',
				'Sales Order-bank_details',
				'Sales Order-sales_order_qty',
				'Sales Order-naming_series-options',
				'Sales Order-naming_series-default',
				'Sales Order-container_type',
				'Sales Order-forwarder',
				'Sales Order-detailed_payment_term'


				#Sales Invoice
				'Sales Invoice-section_break_22',
				'Sales Invoice-shipping_term',
				'Sales Invoice-port_of_loading',
				'Sales Invoice-final_destination',
				'Sales Invoice-packing',
				'Sales Invoice-item_description',
				'Sales Invoice-column_break_28',
				'Sales Invoice-origin',
				'Sales Invoice-port_of_discharge',
				'Sales Invoice-sold_by',
				'Sales Invoice-allocation',
				'Sales Invoice-commission',
				'Sales Invoice-commission_income',
				'Sales Invoice-commission_income_account_name',
				'Sales Invoice-commission_income_rate',
				'Sales Invoice-commission_expense',
				'Sales Invoice-commission_expense_account_name',
				'Sales Invoice-commission_expense_rate',
				'Sales Invoice-naming_series-options',
				'Sales Invoice-naming_series-default',
				'Sales Invoice-forwarder',
				'Sales Invoice-detailed_payment_term',

				#Sales Invoice Item
				'Sales Invoice Item-gross_weight',
				'Sales Invoice Item-tare_weight',
				'Sales Invoice Item-sales_order_qty',

				#Company
				'Company-default_commission_income',
				'Company-default_commission_expense',






			]
			]
        ]
    },
	{
		"dt":"Property Setter",
		"filters":[
			["name","in",[
				'Sales Order-customer-allow_on_submit',
				'BL Description-bl_description-fieldtype',
				'Shipper-shipper_address-fieldtype',
				'Notify Info-notify_address-fieldtype',
				'Purchase Invoice-due_date-label',
				'Purchase Invoice Item-rate-columns',
				'Purchase Invoice Item-item_code-columns',
				'Purchase Invoice Item-amount-columns',
				'Sales Order-due_date-print_hide',
				'Sales Order-payment_schedule-print_hide',
				'Sales Invoice-due_date-print_hide',
				'Sales Invoice-payment_schedule-print_hide',
				'Purchase Order-due_date-print_hide',
				'Purchase Order-payment_schedule-print_hide',
				'Purchase Invoice-due_date-print_hide',
				'Purchase Invoice-payment_schedule-print_hide',
				'Sales Invoice Item-discount_account-hidden',
				'Sales Invoice Item-discount_account-mandatory_depends_on',
				'Purchase Invoice Item-discount_account-hidden',
				'Purchase Invoice Item-discount_account-mandatory_depends_on',
				'Sales Invoice-additional_discount_account-hidden',
				'Sales Invoice-additional_discount_account-mandatory_depends_on',
				'Purchase Invoice-additional_discount_account-hidden',
				'Purchase Invoice-additional_discount_account-mandatory_depends_on',
				'Item-default_discount_account-hidden',
				'Sales Invoice-naming_series-default',
				'Payment Term-due_date_based_on-options',
				'Purchase Order-tax_category-hidden',
				'Purchase Order-taxes_and_charges-hidden',
				'Purchase Order-taxes-hidden',
				'Purchase Invoice-tax_category-hidden',
				'Purchase Invoice-taxes_and_charges-hidden',
				'Purchase Invoice-taxes-hidden',
				'Purchase Invoice-base_taxes_and_charges_added-hidden',
				'Purchase Invoice-taxes_and_charges_deducted-hidden',
				'Purchase Invoice-total_taxes_and_charges-hidden',
				'Purchase Invoice-taxes_and_charges_added-hidden',
				'Sales Order-tax_category-hidden',
				'Sales Order-taxes_and_charges-hidden',
				'Sales Order-taxes-hidden',
				'Sales Order-base_total_taxes_and_charges-hidden',
				'Sales Order-total_taxes_and_charges-hidden',
				'Sales Order-shipping_rule-hidden',
				'Sales Invoice-taxes_and_charges-hidden',
				'Sales Invoice-shipping_rule-hidden',
				'Sales Invoice-tax_category-hidden',
				'Sales Invoice-taxes-hidden',
				'Sales Invoice-other_charges_calculation-hidden',
				'Sales Invoice-base_total_taxes_and_charges-hidden',
				'Sales Invoice-select_print_heading-hidden',
				'Sales Invoice-language-hidden',
				'Purchase Order-shipping_rule-hidden',
				'Purchase Invoice-shipping_rule-hidden',
				
				'Sales Invoice Item-qty-columns',
				
				'Sales Invoice Item-qty-label',
				'Purchase Invoice Item-item_code-label',
				'Purchase Order Item-item_code-label',
				'Sales Invoice Item-item_code-label',
				'Sales Order Item-item_code-label',
				'Consignee-consignee_address-fieldtype',
				'Purchase Invoice Item-qty-label',
				'Purchase Order-schedule_date-label',
				'Sales Invoice Item-qty-label',
				'Account-account_type-options',

			]
			]
		]
	}

]
