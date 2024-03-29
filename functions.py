# -*- coding: utf-8 -*-
"""
Created on Tue May 18 13:19:01 2021

@author: Eric
"""
import math
import numpy as np

# describe the physical decay of radioactivity
def decay_equation(a0,T,t):
	# A = A0 * e^(- λ * t)
	a = int(a0 * math.exp(-math.log(2)/T * t))
	return a

def eff_decay_10(a0,T,t):
    t_10 = 2.107
    t_eff = 1/(1/T + 1/t_10)
    a = float(a0 * math.exp(-math.log(2)/t_eff * t))
    return a

def eff_decay_15(a0,T,t):
    t_15 = 2.558
    t_eff = 1/(1/T + 1/t_15)
    a = float(a0 * math.exp(-math.log(2)/t_eff * t))
    return a

# calculate physical decay of Se-75
def selen_decay(counts_0d, T_75se):
    dt = 0.0
    dt_list = []
    decay =  []
    while dt <= 8.0:
        x = decay_equation(counts_0d, T_75se, dt)
        decay.append(x)
        dt_list.append(dt)
        dt += 0.1
    return dt_list, decay

# calculate 10% and 15% retentions curve
def retention_lists(counts_0d, T_75se):
    retention_10 = []
    retention_15 = []
    dt = 0.0
    dt_list = []
    while dt <= 8.0:
        x = eff_decay_10(counts_0d, T_75se, dt) 
        y = eff_decay_15(counts_0d, T_75se, dt) 
        retention_10.append(x)
        retention_15.append(y)
        dt_list.append(dt)
        dt += 0.2
    return dt_list, retention_10, retention_15

# retention 1-energy-window
def retention_1w_calc(decay_factor, ant_counts_0d, ant_counts_7d, background_0d_ant, background_7d_ant, post_counts_0d, post_counts_7d, background_0d_post, background_7d_post):
    retention_1w = round(decay_factor * (np.sqrt((ant_counts_7d - background_7d_ant)*(post_counts_7d - background_7d_post)) \
                                          / np.sqrt((ant_counts_0d - background_0d_ant)*(post_counts_0d - background_0d_post))) * 100., 2)
    return retention_1w

# retention 2-energy-windows
def retention_2w_calc(decay_factor, ant_counts_0d_window1, ant_counts_0d_window2, ant_counts_7d_window1, ant_counts_7d_window2, background_0d_ant_w1, background_0d_ant_w2, background_7d_ant_w1, background_7d_ant_w2, post_counts_0d_window1, post_counts_0d_window2, post_counts_7d_window1, post_counts_7d_window2, background_0d_post_w1, background_0d_post_w2, background_7d_post_w1, background_7d_post_w2):
    retention_2w = round(decay_factor * (np.sqrt((ant_counts_7d_window1 + ant_counts_7d_window2 - background_7d_ant_w1 - background_7d_ant_w2)*(post_counts_7d_window1 + post_counts_7d_window2 - background_7d_post_w1 - background_7d_post_w2))) \
                      / np.sqrt((ant_counts_0d_window1 + ant_counts_0d_window2 - background_0d_ant_w1 - background_0d_ant_w2)*(post_counts_0d_window1 + post_counts_0d_window2 - background_0d_post_w1 - background_0d_post_w2)) * 100., 2)
    return retention_2w