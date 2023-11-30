# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import date_utils
import io
import json

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class StockMoveReport(models.TransientModel):
    _name = 'advanced.stock'
    _description = 'transient model to generate pdf excel report based on the condition'

    product_id = fields.Many2one('product.product', string='Select product')
    form_date = fields.Date(string="From date")
    to_date = fields.Date(string="To date")
    stock_move_status = fields.Selection(selection=[
        ('done', 'Done'),
        ('assigned', 'Available'),
        ('partially_available', 'Partially Available'),
        ('confirmed', 'Waiting Availability'),
        ('waiting', 'Waiting Another Move'),
        ('cancel', 'Cancelled'),
        ('draft', 'New'),
    ], string="Stock move status")
    from_location_id = fields.Many2one('stock.location', string="From location")
    destination_id = fields.Many2one('stock.location', string='Destination')

    def query(self):
        """this function provide the query for the required report"""
        from_date = self.form_date
        to_date = self.to_date
        product_id = self.product_id.id
        destination_id = self.destination_id.id
        source_id = self.from_location_id.id
        status = self.stock_move_status
        query = """select pt.name::json->'en_US' AS name, product_uom_qty as "Quantity", date(stock_move.create_date) as "Date",
                        stock.complete_name as "Source location", s.complete_name as "Destination location", state as "status"
                        from stock_move 
                        join stock_location as stock on stock_move.location_id = stock.id
                        join stock_location as s on stock_move.location_dest_id = s.id
                        
                        join product_product as pp on stock_move.product_id = pp.id
                        
                        JOIN
                            product_template pt ON pp.product_tmpl_id = pt.id
                        """
        params = []
        flag = """"""
        if not from_date:
            flag = """ where """
        if from_date:
            query = query + """ where date(stock_move.create_date) >= %s """
            params.append(from_date)
            flag = """ and """
        if to_date:
            query = query + flag + """date(stock_move.create_date) <=  %s"""
            params.append(to_date)
            flag = """ and """
        if product_id:
            query = query + flag + """stock_move.product_id = %s"""
            params.append(product_id)
            flag = """ and """
        if source_id:
            query = query + flag + """stock_move.location_id = %s"""
            params.append(source_id)
            flag = """ and """
        if destination_id:
            query = query + flag + """stock_move.location_dest_id = %s"""
            params.append(destination_id)
            flag = """ and """
        if status:
            query = query + flag + """stock_move.state = %s"""
            params.append(status)

        self.env.cr.execute(query, tuple(params))
        report = self.env.cr.dictfetchall()
        if not report:
            raise UserError(_("No matching records to generate reports."))
        return report

    def excel_generate(self):
        """this generates the Excel report"""
        report = self.query()
        data = {
            'report': report,
            'from_date': self.form_date,
            'to_date': self.to_date,
            'product_id': self.product_id.id,
            'product_name': self.product_id.name

        }
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'advanced.stock',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': 'Excel Report',
            },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        from_date = data['from_date']
        to_date = data['to_date']
        product_name = data['product_name']
        report = data['report']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'left'})

        style = workbook.add_format({
            'font_size': '12px', 'align': 'left'})

        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '25px'})

        color = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'border': 2, 'border_color': 'black'})
        font = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'border_color': 'black'})
        sheet.set_column(0, 0, 10)
        today = datetime.today().date()
        sheet.write('A6', 'Print date:', style)
        sheet.write('B6', today, date_style)
        if from_date:
            sheet.write('A8', 'From date:', style)
            sheet.write('B8', from_date)
        if to_date:
            sheet.write('A9', 'To date:', style)
            sheet.write('B9', to_date)
        company_name = self.env.company.name
        company_street = self.env.company.street
        company_phone = self.env.company.phone

        sheet.write('D6', company_name, style)
        sheet.write('D7', company_street, style)
        sheet.write('D8', company_phone, style)

        sheet.merge_range('A1:F3', 'Advanced stock Excel Report', head)

        if product_name:
            sheet.write('A7', 'Product:', style)
            sheet.write('B7', product_name, style)
            sheet.write('A14', 'SI.no', color)
            sheet.set_column(1, 14, 35)
            sheet.write('B14', 'Quantity', color)
            sheet.write('C14', 'From', color)
            sheet.write('D14', 'To', color)
            sheet.write('E14', 'Date', color)
            sheet.write('F14', 'State', color)

            row = 14
            col = 0
            lines = 14
            si = 1
            for dictionary in report:
                sheet.write(lines, 0, si, font)
                lines += 1
                si += 1
                sheet.write(row, col + 1, dictionary.get('Quantity'), font)
                sheet.write(row, col + 2, dictionary.get('Source location'), font)
                sheet.write(row, col + 3, dictionary.get('Destination location'), font)
                sheet.write(row, col + 4, dictionary.get('Date'), font)
                sheet.write(row, col + 5, dictionary.get('status'), font)
                row += 1
        else:
            sheet.write('A14', 'SI.no', color)
            sheet.write('B14', 'Product Name', color)
            sheet.set_column(1, 14, 35)
            sheet.write('C14', 'Quantity', color)
            sheet.write('D14', 'From', color)
            sheet.write('E14', 'To', color)
            sheet.write('F14', 'Date', color)
            sheet.write('G14', 'State', color)

            row = 14
            col = 0
            lines = 14
            si = 1
            for dictionary in report:
                sheet.write(lines, 0, si, font)
                lines += 1
                si += 1
                sheet.write(row, col + 1, dictionary.get('name'), font)
                sheet.write(row, col + 2, dictionary.get('Quantity'), font)
                sheet.write(row, col + 3, dictionary.get('Source location'), font)
                sheet.write(row, col + 4, dictionary.get('Destination location'), font)
                sheet.write(row, col + 5, dictionary.get('Date'), font)
                sheet.write(row, col + 6, dictionary.get('status'), font)
                row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()



    def pdf_generate(self):
        """this button prints the pdf report"""
        report = self.query()
        datas = {
            'report': report,
            'from_date': self.form_date,
            'to_date': self.to_date,
            'state': self.stock_move_status,
            'product_id': self.product_id.name,
        }
        return self.env.ref('advanced_stock_move_report.action_report_advanced_stock').report_action(self, data=datas)

    class VehicleReport(models.AbstractModel):
        _name = 'report.advanced_stock_move_report.advance_stock_report'

        @api.model
        def _get_report_values(self, docids, data=None):
            """prints the pdf"""
            report = data['report']
            return {
                'data': data,
                'report': report,
            }
