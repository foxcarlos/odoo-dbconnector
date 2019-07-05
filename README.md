# Odoo Module

Odoo Module for store string connect of database engine .



= Install the dependencies =
```sh
$ pip install -r requirements.txt
```

= Ejemlo de uso =

```sh
driver = env['dbconnector.dbconnector'].search([('name', 'ilike', 'webdb'), ('host', 'ilike', 'localhost')])
conn, msg = driver.connect()
if conn:
    print(msg)
    cursor = conn.cursor()
    cursor.execute("select *from GuiaCompleta")
    rows = cursor.fetchall()
else:
    print('ocurrio el siguiente error {0}'.format(msg))

= Otro uso que se le puede dar es solo para almanecar los datos de la conexion =

import pymysql

driver = env['dbconnector.dbconnector'].search(
    [('name', 'ilike', 'webdb'),
    ('host', 'ilike', 'localhost')]
    )


conn = pymysql.connect(host=driver.host,
                    user=driver.user,
                    password=self.env['dbconnector.password'].decode(driver.password),
                    db=driver.name)

cursor = conn.cursor()
cursor.execute("select *from GuiaCompleta")
rows = cursor.fetchall()

```

### Todos

 - Write Tests

### readme.md Creado con https://dillinger.io/
