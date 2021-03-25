# Simple python projection mapping

## Background

Simple projection mapping using tkinter and opencv for a school project. Designed to run on my mac with a 1024x768 projector with 1280x720 videos due to having barely any time to add better support, I may add better support in the future if I can be bothered.

Currently only supports mapping to quadrilaterals, such as boxes.

## Defining points

Points are defined with definedpoints.py Right clicking creates a polygon, left clicking sets a corner. Top left -> top right -> bottom right -> bottom left will ensure that the video is upright. Array of points will be printed to the console after each polygon is created.

## Projecting videos

Some demo videos are in the "media folder". Videos currently seem to only work at 1280x720, for some reason. Probably something about having to be the same size. Points are just defined in the "r" variable as an array straight from the output of definedpoints.py, and sources are in an array just below it. Should be easy enough to work out.

## Plans for future

As I work on this more, I will likely implement:

- Basic structured light scanning with webcam
- Video masking for shapes with more than 4 corners, such as circles
