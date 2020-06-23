import io
import os

print("hello1")
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
print("hello3")
IMAGE_NAME = "my_image"
OBJECTS_NAME = "my_objects"
MASKING_OBJECTS_NAME = "masking_objects"
MEASUREMENT_NAME = "my_measurement"
print("hello4")


# image=np.array(['C:/Users/Immuno4/noyau.tif'])
# image=np.ndarray(image)
# skimage.io.imshow(image)
# img=np.float32(image)

imaage=IMG.open("C:/Users/Immuno4/noyau.tif")
inpuut=imaage.convert('F') #conv en 32-bit float


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
x.watershed_method.value = ( cellprofiler.modules.identifyprimaryobjects.WA_INTENSITY )
x.automatic_smoothing.value=True
x.fill_holes.value=cellprofiler.modules.identifyprimaryobjects.FH_THRESHOLDING

pipeline = cellprofiler_core.pipeline.Pipeline()
#pipeline.add_module(x)

m=cellprofiler_core.measurement.Measurements()
cpimage = cellprofiler_core.image.Image(inpuut)
print(cpimage.multichannel)
image_set_list = cellprofiler_core.image.ImageSetList()
image_set = image_set_list.get_image_set(0)
image_set.providers.append(
        cellprofiler_core.image.VanillaImageProvider("my_image", cpimage))
object_set = cellprofiler_core.object.ObjectSet()
#features = m.get_feature_names("my_objects")
print("hello5")
app = wx.App()
frm=wx.Frame(None, title="test")
x.run(
cellprofiler_core.workspace.Workspace(
        pipeline, x, image_set, object_set, m, None, frm, create_new_window=False
    )
)

# fig= cellprofiler.gui.figure.Figure(frm)

# print("hello6")
# # x.display(cellprofiler_core.workspace.Workspace(
# #         pipeline, x, image_set, object_set, measurements, None
# #     ), fig)
# print("hello7")
