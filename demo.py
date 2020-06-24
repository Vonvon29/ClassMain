import os

import cellprofiler_core.image
import cellprofiler_core.measurement
import cellprofiler_core.object
import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.workspace
import numpy as np
import pandas as pd
import skimage.io


def run_pipeline(pipeline_filename, image_dict):
    cellprofiler_core.preferences.set_headless()

    # Create and load the pipeline
    pipeline = cellprofiler_core.pipeline.Pipeline()
    pipeline.load(pipeline_filename)

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



def objects2df(measurements, objects_name):
    features = measurements.get_feature_names(objects_name)

    n_features = len(features)
    n_objects = int(measurements.get_measurement("Image", "Count_{}".format(objects_name)))

    data = np.empty((n_objects, n_features))

    for feature_idx, feature in enumerate(features):
        data[:, feature_idx] = measurements.get_measurement(objects_name, feature)

    return pd.DataFrame(
        data=data,
        index=np.arange(1, n_objects + 1),
        columns=features
    )


# This should match what NamesAndTypes would produce.
images = {
    "OrigBlue": skimage.io.imread("data/01_POS002_D.TIF"),
    "OrigGreen": skimage.io.imread("data/01_POS002_F.TIF"),
    "OrigRed": skimage.io.imread("data/01_POS002_R.TIF")
}


pipeline_filename = "ExampleFly.cppipe"

workspace = run_pipeline(pipeline_filename, images)


# Get the "Nuclei" object measurements, as a pandas DataFrame
df = objects2df(workspace.measurements, "Nuclei")
print(df.head())

# Display the "RGBImage" image, created by GrayToColor

import matplotlib.pyplot as plt
rgb_image = workspace.image_set.get_image("RGBImage")
skimage.io.imshow(rgb_image.pixel_data)
plt.show()
