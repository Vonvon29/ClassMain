## importation
import io
import os
import centrosome.threshold
import numpy as np
import numpy
import wx
import scipy.ndimage
import cellprofiler_core.image
import cellprofiler_core.measurement
import cellprofiler_core.modules.identify
import cellprofiler.modules.identifyprimaryobjects
import cellprofiler.modules.identifysecondaryobjects
import cellprofiler.modules.measureobjectsizeshape
import cellprofiler.modules.imagemath
import cellprofiler.modules.colortogray
import cellprofiler.modules.filterobjects
import cellprofiler.modules.saveimages
import cellprofiler.modules.threshold
import cellprofiler_core.object
import cellprofiler_core.pipeline
import cellprofiler_core.setting
import cellprofiler_core.workspace
import cellprofiler.gui.figure
import cellprofiler.gui.workspace
import skimage
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image as IMG

## parameters
IMAGE_NAME = "my_image"
OBJECTS_NAME = "nuclei"
MASKING_OBJECTS_NAME = "masking_objects"
MEASUREMENT_NAME = "my_measurement"

## Load Image
imaage0=IMG.open("/home/perceval/Téléchargements/maskrgb.tiff")
imaage = numpy.asarray(imaage0)

## MODULE 1 - COLOR TO GRAY : SPLIT IMAGE EN 3 IMAGES 
ctg = cellprofiler.modules.colortogray.ColorToGray()
ctg.image_name.value = "my_image"
ctg.combine_or_split.value = cellprofiler.modules.colortogray.SPLIT
ctg.rgb_or_channels.value = cellprofiler.modules.colortogray.CH_RGB
ctg.use_red.value = True
ctg.use_blue.value = True
ctg.use_green.value = True
ctg.red_name.value = "my_red"
ctg.green_name.value = "my_green"
ctg.blue_name.value = "my_blue"

## INITIALISATION DES ARGUMENTS DU WORKFLOW
pipeline = cellprofiler_core.pipeline.Pipeline()
pipeline.add_module(ctg)
cpimage = cellprofiler_core.image.Image(imaage) #IMAGE MASK RGB POUR SPLIT
m0 = cellprofiler_core.measurement.Measurements()
object_set0 = cellprofiler_core.object.ObjectSet()
image_set_list0 = cellprofiler_core.image.ImageSetList()
image_set0 = cellprofiler_core.image.ImageSet(0, {}, {})
image_set0.add("my_image", cpimage)
app = wx.App()
frm0=wx.Frame(None, -1, title="test")

## init Workspace
workspace0 = cellprofiler_core.workspace.Workspace(pipeline=pipeline,
                                                  module=ctg,
                                                  image_set=image_set0,
                                                  object_set=object_set0,
                                                  measurements=m0,
                                                  image_set_list=image_set_list0,
                                                  frame=frm0,
                                                  create_new_window=False)

frm0.Show(False)
ctg.show_window = True
ctg.run(workspace0) # EN SORTIE : 3 IMAGES GRAYSCALE DES CANAUX RGB ON VEUT R+G
figure0 = cellprofiler.gui.figure.Figure(frm0)
#ctg.display(workspace0, figure0)

## try to catch grey scale image
print("[DEBUG] Catch GreyScale Image")
collect = workspace0.display_data.disp_collection
img_noyo = collect[0][0]
img_cyto = collect[1][0]

####################################################################

## MODULE 2 - IMAGE MATHS : ADDITION CANAUX RED + GREEN (NUCLEI + CYTO)
im = cellprofiler.modules.imagemath.ImageMath()
im.operation.value = cellprofiler.modules.imagemath.O_ADD
im.output_image_name.value = "nuccyto" 
im.images[0].image_name.value = "my_red" # nom de l'image canal rouge
im.images[0].factor.value = 1.0
im.images[1].image_name.value = "my_green" # nom de l'image canal vert
im.images[1].factor.value = 1.0
pipeline.add_module(im)
image_set_list00 = cellprofiler_core.image.ImageSetList()
image_set00 = image_set_list00.get_image_set(0)

