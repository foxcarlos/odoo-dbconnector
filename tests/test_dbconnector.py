
from openerp.tests.common import TransactionCase
from openerp.exceptions import AccessError


class TestDbconnector(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestDbconnector, self).setUp(*args, **kwargs)
        self.engine = self.env['dbconnector.engine']

    def create_engine(self, engine_name, description, lib_module, text, active):
        "Create a simple engine."

        engine_id = self.engine.create({
            'name': engine_name,
            'description': description,
            'lib_module': lib_module,
            'text': text,
            'active': active
            })

        return engine_id

    def test_engine_create(self):
        engine_id = self.create_engine(
                'MySQL',
                'MySQL Database',
                'pymysql',
                '',
                True)

        self.assertTrue(engine_id, 'error al crear registro')


