# -*- coding: utf-8 -*-
import base64
from datetime import date, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class SalesReport(models.Model):
    """class defined for the weekly.sale.report model"""

    _name = 'report.sales'
    _description = "custom model for generating monthly weekly report"
    _rec_name = 'sequence'

    select_customer_ids = fields.Many2many('res.partner', string="Select customer", help="select customer",
                                           required=True)
    sales_team_id = fields.Many2one('crm.team', string="Select sales team", help="Select sales team")
    duration = fields.Selection(selection=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], string="Select timespan", help="select a time period", required=True)
    from_date = fields.Date(string="From date", help="Select from date", required=True)
    to_date = fields.Date(string="To date", help="select to date")
    sequence = fields.Char(required=True,
                           readonly=True, default=lambda self: _('New'), copy=False)

    @api.constrains('from_date', 'to_date')
    def _check_date_range(self):
        """function to check to date is earlier than from date"""
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From date must be earlier than To date.")

    @api.model
    def create(self, vals):
        """function to create sequence in sales report form"""
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'report.sales') or _('New')
            print(vals['sequence'])
        res = super(SalesReport, self).create(vals)
        return res

    def create_monthly_report(self):
        """function called by schedular to create monthly report"""
        today = date.today()
        record = self.env['report.sales'].search([('duration', '=', 'monthly')])
        record = record.filtered(lambda x: x.to_date == False or x.to_date >= today)
        self.create_sales_report(data=record)

    def create_weekly_report(self):
        """function called by schedular to create weekly report"""
        today = date.today()
        record = self.env['report.sales'].search([('duration', '=', 'weekly')])
        record = record.filtered(lambda x: x.to_date == False or x.to_date >= today)
        self.create_sales_report(data=record)

    def create_sales_report(self, data):
        """function when called creates the weekly report"""
        record = data
        today = date.today()
        for rec in record:
            # if rec.to_date >= today:
            if rec.duration == 'weekly':
                from_date = today - timedelta(7)
                to_date = today
            if rec.duration == 'monthly':
                from_date = today - timedelta(30)
                to_date = today
            query = """select res_partner.name as customer ,crm_team.name::json->'en_US' as sales_team,sale_order.user_id as sales_person,
                           date_order as order_date, sale_order.name as names, state as state,
                           amount_total as total from sale_order
                           join res_partner on sale_order.partner_id = res_partner.id
                           join crm_team on sale_order.team_id = crm_team.id"""
            params = []
            flag = """"""
            if not rec.from_date:
                flag = """ where """
            if rec.from_date is not False:
                query = query + """ where sale_order.date_order >= %s """
                params.append(rec.from_date)
                flag = """ and """
            if rec.to_date is not False:
                query = query + flag + """sale_order.date_order <=  %s"""
                params.append(rec.to_date)
                flag = """ and """
            if rec.sales_team_id.id is not False:
                query = query + flag + """sale_order.team_id = %s"""
                params.append(rec.sales_team_id.id)
            query = query + """ order by order_date"""
            self.env.cr.execute(query, tuple(params))
            report = self.env.cr.dictfetchall()
            customers = rec.select_customer_ids
            emails = ""
            for record in customers:
                if record.email:
                    emails = emails + str(record.email) + ","
            data = {'report': report,
                    'period': rec.duration,
                    'from_date': from_date,
                    'to_date': to_date,
                    }

            sales_report_pdf = self.env.ref('sales_report.action_report_sales_request')

            data_values = base64.b64encode(
                self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                    sales_report_pdf, data=data)[0])

            ir_values = {
                'name': "sales Report",
                'type': 'binary',
                'datas': data_values,
                'store_fname': data_values,
                'mimetype': 'application/x-pdf',
                'res_model': 'report.sales',
            }
            data_id = self.env['ir.attachment'].create(ir_values)
            template = self.env.ref('sales_report.sales_email_template')
            template.attachment_ids = [(6, 0, [data_id.id])]
            email_values = {
                'email_to': emails,
                'subject': f'{rec.duration} sales Report from {from_date} to {to_date}'
            }

            template.send_mail(self.id, email_values=email_values, force_send=True)
            template.attachment_ids = [(3, data_id.id)]
