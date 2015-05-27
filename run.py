#!flask/bin/python
from monkey import app
from monkey.database import init_db

init_db()
app.run(debug=False)

