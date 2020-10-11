# Snowmaker PY
[![Snowmaker PY](https://github.com/LyfeOnEdge/snowmaker/blob/master/console.png?raw=true)]()

Snowmaker is a tool for generating snow animations in python for use in gifs / games.

For module use download snowmaker.py and import the snow generating function with `from snowmaker import generate_snow`

## Function Arguments:
```py
def generate_snow(
		canvas_size,
		scale : int = 1,
		rate : int = 4,
		vector : tuple = (0,1),
		frames : int = 10,
		color : tuple = (255,255,255,255),
		background : tuple = (0,0,0,0),
		wrap_left_shift : bool = False,
		wrap_right_shift : bool = False,
		wrap_up_shift : bool = False,
		wrap_down_shift : bool = False,
		h_drift : int = 50,
		h_drift_radius : int = 4,
		wrap_h_drift : int = True,
		v_drift : int = 10,
		v_drift_radius : int = 4,
		wrap_v_drift : bool = False
	):

```

- Vector is a tuple of two ints like (0,-1) [which would make the particles move south]
- Scale is an integer to scale the output frames by
- Rate is the number of new particles spawned per frame
- frames is the number of frames to produce
- color is the rgba color tuple to set the droplet particles to
- background is the rgba color tuple to set the background to
- the wrap_*_shift arguments specify if the area introduced after the move of the array should be filled with a wrapped copy of the overwritten data or a different value
- \*_drift is the number of row / column shifts to attempt each frame advance
- \*_drift_radius is the max number of pixels a particle can move in that dimension each frame advance
- \*wrap_*_drift argumewnts specify if random drift should cause particles to wrap in that direction



## Command Line Usage

```
usage: snowmaker.py [-h] [--width WIDTH] [--height HEIGHT] 
[-fg FOREGROUND] [-bg BACKGROUND] [-f FRAMES] [-s SCALE]
[-r RATE] [-x XVELOCITY] [-y YVELOCITY] [-wl] [-wr] [-wu] 
[-wd] [-hd HORIZONTALDRIFT] [-hr HORIZONTALDRIFTRADIUS]
[-whd] [-vd VERTICALDRIFT] [-vr VERTICALDRIFTRADIUS] [-wvd]
output

positional arguments:
  output                Output gif path

optional arguments:
  -h, --help            show this help message and exit
  --width WIDTH         Width of canvas, defaults to 500
  --height HEIGHT       Height of canvas, defaults to 500
  -fg FOREGROUND, --foreground FOREGROUND
                        Color of flakes in hex RGBA, defaults to #FFFFFFFF
  -bg BACKGROUND, --background BACKGROUND
                        Color of background in hex RGBA, defaults to #00000000
  -f FRAMES, --frames FRAMES
                        Number of frames to output, defaults to 300
  -s SCALE, --scale SCALE
                        Output scale of image, defaults to 1
  -r RATE, --rate RATE  Particle generation rate, defaults to 2
  -x XVELOCITY, --xvelocity XVELOCITY
                        X velocity of particles on the canvas, defaults to 0
  -y YVELOCITY, --yvelocity YVELOCITY
                        Y velocity of particles on the canvas, defaults to -1
  -wl, --wrapleft       Wrap particles on canvas shift left
  -wr, --wrapright      Wrap particles on canvas shift right
  -wu, --wrapup         Wrap particles on canvas shift up
  -wd, --wrapdown       Wrap particles on canvas shift down
  -hd HORIZONTALDRIFT, --horizontaldrift HORIZONTALDRIFT
                        Number of horizontal drifts to apply in each direction to the canvas to simulate flutter,
                        defaults to 50.
  -hr HORIZONTALDRIFTRADIUS, --horizontaldriftradius HORIZONTALDRIFTRADIUS
                        Max size of horizontal drift, defaults to 4
  -whd, --wraphorizontaldrift
                        Wrap particles on horizontal drift
  -vd VERTICALDRIFT, --verticaldrift VERTICALDRIFT
                        Number of vertical drifts to apply in each direction to the canvas to simulate flutter,
                        defaults to 50.
  -vr VERTICALDRIFTRADIUS, --verticaldriftradius VERTICALDRIFTRADIUS
                        Max size of vertical drift, defaults to 10
  -wvd, --wrapverticaldrift
                        Wrap particles on vertical drift
```

For example `python snowmaker.py snowmaker.gif --width 100 --height 200 -f 300 -s 2 -r 1 -x "1" -y "-1" -wr -whd -wvd` would create a 200x400 gif at snowmaker.gif with the particles shift down and to the right 1 pixel each frame and wrapping to the right. Wrap horizontal (-whd) and vertical (-wvd) on drift helps to prevent noticible blank areas when an area has shifted.

[![Snowmaker GIF](https://github.com/LyfeOnEdge/snowmaker/blob/master/snowmaker.gif?raw=true)]()