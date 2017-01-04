# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/12/18


class para:
    # DoG space consturction
    s = 2
    k = 2**(1/s)
    # when using DoG space to find keypoints
    # key points can be searched in `s` images in each octave in DoG space,
    # which means there is s+2 images in each octave in DoG space,
    # and s+3 image in Gaussian space
    # σ(i+1) = kσ(i) in one octave

    DoG_octave_layers = s+2
    pyramid_octave_layers = s+3

    initial_sigma = 1.6
    gaussian_size = (3, 3)

    pyramid_top_size = 32*32  # if this value is too small, no neiborhood can be set on the image to calculate orientation
    pyramid_size_ratio = 0.6
    max_keypoints_per_layer = 50

    # calculate orientation of keypoints
    orient_bins = 36
    sample_size = 8
    sample_radius = int(sample_size * 1.414)
    orient_threshold = 0.8

    # descriptor
    descr_n = 4  # we have `descr_n**2` descriptor seed points in total
    descr_size = 4  # a width of window used to calc each descriptor seed point
    # it should be assured that `descr_n / 2 * descr_size` < `sample_size`
    # otherwise extra endavor should be made to prevent descriptor sample neighrhood from exceeding img boundary
    descr_bins = 8
    descr_gaussian_ratio = 6

    # descriptor matching
    descr_match_contrast = 0.7  # the larger, the more matches
    descr_match_threshold = 0.2  # the larger, the more matches


def get_sigma_by_layer_relative(layer_ind):
    return para.initial_sigma * (para.k ** (layer_ind*2) - para.k ** ((layer_ind - 1) * 2)) ** 0.5

def get_sigma_by_layer(layer_ind):
    return para.initial_sigma * (para.k ** layer_ind)

def get_scale_by_ind(octave_ind, layer_ind):
    return get_sigma_by_layer(layer_ind) / get_size_ratio_by_octave(octave_ind)

def get_size_ratio_by_octave(octave_ind):
    return para.pyramid_size_ratio ** octave_ind

