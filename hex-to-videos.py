"""
This is a script that takes a CSV file with hex values and converts them to a video file.
It's meant to preview videos encoded with videos-to-hex.py
Arguments:
    -i: input file
    -o: output file
    -d: dimensions of each frame
    -f: frame rate
"""

import cv2
import numpy as np
import argparse
import csv
import sys

def main():
    parser = argparse.ArgumentParser(description='Convert a csv of frames in hex format to a video.')
    parser.add_argument('-i', '--input', type=str, help='Input csv file')
    parser.add_argument('-o', '--output', type=str, help='Output video file')
    parser.add_argument('-d', '--dimensions', type=str, help='Dimensions of each frame in the format widthxheight')
    parser.add_argument('-f', '--frame_rate', type=int, help='Frame rate')
    args = parser.parse_args()

    # read height rows of width columns each for each frame
    width, height = map(int, args.dimensions.split('x'))
    frame_rate = args.frame_rate
    frame_interval = int(frame_rate / 30)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(args.output, fourcc, frame_rate, (width, height))

    with open(args.input, 'r') as csvfile:
        reader = csv.reader(csvfile)
        frame = 0
        while True:
            row_data = []
            for i in range(height):
                row = next(reader, None)
                if row is None:
                    break
                row_data.append(row)
            if row_data == []:
                break
            img = np.zeros((height, width, 3), dtype=np.uint8)
            for i, row in enumerate(row_data):
                for j, pixel in enumerate(row):
                    img[i, j] = tuple(int(pixel.lstrip('#')[k:k+2], 16) for k in (0, 2, 4))
            if frame == 0:
                cv2.imwrite('test.png', img)
            out.write(img)
            frame += 1

    out.release()

if __name__ == '__main__':
    main()
