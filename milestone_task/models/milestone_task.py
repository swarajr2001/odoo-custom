# -*- coding: utf-8 -*-
from odoo import fields, models


class MilestoneTasks(models.Model):
    """sale.order is inherited inorder to add create project button """
    _inherit = 'sale.order'
    is_created = fields.Boolean()

    def loop_order_line(self, created_project_id):
        milestone_tasks = {}
        for record in self.order_line:
            if record.milestone:
                self.is_created = True
                milestone = record.milestone
                name = "{}{}".format("milestone", milestone)
                task = milestone_tasks.get(milestone)
                if not task:
                    task = self.env['project.task'].create({
                        'name': name,
                        'project_id': created_project_id.id,
                        'partner_id': self.partner_id.id,
                    })
                    milestone_tasks[milestone] = task
                subtask_name = "{}-{}".format(name, record.product_template_id.name)
                task.child_ids = [fields.Command.create({
                    'name': subtask_name,
                })]

    def create_project(self):
        """this function responsible for creating the project"""
        for record in self.order_line:
            if record.milestone:
                created_project_id = self.env['project.project'].create({
                    'name': self.name,
                })
                self.project_id = created_project_id.id
                self.loop_order_line(created_project_id)
                break

    def update_project(self):
        print(self.project_id.task_ids)


class AddOrderLine(models.Model):
    """this model is inherited to add additional field in the sale order line"""
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string="Milestone")
