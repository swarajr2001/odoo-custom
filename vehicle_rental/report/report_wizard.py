# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import date_utils
import io
import json

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ReportWizard(models.TransientModel):
    """model for the popup wizard"""
    _name = 'vehicle.report'

    from_date = fields.Date(string="From date")
    partner_ids = fields.Many2many('res.partner', string="Customer")
    to_date = fields.Date(string="To date")
    vehicle_name = fields.Many2one('vehicle.details', string="Vehicle name")

    @api.constrains('from_date', 'to_date')
    def _check_date_range(self):
        """function to check to date is earlier than from date"""
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From date must be earlier than To date.")

    def query(self):
        """this function provide the query for the required report"""
        customer_ids = self.partner_ids.ids
        from_date = self.from_date
        to_date = self.to_date
        vehicle_id = self.vehicle_name.id
        query = """select res_partner.name as customer , vehicle_details.name as model,
                                                        period,states from vehicle_request join 
                                                        res_partner on vehicle_request.partner_id = res_partner.id
                                                        join vehicle_details on 
                                                        vehicle_details.id = vehicle_request.vehicle_id"""
        params = []
        flag = """"""
        if not from_date:
            flag = """ where """

        if from_date:
            query = query + """ where vehicle_request.from_date >= %s """
            params.append(from_date)
            flag = """ and """
        if to_date:
            query = query + flag + """vehicle_request.to_date <=  %s"""
            params.append(to_date)
            flag = """ and """
        if vehicle_id:
            query = query + flag + """vehicle_request.vehicle_id = %s"""
            params.append(vehicle_id)
            flag = """ and """
        if customer_ids:
            query = query + flag + """vehicle_request.partner_id in %s"""
            params.append(tuple(customer_ids))
        self.env.cr.execute(query, tuple(params))
        report = self.env.cr.dictfetchall()
        if not report:
            raise UserError(_("No matching records to generate reports."))
        return report

    def action_confirm(self):
        """this button prints the pdf report"""
        report = self.query()
        datas = {
            'report': report,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'vehicle': self.vehicle_name.name,
        }
        return self.env.ref('vehicle_rental.action_report_vehicle_request').report_action(self, data=datas)

    def excel_generate(self):
        """this generates the Excel report"""
        report = self.query()
        data = {
            'report': report,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'customer_ids': self.partner_ids.ids,

        }
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'vehicle.report',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': 'Excel Report',
            },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        report = data.get('report')
        from_date = data['from_date']
        to_date = data['to_date']
        partner_ids = data['customer_ids']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        customer = workbook.add_format(
            {'font_size': '12px', 'align': 'left'})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'left'})

        style = workbook.add_format({
            'font_size': '12px', 'align': 'left'})

        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '25px'})

        color = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'border': 2, 'border_color': 'black'})
        font = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'border_color': 'black'})
        today = datetime.today().date()
        sheet.write('A6', 'Print date:', style)
        sheet.write('B6', today, date_style)
        sheet.set_column(0, 0, 10)
        company_name = self.env.company.name
        company_street = self.env.company.street
        company_phone = self.env.company.phone
        sheet.write('D6', company_name, style)
        sheet.write('D7', company_street, style)
        sheet.write('D8', company_phone, style)

        if from_date:
            sheet.write('A9', 'From date:', style)
            sheet.write('B9', from_date, date_style)
        if to_date:
            sheet.write('A10', 'To Date', style)
            sheet.write('B10', to_date, date_style)

        if len(partner_ids) == 1:
            sheet.merge_range('A1:D2', 'Vehicle Rental Excel Report', head)
            partner_name = self.env['res.partner'].browse(partner_ids[0]).name
            sheet.write('A7', 'Customer:', style)
            sheet.write('B7', partner_name, customer)

            sheet.write('A12', 'SI.no', color)
            sheet.set_column(1, 12, 20)
            sheet.write('B12', 'Vehicle name', color)
            sheet.set_column(3, 7, 20)
            sheet.write('C12', 'Period', color)
            sheet.write('D12', 'State', color)
            row = 12
            col = 0
            lines = 12
            si = 1
            for dictionary in report:
                sheet.write(lines, 0, si, font)
                lines += 1
                si += 1
                sheet.write(row, col + 1, dictionary.get('model'), font)
                sheet.write(row, col + 2, dictionary.get('period'), font)
                sheet.write(row, col + 3, dictionary.get('states'), font)
                row += 1

        else:
            sheet.merge_range('A1:E2', 'Vehicle Rental Excel Report', head)
            sheet.write('A12', 'SI.no', color)
            sheet.set_column(1, 12, 20)
            sheet.write('B12', 'Customer', color)
            sheet.write('C12', 'Vehicle name', color)
            sheet.set_column(3, 7, 20)
            sheet.write('D12', 'Period', color)
            sheet.write('E12', 'State', color)
            row = 12
            col = 1
            lines = 12
            si = 1
            for dictionary in report:
                sheet.write(lines, 0, si, font)
                lines += 1
                si += 1
                for item in dictionary.values():
                    sheet.set_column(row, col, 20)
                    sheet.write(row, col, item, font)
                    col += 1
                row += 1
                col = 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


class VehicleReport(models.AbstractModel):
    _name = 'report.vehicle_rental.vehicle_request_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        """prints the pdf"""
        report = data['report']
        return {
            'data': data,
            'report': report,
        }
