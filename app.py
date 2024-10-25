from flask import Flask, jsonify, request, render_template_string
import ast

app = Flask(__name__)

class RuleEngine:
    def __init__(self):
        self.rules = {}

    def add_rule(self, rule_name, rule_expression):
        parsed_rule = ast.parse(rule_expression, mode='eval')
        self.rules[rule_name] = parsed_rule

    def evaluate_rule(self, rule_name, user_data):
        if rule_name not in self.rules:
            raise ValueError(f"Rule '{rule_name}' not found.")
        rule = self.rules[rule_name]
        compiled_rule = compile(rule, filename="<ast>", mode="eval")
        return eval(compiled_rule, {}, user_data)

class UserDataStore:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, user_data):
        self.users[user_id] = user_data

    def get_user_data(self, user_id):
        return self.users.get(user_id, None)

# Create instances of RuleEngine and UserDataStore
rule_engine = RuleEngine()
user_store = UserDataStore()

@app.route("/", methods=["GET", "POST"])
def index():
    # HTML template for the dynamic interface
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rule Engine API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; }
            h1 { color: #333; }
            .section { margin-top: 20px; }
            .endpoint { font-weight: bold; }
            form { margin-top: 15px; }
            label { display: block; margin-top: 8px; }
            input[type="text"], textarea { width: 100%; padding: 8px; margin-top: 5px; }
            button { margin-top: 10px; padding: 8px 12px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            .result { color: #333; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>Welcome to the Rule Engine API</h1>
        <p>This interface provides options to add rules, users, and evaluate rules dynamically.</p>

        <div class="section">
            <h2>Add Rule</h2>
            <form method="post" action="/add_rule">
                <label for="rule_name">Rule Name:</label>
                <input type="text" id="rule_name" name="rule_name" required>
                
                <label for="rule_expression">Rule Expression:</label>
                <textarea id="rule_expression" name="rule_expression" required></textarea>
                
                <button type="submit">Add Rule</button>
            </form>
        </div>

        <div class="section">
            <h2>Add User</h2>
            <form method="post" action="/add_user">
                <label for="user_id">User ID:</label>
                <input type="text" id="user_id" name="user_id" required>
                
                <label for="user_data">User Data (JSON format):</label>
                <textarea id="user_data" name="user_data" required></textarea>
                
                <button type="submit">Add User</button>
            </form>
        </div>

        <div class="section">
            <h2>Evaluate Rule</h2>
            <form method="post" action="/evaluate_rule">
                <label for="user_id_eval">User ID:</label>
                <input type="text" id="user_id_eval" name="user_id_eval" required>
                
                <label for="rule_name_eval">Rule Name:</label>
                <input type="text" id="rule_name_eval" name="rule_name_eval" required>
                
                <button type="submit">Evaluate Rule</button>
            </form>
            {% if result %}
                <div class="result"><strong>Result:</strong> {{ result }}</div>
            {% endif %}
            {% if error %}
                <div class="result" style="color: red;"><strong>Error:</strong> {{ error }}</div>
            {% endif %}
        </div>
    </body>
    </html>
    """

    result = request.args.get("result")
    error = request.args.get("error")

    return render_template_string(html_template, result=result, error=error)

@app.route("/add_rule", methods=["POST"])
def add_rule():
    rule_name = request.form["rule_name"]
    rule_expression = request.form["rule_expression"]
    rule_engine.add_rule(rule_name, rule_expression)
    return jsonify({"status": f"Rule '{rule_name}' added successfully!"})

@app.route("/add_user", methods=["POST"])
def add_user():
    user_id = request.form["user_id"]
    user_data_str = request.form["user_data"]
    try:
        user_data = eval(user_data_str)  # Use `json.loads` in production for security
    except Exception as e:
        return jsonify({"error": "Invalid JSON format"}), 400
    user_store.add_user(user_id, user_data)
    return jsonify({"status": f"User '{user_id}' added successfully!"})

@app.route("/evaluate_rule", methods=["POST"])
def evaluate_rule():
    user_id = request.form["user_id_eval"]
    rule_name = request.form["rule_name_eval"]

    user_data = user_store.get_user_data(user_id)
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    try:
        result = rule_engine.evaluate_rule(rule_name, user_data)
        return jsonify({"result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/favicon.ico")
def favicon():
    return "", 204  # No content for favicon

if __name__ == "__main__":
    app.run(debug=True)
