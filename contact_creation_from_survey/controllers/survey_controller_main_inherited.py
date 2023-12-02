# -*- coding: utf-8 -*-

from odoo.http import request
from odoo.addons.survey.controllers.main import Survey


class SurveyMainInherited(Survey):
    """inherited the controller and made suitable changes"""
    def survey_submit(self, survey_token, answer_token, **post):
        ans = super().survey_submit(survey_token, answer_token, **post)
        participation = request.env['survey.user_input'].search([('access_token', '=', post['token'])])
        if participation.state == 'done':
            survey = participation.survey_id
            contact_questions = survey.survey_question_ids

            participation_questions_ids = participation.user_input_line_ids.mapped('question_id.id')
            contact_question_ids = contact_questions.mapped('survey_questions_id.id')
            user_submission = []
            for lines in participation.user_input_line_ids:
                submitted_ans = {}
                submitted_ans[lines.question_id.id] = lines.display_name
                user_submission.append(submitted_ans)
            for id in participation_questions_ids:
                if id not in contact_question_ids:
                    user_submission = [item for item in user_submission if id not in item]
            user_submission = sorted(user_submission, key=lambda x: list(x.keys())[0])
            values = {}
            for rec in contact_questions:
                f_key = f'{rec.res_partner_fields_id.name}'
                for dict in user_submission:
                    for key, value in dict.items():
                        if rec.survey_questions_id.id == key:
                            values[f_key] = value
            check_key = 'name'
            if check_key in values:
                request.env['res.partner'].create(values)
        return ans
