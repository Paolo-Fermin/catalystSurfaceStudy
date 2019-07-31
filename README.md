# Catalyst Surface Study

The purpose of this directory is to use Catalyst with OpenFOAM to extract only the relevant cells in a wake image simulation at every timestep to greatly decrease storage usage. The results of each field at each timestep can be viewed with Paraview, translated along the x-axis based upon velocity of the theoretical ship passing through the water, so that a wake image is produced in an accurate xyz coordinate space. 

## What is Catalyst?

Catalyst is a Paraview plugin that "adds in-situ and live visualization capabilities to arbitrary OpenFOAM simulations". See more details at https://www.openfoam.com/releases/openfoam-v1806/post-processing.php

## Workflow

1. Create Catalyst script for each field extract using the Paraview GUI
2. Include Catalyst scripts in Catalyst function object
3. Modify controlDict
4. Run OpenFOAM
5. Run Python script to translate vtk object results


### Create Catalyst scripts

For each extract you want from the base simulation, you will have to create a new Catalyst script. The majority of this script can be created through the Paraview GUI. In more recent versions of the GUI, open the Catalyst Export Inspector window by clicking `Catalyst > Define Exports` in the toolbar. Under the Data Extracts section of the window, use the leftmost dropdown to select what portions of the pipeline to export using Catalyst. In this case, we are using several Threshold filters to select cells that are within a range of field values. Then, use the middle dropdown to select the `XMLMultiBlockDataWriter`, and check the checkbox. Finally, click the `...` button on the right and check the checkbox to "Write timesteps as file-series". You are done defining what to export. 

Before proceeding, take a look at your Catalyst dictionary and rename the root object in your Pipeline to the name of the input that is defined in that dictionary. For example, in this case, I renamed the object "basecase.foam" to "region". If you forget to do this step, don't worry. You can edit the Catalyst script manually and update all instances of the old name where they are defined in the `_CreatePipeline()` function. 

Finally, go back to the toolbar and select Catalyst > Export Catalyst Script, and save it wherever you like. In this case, the scripts are stored in the `<case>/system/scripts` directory, and named according to which field was used in the Threshold filter. 

### Include Catalyst script in Catalyst function object

We are still using OpenFOAM, and thus, many things are defined in C++ dictionaries. To use Catalyst, we need to have a dictionary known as the "Catalyst function object for OpenFOAM". Examples of this can be found online, and the one for this case is stored as `<case>/system/catalyst`. Include the pathname leading to your Catalyst scripts within the scripts section at the top of the Catalyst dictionary, and define what fields and regions you want to export in the input section at the bottom. 

### Modify controlDict

At the bottom of `<case>/system/controlDict`, make sure that OpenFOAM calls the Catalyst function object by including in `functions { #include catalyst }`. Also, modify the `purgeWrite` variable to any nonzero value. This will save memory in your system. Because we are using Catalyst, we extract the relevant data on the fly and can ignore the rest. 

### Run OpenFOAM

The relevant bash commands are included in `runCase`. If you are running Catalyst, you can comment out the postProcessing line, as it is not necessary.

### Transform results

Run `python ./scripts/transform.py` to iterate through every timestep available in the /insitu/ directory and translate each object along the x-axis according to the position that it would be given the time and velocity of the ship. The transform results are stored in the `/transform/ directory`, and can be viewed in Paraview by selecting the .vtm object associated with each field produced by the Python script. Using the Group Timesteps filter in Paraview will allow you to view all timesteps at once, and the Extract Timesteps filter allows you to select a range of timesteps for more focused viewing. 

