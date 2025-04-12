import os


class GalleryConfig:
    GALLERY_DIRECTORY = os.getcwd()
    GALLERY_IMAGE_DATE_FORMAT = '%m/%d/%Y %I:%M %p'
    GALLERY_HEADER = 'my gallery'
    GALLERY_DIASHOW_MIN_BATCH_SIZE = 5
