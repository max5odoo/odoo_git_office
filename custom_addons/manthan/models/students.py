import re

import self as self

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
# from datetime import datetime
import datetime, time
from datetime import timedelta, date
import math
import sys

sys.setrecursionlimit(2000)


class Students(models.Model):
    _name = 'student.student'
    _description = 'student description'
    _inherit = ['website.published.mixin', 'mail.thread', 'mail.activity.mixin']
    _sql_constraints = [('unique_names', 'unique(name)', 'it already exits..')]



    # use of ---->>>get_param<<<--- in default of company_name
    def get_the_set_value(self):
        res = self.env['ir.config_parameter'].sudo().get_param('manthan.company_name')
        return res

    name = fields.Char('name', required=False)
    # student_user = fields.Many2one('res.users', 'All users')
    address = fields.Char('address')
    rollno = fields.Integer('Roll No.')
    phoneno = fields.Char('mobile')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ], 'Gender', default='male')
    company_name = fields.Char("Company Name", placeholder="enter the comapny name", default=get_the_set_value)
    student_email = fields.Char()
    professor_choose = fields.Many2one('professor.professor', string='Professor')
    professor_id_read_only = fields.Char(related='professor_choose.address', string='Changable address ', readonly=True)
    student_signature = fields.Binary(string='Signature')
    active = fields.Boolean(default=True)
    handle_widget = fields.Integer()
    task_tech = fields.Many2one('tasks.tasks', string='task technologies')
    tasks_id = fields.One2many('tasks.tasks', 'student_id', string='Task names')
    student_compute = fields.Char('Invitation ', compute='_compute_name')
    age = fields.Integer("Age of student", compute='age_student', store=False)
    dob = fields.Date(string="Date of Birth", required=False, help="Date of Birth")
    pin_code = fields.Integer(string='Pincode ')
    pin_code_area = fields.Char('Area', compute='area_student')
    students_professor_id = fields.Char('professor id', compute='professor_unique_id')
    student_tasks_ids = tax_ids = fields.Many2many('tasks.tasks', 'student_student_task',
                                                   'student_id', 'tasks_id', string='student tasks')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancle', 'Canclled')], 'Student Status')
    total_proffesor = fields.Integer(string='total professor', compute='total_professors')
    # total_tasks = fields.Integer(string='total tasks', compute='total_taks')
    # new_task_id = fields.One2many('another.another', 'student_another', string='new one')
    sale_new = fields.Many2one('sale.order.line')
    sale_re = fields.Text(related='sale_new.name')
    new_name = fields.Char(string="New Name", readonly=True, required=True, copy=False, default='New')

    # here on creating the record the field new_name will have the sequence number ("ss000001") ..in short ir.sequence generate karva mate

    @api.model
    def create(self, vals):
        print(f"\n\n\nvals mate  {vals.get('new_name', 'new')}\n\n\n")
        print(
            f"\n\n\nset value mate--> {self.env['ir.config_parameter'].sudo().set_param('manthan.abc', 'manthan the boss')}\n\n\n")
        # use of ---->>>>set_param<<<<--- in ir.config_parameter
        self.env['ir.config_parameter'].sudo().set_param("manthan.company_name", "manthan the boss")
        # use of ---->>>>get_param<<<<--- in ir.config_parameter
        self.env['ir.config_parameter'].sudo().get_param('manthan.company_name')
        print(
            f"\n\n\nget value mate--------> {self.env['ir.config_parameter'].sudo().get_param('manthan.company_name')}\n\n")
        if vals.get('new_name', 'New') == 'New':
            vals['new_name'] = self.env['ir.sequence'].next_by_code(
                'cory') or 'New'
            # vals['name'] = self.env.user.name ----->>>>this is to print the current login user
        result = super(Students, self).create(vals)
        return result

    # @api.onchange('tasks_id')
    # def onchange_amo(self):
    #     for rec in self:
    #         print(f"\n\n\n\n\nname--------------\n\n\n\n\n")
    #         if rec.tasks_id:
    #             print(f"\n\n\n\n\nline ids--------------hii python\n\n\n\n\n")
    #             rec.write({'state': 'draft'})
    #         else:
    #             rec.update({'state': ''})

    # this is to count the total number of professor in student's form view button
    def total_professors(self):
        count = self.env['professor.professor'].search_count([('name', '=', self.name)])
        print(f"\n\n\nsearch_count {count}\n\n\n")
        self.total_proffesor = count

    # this is to count the total number of tasks in student's form view button
    def total_taks(self):
        pass

    #     count = self.env['another.another'].search_count([('student_another', '=', self.id)])
    #     print(f"\n\n\nsearch_count {count}\n\n\n")
    #     self.total_tasks = count

    # this is for validating the mobile number which was taken as integer fields
    @api.constrains("phoneno")
    def check_mobile_no(self):
        if str(self.phoneno) != 'False':
            if not str(self.phoneno).isdigit():
                raise ValidationError("Please enter valid mobile no.")
            else:
                if len(str(self.phoneno).strip()) != 10:
                    raise ValidationError("mobile no. size must be 10.")

    # def name_get(self):
    #     student_name_gets = []
    #     for rec in self:
    #         name = f"{rec.professor_choose.name}/{rec.professor_choose.pro_id} "
    #         student_name_gets.append((rec.id, name))
    #         print(f"\n\n\n\n\n\n{name}\n\n\n\n\n")
    #     return student_name_gets

    # here we have created a button_done function which we declared in xml file
    def button_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    # here we have created a button_reset function which we declared in xml file
    def button_reset(self):
        for rec in self:
            rec.state = "draft"

    # here we have created a button_cancel function which we declared in xml file
    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancle'})

    # @api.constrains("name")
    # def search_name_student(self):
    #
    #     searh_name_manthan = self.search(
    #         [('name', '!=', 'maxy')])
    #     print(f'\n\n\n\n\n{searh_name_manthan}\n\n\n')
    #     if searh_name_manthan:
    #         print("\n\n\n\n if ma jay che bete..\n\n\n")
    #         self.env['professor.professor'].create({
    #             'name': 'raja',
    #             'address': 'xyzabc',
    #             'pro_id': 505,
    #         })
    #     else:
    #         print("\n\n\n\n else ma bhi jay che\n\n\n")s

    @api.onchange("name")
    def _compute_name(self):
        self.student_compute = 0
        for lead in self:
            if lead.name == 'manthan':
                lead.student_compute = "Welcome Manthan"
            else:
                lead.student_compute = (f"Welcome {lead.name}")

    @api.depends("dob")
    def age_student(self):
        self.age = 0
        for rec in self:
            if rec.dob:
                your_date = rec.dob
                today_date = datetime.date.today()
                rec.age = abs((today_date - your_date).days // 365)

    @api.onchange("pin_code")
    def area_student(self):
        self.pin_code_area = 0
        for lead in self:
            pins_list = [(380061, 'GHATLODIA'), (380062, 'CHANAKYA PURI'), (3800563, 'SATADHAR')]
            for x in pins_list:
                if lead.pin_code == x[0]:
                    lead.pin_code_area = x[1]

    @api.onchange("professor_choose")
    def professor_unique_id(self):
        self.students_professor_id = 0
        for lead in self:
            if lead.professor_choose:
                lead.students_professor_id = lead.professor_choose.pro_id

    #
    # @api.onchange('address')
    # def address_unique(self):
    #     for lead in self:
    #         record = super(Students, self).default_get(['address'])
    #         print(f'\n\n\n\n{record}\n\n\n\n')
    #         lead.address = record['address']

    # @api.model
    # def create(self, values):
    #     z=self.env['student.student'].create(
    #         {
    #
    #
    #         }
    #     )
    #     return z

    # @api.model
    # def create(self, values):
    #     student_data = super(Students, self).create({
    #         'name': values["name"],
    #         'tasks_id': [(0, 0, {
    #             'task_name': 'dfbguiwfrwfhewbnofnhewvofnvie',
    #         })]
    #     })
    #     print(f"\n\nstudent - - {student_data}\n\n\n")
    #     return student_data

    # @api.model
    # def create(self, values):
    #     student_data = super(Students, self).create({
    #         'name': values["name"],
    #         'address': values['address'],
    #         'rollno': values['rollno'],
    #         'student_tasks_ids': [(0, 0, {
    #             'task_name': 'dfbguiwfrwfhewbnofnhewvofnvie',
    #         })]
    #     })
    #
    #     return student_data

    # def write(self, values):
    #     student_data = super(Students, self).write({
    #
    #         'tasks_id':[(5,0,0)]
    #     })
    #     print(f"\n\nstudent - - {student_data}\n\n\n")
    #     return student_data

    # @api.model
    # def create(self, vals):
    #     print(f"student vals {vals}")
    #     clg_student = super(Students, self).create(vals)
    #     course_dt = self.env['professor.professor'].create(
    #         {'name': 'Manthan sir '})
    #     vals['rollno'] = 10
    #     clg_student.write(vals)
    #     print('hello')
    #     return clg_student
    # #
    # def write(self, vals):
    #     # vals['email_id'] = 'aktiv_new@gmail.com'
    #     # professor_obj = super(Professors, self).search([])
    #     print(f"\n\n\n{super(Students, self).read()}\n\n\n")
    #     subject_records = super(Students, self).read(['tasks_id'])
    #     print(f"\n\n\n\n{subject_records[0]['tasks_id']}\n\n\n\n")
    #
    #     subject_lines_ids = subject_records[0]['tasks_id']
    #     single_sub_id = subject_lines_ids[0]['tasks_id'][0]
    #     # write into
    #     return self.env["student.student"].browse(
    #         [single_sub_id]).write({
    #         'task_name': 'master is always ..',
    #
    #     })

    # def write(self, vals):
    #     vals['student_email'] = 'aktiv@gmail.com'
    #     clg_up_student = super(Students, self).write(vals)
    #     print(f"\n\n\n\nthis is write method...{clg_up_student}\n\n\n\n\n")
    #     return clg_up_student

    def search_func(self):
        # search
        # search_res = self.env['student.student'].search(
        #     [('gender', '=', 'male')])
        # print(f"\n\n\n search() res : {search_res} \n\n\n")
        # # search_count
        # search_cnt = self.env['student.student'].search_count(
        #     ['', ])
        search_read = self.search_read([('name', '=', 'manthan')], fields=['student_email'])
        print(f"\n\n\nsearch_read {search_read}\n\n\n")

    # this is a button from which we can check student name is equal to professor name ,,accordingly, it shows the view
    def button_employee(self):

        for rec in self:
            name = rec.env['professor.professor'].search([('name', '=', self.name)])
            print(f"\n\n--->>>this is in the button name{name}<<<---\n\n\n")

            if name:
                return {
                    'name': ('professor'),

                    # 'view_type': 'tree',

                    'view_mode': 'tree,form',

                    'res_model': 'professor.professor',

                    'domain': [('name', '=', self.name)],

                    'type': 'ir.actions.act_window',
                    # this is predefined in odoo for redirection purpose aa fixed hoyy hamesha
                }

            else:

                return {
                    'name': ('professor'),

                    # 'view_type': 'tree',

                    'view_mode': 'form',

                    'res_model': 'professor.professor',

                    'type': 'ir.actions.act_window',
                    # this is predefined in odoo for redirection purpose aa fixed hoyy hamesha
                }

    # this is for wizard button placed inside the student form for opening the wizard
    # def open_wizard(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'task.creation.report.wizard',
    #         'target': 'new'
    #     }
    #
    def open_chatter_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'task.mail.report.wizard',
            'target': 'new'
        }

#
# class Another(models.Model):
#     _name = 'another.another'
#
#     student_another = fields.Many2one('student.student')
#     task_another_id = fields.Many2one('tasks.tasks', string='tasks')

