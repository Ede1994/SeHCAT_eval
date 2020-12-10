#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2020

Author: Eric Einspänner, Clinic for Radiology and Nuclear Medicine, UMMD Magdeburg (Germany)

This program is free software.
"""

import numpy as np

background_0d = 91*10**3
background_7d = 86*10**3

ant_counts_0d = 1672*10**3
post_counts_0d = 1572*10**3

ant_counts_7d = 630*10**3
post_counts_7d = 580*10**3

decay_factor = 1.04

retention = decay_factor * (np.sqrt((ant_counts_7d - background_7d)*(post_counts_7d - background_7d))/np.sqrt((ant_counts_0d - background_0d)*(post_counts_0d - background_0d))) * 100.

print(retention)