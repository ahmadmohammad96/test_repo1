// frappe.uo.form.on('Commission PO_SO','refresh', function(frm){
//     frm.add_custom_button(__('Commission Shipment'),function(){
//         frappe.model.open_maped_doc({
//             method:'nizmet.nizmet.doctype.commission_po_so.commission_po_so.abc',
//             frm:cur_frm
//         })
//     })
// })
//


const doc = cur_frm.doc

const add_data = () =>{
    cur_frm.add_custom_button('Commission Shipment',() => {
        const doc = cur_frm.doc
        frappe.run_serially([
            () => frappe.new_doc('Commission Shipment'),
            () => {
                const cur_doc = cur_frm.doc
                cur_doc.naming_series = doc.naming_series
                console.log(cur_doc.naming_series)
                console.log( doc.naming_series)
                console.log(cur_doc.name)

                // cur_doc.name = doc.name
                cur_doc.company = doc.company
                cur_doc.date = doc.date
                cur_doc.time = doc.time
                cur_doc.supplier = doc.supplier
                cur_doc.supplier_so_no = doc.supplier_so_no
                cur_doc.purchased_by = doc.purchased_by
                cur_doc.supplier_payment_terms = doc.supplier_payment_terms
                cur_doc.customer = doc.customer
                cur_doc.buyer_po_no = doc.buyer_po_no
                cur_doc.sales_by = doc.sales_by
                cur_doc.buyer_payment_terms = doc.buyer_payment_terms
                cur_doc.commission_income_supplier_column = doc.commission_income_supplier_column
                cur_doc.commission_income_account_name = doc.commission_income_account_name
                cur_doc.commission_income_rate = doc.commission_income_rate
                cur_doc.commission_expense_account_name = doc.commission_expense_account_name
                cur_doc.commission_expense_rate = doc.commission_expense_rate
                cur_doc.commission_income_customer_account_name = doc.commission_income_customer_account_name
                cur_doc.commission_income_customer_rate = doc.commission_income_customer_rate
                cur_doc.commission_expense_customer_account_name = doc.commission_expense_customer_account_name
                cur_doc.commission_expense_customer_rate = doc.commission_expense_customer_rate
                cur_doc.cost_center = doc.cost_center
                cur_doc.shipment_due_date = doc.shipment_due_date
                cur_doc.shipping_term = doc.shipping_term
                cur_doc.origin = doc.origin
                cur_doc.port_of_loading = doc.port_of_loading
                cur_doc.port_of_discharge = doc.port_of_discharge
                cur_doc.final_destination = doc.final_destination
                cur_doc.packing = doc.packing
                cur_doc.item_description = doc.item_description
                cur_doc.advance_amount = doc.advance_amount
                cur_doc.paid_date = doc.paid_date
                cur_doc.po_so_name_copy = doc.name

                cur_doc.items = []
                for (const row of doc.items){
                    const new_row = cur_frm.add_child('items', {
                        'purchase_price':row.purchase_price,
                        'sales_price':row.sales_price,
                        'invoice_price':row.invoice_price,
                        'description':row.description,
                        'quantity':row.quantity
                    })
                    const cdt = new_row.doctype
					const cdn = new_row.name
                    frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                }
                // frappe.db.set_value("name", doc.name)
                // refresh_field("name")
                cur_frm.refresh()
            }
        ])
    }, 'Create')
    
 
    
}


const create_custom_button = () => {
    const doc = cur_frm.doc
    const status = doc.docstatus

    if (status == 1){
        add_data()
    }
}

frappe.ui.form.on('Commission PO_SO',{
    refresh (frm){
        create_custom_button(frm)
    }
    // refresh: function(frm){
    //     if(frm.doc.docstatus==Item Details 1){
    //         frm.add_custom_button(__("Commission Shipment"),
    //         () => frm.events.make_commission_shipment(frm), __('Create'));
    //     }
    // },
    // make_commission_shipment: function(frm){
    //     frappe.model.open_mapped_doc({
    //         method:'nizmet.nizmet.doctype.commission_po_so.commission_po_so.make_commission_shipment'
    //     })
    // }
})
frappe.ui.form.on("Commission PO_SO","onload",function(frm){
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

frappe.ui.form.on("Commission PO_SO Item", "item_code", function(frm, cdt, cdn) {
        
    var row = locals[cdt][cdn];
   frappe.model.get_value("Item", {'item_code':row.item_code},'item_name',
    function(e){
        frappe.model.set_value(cdt, cdn, "item_name",e.item_name );
    }    
   )
});

frappe.ui.form.on("Commission PO_SO Item", "quantity", function(frm, cdt, cdn) {
        
    var row = locals[cdt][cdn];
    var purch_amount = row.purchase_price*row.quantity
    var sal_amount = row.sales_price * row.quantity
    var inv_amount = row.invoice_price * row.quantity

    frappe.model.set_value(cdt,cdn,'amount',purch_amount)
    frappe.model.set_value(cdt,cdn,'sales_amount',sal_amount)
    frappe.model.set_value(cdt,cdn,'invoice_amount',inv_amount)


});

// frappe.ui.form.on('Commission PO_SO',{
//     refresh(frm){
//         create_custom_buttons(frm)
//     }
// })






frappe.ui.form.on('Commission PO_SO', {
    // frm passed as the first parameter
    loading_by_no: function(frm) {
        // write setup code
        // var take_date1 = frm.doc.loading_by_no // loading by date 
        var take_date1 = frm.doc.loading_by_no //no. of days 
        var take_date2 = new Date() // currnet date 
        take_date2.setDate(take_date2.getDate() + take_date1);

        frm.set_value('schedule_date', take_date2)
        frm.set_value('shipment_due_date' , take_date2 )

    }
})






frappe.ui.form.on('Commission PO_SO', {
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
