import flask


class App(flask.Flask):

    def add_rule(self, rule, view_func, **options):
        endpoint = '{}.{}'.format(view_func.__module__, view_func.__name__)
        self.add_url_rule(rule, endpoint, view_func, **options)

    def add_get(self, rule, view_func):
        self.add_rule(rule, view_func, methods=['GET'])

    def add_post(self, rule, view_func):
        self.add_rule(rule, view_func, methods=['POST'])

    def add_put(self, rule, view_func):
        self.add_rule(rule, view_func, methods=['PUT'])

    def add_delete(self, rule, view_func):
        self.add_rule(rule, view_func, methods=['DELETE'])
