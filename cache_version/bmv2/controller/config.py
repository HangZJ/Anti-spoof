#!/usr/bin/env python
# coding=utf-8

import socket
import struct

CONTROLLER_IP = "192.168.56.101"
TYPE_IPV4 = 0x0800
TYPE_TCP = 0x06
FLAG_SYN = 0b000010
FLAG_ACK = 0b010000
# # TYPE_NETHCF_IP2HC is used for transfering counter arrays of switch
# TYPE_NETHCF_IP2HC = 0xAB
# # TYPE_NETHCF_MISX is used for transfering miss and mismatch counters
# TYPE_NETHCF_MISX = 0xCD
TYPE_NETHCF = 0xAB
ALPHA = 0.2
LAMBDA = 0.1
THETA = 20
CACHE_SIZE = 10
# CACHE_SIZE = 100000

IP_SPACE_SIZE = 2**8
# IP_SPACE_SIZE = 2**25

LEARN_TO_FILTER_THR = 20
FILTER_TO_LEARN_THR = 15

BMV2_PATH = "/home/dracula/p4_environment/behavioral-model"
TARGET_SWITCH = BMV2_PATH +  "/targets/simple_switch/sswitch_CLI"
TARGET_CODE = "hop_count.json"
TARGET_PORT = 22223

NETHCF_SWITCH_CONFIG = {
    # counter name in p4
    "miss_counter": "miss_counter",
    "mismatch_counter": "abnormal_counter",
    "ip2hc_counter": "hit_count",
    # hc value register array name in p4
    "ip2hc_register": "hop_count",
    # IP2HC Match-Action-Table name in p4
    "ip2hc_mat": "ip_to_hc_table",
    # IP2HC Match-Action-Table action name in p4
    "read_hc_function": "table_hit",
    # State register name in p4
    "hcf_state": "current_state"
}

DEBUG_OPTION = True

def impact_factor_function(total_matched, last_matched):
    impact_factor = ALPHA * total_matched + (1 - ALPHA) * last_matched
    return impact_factor

def number_to_be_replaced(miss_counter):
    return min(int(miss_counter * LAMBDA), THETA)

