## importation
import io
import os
import centrosome.threshold
import numpy as np
import wx
import pytest
import scipy.ndimage
import cellprofiler_core.image
import cellprofiler_core.measurement
import cellprofiler_core.modules.identify
import cellprofiler.modules.identifyprimaryobjects
import cellprofiler.modules.threshold
import cellprofiler_core.object
import cellprofiler_core.pipeline
import cellprofiler_core.setting
import cellprofiler_core.workspace
import cellprofiler.gui.figure
import skimage
from PIL import Image as IMG
import six
import six.moves

def run_pipeline(image_dict):

    cellprofiler_core.preferences.set_headless()

    # Create the pipeline
    pipeline = cellprofiler_core.pipeline.Pipeline()

    # Create the module
    IMAGE_NAME = "my_image"
    OBJECTS_NAME = "Nuclei"
    MASKING_OBJECTS_NAME = "masking_objects"
    MEASUREMENT_NAME = "my_measurement"
    x = cellprofiler.modules.identifyprimaryobjects.IdentifyPrimaryObjects()
    x.use_advanced.value = True
    x.size_range.value = (4, 15)
    x.y_name.value = "my_object"
    x.x_name.value = "my_image"
    x.exclude_size.value = False
    #x.watershed_method.value = cellprofiler.modules.identifyprimaryobjects.WA_NONE
    x.threshold.local_operation.value == centrosome.threshold.TM_OTSU
    x.threshold.threshold_scope.value = cellprofiler_core.modules.identify.TS_GLOBAL
    x.threshold.global_operation.value = cellprofiler.modules.threshold.TM_MEASUREMENT
    x.threshold.threshold_smoothing_scale.value = 0
    x.threshold.threshold_correction_factor.value = 2.5
    x.threshold.threshold_range.min = 0
    x.threshold.threshold_range.max = 1
    x.unclump_method.value = (cellprofiler.modules.identifyprimaryobjects.UN_SHAPE)
    x.watershed_method.value = (cellprofiler.modules.identifyprimaryobjects.WA_INTENSITY)
    x.automatic_smoothing.value=True
    x.fill_holes.value=cellprofiler.modules.identifyprimaryobjects.FH_THRESHOLDING

    ## add module to pipeline
    pipeline.add_module(x)
    fd = os.open( "foo.txt", os.O_RDWR|os.O_CREAT )
    fo = os.fdopen(fd, "w+")
    pipeline.dump(fo)

    # Create the image set, and add the image data
    image_set_list = cellprofiler_core.image.ImageSetList()
    image_set = image_set_list.get_image_set(0)
    for image_name, input_pixels in image_dict.items():
        image_set.add(image_name, cellprofiler_core.image.Image(input_pixels))

    # Persist the object set here (for now, see workspace TODO)
    object_set = cellprofiler_core.object.ObjectSet()

    # We can only run one group -- set the group index to 1.
    measurements = cellprofiler_core.measurement.Measurements()
    measurements.group_index = 1

    # Run the modules!
    for module in pipeline.modules():
        # Yes, we really do have to create a new workspace for each module
        # because the module attribute is required. Go team.
        workspace = cellprofiler_core.workspace.Workspace(
            image_set=image_set,
            image_set_list=image_set_list,
            measurements=measurements,
            module=module,
            object_set=object_set,
            pipeline=pipeline
        )

        module.prepare_run(workspace)
        module.run(workspace)
        module.post_run(workspace)

    # The workspace object has access to the measurements
    # and the image set/image set list which can be used
    # to use/view/store/whatever output data.
    return workspace



# This should match what NamesAndTypes would produce.
images = {
    "my_image": skimage.io.imread("data/01_POS002_R.TIF"),
}



workspace = run_pipeline(images)



"""
# Get the "Nuclei" object measurements, as a pandas DataFrame
df = objects2df(workspace.measurements, "Nuclei")
print(df.head())

# Display the "RGBImage" image, created by GrayToColor

import matplotlib.pyplot as plt
rgb_image = workspace.image_set.get_image("RGBImage")
skimage.io.imshow(rgb_image.pixel_data)
plt.show()
"""
