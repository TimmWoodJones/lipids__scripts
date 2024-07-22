import os
import cv2
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('press')
parser.add_argument('mode')
parser.add_argument('subject')

args=parser.parse_args()

press=args.press
mode=args.mode
subj=args.subject

directory='TP_space/P'+press+'/'+mode+'ing/'

if subj=='hex_proj':

    path=directory+'hex_proj_frames/'

    name=directory+'hex_proj_movie_P'+press+'.avi'

elif subj=='hex_mod':

    path=directory+'hex_mod_frames/'

    name=directory+'hex_mod_movie_P'+press+'.avi'

elif subj=='spin':

    path=directory+'spin_frames/'

    name=directory+'spin_movie_P'+press+'.avi'

elif subj=='dens_hist':

    path=directory+'dens_hist_frames/'

    name=directory+'dens_hist_movie_P'+press+'.avi'

elif subj=='hex_hist':

    path=directory+'hex_mod_hist_frames/'

    name=directory+'hex_mod_hist_movie_P'+press+'.avi'

elif subj=='spin_hist':

    path=directory+'spin_hist_frames/'

    name=directory+'spin_hist_movie_P'+press+'.avi'


images=[image for image in os.listdir(path)]

frame = cv2.imread(os.path.join(path, images[0]))

height, width, layers = frame.shape


movie = cv2.VideoWriter(name, 0, 5, (width,height))

for img in images:
    movie.write(cv2.imread(os.path.join(path, img)))

cv2.destroyAllWindows()
movie.release()


#create array of images



