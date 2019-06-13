# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EngineDatabase(models.Model):
    _name = 'dbconnector.engine'
    _description = 'Databases Engine'
    _rec_name = 'name'

    name = fields.Char(string='Database Engine name', required=True)
    description = fields.Char(string='Description')

    _sql_constraints = [
            ('database_uniq', 'UNIQUE(name)',
                'Database Engine already exist'), ]

class Dbconnector(models.Model):
    _name = 'dbconnector.dbconnector'
    _description = 'Databases Conections'
    _rec_name = 'name'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

    name = fields.Char(string="Name Database", required=True)
    description = fields.Text(string="Description", required=True)
    host = fields.Char(string="Host", required=True)
    port = fields.Char(string="Port", required=True)
    user = fields.Char(string="User", required=True)
    password = fields.Char(string="Password", required=True)
    engine_id = fields.Many2one("dbconnector.engine", string="Engine",
            required=True)
    active = fields.Boolean(string="Active",
            help="Activate or deactivate record", default=True)

    _sql_constraints = [
            ('database_uniq', 'UNIQUE(name, host)',
                'Database already exist'), ]

    """
    @api.multi
    def name_get(self):
        result = []
        for dbconection in self:
            name = u"{0}-{1}".format(host, name)
            result.append((dbconection.id, name))
        return result"""

    @api.one
    def test_conection(self):
        response = []
        try:
            conn = pymssql.connect(self.host, self.user, self.password,
                    self.database)
            response = True, 'Conexión exitosa'
        except pymssql.Error as e:
            response = False, e
        return response

