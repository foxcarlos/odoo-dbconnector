# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError, Warning, currentframe

import importlib

# import mysql.connector as mysql
import pymysql  # Nueva libreria
import pymssql
import sqlite3

class MessageBox(models.TransientModel):
    _name = 'dbconnector.messagebox'
    _description = 'MessageBox Popup'
    _rec_name = 'text'

    def _default_engine(self):
        engine_obj = self.env['dbconnector.engine']
        engine_id = self._context.get('active_id')
        engine_record = engine_obj.browse(engine_id)
        return engine_record

    engine_id = fields.Many2one("dbconnector.engine", string="Engine",
            required=True, default=_default_engine)
    text = fields.Text()

    def _reopen_form(self):
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    def test_module_install(self):
        msg_text = self.engine_id._message()
        ok, msg = self.engine_id.test_lib(), msg_text
        if ok:
            self.text = '<p><b><font style="font-size: 14px;" class="text-alpha">{0}</font></b></p>'.format(msg)
        else:
            self.text = '<p><b><font style="font-size: 14px;" class="text-gamma">{0}</font></b></p>'.format(msg)

        return self._reopen_form()


class EngineDatabase(models.Model):
    _name = 'dbconnector.engine'
    _description = 'Databases Engine'
    _rec_name = 'name'

    name = fields.Char(string='Database Engine name', required=True)
    description = fields.Char(string='Description')
    lib_module = fields.Char(string='Library Python Module', required=True)
    text = fields.Text()
    active = fields.Boolean(string="Active",
            help="Activate or deactivate record", default=True)

    _sql_constraints = [
            ('database_uniq', 'UNIQUE(name)',
                'Database Engine already exist'), ]

    @api.constrains("lib_module")
    def _validate_lib(self):
        if not self.lib_module:
            raise ValidationError('Library can not be empty')
        else:
            if not self.test_lib():
                raise ValidationError(self._message())

    def _message(self):
        if self.test_lib():
            msg = 'Module is installed'
        else:
            msg = 'No module named {0}, "install module"'.format(self.lib_module)
        return msg

    def test_lib(self):
        lib = self.lib_module
        return importlib.util.find_spec(lib)

    def button_test_module_install(self):
        msg = self._message()
        if self.test_lib:
            self.text = '<p><b><font style="font-size: 14px;" class="text-success">{0}</font></b></p>'.format(msg)
        else:
            self.text = '<p><b><font style="font-size: 14px;" class="text-danger">{0}</font></b></p>'.format(msg)


class Dbconnector(models.Model):
    _name = 'dbconnector.dbconnector'
    _description = 'Databases Conections'
    _rec_name = 'name'

    name = fields.Char(string="Name Database", required=True)
    description = fields.Text(string="Description", required=True)
    host = fields.Char(string="Host", required=True)
    port = fields.Integer(string="Port")
    user = fields.Char(string="User", required=True)
    password = fields.Char(string="Password", required=True)
    engine_id = fields.Many2one("dbconnector.engine", string="Engine",
            required=True)
    active = fields.Boolean(string="Active",
            help="Activate or deactivate record", default=True)
    text = fields.Text()

    _sql_constraints = [
            ('database_uniq', 'UNIQUE(name, host)',
                'Database already exist'), ]


    def see_password(self):
        pass

    @api.constrains('engine_id')
    def valida(self):
        ok, msg = self.test_conection()[0]
        if ok:
            self.text = '<p><b><font style="font-size: 14px;" class="text-success">{0}</font></b></p>'.format(msg)
        else:
            self.text = '<p><b><font style="font-size: 14px;" class="text-warning">{0}</font></b></p>'.format(msg)
        return True

    @api.one
    def test_conection(self):
        pluginX = importlib.import_module(self.engine_id.lib_module)

        response = []
        try:
            conn = pluginX.connect(host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.name)

            response = True, 'Successful connection'
        except Exception as e:
            response = False, e
        return response

