# Component specification
### Main components
1. [Authenticate users](#1-authenticate-users)
2. [Image visualizer and navigation tools](#2-image-visualizer-and-navigation-tools)
3. [Displays: "User name", "x-coordinate", "y-coordinate"](#3-displays-user-name-x-coordinate-y-coordinate)
4. [Comment textbox](#4-comment-text-box)
5. [Dropdowns: "Primary grading", "Secondary grading"](#5-dropdowns-primary-grading-secondary-grading)
6. [Buttons: "Next", "Previous", "Clear all", "Save"](#6-buttons-next-previous-clear-all-save)

## 1. Authenticate users
- *What it does:* Verifies a user is in the database or creates new user.
- *Inputs:* User name, user password (stings).
- *Outputs:* True if success, Flase if failure (Boolean).

## 2. Image visualizer and navigation tools
**Image visualizer**

- *What it does:* Visualize prostate cancer pathology image, along with an image title of sample name, x and y-axis. 
- *Inputs:* Raw data of .TIF files directories (String).
- *Outputs:* Matplotlib canvas showing the 2D numpy array image.

**Navigation tools**
- *What it does:* Zoom in, pan to a different region.
- *Inputs:* Click trigger (Boolean).
- *Outputs:* Shows zoomed in or specific regions of the image.

## 3. Displays: "User name", "x-coordinate", "y-coordinate"
**User name display**
- *What it does:* Displays the name of the user who logged in.
- *Inputs*: Initialized/triggered by "Authenticate user" (Boolean).
- *Outputs*: Name of the user displays on the Username textbox (String). 

**x-coordinate display**
- *What it does:* Displays the x-coordinate of a zoomed in region .
- *Inputs:* Triggered when the navigation button is pushed and canvas finished visualizing image (Boolean). 
- *Outputs:* x-coordinate of the current zoomed in region of the image, displaying on the x-coordinate textbox (float64). 

**y-coordinate display**
- *What it does:* Displays the y-coordinate of a zoomed in region .
- *Inputs:* Triggered when the navigation button is pushed and canvas finished visualizing image (Boolean). 
- *Outputs:* y-coordinate of the current zoomed in region of the image, displaying on the y-coordinate textbox (float64). 

## 4. Comment text box
- *What it does:* Allows user to enter comment about the image.
- *Inputs*: User comments (String)
- *Ouputs:* /

## 5. Dropdowns: "Primary grading", "Secondary grading"
**Primary grading**
- *What it does:* Allows user to choose the cancer aggressiveness of the displaying prostate cancer pathology image, i.e. grade 3, grade 4, and grade 5, as the primary (dominating) cancer pattern. 
- *Inputs:* Dropdown manuals of "3", "4", or "5" (String)
- *Outputs:* /

**Secondary grading**
- *What it does:* Allows user to choose the cancer aggressiveness of the displaying prostate cancer pathology image, i.e. grade 3, grade 4, and grade 5, as the secondary(non-dominating) cancer pattern. 
- *Inputs:* Dropdown manuals of "3", "4", or "5" (String)
- *Outputs:* /

## 6. Buttons: "Next", "Previous", "Clear all", "Save"
**Next button**
- *What it does:* Display the next pathology image on the image dataset list. 
- *Inputs:* Triggered by pushing the button (boolean), loading the next .TIF file directory (String)
- *Outputs:* Matplotlib canvas showing the next 2D numpy array image.

**Previous button**
- *What it does:* Display the previous pathology image on the image dataset list. 
- *Inputs:* Triggered by pushing the button (boolean), loading the previous .TIF file directory (String).
- *Outputs:* Matplotlib canvas showing the previous 2D numpy array image.

**Clear all button**
- *What it does:* Clear all entries for user inputs, including primary grading, secondary grading, and user comments.
- *Inputs: *Triggered by pushing the button (boolean).
- *Outputs:* Cleared primary grade and secondary grade and dropdowns.

**Save button**
- *What it does:* Save all user inputs into a .csv file, including the following 8 parameters: Datetime, user name, image name, user comments, x-coordinate, y-coordinate, primary grading, and secondary grading. 
- *Inputs:* Triggered by pushing the button (boolean), and the values of the 8 parameters (String).
- *Outputs:* .CSV file tabulating all the 8 parameters.