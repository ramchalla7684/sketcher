from flask import Flask
import router
app = Flask(__name__, template_folder="web", static_folder="web")

router.init(app)

app.run(debug=True)
