frappe.ui.form.on("Purchase Order","onload",function(frm){
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
frappe.ui.form.on("Purchase Order Item", "item_code", function(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
 
    	setTimeout(() => {
    	   var Qty = row.qty;
    console.log("hi");
    frappe.model.set_value(cdt, cdn, "purchase_order_qty", Qty);
    frm.refresh_field('purchase_order_qty');
    	}, 1000);
});
frappe.ui.form.on("Purchase Order Item", "qty", function(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    var Qty = row.qty;
    console.log(Qty);
    frappe.model.set_value(cdt, cdn, "purchase_order_qty", Qty);
    frm.refresh_field('purchase_order_qty');
});




// frappe.ui.form.on("Purchase Order Item", "qty", function(frm, cdt, cdn) {
//     var row = locals[cdt][cdn];
//     var Qty = row.qty;
//     console.log(Qty);
//     frappe.model.set_value(cdt, cdn, "purchase_order_qty", Qty);
//     frm.refresh_field('purchase_order_qty');
// });


frappe.ui.form.on('Purchase Order', {
    // frm passed as the first parameter

    loading_by_no(frm) {
        // write setup code
        var take_date1 = frm.doc.loading_by_no // loading by date 
        var take_date2 = new Date() // currnet date 
        take_date2.setDate(take_date2.getDate() + take_date1);

        frm.set_value('schedule_date', take_date2)



    }
})

frappe.ui.form.on('Purchase Order', {
    // frm passed as the first parameter
    many_terms_and_conditions(frm) {
        var final_dic = ''
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


frappe.ui.form.on('Purchase Order', {
    // frm passed as the first parameter
    on_submit(frm) {
        // write setup code

        frm.set_value('purchase_order_number', frm.doc.name)
    }
})