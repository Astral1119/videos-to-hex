"""
This is a script that takes a video file and converts it to a csv of consecutive frames in hex format.
It is intended for use with Google Sheets color divs.
Arguments:
    -i: input file
    -o: output file
    -d: dimensions of each frame
    -f: frame rate

Due to the nature of Google Sheets color divs, it only works within a reduced color space (3 bits per channel).
"""

import cv2
import numpy as np
import argparse
import csv

def main():
    parser = argparse.ArgumentParser(description='Convert a video to a csv of frames in hex format.')
    parser.add_argument('-i', '--input', type=str, help='Input video file')
    parser.add_argument('-o', '--output', type=str, help='Output csv file')
    parser.add_argument('-d', '--dimensions', type=str, help='Dimensions of each frame in the format widthxheight')
    parser.add_argument('-f', '--frame_rate', type=int, help='Frame rate')
    args = parser.parse_args()

    # Read video
    cap = cv2.VideoCapture(args.input)
    width, height = map(int, args.dimensions.split('x'))
    frame_rate = args.frame_rate
    frame_interval = int(cap.get(cv2.CAP_PROP_FPS) / frame_rate)

    # Write csv
    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        frame = 0
        while True:
            ret, img = cap.read()
            if not ret:
                break
            if frame % frame_interval != 0:
                frame += 1
                continue
            img = cv2.resize(img, (width, height))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img.astype(np.uint16)
            img = (img // 32) * 32
            for row in img:
                row_data = []
                for pixel in row:
                    row_data.append(f"#{pixel[0]:02X}{pixel[1]:02X}{pixel[2]:02X}")
                writer.writerow(row_data)
            frame += 1

    cap.release()

if __name__ == '__main__':
    main()
