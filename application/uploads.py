import os
import json
import io
import logging

from subprocess import call
from time import time
from hashlib import sha1

from application.base import BaseHandler
from application.libs.images import Image

class UploadHandler(BaseHandler):

    def initialize(self) -> None:  # type: ignore
        # Override default logger
        self.logger = logging.getLogger("UploadHandler")

    def error(self, message):
        if isinstance(message, dict):
            message = json.dumps(message)
        self.write(message)


    def post(self):
        self.logger.debug("Reveived an upload request")

        icon_type = self.get_argument('icon_type', 'ios')
        if not 'file' in self.request.files:
            self.logger.debug("Missing input data")
            self.error({'error': {'code': 21, 'msg': 'Missing input data'}})
            return

        # Try opening the image
        self.logger.debug("Trying to open the image")
        media1 = self.request.files['file'][0]
        img = Image(image_data=media1['body'])
        if img.isValid() == False:
            self.logger.debug("Unrecognized image format")
            self.write({'error': {'code': 21, 'msg': 'Unrecognized image format'}})
            return

        size = img.img.size()
        self.logger.debug("Image size: %s", size)
        if size.width() != 1024 or size.height() != 1024:
            self.logger.debug("Image size must match 1024 x 1024 px")
            self.error({'error': {'code': 31, 'msg': 'Image size must match 1024 x 1024 px'}})
            return

        # Generate upload filename
        filename = 'icon'
        folder_name = sha1(str(time()).encode('utf-8')).hexdigest()
        upload_path = self.settings['static_path'] + 'icons/' + folder_name
        iconset_path = self.settings['static_path'] + 'icons/' + folder_name + '/AppIcon.appiconset'

        # Create directory
        try:
            self.logger.debug("Creating directory: %s", upload_path)
            os.makedirs(iconset_path)
        except:
            self.logger.debug("Unable to create directory: %s", upload_path)
            self.error({'error': {'code': -3, 'msg': 'Opps! System error, plase try again later..'}})
            return

        # Fix the image
        img.setAttributes()
        img.removeIcc()

        # Get icon sizes
        icon_sizes = self.settings['mac_sizes' if icon_type == 'mac' else 'ios_sizes']

        # Render images
        self.logger.debug("Rendering images")
        for item in icon_sizes:
            self.logger.debug("Rendering image: %s for size: %s and scale: %s", item['filename'], item['size'], item['scale'])
            size = item['size'].split('x')
            scale = float(item['scale'][0])
            size = [ int(float(x) * scale) for x in size ]
            img.render(iconset_path + '/' + item['filename'], resize=size)

        # Create Contents.json
        self.logger.debug("Creating Contents.json")
        contents = {
            "images" : icon_sizes,
            "info" : {
                "version" : 1,
                "author" : "xcode"
            },
            "properties" : {
                "pre-rendered" : True
            }
        }
        contents = json.dumps(contents)
        fh = open(iconset_path + '/Contents.json', 'w')
        fh.write(contents)
        fh.close()

        # Zip it
        command = ['zip', '-1', '-q', '-m', '-j', '-r', iconset_path + '.zip', iconset_path]
        call(command)

        # Send response
        response = {'error': {'code': 0}, 'filename': folder_name + '/AppIcon.appiconset.zip'}
        self.write(response)
