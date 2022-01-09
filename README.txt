To build the app follow the steps:
READ ALL THE STEPS FIRST, then proceed with your project.

MAKE OPENCV APPS:
It's recommended to use Linux 18.04 and use pycharm, to download pycharm and setup linux to build android apps see the tutorial:
https://www.youtube.com/watch?v=c4tuSxSoERY&t=245s&ab_channel=NorbertTiborcz
On the OpencvAPP folder there are a few exemples of opencv codes with kivy, the buildozer.specs and app_layout.kv files are included too

USE ZBARCAM:
It's also recommended to use Linux 18.04 and use pycharm
1- Download the zbarcam github project: https://github.com/kivy-garden/zbarcam
2- Create a python project on Pycharm or any other IDE virtual enviroment
3- Extract the zbarcam files in the python project
4- Install Cython and Buildozer libraries on your python enviorment
5- On the "scr" there is a main.py file, white your code inside this file
6- On the terminal of the virtual enviroment (On Pycharm is the terminal option in the bottom) write: buildozer init
7- Now write on the terminal: buildozer android debug deploy run