cpimage001 = cellprofiler_core.image.Image(img_noyo) #input1 from color to gray
cpimage002 = cellprofiler_core.image.Image(img_cyto) #input2 from color to gray
image_set00.add("my_red", cpimage001)
image_set00.add("my_green", cpimage002)

frm00=wx.Frame(None, -1, title="yoooooooooooooooooooooooooooo")

workspace00 = cellprofiler_core.workspace.Workspace(
        image_set=image_set00,
        image_set_list=image_set_list00,
        module=im,
        pipeline=pipeline,
        measurements=cellprofiler_core.measurement.Measurements(),
        object_set=cellprofiler_core.object.ObjectSet(),
    )
frm00.Show(False)
fig00 = cellprofiler.gui.figure.Figure(frm00)
im.show_window = True
im.run(workspace00) ## EN SORTIE LA SOMME DES CANAUX R+G A RECUPERER :
im_output = workspace00.image_set.get_image("nuccyto")

########################################################################

# SETTINGS identify primary objects ------------------------------------
x = cellprofiler.modules.identifyprimaryobjects.IdentifyPrimaryObjects()
x.use_advanced.value = True
x.size_range.value = (4, 15)
x.y_name.value = "nuclei"
x.x_name.value = "my_image"
x.exclude_size.value = False
x.exclude_border_objects.value = False
x.low_res_maxima.value = True 
x.threshold.threshold_scope.value = cellprofiler_core.modules.identify.TS_GLOBAL
x.threshold.global_operation.value = cellprofiler.modules.threshold.TM_LI
x.threshold.threshold_smoothing_scale.value = 0
x.threshold.threshold_correction_factor.value = 2.5
x.threshold.threshold_range.min = 0
x.threshold.threshold_range.max = 1
x.unclump_method.value = (cellprofiler.modules.identifyprimaryobjects.UN_SHAPE)
x.watershed_method.value = (cellprofiler.modules.identifyprimaryobjects.WA_INTENSITY)
x.automatic_smoothing.value=True
x.fill_holes.value=cellprofiler.modules.identifyprimaryobjects.FH_THRESHOLDING

## create pipeline
pipeline.add_module(x)

## init measurement
m=cellprofiler_core.measurement.Measurements()
m.add_measurement("my_image", "Tardis", "Value")

## init cpimage
cpimage = cellprofiler_core.image.Image(img_noyo) ## IMAGE NOYAU DE "COLOR TO GRAY"
image_set = cellprofiler_core.image.ImageSet(0, {}, {})
image_set.add("my_image", cpimage)
print(image_set.providers[0].name)

## init set list
image_set_list = cellprofiler_core.image.ImageSetList()

## init object set
object_set = cellprofiler_core.object.ObjectSet() #INIT SET D'OBJECTS A REMPLIR PENDANT LE "RUN"
#features = m.get_feature_names("my_objects")

## Run app
import wx.adv
import wx.html

width, height = imaage0.size
#app = wx.App()
frm=wx.Frame(None, -1, title="test")

## init Workspace
workspace = cellprofiler_core.workspace.Workspace(pipeline=pipeline,
                                                  module=x,
                                                  image_set=image_set,
                                                  object_set=object_set,
                                                  measurements=m,
                                                  image_set_list=image_set_list,
                                                  frame=frm,
                                                  create_new_window=False)
frm.Show(False)
## generate identify primary objects' output
x.show_window = True
x.run(workspace) #ON CHERCHE A RECUP NOYAUX SEGMENTÉS - COMMENT FAIRE ?

figure = cellprofiler.gui.figure.Figure(frm)
labeled_image = workspace.display_data.labeled_image
objects = object_set.get_objects("nuclei") #SET D'OBJETS CONTIENT JUSTE LE NOM "NUCLEI" MAIS PAS D'IMAGE, COMMENT OBTENIR L'IMAGE QUI VA AVEC L'OBJET ?

from matplotlib.figure import Figure
#x.display(workspace,figure)
figure.set_subplots((1, 1))


print("[EXTRACTING DATA]")

