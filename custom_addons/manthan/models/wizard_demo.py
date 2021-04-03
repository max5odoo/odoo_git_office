from odoo import models, fields, api


class TaskCreationReportWizard(models.TransientModel):
    _name = 'task.creation.report.wizard'
    _inherit = 'tasks.tasks'

    tasks_id = fields.One2many('tasks.tasks', 'student_id', string='Task names')
    task_name = fields.Char(string='Task Name')
    task_technology = fields.Char(string='Task Technology Used')

    # def set_data(self):
    #     fees = self.env['student.student'].browse(
    #         self._context.get("active_id")).read(['task_name'])
    #     print(f"n\n\n {fees} \n\n\n")
    #     new_fees = fees[0]['task_name']
    #     return new_fees


    # this is a wizard function ('ama apde potana student ni one2many ma create thai jay record---------particularly same student ma ')
    def create_new_button(self):
        events = self.env['student.student'].browse(self._context.get("active_id"))
        print(f"\n\nstudent normal - - {events}\n\n\n")
        student_data = events.write({
            'tasks_id': [(0, 0, {
                'task_name': self.task_name,
                'task_technology': self.task_technology
            })]
        })
        print(f"\n\nstudent data- - {student_data}\n\n\n")
        return student_data


