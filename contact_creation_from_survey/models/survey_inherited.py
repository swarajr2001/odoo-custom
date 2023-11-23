# -*- coding: utf-8 -*-

from odoo import fields, models


class SurveySurvey(models.Model):
    """inherited survey survey and added field """
    _inherit = 'survey.survey'

    survey_question_ids = fields.One2many('survey.contact', 'survey_id')


class ContactCreation(models.Model):
    """Added a new model to inherited by survey.survey for the tree view"""
    _name = 'survey.contact'

    survey_id = fields.Many2one('survey.survey')
    survey_questions_id = fields.Many2one('survey.question', domain="[('survey_id', '=', survey_id)]")
    res_partner_fields_id = fields.Many2one('ir.model.fields', domain=[('model_id.name', '=', 'Contact')])
