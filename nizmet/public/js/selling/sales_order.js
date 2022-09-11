frappe.ui.form.on("Sales Order","onload",function(frm){
    console.log(frm)
    console.log(frm.doc.company)

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

    frm.set_query('port_of_loading',function(){
        return{
            'filters':[
                ['Port','port_of_loading','=',1],
			]
        }
    })
	
	frm.set_query('port_of_discharge',function(){
        return{
            'filters':[
                ['Port','port_of_discharge','=',1],
			]
        }
    })
}
)
frappe.ui.form.on("Sales Order Item", "item_code", function(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
 
    	setTimeout(() => {
    	   var Qty = row.qty;
    console.log("hi");
    frappe.model.set_value(cdt, cdn, "sales_order_qty", Qty);
    frm.refresh_field('sales_order_qty');
    	}, 1000);
});
frappe.ui.form.on("Sales Order Item", "qty", function(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    var Qty = row.qty;
    console.log(Qty);
    frappe.model.set_value(cdt, cdn, "sales_order_qty", Qty);
    frm.refresh_field('sales_order_qty');
});





frappe.ui.form.on('Sales Order', {
    // frm passed as the first parameter
    
    
    loading_by_no(frm) {
        // write setup code
        var take_date1 = frm.doc.loading_by_no // loading by date 
        var take_date2 = new Date() // currnet date 
        take_date2.setDate(take_date2.getDate() + take_date1);

        frm.set_value('schedule_date', take_date2)



    }
})




frappe.ui.form.on('Sales Order', {
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



// frappe.ui.form.on('Sales Order', {
//     refresh: function(frm) {
//       frm.add_custom_button(__('Create a sub-sales-invoice'), function(){
          
//         // frappe.msgprint('FUCK');
//         // console.log(frm.doc.customer)
//         // console.log(frm.doc.items)
//         // console.log(typeof(frm.doc.items))
//         const perc = frm.doc.percentage

//         if (perc != 1) {
//     //         frappe.db.count('Task', { status: 'Open' })

//     //         .then(count => {
//     //             console.log(count)
//     // })

//             // for (var i = 0; i< (frm.doc.items).length ; i ++ ) { 
//             //     perc[i].amount = (perc[i].amount * perc) / 100 

//             // }
//             console.log(frm.doc.cost_center)
//         frappe.db.insert({
//             doctype: 'Sales Invoice',
//             customer : frm.doc.customer ,
//             company : 'Alco Metal Trading LLC' , 
//             order_type : frm.doc.order_type , 
//             schedule_date : frm.doc.schedule_date , 
//             loading_by_no : frm.doc.loading_by_no , 
//             posting_date : frm.doc.transaction_date , 
//             due_date : new Date() , 
//             container_type : frm.doc.container_type , 
//             shipping_term : frm.doc.shipping_term , 
//             port_of_loading : frm.doc.port_of_loading , 
//             final_destination :frm.doc.final_destination , 
//             packing :frm.doc.packing , 
//             origin : frm.doc.origin, 
//             port_of_discharge : frm.doc.port_of_discharge, 
//             sold_by : frm.doc.sold_by , 
//             forwarder : frm.doc.forwarder, 
//             cost_center : 'Main - AM' , 

//             currency : frm.doc.currency, 
//             conversion_rate : frm.doc.conversion_rate, 
//             selling_price_list :frm.doc.selling_price_list , 
//             price_list_currency :frm.doc.price_list_currency , 
//             plc_conversion_rate :frm.doc.plc_conversion_rate , 
//             items : frm.doc.items , 
//             debit_to :frm.doc.debit_to  , 


//         }).then(doc => {
//             console.log(doc);
//         })
        
//     }// end if 


//     }, __("make sub invoice"));
//   }
// });



frappe.ui.form.on('Sales Order', {
    // frm passed as the first parameter
    on_submit(frm) {
        // write setup code

        frm.set_value('sales_order_number', frm.doc.name)
    }
})