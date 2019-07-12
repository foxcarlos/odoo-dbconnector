# -*- coding: utf-8 -*-

import importlib

# import mysql.connector as mysql
import pymysql  # Nueva libreria
import pymssql
import sqlite3
import base64

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError, Warning, currentframe


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
            ('database_uniq', 'UNIQUE(lib_module)',
                'Python Library already exist'), ]

    @api.constrains("lib_module")
    def _validate_lib(self):
        if not self.lib_module:
            raise ValidationError('Library can not be empty')
        else:
            if not self.test_lib():
                raise ValidationError(self._message())
            self.text = ''
        return True

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
        html = '<p><b><font style="font-size: 14px;" class="{0}">{1}</font></b></p>'
        msg = self._message()
        if self.test_lib:
            self.text = html.format('text-success', msg)
        else:
            self.text = html.format('text-danger', msg)


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


    @api.onchange('password')
    @api.depends('password')
    def obfuscate_passw(self):
        self.password = self.env['dbconnector.password'].encode(self.password)

    @api.constrains('engine_id', 'user', 'name', 'host', 'port', 'password')
    def _vigila(self):
        self.text = ''
        return True

    @api.one
    def valida(self):
        html = '<p><b><font style="font-size: 14px;" class="{0}">{1}</font></b></p>'
        conn, msg = self.connect()
        if conn:
            self.text = html.format('text-success', msg)
            conn.close()
        else:
            self.text = html.format('text-warning', msg)
        return True

    def connect(self):
        self.ensure_one()
        pluginX = importlib.import_module(self.engine_id.lib_module)
        try:
            conn = pluginX.connect(host=self.host,
                    user=self.user,
                    password=self.env['dbconnector.password'].decode(self.password),
                    db=self.name)

            response = conn, 'successful connection'
        except Exception as error:
            response = False, str(error)

        return response

class PasswordEncryption(models.AbstractModel):

    _name = 'dbconnector.password'
    _description = 'Ofuscate password'

    def encode(self, text_to_encrypt=''):
        encrypted_text = ''
        if text_to_encrypt:
            key = "1234567890"
            enc = []
            for i in range(len(text_to_encrypt)):
                key_c = key[i % len(key)]
                enc_c = chr((ord(text_to_encrypt[i]) + ord(key_c)) % 256)
                enc.append(enc_c)
            encrypted_text = base64.urlsafe_b64encode("".join(enc).encode()).decode()

        return encrypted_text or None

    @staticmethod
    def decode(encrypted):
        key = "1234567890"
        dec = []
        enc = base64.urlsafe_b64decode(encrypted).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec) or None

