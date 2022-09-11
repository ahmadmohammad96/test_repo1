frappe.ui.form.on("Commission Shipment","onload",function(frm){
    frm.set_query('commission_income_account_name',function(){
        return{
            'filters':{
                'account_type': 'Commission Receivable',
                'is_group':0 , 
                'company' : frm.doc.company

            }
        }
    }
    )
    frm.set_query('commission_expense_account_name',function(){
        return{
            'filters':{
                'account_type':'Commission Payable',
                'is_group':0 , 
                'company' : frm.doc.company

            }
        }
    })
    frm.set_query('commission_income_customer_account_name',function(){
        return{
            'filters':{
                'parent_account': 'Commission Receivable - NF',
                'is_group':0
            }
        }
    })
    frm.set_query('commission_expense_customer_account_name',function(){
        return{
            'filters':{
                'parent_account': 'Commission Payable - NF',
                'is_group':0
            }
        }
    })
}
)

frappe.ui.form.on("Commission Shipment Item", "item_code", function(frm, cdt, cdn) {
        
    var row = locals[cdt][cdn];
   frappe.model.get_value("Item", {'item_code':row.item_code},'item_name',
    function(e){
        frappe.model.set_value(cdt, cdn, "item_name",e.item_name );
    }    
   )
});

frappe.ui.form.on("Commission Shipment Item", "tare_weight", function(frm, cdt, cdn) {
        
    var row = locals[cdt][cdn];
    var net_weight_ = row.gross_weight-row.tare_weight
    frappe.model.set_value(cdt,cdn,'net_weight',net_weight_)
});

frappe.ui.form.on("Commission Shipment Item", "net_weight", function(frm, cdt, cdn) {
        
    var row = locals[cdt][cdn];
    var amount_ = row.invoice_price*row.net_weight
    frappe.model.set_value(cdt,cdn,'amount',amount_)
});

frappe.ui.form.on('Commission Shipment',{
    refresh: function(frm) {
		var me = this;
		if(frm.doc.docstatus > 0) {
			cur_frm.add_custom_button(__('Accounting Ledger'), function() {
				frappe.route_options = {
					voucher_no: frm.doc.name,
					from_date: frm.doc.posting_date,
					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
					company: frm.doc.company,
					group_by: "Group by Voucher (Consolidated)",
					show_cancelled_entries: frm.doc.docstatus === 2
				};
				frappe.set_route("query-report", "General Ledger");
			}, __("View"));
		}
	}

})






frappe.ui.form.on('Commission Shipment', {
    // frm passed as the first parameter
    loading_by_no(frm) {
        // write setup code
        var take_date1 = frm.doc.loading_by_no // loading by date 
        var take_date2 = new Date() // currnet date 
        take_date2.setDate(take_date2.getDate() + take_date1);

        frm.set_value('schedule_date', take_date2)
        frm.set_value('shipment_due_date' , take_date2 )


    }
})






frappe.ui.form.on('Commission Shipment', {
    // frm passed as the first parameter
    many_terms_and_conditions(frm) {
        var final_dic = ''
  
//             console.log(frm.doc.many_terms_and_conditions)
            
            for (var i=0 ; i < frm.doc.many_terms_and_conditions.length; i++) { 


                frappe.db.get_doc('Terms and Conditions', frm.doc.many_terms_and_conditions[i].termsandconditions)
                .then(doc => {
                console.log(doc)
                final_dic = final_dic + '\n' + '\n' + doc.terms
                
                console.log(final_dic)
            frm.set_value('terms' , final_dic )

             })    
            }

            
        
    }
})
