/**
 * @file stack_trace.c
 * @author Ballaam
 * @brief Modifies the stack trace system to be vastly improved
 * @version 0.1
 * @date 2023-02-19
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

/*
    Register order
    v0-1
    a0-3
    t0-7
    s0-7
    t8-9
    gp, sp, s8, ra
    lo, hi
*/

static char version_string[] = "DK64R 4.0D\n";

typedef struct crash_handler_info {
    /* 0x000 */ char unk_000[0x28];
    /* 0x028 */ int general_registers[30][2];
    /* 0x118 */ char unk_118[0x11C-0x118];
    /* 0x11C */ void* pc;
    /* 0x120 */ int cause;
    /* 0x124 */ int va;
    /* 0x128 */ char unk_128[0x12C-0x128];
    /* 0x12C */ int fcsr;
    /* 0x130 */ int float_registers[32]; // float type, but will be represented as int on stack trace
} crash_handler_info;

static char* general_text[] = {
    "V0:%08X\tV1:%08X\tA0:%08X\n",
    "A1:%08X\tA2:%08X\tA3:%08X\n",
    "T0:%08X\tT1:%08X\tT2:%08X\n",
    "T3:%08X\tT4:%08X\tT5:%08X\n",
    "T6:%08X\tT7:%08X\tS0:%08X\n",
    "S1:%08X\tS2:%08X\tS3:%08X\n",
    "S4:%08X\tS5:%08X\tS6:%08X\n",
    "S7:%08X\tT8:%08X\tT9:%08X\n",
    "GP:%08X\tSP:%08X\tFP:%08X\n",
    "RA:%08X\tLO:%08X\tHI:%08X\n",
};

static char* float_text[] = {
    "F00:%08X\tF01:%08X\tF02:%08X\n",
    "F03:%08X\tF04:%08X\tF05:%08X\n",
    "F06:%08X\tF07:%08X\tF08:%08X\n",
    "F09:%08X\tF10:%08X\tF11:%08X\n",
    "F12:%08X\tF13:%08X\tF14:%08X\n",
    "F15:%08X\tF16:%08X\tF17:%08X\n",
    "F18:%08X\tF19:%08X\tF20:%08X\n",
    "F21:%08X\tF22:%08X\tF23:%08X\n",
    "F24:%08X\tF25:%08X\tF26:%08X\n",
    "F27:%08X\tF28:%08X\tF29:%08X\n",
    "F30:%08X\tF31:%08X\n",
};

static char* general_causes[] = {
    "INTERRUPT",
    "TLB MODIFICATION", 
    "TLB EXCEPTION ON LOAD", 
    "TLB EXCEPTION ON STORE", 
    "ADDRESS ERROR ON LOAD", 
    "ADDRESS ERROR ON STORE", 
    "BUS ERROR ON INST.", 
    "BUS ERROR ON DATA", 
    "SYSTEM CALL EXCEPTION", 
    "BREAKPOINT EXCEPTION", 
    "RESERVED INSTRUCTION", 
    "COPROCESSOR UNUSABLE", 
    "ARITHMETIC OVERFLOW", 
    "TRAP EXCEPTION", 
    "VIRTUAL COHERENCY ON INST.", 
    "FLOATING POINT EXCEPTION", 
    "WATCHPOINT EXCEPTION", 
    "VIRTUAL COHERENCY ON DATA"
};

static char* float_causes[] = {
    "UNIMPLEMENTED OPERATION", 
    "INVALID OPERATION", 
    "DIVISION BY ZERO", 
    "OVERFLOW", 
    "UNDERFLOW", 
    "INEXACT OPERATION"
};

void CrashHandler(crash_handler_info* info) {
    StackTraceSize = 2; // Pixel Size
    *(short*)(0x807FEF84) = -1; // Letter Color
    *(short*)(0x807FEF86) = 1; // Background Color
    int x = 0;
    int y = 0;
    StackTraceX = x;
    StackTraceY = y;
    StackTraceStartX = x;
    printDebugText("OOPS! YOUR GAME HAS CRASHED.\n", 0, 0, 0, 0);
    printDebugText("SEND A PICTURE OF THIS SCREEN TO:\n", 0, 0, 0, 0);
    printDebugText("DISCORD.DK64RANDOMIZER.COM\n", 0, 0, 0, 0);
    StackTraceSize = 1; // Pixel Size
    printDebugText("\n", 0, 0, 0, 0);
    y = StackTraceY; // Store Y for stack trace dump
    if (ReasonCode != 0) { // Reason
        printDebugText("REASON: %s\n", (int)ReasonExceptions[(int)ReasonCode], 0, 0, 0);
    } else {
        printDebugText("REASON: NONE ASCERTAINABLE\n", 0, 0, 0, 0);
    }
    // General Exception
    int cause_index = _SHIFTR(info->cause, 2, 5);
    if (cause_index == 23) { // Watch Point
        cause_index = 16;
    }
    if (cause_index == 31) { // Virtual coherency on data
        cause_index = 17;
    }
    printDebugText("GENERAL EXCEPTION: %s\n", (int)general_causes[cause_index], 0, 0, 0);
    // Float Exception
    int flag = FPCSR_CE;
    for (int i = 0; i < sizeof(float_causes)/4; i++) {
        if (info->fcsr & flag) {
            printDebugText("FLOAT EXCEPTION: %s\n", (int)float_causes[i], 0, 0, 0);
        }
        flag >>= 1;
    }
    printDebugText("PC:%08X\tFCSR:%08X\tTHREAD:%d\n", (int)info->pc, (int)info->fcsr, __osGetThreadId(info), 0);
    for (int i = 0; i < 10; i++) {
        int reg_start = 3 * i;
        int v1 = info->general_registers[reg_start][1];
        int v2 = info->general_registers[reg_start + 1][1];
        int v3 = info->general_registers[reg_start + 2][1];
        printDebugText(general_text[i], v1, v2, v3, 0);
    }
    printDebugText("\n",0,0,0,0);
    for (int i = 0; i < 11; i++) {
        int reg_start = 3 * i;
        int v1 = *(int*)&info->float_registers[reg_start];
        int v2 = *(int*)&info->float_registers[reg_start + 1];
        int v3 = 0;
        if (i < 10) {
            v3 = *(int*)&info->float_registers[reg_start + 2];
        }
        printDebugText(float_text[i], v1, v2, v3, 0);
    }
    StackTraceY = y;
    int stack_x = 210;
    StackTraceX = stack_x;
    StackTraceStartX = stack_x;
    StackTraceSize = 2; // Pixel Size
    printDebugText(version_string, 0, 0, 0, 0);
    printDebugText("STACK TRACE:\n",0,0,0,0);
    printDebugText("%X\n", (int)info->pc, 0, 0, 0);
    printDebugText("%X\n", (int)info->general_registers[27][1], 0, 0, 0);
    if (*(int*)(0x807563B8) > 3) {
        for (int i = 1; i < *(int*)(0x807FF018); i++) { // Stack Depth
            printDebugText("%X\n", (int)StackTraceAddresses[i].address, 0, 0, 0);
        }
    }
    
    if (*(int*)(0x807563B8) < 4) {
        *(int*)(0x807563B8) += 1;
    }
    if (*(int*)(0x807563B8) == 4) {
        dumpReturns(info);
    }
}

OSThread* getFaultedThread(void) {
    OSThread* thread = __osActiveQueue;
    
    while (thread->priority != -1) {
        if (thread->priority > 0 && thread->priority < 0x7F && (thread->flags & 3)) {
            return thread;
        }
        thread = thread->tlnext;
    }
    return 0;
}