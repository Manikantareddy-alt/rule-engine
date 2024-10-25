import ast

class RuleEngine:
    def __init__(self):
        self.rules = {}

    def add_rule(self, rule_name, rule_expression):
        # Parse rule using AST and store it
        parsed_rule = ast.parse(rule_expression, mode='eval')
        self.rules[rule_name] = parsed_rule

    def evaluate_rule(self, rule_name, user_data):
        if rule_name not in self.rules:
            raise ValueError(f"Rule '{rule_name}' not found.")
        rule = self.rules[rule_name]
        compiled_rule = compile(rule, filename="<ast>", mode="eval")
        return eval(compiled_rule, {}, user_data)
