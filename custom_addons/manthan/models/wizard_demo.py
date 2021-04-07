from odoo import models, fields, api


class TaskCreationReportWizard(models.TransientModel):
    _name = 'task.creation.report.wizard'
    _inherit = 'tasks.tasks'

    tasks_id = fields.One2many('tasks.tasks', 'student_id', string='Task names')
    # task_name = fields.Char(string='Task Name')
    # task_technology = fields.Char(string='Task Technology Used')
    task_new_id = fields.Many2many('tasks.tasks', 'task_task_wizard', 'wiz_id', 'task_id', string='tasks')

    # def set_data(self):
    #     fees = self.env['student.student'].browse(s
    #         self._context.get("active_id")).read(['task_name'])
    #     print(f"n\n\n {fees} \n\n\n")
    #     new_fees = fees[0]['task_name']
    #     return new_fees

    # this is a wizard function ('ama apde potana student ni one2many ma create thai jay record---------particularly same student ma ')
    # def create_new_button(self):
    #     events = self.env['student.student'].browse(self._context.get("active_id"))
    #     print(f"\n\nstudent normal - - {events}\n\n\n")
    #     student_data = events.create({
    #         'tasks_id': [(0, 0, {
    #             'task_name': self.task_name,
    #             'task_technology': self.task_technology
    #         })]
    #     })
    #     print(f"\n\nstudent data- - {student_data}\n\n\n")
    #     return student_data

    # this is a wizard function ('ama apde potana student  (4,id) use karyu che ni one2many ma create thai jay record---------particularly same student ma ')
    def create_new_button(self):
        new_task_ids = self.task_new_id
        print(f"n\n\n {new_task_ids} \n\n\n")
        for i in range(len(new_task_ids)):
            events = self.env['student.student'].browse(self._context.get("active_id"))
            print(f"\n\nstudent normal - - {events}\n\n\n")
            student_data = events.write({
                'tasks_id': [(4, new_task_ids[i].id)]
            })


class TaskMailWizard(models.TransientModel):
    _name = 'task.mail.report.wizard'
    activity_type_id = fields.Many2one(
        'mail.activity.type', string='Activity Type', readonly=True,
        default=lambda self: self.env['mail.activity.type'].search([('name', '=', 'To Do')])
    )
    summary = fields.Char('Summary')
    date_deadline = fields.Date('Due Date', index=True, default=fields.Date.context_today)
    user_id = fields.Many2one(
        'res.users', 'Assigned to',
        default=lambda self: self.env.user,
        index=True)

    def create_new_button(self):
        print(f"n\n\n context male:----{self.env.context} \n\n\n")
        data_res = self.env['ir.model'].search([('model', '=', self.env.context.get('active_model'))])
        print(f"n\n\n res data:----{data_res.model} \n\n\n")
        student_data = self.env['mail.activity'].create({
            'res_id': self.env.context.get('active_id'),
            'res_model_id': data_res.id,
            'activity_type_id': self.activity_type_id.id,
            'summary': self.summary,
            'date_deadline': self.date_deadline,
        })
        print(f"\n\nstudent - - {student_data}\n\n\n")
        return student_data
