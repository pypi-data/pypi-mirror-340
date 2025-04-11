/**
 * @file   attenuation.c
 * @author Zhu Dengda (zhudengda@mail.iggcas.ac.cn)
 * @date   2024-07-24
 * 
 * 
 */


#include "common/attenuation.h"
#include "common/const.h"



MYCOMPLEX attenuation_law(MYREAL Qinv, MYCOMPLEX omega){
    return RONE + Qinv/PI * CLOG(omega/PI2) + RHALF*Qinv*I;
    // return RONE;
}