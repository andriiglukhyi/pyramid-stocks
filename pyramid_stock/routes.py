def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('autho', '/autho')
    config.add_route('stock-details', '/stock-details/{symbol}')
    config.add_route('portfolio', '/portfolio')
    config.add_route('stock-add', '/stock-add')

