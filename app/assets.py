from flask import current_app as app
from flask_assets import Bundle, Environment


def compile_assets(assets):
    assets.auto_build = True
    assets.debug = False
    base_style = Bundle(
        'base_bp/css/volt.css',
        filters='cssmin',
        output='dist/css/base.min.css'
    )
    base_script = Bundle(
        'base_bp/js/volt.js',
        filters='jsmin',
        output='dist/js/base.min.js'
    )

    assets.register('base_style', base_style)
    assets.register('base_script', base_script)

    base_style.build()
    base_script.build()

    return assets
