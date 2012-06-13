1. Turn on computer and projector (red button on top of projector)

2. Log in to Jack Kalish on the computer (double click on the icon to log in)

3. When RemoteCapture software starts, connect to camera. If connection fails, just click the "connect" button in the top right corner to try again.

4. Once the camera is connected, click the "ViewFinder On" button, then zoom in about half way, or a little more than half way, using the zoom slider on the bottom right.

5. Click the "AF lock" button to lock the autofocus

6. Turn the AF Assist Light off.

7. Now go to File > Interval Timer Shooting…

8. Click "yes" when prompted.

9. Leave minutes as 0, enter 5 for seconds, and for total number of frames,  enter the number of "Shots to Go" (this should be around 9000 or so)

10. Hit start

11. Make sure there is no paper in the clip board, but place a piece of text ON TOP of the clipboard (you will need this later for calibration)

12. To run software from terminal (you can use the up arrow key to cycle through previously entered commends):

cd /Users/kalicious/itp/spring2011/illuminated_man/build 

<hit enter>

java -d32 -jar -Xmx500M processing/processing-py.jar illumination.py

<hit enter>

13. After a few seconds, a yellow window will appear on the screen, drag this over to the right, so that it is positioned in the top-right corner of the projector image.

14. Calibration - hit the "C" key on the keyboard to enter calibration mode. After a few seconds, an image of the text on the clipboard will be projected.

15. Align the image. Use the arrow keys on the clipboard to move the image. Use the < > keys to scale the image. Use the + - keys to control horizontal scale, and the { } keys to control vertical scale.

16. Once the image is lined up sufficiently with the text, hit the "c" key again to exit from calibration mode.

16. You are done. To test it, place a text in the clipboard. After a few seconds, the light will begin to flicker. After 1-2 minutes, the light will fade and the poetry will begin.

17. If the boxes ever seem a bit off, you can calibrate by using the arrow keys as outlined above, even while the poetry is running.

18. If the software ever crashed, restart from step 