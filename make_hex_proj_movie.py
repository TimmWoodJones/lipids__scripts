import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('press')
parser.add_argument('mode')

args=parser.parse_args()

press=args.press
mode=args.mode


os.system('python hex_proj_traj_maker.py ' + press + ' ' + mode)

os.system('python plot_hex_proj_traj.py ' + press + ' ' + mode + ' all')

os.system('python movie_maker.py ' + press + ' ' + mode + ' hex_proj')
