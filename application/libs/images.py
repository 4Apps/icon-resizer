
from pgmagick import Image as pgImage, Blob, Geometry, ColorspaceType, ImageType, ResolutionType, CompressionType
from settings import settings

class Image():
    img = None

    def __init__(self, filename: str):
        try:
            self.img = pgImage(filename)
        except:
            self.img = None


    def __init__(self, image_data: bytes):
#         try:
        blob = Blob()
        blob.update(image_data)
        self.img = pgImage()
        self.img.read(blob)

#         if self.img:
#             self.size = self.img.size()
#
#         except:
#             self.img = None


    def isValid(self):
        return self.img != None


    def setAttributes(self, quality=95):
        """ Set basic attributes """
        self.img.quality(quality)

        # Set other image properties
        self.img.resolutionUnits(ResolutionType.PixelsPerInchResolution)


    def applyIcc(self):
        """ Fix icc profiles """
        try:
            self.img.profile('icm')
        except:
            if self.img.colorSpace() == ColorspaceType.CMYKColorspace:
                icc_data = Blob()
                icc_data.update(open(settings['resources_path'] + 'icc/USWebUncoated.icc', 'rb').read())
                self.img.profile('icm', icc_data)

            if self.img.type() == ImageType.GrayscaleType:
                icc_data = Blob()
                icc_data.update(open(settings['resources_path'] + 'icc/sGray.icc', 'rb').read())
                self.img.profile('icm', icc_data)

        self.img.profile('!icm,*', Blob())

        icc_data = Blob()
        icc_data.update(open(settings['resources_path'] + 'icc/sRGB_v2.1bs.icc', 'rb').read())
        self.img.profile('icm', icc_data)

    def removeIcc(self):
        """ Remove all profiles """
        self.img.profile('*', Blob())


    """
        resizeKeepRatio:
        * 'yes' - no changes applied (default)
        * 'no' - Resize to exact size
        * 'long' - keep ratio by longest side
        * 'short' - keep ratio by shortest side
        * 'width' - keep ratio by width
        * 'height' - keep ratio by height

        crop: list
        * [width, height]
        * [width, height, x, y]

        cropCenter: str
        * 'both' - crop center by both x and y axis
        * 'x' - only crop center by x, y will be 0
        * 'y' - only crop center by y, x will be 0
    """
    def render(self, filename: str, resize: list = None, resizeKeepRatio: str = 'yes', crop: list = None, cropCenter: str = 'both'):
        # Copy current image to new Blob object
        blob = Blob()
        self.img.write(blob)

        # Paste that data in new Image object
        im = pgImage()
        im.read(blob)
        new_size = im.size()

        # Scale the new Image
        if resize != None:
            size_param = '%dx%d'

            if resizeKeepRatio == 'no':
                size_param += '!'

            elif resizeKeepRatio == 'long':
                new_size = im.size()
                if new_size.width() < new_size.height():
                    resize[0] = 0
                else:
                    resize[1] = 0

            elif resizeKeepRatio == 'short':
                new_size = im.size()
                if new_size.width() > new_size.height():
                    resize[0] = 0
                else:
                    resize[1] = 0

            elif resizeKeepRatio == 'width':
                resize[1] = 0

            elif resizeKeepRatio == 'height':
                resize[0] = 0
            im.scale(size_param % (resize[0], resize[1]))

        # Crop the new Image
        if crop != None:
            crop_param = None
            if len(crop) == 4:
                crop_param = Geometry(int(crop[0]), int(crop[1]), int(crop[2]), int(crop[3]))
            else:
                x = 0
                y = 0
                if cropCenter == 'both':
                    new_size = im.size()
                    x = ((new_size.width() - crop[0]) / 2)
                    y = ((new_size.height() - crop[1]) / 2)
                elif cropCenter == 'x':
                    new_size = im.size()
                    x = ((new_size.width() - crop[0]) / 2)
                elif cropCenter == 'y':
                    new_size = im.size()
                    y = ((new_size.height() - crop[1]) / 2)
                crop_param = Geometry(int(crop[0]), int(crop[1]), int(x), int(y))
            im.crop(crop_param)

        # Write the Image to a file
        new_size = im.size()
        im.write(filename % {'sizeX': new_size.width(), 'sizeY': new_size.height()})
