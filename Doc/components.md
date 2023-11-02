# Components

## GUI:

- What it does: Shows features, allows pathologist to grade and tag data. Displays and moves through sequence of images.
- Inputs: Raw data (file directory with .tif files), pathologist UID, model selection for AI pregrading.
- Outputs: Tagged/graded images (.csv or .json dict or both)
- How to use other components: Buttons, dropdouns, mouse clicks

## Annotation of Images:

- What it does: Displays a box where the user selects, records the coordinates of the box, associates the boxes with their respective image. 
- Inputs: Boxes, images
- Outputs: images and box coordinates (linked)
- How to use other components: Click and drag to generate box regions for each image

## Buttons:

### Next Image:

### Previous Image:

### Select Directory:

### Export:

### Save (partially graded):

### Clear Image:

### Clear All Images:

### Grading tags: if Good/Bad

## Dropdowns:

### Grading tags: if >2 attributes

### Select Model

## Pan:

## Zoom:

## Input Image Directory:

### Popup Window:

## Output Directory:

### Popup Window:

## UID Database:

### Popup for Entry and Auth.:

## Model Database/Directory:

## Executable File: