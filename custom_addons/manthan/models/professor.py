from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Professor(models.Model):
    _name = 'professor.professor'
    _description = 'professor description'


    name = fields.Char('name')
    address = fields.Char('address')
    pro_id = fields.Integer('pro_id')
    phoneno = fields.Char('phoneno')
    male = fields.Boolean()
    female = fields.Boolean()
    company_name = fields.Char("Company Name", placeholder="enter the comapny name")


    @api.constrains("phoneno")
    def check_mobile_no(self):
        if str(self.phoneno) != 'False':
            if not str(self.phoneno).isdigit():
                raise ValidationError("Please enter valid mobile no.")
            else:
                if len(str(self.phoneno).strip()) != 10:
                    raise ValidationError("mobile no. size must be 10.")
