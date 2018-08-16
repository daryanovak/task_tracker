class ParseHelper:

    @staticmethod
    def parse_args(args):
        _args = vars(args)
        if 'func' in _args:
            _args.pop('func')
        return _args

    @staticmethod
    def parse_private_vars(vars):
        _vars = dict()
        for var_key in vars:
            _vars[var_key[1:]] = vars[var_key]
        return _vars





