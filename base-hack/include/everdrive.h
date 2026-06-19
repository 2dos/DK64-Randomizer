#ifndef _EVERDRIVE_H_
#define _EVERDRIVE_H_

/**
 * @file everdrive.h
 * @brief Real-hardware Archipelago bridge for the EverDrive 64.
 */

#define ED_DATATYPE_RDRAM_READ 0x30  // PC -> N64: addr(4 BE) + len(4 BE)
#define ED_DATATYPE_RDRAM_WRITE 0x31 // PC -> N64: addr(4 BE) + len(4 BE) + bytes
#define ED_DATATYPE_RDRAM_DATA 0x32  // N64 -> PC: the requested bytes
#define ED_DATATYPE_RDRAM_ACK 0x33   // N64 -> PC: 1 status byte

// Called once when an AP seed initializes
extern void everdrive_init(void);
extern void everdrive_service(void);

#endif // _EVERDRIVE_H_
