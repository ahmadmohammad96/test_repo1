// Copyright (c) 2022, craft and contributors
// For license information, please see license.txt




const doc = cur_frm.doc

var take_code1 = doc.items[0].item_code[0]
var take_code2 = doc.items[0].item_code[1]
var final_code = take_code1 +  take_code2
const call_add = ()=>{

if (final_code == "S0") { 


	const add_data = () =>{
		cur_frm.add_custom_button('Asset Movement',() => {
	
			const doc = cur_frm.doc
			frappe.run_serially([
				() => frappe.new_doc('Asset Movement'),
				() => {
					
	
						const cur_doc = cur_frm.doc
						cur_doc.naming_series = doc.naming_series
						console.log(cur_doc.naming_series)
						console.log( doc.naming_series)
						console.log(cur_doc.name)
		
						cur_doc.transaction_date = doc.transaction_date
						
		
						// cur_doc.items = []
						console.log(doc.items)
						var ass_list = []
						// var many_arr = []

						var test = ['Aluminium Scrap High Magnesium' , 'Stainless Steel Scrap 200 series' , 'Aluminium Scrap Radiator' ]
						
						for (var i =0 ;  i < doc.items.length ; i ++  ) { 
							frappe.db.get_list('Asset', {
								fields: ['asset_name' , 'naming_series'],
								filters: {
									item_code: doc.items[i].item_code
								}
							}).then(records => {
								// console.log(records);
								ass_list.push(records)
								console.log(ass_list);
					console.log('OUTTT IF ---------------------')

					if (i+ 1 >= doc.items.length) { 
						console.log('IN IF ---------------------')

						for (const row of ass_list){
							for (const row2 of row) { 

								const new_row = cur_frm.add_child('assets', {
									'asset_name':row2.asset_name , 
									'naming_series': row2.naming_series
								})
								console.log(',,,,,,,,' , new_row)
								const cdt = new_row.doctype
								const cdn = new_row.name
								frappe.model.set_value(cdt, cdn, "asset_name", row2.asset_name)
								frappe.model.set_value(cdt, cdn, "naming_series", row2.naming_series)

						cur_frm.refresh()


							}

						}
						cur_frm.refresh()
						


								} // END if finishing the items 
								
		
							})
						} // END for iterating through items 

						// console.log(doc.items)
						
						
						// frappe.db.set_value("name", doc.name)
						// refresh_field("name")
						cur_frm.refresh()
	
	
					
				   
				}
			])
		}, 'Create Asset Movement')
		
	 
		
	} // END add_data()
	
	add_data()


	}else { 
		frappe.msgprint('Sorry - only FA items')
	}
	
	

}






const create_custom_button = () => {
    const doc = cur_frm.doc
    const status = doc.docstatus

    if (status == 1){
        call_add()
    }
}

frappe.ui.form.on('Material Request',{
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