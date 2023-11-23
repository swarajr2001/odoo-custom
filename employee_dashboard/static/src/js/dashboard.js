/** @odoo-module **/
import { registry} from "@web/core/registry"
const { Component,useState} = owl
import { useService } from "@web/core/utils/hooks";
const rpc = require('web.rpc')
const { useRef } = owl;


class EmployeeDashboard extends Component {
        async setup() {
            this.state = useState({
                partner : {} ,
                payslip : {} ,
                upcoming_events : {},
                labels: undefined,
            });
            this.action = useService("action");
            var values = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_current_user",
                    });
            this.user_id = values
            var chart_values = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_chart_data",
                    });
            this.state.labels = chart_values['labels']
            this.count = chart_values['count']
            var employee = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_employee_data",
                    });
             this.state.partner = employee

             var task_data = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_task_details",
                    });
             this.task_name = task_data['task_name']
             this.task_deadline = task_data['task_deadline']

             var experience = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_user_experience",
                    });
             this.state.years = experience[0]
             this.state.days = experience[1]

             var payslip_data = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_payslip_details",
                    });
             this.state.payslip = payslip_data

             var leave_data = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_leave_details",
                    });
             this.leave_reason = leave_data['leave_reason']
             this.leave_days = leave_data['leave_days']

             var upcoming_event = await rpc.query({
                      model: "employee.dashboard",
                      method: "upcoming_event",
                    });
             this.state.upcoming_events = upcoming_event
             console.log(this)

            this.leave_chart = new Chart(
            $('#leave'),
            {
              type: 'bar',
              data: {
                labels: this.leave_reason,
                datasets: [{
                    backgroundColor: [
                          'rgba(208, 66, 255, 0.8)',
                          'rgba(228, 0, 87, 0.8)',
                          'rgba(0, 228, 182, 0.8)',

                        ],
                    label: 'Number of leaves',
                    data: this.leave_days
                  }
                ]
              }
            }
          );


          this.task_chart =   new Chart(
            $('#acquisitions'),
            {
              type: 'bar',
              data: {
                labels: this.state.labels,
                datasets: [{
                    backgroundColor: [
                          'rgba(208, 66, 255, 0.8)',
                          'rgba(228, 0, 87, 0.8)',
                          'rgba(0, 228, 182, 0.8)',

                        ],
                    label: 'Total task',
                    data: this.count
                  }
                ]
              }
            }
          );

          this.task_details = new Chart(
            $('#task_details'),
            {
              type: 'pie',
              data: {
                labels: this.task_name,
                datasets: [{
                    backgroundColor: [
                          'rgba(208, 66, 255, 0.8)',
                          'rgba(228, 0, 87, 0.8)',
                          'rgba(0, 228, 182, 0.8)',
                        ],
                    label: 'Days to complete',
                    data: this.task_deadline
                  }
                ]
              }
            }
          );

        }

        onClickAttendance(ev){
                ev.action.doAction({
                name: "Employee attendance",
                tag: "hr_attendance_my_attendances",
                target: "main",
                type: "ir.actions.client",
              });

        }

         async ThisMonthProjects(){
            var monthly_project= await rpc.query({
                      model: "employee.dashboard",
                      method: "get_monthly_project",
                    });
            this.task_chart.data.labels = monthly_project
            this.task_chart.update();

            var monthly_task= await rpc.query({
                      model: "employee.dashboard",
                      method: "get_monthly_task",
                    });
            this.task_details.data.labels = monthly_task[1]
            this.task_details.data.datasets[0].data = monthly_task[0]
            this.task_details.update();

            var monthly_leaves = await rpc.query({
                      model: "employee.dashboard",
                      method: "this_month_get_leave_details",
                    });
            this.leave_chart.data.labels = monthly_leaves['leave_reason']
            this.leave_chart.data.datasets[0].data = monthly_leaves['leave_days']
            this.leave_chart.update();

            var upcoming_event = await rpc.query({
                      model: "employee.dashboard",
                      method: "upcoming_event_this_month",
                    });
             this.state.upcoming_events = upcoming_event
        }



        async AllProject(){
            var all_project= await rpc.query({
                      model: "employee.dashboard",
                      method: "get_chart_data",
                    });
            this.task_chart.data.labels = all_project['labels']
            this.task_chart.update();

            var task_data = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_task_details",
                    });
             this.task_details.data.labels = task_data['task_name']
             this.task_details.data.datasets[0].data = task_data['task_deadline']
             this.task_details.update();

             var leave_data = await rpc.query({
                      model: "employee.dashboard",
                      method: "get_leave_details",
                    });
             this.leave_chart.data.labels = leave_data['leave_reason']
             this.leave_chart.data.datasets[0].data = leave_data['leave_days']
             this.leave_chart.update();

             var upcoming_event = await rpc.query({
                      model: "employee.dashboard",
                      method: "upcoming_event",
                    });
             this.state.upcoming_events = upcoming_event

        }


        MyInfo(ev){
            ev.action.doAction({
                name: "Employee info",
                type: 'ir.actions.act_window',
                views: [[false, "form"]],
                res_model: 'hr.employee',
                res_id: ev.user_id,
                target: 'main',
                context: "{'create': True}",
              });
        }

}

EmployeeDashboard.template = "EmployeeDashboard";

registry.category("actions").add("custom_dashboard_tags", EmployeeDashboard);