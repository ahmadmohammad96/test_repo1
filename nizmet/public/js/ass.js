
frappe.ui.form.on("Asset","onload",function(frm){
    frm.set_query('item-code',function(){
        return{
            'filters':{
                'item_group' : 'Aluminium'
                // 'account_type': 'Commission Receivable',
                // 'is_group':0 , 
                // 'company' : frm.doc.company

            }
        }
    }
    )
    
    
  
    
}
)