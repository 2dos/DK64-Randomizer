/**
 * @file switches.c
 * @author Ballaam
 * @brief Functions related to switches
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

int hasChunkyPhaseSlam(void) {
	return MovesBase[KONG_CHUNKY].simian_slam >= Rando.chunky_phase_krool_slam_req;
}