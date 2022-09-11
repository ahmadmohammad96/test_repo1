frappe.ui.form.on("Purchase Invoice","onload",function(frm){
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

frappe.ui.form.on("Purchase Invoice Item", "gross_weight", function (frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	var poQunatity=row.purchase_order_qty*10/100;
	var a;

    if(parseFloat(row.gross_weight) <= parseFloat(row.tare_weight)){
		frappe.model.set_value(cdt, cdn, "tare_weight", parseFloat(0)) ;
	}
	else{
	 a = parseFloat(row.gross_weight) -parseFloat(row.tare_weight);
	 console.log(poQunatity + row.purchase_order_qty);
	 if(a<=parseFloat(poQunatity) + parseFloat(row.purchase_order_qty)){
        frappe.model.set_value(cdt, cdn, "qty", parseFloat(a));
	 }
	 else{
		frappe.msgprint("Net Weight must be 10% of po Quantity");
	 }
	}
		frm.refresh_field("tare_weight"),
        frm.refresh_field("amount"),
        frm.refresh_field("accepted_rate"),
        frm.refresh_field("total"),
        frm.refresh_field("gross_weight");
		frm.refresh_field("qty");

});
frappe.ui.form.on("Purchase Invoice Item", "tare_weight", function (frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	var poQunatity=row.purchase_order_qty*10/100;
	var a;

    if(parseFloat(row.gross_weight) <= parseFloat(row.tare_weight)){
		frappe.model.set_value(cdt, cdn, "tare_weight", parseFloat(0)) ;
	}
	else{
	 a = parseFloat(row.gross_weight) -parseFloat(row.tare_weight);
	 console.log(poQunatity + row.purchase_order_qty);
	 if(a<=parseFloat(poQunatity) + parseFloat(row.purchase_order_qty)){
        frappe.model.set_value(cdt, cdn, "qty", parseFloat(a));
	 }
	 else{
		frappe.msgprint("Net Weight must be 10% of po Quantity");
	 }
	}
		frm.refresh_field("tare_weight"),
        frm.refresh_field("amount"),
        frm.refresh_field("accepted_rate"),
        frm.refresh_field("total"),
        frm.refresh_field("gross_weight");
		frm.refresh_field("qty");
});
frappe.ui.form.on("Purchase Invoice Item", "qty", function (frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	var poQunatity=row.purchase_order_qty*10/100;
	var a;

    if(parseFloat(row.gross_weight) <= parseFloat(row.tare_weight)){
		frappe.model.set_value(cdt, cdn, "tare_weight", parseFloat(0)) ;
	}
	else{
	 a = parseFloat(row.gross_weight) -parseFloat(row.tare_weight);
	 console.log(poQunatity + row.purchase_order_qty);
	 if(a<=parseFloat(poQunatity) + parseFloat(row.purchase_order_qty)){
        frappe.model.set_value(cdt, cdn, "qty", parseFloat(a));
	 }
	 else{
		frappe.msgprint("Net Weight must be 10% of po Quantity");
	 }
	}
		frm.refresh_field("tare_weight"),
        frm.refresh_field("amount"),
        frm.refresh_field("accepted_rate"),
        frm.refresh_field("total"),
        frm.refresh_field("gross_weight");
		frm.refresh_field("qty");
});




frappe.ui.form.on('Purchase Invoice', {
    // frm passed as the first parameter

    loading_by_no(frm) {
        // write setup code
        var take_date1 = frm.doc.loading_by_no // loading by date 
        var take_date2 = new Date() // currnet date 
        take_date2.setDate(take_date2.getDate() + take_date1);

        frm.set_value('schedule_date', take_date2)



    }
})




frappe.ui.form.on('Purchase Invoice', {
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


