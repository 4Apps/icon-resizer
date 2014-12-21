import os

# Define some app settings
settings = {
    'env': os.getenv('app_env', 'live'),
    'debug': False,
    'version': '0.2',

    'resources_path': os.path.dirname(os.path.realpath(__file__)) + '/resources/',
    'template_path': os.path.dirname(os.path.realpath(__file__)) + '/templates/',
    'static_path': os.path.dirname(os.path.realpath(__file__)) + '/static/',
    'static_url_prefix': 'http://ios-icons.4apps.lv/static/',


    'image_size': [
        1024,

        152, #iPad - iOS 7
        76,

        144, #iPad - iOS 5,6
        72,

        120, #iPhone - iOS 7

        114, #iPhone - iOS 5,6
        57,

        80, #iPad spotlight - iOS 7, #iPhone spotlight - iOS 7
        40,

        100, #iPad spotlight - iOS 5,6
        50,

        58, #iPad settings - iOS 5-7, #iPhone spotlight - iOS 5,6, #iPhone settings - iOS 5-7
        29
    ],

    'dev': {
        'debug': True,
        'static_url_prefix': '/static/',
    }
}

if settings['env'] in settings:
   settings.update(settings[settings['env']]);
