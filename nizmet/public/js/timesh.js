

frappe.ui.form.on('Timesheet' , {
    before_submit(frm){ 
        console.log(frm)

        // console.log(frm.ready_submit)
        // console.log(typeof (frm.ready_submit))

        if ( frm.doc.ready_submit ) { 

        }if (! frm.doc.ready_submit ){ 
            frm.set_value('time_logs' , [])
            frm.refresh_field('time_logs')
            frappe.throw('Can not submit - CheckBox 0_0')
        }
    }
})