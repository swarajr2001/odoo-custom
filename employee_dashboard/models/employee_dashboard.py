# -*- coding: utf-8 -*-
from datetime import date, datetime

from odoo import api, models


class EmployeeDashboard(models.Model):

    _name = 'employee.dashboard'
    _description = "this model represents the functionality of employee dashboard model"

    @api.model
    def get_current_user(self):
        """function returns the current user id"""
        current_user = self.env.user.employee_id.id
        return current_user

    @api.model
    def get_chart_data(self):
        """this function returns the data for project analysis"""
        projects = self.env['project.project'].search([('user_id', '=', self.env.user.id)])
        label = self.env['project.project'].search([('user_id', '=', self.env.user.id)]).mapped('display_name')
        task_count = []
        for project in projects:
            total_len = self.env['project.task'].search_count([('project_id', '=', project.id)])
            task_count.append(total_len)
        return {
            'labels': label,
            "count": task_count,
        }

    @api.model
    def get_employee_data(self):
        """this function returns the details of current user"""
        current_user_info = self.env.user.employee_id
        return {
            'name': current_user_info.name,
            'phone': current_user_info.work_phone,
            'email': current_user_info.work_email,
            'department': current_user_info.department_id.name,
            'job': current_user_info.job_id.name,
            'title': current_user_info.job_title,
            'image': current_user_info.image_1920,
            'birthday': current_user_info.birthday,
        }

    @api.model
    def get_task_details(self):
        """this function returns the task details of current user"""
        today = date.today()
        task = self.env['project.task'].search([('user_ids', '=', self.env.user.id)])
        get_task = task.filtered(lambda x: x.stage_id.name == 'In Progress' or x.stage_id.name == 'New')
        task_name = get_task.mapped('name')
        task_deadline = []
        for value in get_task:
            if value.date_deadline:
                remaining_day = abs(value.date_deadline - today)
                task_deadline.append(remaining_day.days)
        return {
            'task_name': task_name,
            'task_deadline': task_deadline,
        }

    @api.model
    def get_payslip_details(self):
        """this function returns the payslip details of current user"""
        employee_payslip = self.env['hr.payslip'].search([])
        payslip = employee_payslip.filtered(lambda x: x.employee_id.name == self.env.user.name)
        payslip = payslip[0]
        if payslip.contract_id.name:
            payslip_data = {
                'payslip_name': payslip.name,
                'wage': sum(payslip.mapped('line_ids.total')),
                'reference': payslip.number,
                'contract_name': payslip.contract_id.name,
            }
        else:
            payslip_data = {
                'payslip_name': payslip.name,
                'wage': sum(payslip.mapped('line_ids.total')),
                'reference': payslip.number,
                'contract_name': "No contract",
            }

        return payslip_data

    @api.model
    def get_leave_details(self):
        """this function returns the leave details of current user"""
        leave_data = self.env['hr.leave'].search([('employee_id', '=', self.env.user.employee_ids.id)])
        leave_reason = leave_data.mapped('name')
        leave_days = leave_data.mapped('number_of_days_display')
        return {
            'leave_reason': leave_reason,
            'leave_days': leave_days,
        }

    @api.model
    def upcoming_event(self):
        """this function returns data containing upcoming events like birthday of employees"""
        employee_birthday = self.env['hr.employee'].search([('birthday', '!=', False)])
        events = []
        for employee in employee_birthday:
            upcoming_events = {}
            upcoming_events['name'] = employee.name
            upcoming_events['birthday'] = str(employee.birthday)
            events.append(upcoming_events)
        return events

    @api.model
    def get_monthly_project(self):
        """this function returns the project details of current user of this month"""
        first_date = date.today().replace(day=1)
        last_date = date.today().replace(day=30)
        first_datetime = datetime.combine(first_date, datetime.min.time())
        last_datetime = datetime.combine(last_date, datetime.max.time())
        projects = self.env['project.project'].search([
            ('create_date', '>=', first_datetime),
            ('create_date', '<=', last_datetime),
            ('user_id', '=', self.env.user.id)
        ])
        names = projects.mapped('name')
        return names

    @api.model
    def get_monthly_task(self):
        """this function returns the task details of current user of this month"""
        today = date.today()
        first_date = date.today().replace(day=1)
        last_date = date.today().replace(day=30)
        first_datetime = datetime.combine(first_date, datetime.min.time())
        last_datetime = datetime.combine(last_date, datetime.max.time())
        task = self.env['project.task'].search([
            ('create_date', '>=', first_datetime),
            ('create_date', '<=', last_datetime),
            ('user_ids', '=', self.env.user.id)
        ])
        get_task = task.filtered(lambda x: x.stage_id.name == 'In Progress' or x.stage_id.name == 'New')
        task_name = get_task.mapped('name')
        task_deadline = []
        for value in get_task:
            if value.date_deadline:
                remaining_day = abs(value.date_deadline - today)
                task_deadline.append(remaining_day.days)
        return task_deadline, task_name

    @api.model
    def this_month_get_leave_details(self):
        """this function returns the leave details of current user this month"""
        today = date.today()
        first_date = date.today().replace(day=1)
        last_date = date.today().replace(day=30)
        leave_data = self.env['hr.leave'].search([('employee_id', '=', self.env.user.employee_ids.id),
                                                  ('request_date_from', '>=', first_date),
                                                  ('request_date_from', '<=', last_date),
                                                  ])
        leave_reason = leave_data.mapped('name')
        leave_days = leave_data.mapped('number_of_days_display')
        return {
            'leave_reason': leave_reason,
            'leave_days': leave_days,
        }

    @api.model
    def upcoming_event_this_month(self):
        """this function returns data containing upcoming events like birthday of employees"""
        today = date.today()
        first_date = date.today().replace(day=1)
        last_date = date.today().replace(day=30)
        employee_birthday = self.env['hr.employee'].search([('birthday', '!=', False),
                                                            ('birthday', '>=', first_date),
                                                            ('birthday', '<=', last_date),
                                                            ])
        events = []
        for employee in employee_birthday:
            upcoming_events = {}
            upcoming_events['name'] = employee.name
            upcoming_events['birthday'] = str(employee.birthday)
            events.append(upcoming_events)
        return events

    @api.model
    def get_user_experience(self):
        """function returns the experience level of current user"""
        user_experience = self.env['hr.contract'].search([('employee_id', '=', self.env.user.employee_ids.id),
                                                          ('state', '=', 'open')])
        today = date.today()
        experience = abs(user_experience.date_start - today).days
        years = experience // 365
        remaining_days = experience % 365
        return years, remaining_days






