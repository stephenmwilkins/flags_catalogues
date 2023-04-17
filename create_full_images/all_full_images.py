from create_detection_image import create_detection_image
from create_segmentation_image import create_segmentation_image
from create_single_band_image import create_single_band_image

if __name__ == '__main__':

    subcat = 'high-z.v0.1'
    survey = 'CEERS'
    pointing = 4
    cat_version = '0.51.2'
    img_version = '0.51'
    survey_dir = '/Users/jt458/ceers'


    filters = []
    filters += [f'JWST/NIRCam.{f}' for f in ['F115W', 'F150W', 'F200W', 'F277W', 'F356W', 'F410M', 'F444W']]

    create_single_band_image(survey, img_version, pointing, filters, survey_dir=survey_dir)
    create_segmentation_image(survey, img_version, pointing, survey_dir=survey_dir)
    create_detection_image(survey, img_version, pointing, cat_version=cat_version, add_sources= True, survey_dir=survey_dir)