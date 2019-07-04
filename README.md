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
cursor = conn.cursor()
cursor.execute("select *from GuiaCompleta")
rows = cursor.fetchall() 
```

### Todos

 - Write Tests

### readme.md Creado con https://dillinger.io/