## ATTENTION : MODIFICATION DU CODE FIGURE.PY QUI RESORT L'IMAGE AVEC LES NOYAUX COLORÉS :
stuff = figure.subplot_imshow_labels(0, 0, labeled_image, title = None, use_imshow=False)

print("[DEBUG] FLAG 2")
data_primary = stuff[1] # = image avec noyaux colorés

## test - save data to txt files
#np.save("data_primary.npy", data_primary)

fig = figure.figure

## try to extract numpy array from fig
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


###############################################################################
# IDENTIFY SECONDARY OBJECTS -------------------------------------------------
## COMME DATA_PRIMARY EST EN DIMENSION 3 ON SEPARE + ADDITIONNE LES CANAUX
output0 = data_primary[:,:,0]
output1 = data_primary[:,:,1]
output2 = data_primary[:,:,2]

output4 = output0 + output1 +output2 #OUTPUT 4 = NOYAUX COLORÉS SERVIRA D'OBJET

# SETTINGS -------------------------------------------------
z= cellprofiler.modules.identifysecondaryobjects.IdentifySecondaryObjects()
z.image_name.value = "nuccyto"
z.x_name.value = "nuclei"
z.y_name.value == "cells"
z.method.value = cellprofiler.modules.identifysecondaryobjects.M_WATERSHED_G
z.threshold.threshold_scope.value = cellprofiler.modules.threshold.TS_GLOBAL
z.threshold.global_operation.value = cellprofiler.modules.threshold.TM_LI
z.threshold.threshold_smoothing_scale.value = 0
z.threshold.threshold_correction_factor.value = 1
z.threshold.threshold_range.min = 0
z.threshold.threshold_range.max= 1
z.regularization_factor.value = 0.05
z.fill_holes.value= True
z.wants_discard_edge.value = True
z.wants_discard_primary.value = False

## create pipeline
pipeline.add_module(z)

## init measurement
m2=cellprofiler_core.measurement.Measurements()
m2.add_measurement("my_image", "Tardis", "Value")

## init cpimage
#cpimage2 = cellprofiler_core.image.Image(img_cyto) ## NE SERT PLUS CAR ON RECUP L'IMAGE DU MODULE "IMAGE MATH"
image_set2 = cellprofiler_core.image.ImageSet(0, {}, {})
image_set2.add("nuccyto", im_output) #RECUP L'IMAGE DU MODULE "IMAGE MATH"


## init set list
image_set_list2 = cellprofiler_core.image.ImageSetList()

## init object set
# pour tout workspace, il faut un objet + objet set MAIS RIEN NE FONCTIONNE QUEL TYPE D'OBJET PEUT-ON DONNER POUR QUE ÇA FONCTIONNE ?
object_set2 = cellprofiler_core.object.ObjectSet()
objects0 = cellprofiler_core.object.Objects()
objects0.unedited_segmented = output4 ## seule manière de transformer array en object
objects0.segmented = output4
objects0.small_removed_segmented = output4

object_set2.add_objects(objects0, "nuclei") #INPUT OBJECT NAME - DONNE ÉCRAN NOIR

#width, height = combo.size
#app = wx.App()
frm2=wx.Frame(None, -1, title="test")
print("=> Flag 4")
print(image_set2.providers[0].name)
print(len(image_set2.providers))


workspace2 = cellprofiler_core.workspace.Workspace(pipeline=pipeline,
                                                  module=z,
                                                  image_set=image_set2,
                                                  object_set=object_set2,
                                                  measurements=m,
                                                  image_set_list=image_set_list2,
                                                  frame=frm2,
                                                  create_new_window=False)


frm2.Show(False)
#workspace2.image_set.get_image(cpimage2)
## generate identify 2ndary objects' output
figure2 = cellprofiler.gui.figure.Figure(frm2)
z.show_window = True
z.run(workspace2) 
z.display(workspace2, figure2) ## sert à l'affichage du résultat mais écran noir

segmented_out = workspace2.display_data.segmented_out
figure2.set_subplots((1, 1))
stuff = figure2.subplot_imshow_labels(0, 0, segmented_out, title = None, use_imshow=False)

fig2 = figure2.figure

app.MainLoop()






