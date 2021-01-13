import time
import curses
import numpy


def warning(mode='<mode',duration=10):
    print('WARNING!')
    print('{0} mode is enabled with a large number of points.'.format(mode))
    print('Be aware of possible lag while rendering.')
    for remaining in range(duration, -1, -1):
        print("Continue in {:2d} seconds...".format(remaining),end="\r")
        time.sleep(1)
    #https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    print("\033[2K",end="\r")
    print("Moving on to the rendering.")


def screen():
    scr = curses.initscr()
    scr.clear()
    scr.refresh()

    return scr


def reset():
    curses.endwin()


def asciis(pixels,char):
    n_rows, n_columns = pixels.shape
    n_char = len(char)
    ascii_characters =   [
                            [char[int(numpy.floor(n_char*pixels[i,j]))] 
                            for j in range(n_columns)] 
                        for i in range(n_rows)]
    return ascii_characters


def render(ascii_characters,screen,current_frame,n_frames):
    n_rows = len(ascii_characters)
    n_columns = len(ascii_characters[0])
    screen.addstr(0, 0, str(current_frame) )
    for i in range(n_rows):
        for j in range(n_columns):
            screen.addstr(i, j, ascii_characters[i][j])
    msg = '{0}/{1}'.format(current_frame+1,n_frames)
    screen.addstr(0, 0, msg )
    screen.refresh()