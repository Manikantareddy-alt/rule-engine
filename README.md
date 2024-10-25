# rule-engine


Here’s a README file for your Rule Engine API project, detailing the setup, usage, and example usage flow.

Rule Engine API
This project is a dynamic, three-tier rule engine API built using Flask. It allows you to define rules, store user data, and evaluate rules against that data. Rules are created using Python’s Abstract Syntax Tree (AST) to enable flexible and secure expression parsing.

Features
Dynamic Rule Creation: Define rules as expressions that evaluate conditions on user attributes.
User Data Storage: Store user data in memory for evaluation against rules.
Interactive Web Interface: Manage rules, users, and evaluations directly from a browser-based HTML interface.
Setup
Prerequisites
Python 3.x
Flask
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/your_username/rule-engine-api.git
cd rule-engine-api
Install the required dependencies:

bash
Copy code
pip install flask
Running the Application
Start the Flask server:

bash
Copy code
python app.py
Open the browser and navigate to http://127.0.0.1:5000/ to access the Rule Engine API interface.

Usage
1. Add a Rule
Rule Name: A unique name for your rule.
Rule Expression: An expression that defines the rule's condition, using attributes in the user data.
Example:

Rule Name: is_adult
Rule Expression: age >= 18
2. Add a User
User ID: A unique identifier for the user.
User Data: User attributes in JSON format, such as {"age": 25, "income": 40000}.
3. Evaluate a Rule
User ID: The ID of the user whose data you want to evaluate.
Rule Name: The name of the rule to evaluate.
The result of the rule evaluation will be displayed on the page.

API Endpoints
GET /: Displays an HTML interface for managing rules and users.
POST /add_rule: Adds a new rule. Requires rule_name and rule_expression.
POST /add_user: Adds a new user. Requires user_id and user_data (JSON).
POST /evaluate_rule: Evaluates a specified rule for a given user. Requires user_id_eval and rule_name_eval.
Example Workflow
Add a Rule:

Rule Name: is_adult
Rule Expression: age >= 18
Submit the form to add this rule.
Add a User:

User ID: user_1
User Data: {"age": 20, "income": 30000}
Submit the form to add this user.
Evaluate Rule:

User ID: user_1
Rule Name: is_adult
Submit the form to see the evaluation result (true if age >= 18, otherwise false).
Notes
Data Persistence: User data and rules are stored in memory, so they will be reset when the server restarts.
Rule Expressions: Ensure rule expressions are written in valid Python syntax for compatibility with the AST.
