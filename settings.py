import os

base_path = os.path.dirname(os.path.realpath(__file__))

# Define some app settings
settings = {
    # Base stuff
    'env': os.getenv('app_env', 'live'),
    'debug': False,
    'version': '0.2',
    'port': 7001,

    # Paths
    'resources_path': base_path + '/resources/',
    'template_path': base_path + '/templates/',
    'static_path': base_path + '/static/',

    # Urls
    'domain': 'donster.me',
    'static_url_prefix': 'http://icons.4apps.lv/static/',

    # App specific
    'ios_sizes': [
        {
          "idiom" : "iphone",
          "size" : "29x29",
          "scale" : "1x",
          "filename" : "icon-iphone-29.png",
        },
        {
          "idiom" : "iphone",
          "size" : "29x29",
          "scale" : "2x",
          "filename" : "icon-iphone-29@2x.png",
        },
        {
          "idiom" : "iphone",
          "size" : "29x29",
          "scale" : "3x",
          "filename" : "icon-iphone-29@3x.png",
        },
        {
          "idiom" : "iphone",
          "size" : "40x40",
          "scale" : "2x",
          "filename" : "icon-iphone-40@2x.png",
        },
        {
          "idiom" : "iphone",
          "size" : "40x40",
          "scale" : "3x",
          "filename" : "icon-iphone-40@3x.png",
        },
        {
          "idiom" : "iphone",
          "size" : "57x57",
          "scale" : "1x",
          "filename" : "icon-iphone-57.png",
        },
        {
          "idiom" : "iphone",
          "size" : "57x57",
          "scale" : "2x",
          "filename" : "icon-iphone-57@2x.png",
        },
        {
          "idiom" : "iphone",
          "size" : "60x60",
          "scale" : "2x",
          "filename" : "icon-iphone-60@2x.png",
        },
        {
          "idiom" : "iphone",
          "size" : "60x60",
          "scale" : "3x",
          "filename" : "icon-iphone-60@3x.png",
        },
        {
          "idiom" : "ipad",
          "size" : "29x29",
          "scale" : "1x",
          "filename" : "icon-ipad-29.png",
        },
        {
          "idiom" : "ipad",
          "size" : "29x29",
          "scale" : "2x",
          "filename" : "icon-ipad-29@2x.png",
        },
        {
          "idiom" : "ipad",
          "size" : "40x40",
          "scale" : "1x",
          "filename" : "icon-ipad-40.png",
        },
        {
          "idiom" : "ipad",
          "size" : "40x40",
          "scale" : "2x",
          "filename" : "icon-ipad-40@2x.png",
        },
        {
          "idiom" : "ipad",
          "size" : "50x50",
          "scale" : "1x",
          "filename" : "icon-ipad-50.png",
        },
        {
          "idiom" : "ipad",
          "size" : "50x50",
          "scale" : "2x",
          "filename" : "icon-ipad-50@2x.png",
        },
        {
          "size" : "72x72",
          "idiom" : "ipad",
          "scale" : "1x",
          "filename" : "icon-ipad-72.png",
        },
        {
          "size" : "72x72",
          "idiom" : "ipad",
          "scale" : "2x",
          "filename" : "icon-ipad-72@2x.png",
        },
        {
          "size" : "76x76",
          "idiom" : "ipad",
          "scale" : "1x",
          "filename" : "icon-ipad-76.png",
        },
        {
          "size" : "76x76",
          "idiom" : "ipad",
          "scale" : "2x",
          "filename" : "icon-ipad-76@2x.png",
        },
        {
          "size" : "83.5x83.5",
          "idiom" : "ipad",
          "scale" : "2x",
          "filename" : "icon-ipad-83.5@2x.png",
        }
    ],

    'mac_sizes': [
        {
          "idiom" : "mac",
          "size" : "16x16",
          "scale" : "1x",
          "filename" : "icon-mac-16.png",
        },
        {
          "idiom" : "mac",
          "size" : "16x16",
          "scale" : "2x",
          "filename" : "icon-mac-16@2x.png",
        },
        {
          "idiom" : "mac",
          "size" : "32x32",
          "scale" : "1x",
          "filename" : "icon-mac-32.png",
        },
        {
          "idiom" : "mac",
          "size" : "32x32",
          "scale" : "2x",
          "filename" : "icon-mac-32@2x.png",
        },
        {
          "idiom" : "mac",
          "size" : "128x128",
          "scale" : "1x",
          "filename" : "icon-mac-128.png",
        },
        {
          "idiom" : "mac",
          "size" : "128x128",
          "scale" : "2x",
          "filename" : "icon-mac-128@2x.png",
        },
        {
          "idiom" : "mac",
          "size" : "256x256",
          "scale" : "1x",
          "filename" : "icon-mac-256.png",
        },
        {
          "idiom" : "mac",
          "size" : "256x256",
          "scale" : "2x",
          "filename" : "icon-mac-256@2x.png",
        },
        {
          "idiom" : "mac",
          "size" : "512x512",
          "scale" : "1x",
          "filename" : "icon-mac-512.png",
        },
        {
          "idiom" : "mac",
          "size" : "512x512",
          "scale" : "2x",
          "filename" : "icon-mac-512@2x.png",
        }
    ],

    # Debug overrides
    'dev': {
        'debug': True,
        'port': 7000,
        'static_url_prefix': '/static/',
    }
}

if settings['env'] in settings:
   settings.update(settings[settings['env']]);
