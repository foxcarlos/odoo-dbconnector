import importlib

from odoo.tests.common import TransactionCase


class DbconnectorTestCase(TransactionCase):

    '''
    # Crear
    def setUp(self):
        super(DbconnectorTestCase, self).setUp()
        demo_user = self.env.ref('base.user_demo')
        engine_model = self.env['dbconnector.engine'].sudo(demo_user)

	# Create Engine
        self.engine = engine_model.create({
            'name': 'MySQL',
            'description': 'MySQL Server',
            'lib_module':'pymysql2',
            'text': '',
            'active': True})

        # Edit Engine
        self.engine_w = engine_model.write({
            'name': 'MySQL',
            'description': 'MySQL Server Test',
            'active': False})
            '''

    def test_python_lib(self):
        # Create Engine
        engine = self.env['dbconnector.engine'].create({
            'name': 'MySQL',
            'description': 'MySQL Server',
            'lib_module':'pymysql2',
            'text': '',
            'active': True})

        value = engine.test_lib()
        self.assertEqual(value, 'pymysql', 'Python lib not found')


    """
    # Edit
    def test_validate_lib(self):
        '''test validate Lib'''

        print('paso por el test')
        self.engine.test_lib()
        self.assertEqual(self.engine.lib_module, 'pymysql', 'Python lib not found')
        """

    """
    # Generate error
    def test_change_available_draft_no_effect(self):
        '''test forbidden state change from available to draft'''
        self.book.change_state('available')
        self.book.change_state('draft')
        self.assertEqual(
                self.book.state,
                'available',
                'the state cannot change from available to %s' % self.book.state)
    """


