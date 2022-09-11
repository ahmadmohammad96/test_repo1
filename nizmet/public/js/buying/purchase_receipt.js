frappe.ui.form.on("Purchase Receipt","onload",function(frm){
    frm.set_query('commission_income_account_name',function(){
        return{
            'filters':{
                'parent_account': 'Commission Receivable - N',
                'is_group':0
            }
        }
    }
    )
    frm.set_query('commission_expense_account_name',function(){
        return{
            'filters':{
                'parent_account':'Commission Payable - N',
                'is_group':0
            }
        }
    })
}
)