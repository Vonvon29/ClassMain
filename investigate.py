


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

## parameters
IMAGE_NAME = "my_image"
OBJECTS_NAME = "my_objects"
MASKING_OBJECTS_NAME = "masking_objects"
MEASUREMENT_NAME = "my_measurement"

## Load Image
imaage=IMG.open("/home/glorfindel/Spellcraft/SIDEQUEST/Yvonne/noyau.tif")
inpuut=imaage.convert('F')

# SETTINGS
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

## create pipeline
pipeline = cellprofiler_core.pipeline.Pipeline()
pipeline.add_module(x)

## init measurement
m=cellprofiler_core.measurement.Measurements()
#m.add_measurement("Image", "Feature", "Value")
m.add_measurement("my_image", "Tardis", "Value")

print(m.get_feature_names("my_image"))

## init cpimage
cpimage = cellprofiler_core.image.Image(inpuut)
image_set = cellprofiler_core.image.ImageSet(0, {}, {})
image_set.add("my_image", cpimage)
print(image_set.providers[0].name)
#cpimage.set_image(inpuut)
#image_set = cpimage

#provider = cellprofiler_core.image.VanillaImageProvider("my_image", cpimage)
#image_set = cellprofiler_core.image.ImageSet(number=1, keys='tardis', legacy_fields=None)
#image_set.providers.append(provider)


## init set list
image_set_list = cellprofiler_core.image.ImageSetList()

## init image set
#image_set = image_set_list.get_image_set(0)
#image_set.providers.append(cellprofiler_core.image.VanillaImageProvider("my_image", cpimage))


## init object set
object_set = cellprofiler_core.object.ObjectSet()
#features = m.get_feature_names("my_objects")

## Run app
app = wx.App()
frm=wx.Frame(None, title="test")

## init Workspace
workspace = cellprofiler_core.workspace.Workspace(pipeline=pipeline,
                                                  module=x,
                                                  image_set=image_set,
                                                  object_set=object_set,
                                                  measurements=m,
                                                  image_set_list=image_set_list,
                                                  frame=frm,
                                                  create_new_window=False)



print(workspace)
x.run(workspace)
