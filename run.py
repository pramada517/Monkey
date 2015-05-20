#!flask/bin/python
from monkey import create_app

app = create_app()
app.run(debug=False)

