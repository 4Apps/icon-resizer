import os
import json
import io

from subprocess import call
from time import time
from hashlib import sha1
from pgmagick import Image, Blob, Geometry, ColorspaceType, ImageType, ResolutionType, CompressionType

from application.base import BaseHandler


class UploadHandler(BaseHandler):
    def error(self, message):
        if isinstance(message, dict):
            message = json.dumps(message)
        self.write(message)


    def apply_icc(self, im):
        """ Fix icc profiles """
        try:
            im.profile('icm')
        except:
            if im.colorSpace() == ColorspaceType.CMYKColorspace:
                icc_data = Blob()
                icc_data.update(open(self.settings['resources_path'] + 'icc/USWebUncoated.icc', 'rb').read())
                im.profile('icm', icc_data)

            if im.type() == ImageType.GrayscaleType:
                icc_data = Blob()
                icc_data.update(open(self.settings['resources_path'] + 'icc/sGray.icc', 'rb').read())
                im.profile('icm', icc_data)

        im.profile('!icm,*', Blob())

        icc_data = Blob()
        icc_data.update(open(self.settings['resources_path'] + 'icc/sRGB_v2.1bs.icc', 'rb').read())
        im.profile('icm', icc_data)


    def set_image_attributes(self, im):
        """ Set basic attributes """
        im.quality(100)

        # Set other image properties
        im.resolutionUnits(ResolutionType.PixelsPerInchResolution)



    def render_image(self, upload_path, filename, image, size):
        blob = Blob()
        image.write(blob)

        im = Image()
        im.read(blob)

        im.scale('%dx%d' % (size, size))
        im.write('%s/%s-%d.png' % (upload_path, filename, size))

    def post(self):
        upload_key = self.get_argument('upload_key', None)
        media_type = self.get_argument('type', None)


        if not 'file' in self.request.files:
            self.error({'error': {'code': 21, 'msg': 'Missing input data'}})
            return


        # Generate upload filename
        filename = 'icon'
        folder_name = sha1(str(time()).encode('utf-8')).hexdigest()
        upload_path = self.settings['static_path'] + 'icons/' + folder_name


        # Create directory
        try:
            os.makedirs(upload_path)
        except:
            self.error({'error': {'code': -3, 'msg': 'Opps! System error, plase try again later..'}})
            return


        # Handle the upload
        media1 = self.request.files['file'][0]

        original_filename = '%s/%s.png' % (upload_path, filename)
        fh = open(original_filename, 'wb')
        fh.write(media1['body'])
        fh.close()

        try:
            image = Image(original_filename)
        except:
            self.error({'error': {'code': 30, 'msg': 'Image format is not recognized. We support png, jpeg, gif, tiff, bmp images.'}})
            return


        size = image.size()
        print(size.width(), size.height())
        if size.width() != 1024 or size.height() != 1024:
            self.error({'error': {'code': 31, 'msg': 'Image size must match 1024 x 1024 px'}})
            return


        # Fix the image
        self.set_image_attributes(image)
        self.apply_icc(image)


        # Resize images, make rounded corners and save them to disk
        for size in self.settings['image_size']:
            self.render_image(upload_path, filename, image, size)



        # Zip it
        command = ['zip', '-1', '-q', '-m', '-j', '-r', upload_path + '.zip', upload_path]
        call(command)


        # Remove directory (done by cronjob)
#         try:
#             os.rmdir(upload_path)
#         except:
#             pass


        # Send response
        response = {'error': {'code': 0}, 'filename': folder_name + '.zip'}
        self.write(response)
        return
