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

    # @api.constrains("name")
    # def check_name(self):
    #     obj = 0
    #     for rec in self:
    #         print(f"\n\n\n rec.name {rec.name} \n\n\n")
    #         obj = self.search([('name', '=', rec.name)])
    #         if obj:
    #             raise ValidationError("sorry enter new name")

    def name_get(self):
        professor_name_gets = []
        print(f"\n\n\n\n\n{self.env.context.get('journal_idss')}\n\n\n\n")
        for rec in self:
            if self.env.context.get('journal_idss'):
                name = f"{rec.name}"
                print(f"\n\n--->>>{name}<<<---\n\n\n")
                professor_name_gets.append((rec.id, name))
            else:
                name = f"{rec.name}/{rec.pro_id}"
                print(f"\n\n--->>>{name}<<<---\n\n\n")
                professor_name_gets.append((rec.id, name))
        return professor_name_gets

