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
    # _sql_constraints = [('unique_name', 'unique(name)', 'it already exits..')]

    name = fields.Char('name', required=False)
    address = fields.Char('address', default='idhar nai aneka')
    rollno = fields.Integer('Roll No.')
    phoneno = fields.Char('mobile')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ], 'Gender', default='male')
    company_name = fields.Char("Company Name", placeholder="enter the comapny name")
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

    # task_name = fields.One2many('tasks.tasks', 'student_id', string='Task names')
    # tasks_name = fields.Many2one('task.task', string='Task names')
    # tasks_done = fields.Boolean(related='tasks_name.task_done', string='is done')
    # task_fro=fields.One2many('task.task','task_id',string='task fro')

    @api.constrains("phoneno")
    def check_mobile_no(self):
        if str(self.phoneno) != 'False':
            if not str(self.phoneno).isdigit():
                raise ValidationError("Please enter valid mobile no.")
            else:
                if len(str(self.phoneno).strip()) != 10:
                    raise ValidationError("mobile no. size must be 10.")

    def name_get(self):

        student_name_gets = []
        for rec in self:
            print(f"\n\n{rec.professor_choose.name}\n\n\n")
            name = f"{rec.name} ({rec.rollno}) "
            print("hello")
            student_name_gets.append((rec.id, name))
        return student_name_gets

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

    # @api.constrains("name")
    # def unique_name(self):
    #     obj=0
    #     for record in self:
    #         obj = self.search([('name', '=', record.name), ('id', '!=', record.id)])
    #         if obj:
    #             raise ValidationError("name must be unique..")

    @api.onchange("name")
    def _compute_name(self):
        self.student_compute = 0
        for lead in self:
            if lead.name == 'manthan':
                lead.student_compute = "Welcome Manthan"
            else:
                lead.student_compute = (f"Welcome {lead.name}")

    @api.onchange("dob")
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

    @api.onchange('address')
    def address_unique(self):
        for lead in self:
            record = super(Students, self).default_get(['address'])
            print(f'\n\n\n\n{record}\n\n\n\n')
            lead.address = record['address']

    print("hello brother")

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

    def button_employee(self):
        return {
            'name': ('professor'),

            # 'view_type': 'tree',

            'view_mode': 'tree,form',

            'res_model': 'professor.professor',

            'domain': [('pro_id', '=', 5)],

            'type': 'ir.actions.act_window',  # this is predefined in odoo for redirection purpose aa fixed hoyy hamesha
        }
