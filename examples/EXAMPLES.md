# Example for Pathology Grading GUI
This document illustrates how to use Pathology Grading software. Installation guide can be found in *installation_guide.md* in this folder. To start the software, run *'python GUI_pyqt5.py'*

## Login
1) Login page shows up

![1_start_page](./pics/1_start_page.png)

2) Create new user account (First login)

![2_login_create_new_user](./pics/2_login_create_new_user.png)

3) Create new user sucessful

![3_login_sucessfull_create](./pics/3_login_sucessfull_create.png)

4) Login

![4_login](./pics/4_login.png)

5) GUI home page shows up

![5_GUI_home](./pics/5_GUI_home.png)


## Grading 
6) Grading by fill out comment in comment box (1), select primary and secondary grade in drop down (2) & (3)

![6_grading](./pics/6_grading.png)

### Navigation Toolbar

#### Zoom Tool
7) User can zoom in by using zooming tool (1). Then, select area of interest (2).

![7_zoom](./pics/7_zoom.png)

8) After release mouse, the canvas will be zoomed in. Note that x-coordinate and y-coordinate has changed.

![8_zoom_result](./pics/8_zoom_result.png)

#### Adjust Canvas Alignment

9) User can set alignment of canvas (1). Adjust position of borders and spacing when window pop-up (2). Click *tight layout* for auto adjustment or *reset* to reset canvas alignment.

![9_set_canvas](./pics/9_set_canvas.png)

#### Adjust x-coordination and y-coordination

10) User can set x-coordination and y-coordination of the canvas (1) on pop-up window (2)

![10_set_figure](./pics//10_set_figure.png)

#### Save canvas

11) User can save current canvas to image file (1). Select destination folder (2).

![11_save_figure](./pics/11_save_figure.png)

### Saving grading input

12) Click *save* button to save ...
- coordinate of current canvas position
- comments
- primary and secondary grade

![12_save_coor](./pics/12_save_coor.png)

13) Inspect csv output by navigating to result folder

![13_navigate_output_csv](./pics/13_navigate_output_csv.png)

14) Check output result in *Grading_result_[your_username]*

![14_output](./pics/14_output.png)

### Clear grading input

15) Click *Clear all* button to clear all input (comment textbox, primary, and secondary grade)

![15_clear](./pics/15_clear.png)

16) All input are cleared. Note that this only clear input in current GUI, but does not delete input that being save in csv file.

![16_clear_output](./pics/16_clear_output.png)
