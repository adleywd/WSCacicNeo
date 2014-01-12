from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('master', 'master')

    config.add_route('home', 'home')
    config.add_route('dashboard', 'dashboard')
    config.add_route('admin', 'admin')
    config.add_route('busca', 'busca')
    config.add_route('diagnostic', 'diagnostic')
    config.add_route('reports', 'reports')

    config.scan()
    return config.make_wsgi_app()
