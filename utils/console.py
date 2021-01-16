#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" ASCII rendering module for flying donut.

For more information, see README.

For usage, run <python3 donut.py>.

Project can be found here <https://github.com/ingranys/flying-donut>.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "ingranys"
__contact__ = "ingranys@protonmail.com"
__copyright__ = "Copyright 2021, Mustapha Gaies, Toulouse (France)"
__date__ = "2021/01/16"
__deprecated__ = False
__email__ =  "ingranys@protonmail.com"
__license__ = "GPLv3"
__maintainer__ = None
__status__ = "Production"
__version__ = "0.1.0"


import sys
import time
import curses
import numpy


def warning(mode='<mode>',duration=10):
    """Print user warning.

    Args:
        mode (str, optional): Mode (can PREVIEW or DEBUG). Defaults to '<mode>'.
        duration (int, optional): Message duration in seconds. Defaults to 10.
    """
    print('WARNING!')
    print('{0} mode is enabled with a large number of points.'.format(mode))
    print('Be aware of possible lag while rendering.')
    for remaining in range(duration, -1, -1):
        print("Continue in {:2d} seconds...".format(remaining),end="\r")
        time.sleep(1)
    # Use ASCII escape sequence
    #https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    print("\033[2K",end="\r")
    print("Moving on to the rendering.")


def screen(n_pixels):
    """Initialize ascii screen.

    Args:
        n_pixels (int): Screen size in pixels (each pixel is ASCII character).

    Returns:
        scr (screen): Initialized screen.
        frame_height (int) : ASCII frame height. 
        frame_width (int) : ASCII frame width (ASCII image aspect ratio is 2:1).
    """
    # Initialize screen
    scr = curses.initscr()

    # Get the maximum possible size for the current console
    screen_height,screen_width= scr.getmaxyx()
    # Get the maximum possible size for the ascii screen within the console
    # IMPORTANT! It takes twice as much columns than lines to draw ascii art
    frame_size = min(screen_height,numpy.floor(screen_width/2).astype(int))
    if n_pixels<=0:
        # Auto-scale
        frame_height = frame_size
        frame_width = 2*frame_size
    elif n_pixels<=frame_size:
        # Manual scale
        frame_height = n_pixels
        frame_width = 2*n_pixels
    else :
        # Contraints can't be applied
        # Go back to previous console display and print error message
        curses.endwin()
        print('ERROR!')
        print('Image size exceeds console size.')
        print('Please decrease pixels number or widen console.')      
        sys.exit()         

    # Clear screen to finish initialization
    scr.clear()
    scr.refresh()

    return scr,frame_height,frame_width


def reset():
    """Go back to previous console display
    """
    curses.endwin()


def asciis(pixels,char):
    """Convert 2D grayscale image to ASCII characters.

    Args:
        pixels (array(float)): 2D array representing graysclale image.
        char (array(str)): List of ASCII characters.

    Returns:
        ascii_characters (array(str)): 
    """
    n_rows, n_columns = pixels.shape
    n_char = len(char)
    # Map intensity values to characters
    ascii_characters =   [
                            [char[int(numpy.floor(n_char*pixels[i,j]))] 
                            for j in range(n_columns)] 
                        for i in range(n_rows)]
                          
    return ascii_characters


def render(ascii_characters,screen,current_frame,n_frames):
    """Print ASCII characters to console.

    Args:
        ascii_characters (array[str]): 2D array containing ASCII characters.
        screen (screen): ASCII screen. 
        current_frame (int): Current frame number.
        n_frames (int): Total number of frames.
    """
    # Get frame shape
    n_rows = len(ascii_characters)
    n_columns = len(ascii_characters[0])
    # Print ASCII characters one by one
    for i in range(n_rows):
        for j in range(n_columns):
            screen.addstr(i, j, ascii_characters[i][j])
    msg = '{0}/{1}'.format(current_frame+1,n_frames)
    # Refresh screen
    screen.addstr(0, 0, msg )
    screen.refresh()