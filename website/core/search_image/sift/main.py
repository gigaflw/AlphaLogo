# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/11/30
from __future__ import division, print_function

import os
import time
import argparse

from sift import SIFT
from test import precision_test, testset_generator, dataset_generator
import cv2


def ptest(d, ns):
    sift = SIFT(debug=d)

    print("SIFT precision test begins")
    print("preprocessing....")
    im = cv2.imread("target.jpg", 0)
    dp1, pos1 = sift.process(im, draw_keypoints=False)
    print("done")

    for name, im_test, validate in testset_generator(im):
        filename = os.path.join("precision_test", "match_%s.jpg" % name)
        cv2.imwrite(os.path.join("precision_test", "test_%s.jpg" % name), im_test)

        t0 = time.time()
        matches = sift.match(im, im_test, draw_matches=not ns, match_filename=filename, descriptors1=dp1, positions1=pos1)
        t = time.time() - t0
        
        prec = precision_test([[p1, p2] for p1, p2, _ in matches], validate)

        print("%d matches found for '%s'." % (len(matches), name))
        print("precision: %.5f" % prec)
        print("time consumed: %.3f sec" % t)
        if not ns:
            print("Matching result written to '%s'." % filename)


def rtest(d, ns):
    sift = SIFT(debug=d)

    print("SIFT resolution test begins.")

    print("preprocessing target....")
    im = cv2.imread("target.jpg", 0)
    dp1, pos1 = sift.process(im, draw_keypoints=False)
    precompute = []

    m1, m2 = ('nofile', 0), ('nofile', 0)
    print("done")
    
    print("preprocessing dataset....")
    t = 0
    for name, im_test in dataset_generator(dir_name="dataset"):
        t0 = time.time()
        
        dp2, pos2 = sift.process(im_test, draw_keypoints=False)
        precompute.append((dp2, pos2, name, im_test))
        
        t1 = time.time()
        t += t1 - t0
        print("'%s' done in %.5f secs" % (name, t1 - t0))
    print("done %d imgs in %.5f secs, aver %.5f secs" % (len(precompute), t, t / len(precompute)))

    print("matching ....")
    t0 = time.time()
    for dp2, pos2, name, im_test in precompute:
        filename = os.path.join("resolution_test", "match_%s" % name)  # `name` should already end with '.jpg'

        m = sift.match(im, im_test, draw_matches=not ns, 
            match_filename=filename, descriptors1=dp1, positions1=pos1, descriptors2=dp2, positions2=pos2)

        if len(m) > m1[1]:
            m1, m2 = (name, len(m)), m1
        elif len(m) > m2[1]:
            m2 = (name, len(m))

        print("%d matches found for '%s'." % (len(m), name))
        if not ns:
            print("Matching result written to '%s'." % filename)
    t1 = time.time()
    print("done %d matches in %.5f secs" % (len(precompute), t1-t0)) 

    resol = (1 - m2[1] / m1[1]) * (1 - 1 / m1[1])

    print("\n'%s' best matched with %d matches" % m1)
    print("'%s' with %d matches follows" % m2)
    print("Confidence : %.2f%%" % (resol*100))

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--precision_test', action="store_true", default=False,
                    help="Carry out precision test")
parser.add_argument('-r', '--resolution_test', action="store_true", default=False,
                    help="Carry out resolution test")
parser.add_argument('-d', '--debug', action="store_true", default=False,
                    help="Debug mode with intermediate images saved and detail printed")
parser.add_argument('-no_save', action="store_true", default=False,
                    help="Do not save anything")


if __name__ == '__main__':
    args = parser.parse_args()
    if args.precision_test and not args.resolution_test:
        ptest(args.debug, args.no_save)
    elif args.resolution_test and not args.precision_test:
        rtest(args.debug, args.no_save)
    else:
        parser.print_help()



