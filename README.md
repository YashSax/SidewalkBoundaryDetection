# Sidewalk Boundary Detection
A Python program that utilizes OpenCV and Canny edge detection to determine the boundaries of a sidewalk and determine the safest angle the user must turn to remain on the sidewalk. Intended to assist the blind when navigating city environments, this algorithm is paired with a haptic feedback mechanism communicating the direction the user needs to turn via vibrating motors on the wrist.  
  
Using Canny Edge Detection with a Hough Transform, the algorithm calculates potential markers to represent the sidewalk boundary and, using the user's position, calculates the turn angle necessary to stay on the sidewalk.

Green lines represent candidate lines the algorithm considers, and the blue line represents the line the algorithm decides most accurately represents the boundary of the sidewalk the user should follow. 

https://user-images.githubusercontent.com/46911428/142981274-638ad450-319c-48bd-ae7d-b63ceb56e211.mp4

<h2>Edge Detection</h2>
Edge detection, as the name suggests, is the process of detecting edges within a picture. This algorithm uses Canny edge detection which, after applying a Gaussian blur to the image, by finding the intensity gradients and getting rid of edges not connected with strong edges, finds edges in a picture.  

![image](https://user-images.githubusercontent.com/46911428/142983544-cff4d167-5c39-4ad2-930e-4f6c921e5955.png)

<h2>How does the algorithm know which line to follow?</h2>

A picture after the Hough Transform has many candidate lines -- the algorithm uses length as a proxy for estimating the "strength" of a line. When pointing the camera at or below a 45&deg; as intended, the longest lines will always be those outlining the path of the sidewalk. Even if the algorithm wrongly suggests a line perpendicular to the path (for example, by recognizing the cracks between pavement blocks), a rolling average is implemented so deviations are smoothed out over time.  
  
If the heuristic doesn't find any suitable lines, it assumes the path is a curve, calculating and following the tangent line of the curve in front of the user by performing linear regression on the middle 10% of the Canny Edge Detection.

