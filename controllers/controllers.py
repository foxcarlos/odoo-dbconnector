# -*- coding: utf-8 -*-
from odoo import http

# class Dbconnector(http.Controller):
#     @http.route('/dbconnector/dbconnector/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dbconnector/dbconnector/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dbconnector.listing', {
#             'root': '/dbconnector/dbconnector',
#             'objects': http.request.env['dbconnector.dbconnector'].search([]),
#         })

#     @http.route('/dbconnector/dbconnector/objects/<model("dbconnector.dbconnector"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dbconnector.object', {
#             'object': obj
#         })