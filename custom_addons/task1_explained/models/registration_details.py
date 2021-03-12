from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Registration(models.Model):
    _name = 'registrations.details'
    _description = 'Registrations details'
    _rec_name = 'student'

    student = fields.Many2one('student.details', string="Student", required=True)
    batch_id = fields.Many2one('batch.details', string="Batches")
    #course_ids = fields.Many2many('course.details','registration_course_rel','reg_id','course_id',string="Course")
    # course_ids = fields.One2many(related="batch_id.course_ids",string="Course")
    course_ids = fields.Many2many('course.details', 'registration_course_rel', 'reg_id', 'course_id', string="Course")
    select_course = fields.Many2one(comodel_name='course.details')
    color = fields.Integer('Color Index', default=0)


    # course_tobe_print = fields.Many2many('batch.details', 'course_from_batch', 'batch', 'courses', string="Courses")
    # c_ids = fields.Char(related='course_ids.course_name', string='Courses')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done')
    ],string="Status", readonly= True, default = 'draft')

    currency_id = fields.Many2one(related='course_ids.currency_id', string="Currency", readonly=True,
                                  default=lambda self: self.env['res.currency'].browse([20]))
    total_fees = fields.Monetary(related="batch_id.total_fees", string="Total fees")


    def action_confirm(self):
        for rec in self:

            #--------------ORM Search method---------------#

            # students = self.env['registrations.details'].search([])
            # print(f"\n\n\n\n\n--------------Students----{students}---\n\n\n\n")

            # female_students = self.env['registrations.details'].search([('gender','=','female')])
            # print(f"\n\n\n\n\n--------------Students----{female_students}---\n\n\n\n")

            #------ABOVE 2LINES WILL CEARTE AN ERROR BCOZ THIS MODEL DOESN'T HAVE ANY FIELD NAME 'gender'

            rec.state= 'confirm'

    def action_done(self):
        for rec in self:
            rec.state= 'done'

    @api.onchange('batch_id')
    def onchange_batch_id(self):
        for rec in self:
            print(f"\n\n\n---------batch_id.course_ids---- :---{rec.batch_id.course_ids}--\n\n\n")
            rec.course_ids = rec.batch_id.course_ids

    # @api.onchange('batch_id')
    # def onchange_batch_id(self):
    #     for rec in self:
    #         rec.course_ids = rec.batch_id.course_ids.course_name

    @api.constrains('student')
    def one_registration_for_student(self):
        for rec in self:
            result = self.env['registrations.details'].search([('student', '=', rec.student.id)])
            if result:
                raise ValidationError(f'Registration for {rec.student.name.name} already exist.')
