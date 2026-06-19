/**
 * @file everdrive.c
 * @brief USB flashcart bridge for Archipelago on real N64 hardware.
 */

#include "../../include/common.h"

#ifndef ALIGN2
#define ALIGN2(v) (((v) + 1) & ~1u)
#endif
#define ED_CART_NONE 0
#define ED_CART_EVERDRIVE 2
#define ED_CART_SC64 3
#define ED_RDRAM_SIZE 0x800000
#define ED_MAX_XFER 0x200
#define ED_BUF_SIZE 0x400
#define ED_MAX_CMDS_PER_FRAME 8
#define ED_TIMEOUT_MS 100

typedef struct PI_regs_s {
    volatile void *ram_address;
    u32 pi_address;
    u32 read_length;
    u32 write_length;
    u32 status;
} PI_regs_t;
#define PI_regs ((volatile PI_regs_t *)0xA4600000)

#define PI_STATUS_DMA_BUSY (1 << 0)
#define PI_STATUS_IO_BUSY (1 << 1)
#define PI_STATUS_CLR_INTR (1 << 1)

#define C0_STATUS_IE 0x00000001u

// ROM_DATA forces these into .data
ROM_DATA static u32 ed_int_sr = 0;
ROM_DATA static u32 ed_int_depth = 0;

static void ed_disable_interrupts(void) {
    if (!ed_int_depth) {
        u32 sr;
        __asm__ volatile("mfc0 %0,$12" : "=r"(sr));
        ed_int_sr = sr;
        __asm__ volatile("mtc0 %0,$12" ::"r"(sr & ~C0_STATUS_IE));
    }
    ed_int_depth++;
}

static void ed_enable_interrupts(void) {
    if (ed_int_depth == 0) {
        return;
    }
    ed_int_depth--;
    if (!ed_int_depth) {
        __asm__ volatile("mtc0 %0,$12" ::"r"(ed_int_sr));
    }
}

static int ed_dma_busy(void) {
    return PI_regs->status & (PI_STATUS_DMA_BUSY | PI_STATUS_IO_BUSY);
}

static void ed_dma_wait(void) {
    while (ed_dma_busy()) {
    }
}

// VR4300 dcache line is 16 bytes; ops 0x15 = hit writeback invalidate, 0x19 = hit writeback.
#define ed_cache_op(op, linesize)                                              \
    ({                                                                         \
        if (length) {                                                          \
            void *cur = (void *)((unsigned long)addr & ~(linesize - 1));       \
            int count = (int)length + (addr - cur);                            \
            for (int i = 0; i < count; i += linesize)                          \
                __asm__("\tcache %0,(%1)\n" ::"i"(op), "r"(cur + i));          \
        }                                                                      \
    })

static void ed_dcache_wb_inval(volatile void *addr, unsigned long length) {
    ed_cache_op(0x15, 16);
}

static void ed_dcache_wb(volatile void *addr, unsigned long length) {
    ed_cache_op(0x19, 16);
}

static u32 ed_io_read(u32 pi_address) {
    u32 value;
    ed_disable_interrupts();
    ed_dma_wait();
    value = *(volatile u32 *)(pi_address | 0xA0000000);
    ed_enable_interrupts();
    return value;
}

static void ed_io_write(u32 pi_address, u32 data) {
    ed_disable_interrupts();
    ed_dma_wait();
    *(volatile u32 *)(pi_address | 0xA0000000) = data;
    ed_enable_interrupts();
}

// DMA from the cartridge (PI bus) into RDRAM.
static void ed_dma_read(void *ram_address, u32 pi_address, u32 len) {
    ed_dcache_wb_inval(ram_address, len);
    ram_address = (void *)((u32)ram_address & 0x1FFFFFFF);
    ed_disable_interrupts();
    ed_dma_wait();
    PI_regs->ram_address = ram_address;
    PI_regs->pi_address = pi_address;
    PI_regs->write_length = len - 1;
    ed_dma_wait();
    PI_regs->status = PI_STATUS_CLR_INTR;
    ed_enable_interrupts();
}

// DMA from RDRAM out to the cartridge (PI bus).
static void ed_dma_write(void *ram_address, u32 pi_address, u32 len) {
    ed_dcache_wb(ram_address, len);
    ram_address = (void *)((u32)ram_address & 0x1FFFFFFF);
    ed_disable_interrupts();
    ed_dma_wait();
    PI_regs->ram_address = ram_address;
    PI_regs->pi_address = pi_address;
    PI_regs->read_length = len - 1;
    ed_dma_wait();
    PI_regs->status = PI_STATUS_CLR_INTR;
    ed_enable_interrupts();
}

// C0_COUNT increments every other CPU cycle (~46.875 MHz on a 93.75 MHz VR4300).
#define ED_COUNT_PER_MS 46875u

static u32 ed_c0_count(void) {
    u32 x;
    __asm__ volatile("mfc0 %0,$9\n\tnop" : "=r"(x));
    return x;
}

static u8 ed_count_elapsed(u32 start, u32 ms) {
    return (ed_c0_count() - start) >= (ms * ED_COUNT_PER_MS);
}

/*********************************
        Shared bridge state
*********************************/

ROM_DATA static s8 ed_cart = ED_CART_NONE;
ROM_DATA static u8 ed_buffer_raw[ED_BUF_SIZE + 16];
ROM_DATA static u8 *ed_buffer = 0;

static u32 ed_be32(const u8 *p) {
    return ((u32)p[0] << 24) | ((u32)p[1] << 16) | ((u32)p[2] << 8) | (u32)p[3];
}

/*********************************
        EverDrive transport
*********************************/

#define ED_REG_USBCFG 0x1F800004
#define ED_REG_VERSION 0x1F800014
#define ED_REG_USBDAT 0x1F800400
#define ED_REG_SYSCFG 0x1F808000
#define ED_REG_KEY 0x1F808004

#define ED_USBMODE_RDNOP 0xC400
#define ED_USBMODE_RD 0xC600
#define ED_USBMODE_WRNOP 0xC000
#define ED_USBMODE_WR 0xC200

#define ED_USBSTAT_ACT 0x0200
#define ED_USBSTAT_RXF 0x0400
#define ED_USBSTAT_TXE 0x0800
#define ED_USBSTAT_POWER 0x1000

#define ED_REGKEY 0xAA55
#define ED25_VERSION 0xED640007 // V2.5 (no USB support)
#define ED3_VERSION 0xED640008  // V3
#define EDX_VERSION 0xED640013  // X7 / X5

#define ED_FIFO_SIZE 512

// Spin until the USB unit finishes the current transfer, or bail on timeout.
static u8 ed_usbbusy(void) {
    u32 start = ed_c0_count();
    while (ed_io_read(ED_REG_USBCFG) & ED_USBSTAT_ACT) {
        if (ed_count_elapsed(start, ED_TIMEOUT_MS)) {
            ed_io_write(ED_REG_USBCFG, ED_USBMODE_RDNOP);
            return 1;
        }
    }
    return 0;
}

// True when there is data to read (USB powered and the RX FIFO has bytes).
static u8 ed_can_read(void) {
    return (ed_io_read(ED_REG_USBCFG) & (ED_USBSTAT_POWER | ED_USBSTAT_RXF)) == ED_USBSTAT_POWER;
}

// Read exactly len bytes from the USB FIFO into ram. Returns 1 on timeout.
static u8 ed_fifo_read(void *ram, u32 len) {
    ed_io_write(ED_REG_USBCFG, ED_USBMODE_RDNOP);
    while (len) {
        u32 block = (len > ED_FIFO_SIZE) ? ED_FIFO_SIZE : len;
        u32 addr = ED_FIFO_SIZE - block;
        ed_io_write(ED_REG_USBCFG, ED_USBMODE_RD | addr);
        if (ed_usbbusy()) {
            return 1;
        }
        ed_dma_read(ram, ED_REG_USBDAT + addr, block);
        ram = (u8 *)ram + block;
        len -= block;
    }
    return 0;
}

// Write exactly len bytes from ram to the USB FIFO. Returns 1 on timeout.
static u8 ed_fifo_write(void *ram, u32 len) {
    ed_io_write(ED_REG_USBCFG, ED_USBMODE_WRNOP);
    while (len) {
        u32 block = (len > ED_FIFO_SIZE) ? ED_FIFO_SIZE : len;
        u32 addr = ED_FIFO_SIZE - block;
        ed_dma_write(ram, ED_REG_USBDAT + addr, block);
        ed_io_write(ED_REG_USBCFG, ED_USBMODE_WR | addr);
        if (ed_usbbusy()) {
            return 1;
        }
        ram = (u8 *)ram + block;
        len -= block;
    }
    return 0;
}

// Build and send one UNFLoader frame: DMA@ + datatype + size + payload + CMPH,
// padded to an even length (matching everdrive_loader.py's _recv).
static void ed_everdrive_send(u8 datatype, const void *src, u32 size) {
    u32 total;
    ed_buffer[0] = 'D';
    ed_buffer[1] = 'M';
    ed_buffer[2] = 'A';
    ed_buffer[3] = '@';
    ed_buffer[4] = datatype;
    ed_buffer[5] = (size >> 16) & 0xFF;
    ed_buffer[6] = (size >> 8) & 0xFF;
    ed_buffer[7] = size & 0xFF;
    if (size) {
        dk_memcpy(ed_buffer + 8, (void *)src, size);
    }
    total = 8 + size;
    ed_buffer[total + 0] = 'C';
    ed_buffer[total + 1] = 'M';
    ed_buffer[total + 2] = 'P';
    ed_buffer[total + 3] = 'H';
    total += 4;
    if (total & 1) {
        ed_buffer[total] = 0;
        total++;
    }
    ed_fifo_write(ed_buffer, total);
}

// Read one command frame. Returns 1 and fills datatype/size (payload in ed_buffer)
// if a valid command is pending, else 0.
static u8 ed_everdrive_recv(u8 *datatype, u32 *size) {
    u32 sz, bodylen;
    const u8 *cmp;

    if (!ed_can_read()) {
        return 0; // nothing pending
    }
    if (ed_fifo_read(ed_buffer, 8)) {
        return 0; // timed out reading the header
    }
    if (ed_buffer[0] != 'D' || ed_buffer[1] != 'M' || ed_buffer[2] != 'A' || ed_buffer[3] != '@') {
        return 0; // desynced; PC will purge and retry
    }
    *datatype = ed_buffer[4];
    sz = ((u32)ed_buffer[5] << 16) | ((u32)ed_buffer[6] << 8) | (u32)ed_buffer[7];
    bodylen = ALIGN2(sz) + 4; // PC -> N64: payload padded to even, then CMPH
    if (bodylen > ED_BUF_SIZE) {
        return 0; // oversized; drop
    }
    if (ed_fifo_read(ed_buffer, bodylen)) {
        return 0;
    }
    cmp = ed_buffer + ALIGN2(sz);
    if (cmp[0] != 'C' || cmp[1] != 'M' || cmp[2] != 'P' || cmp[3] != 'H') {
        return 0; // bad trailer
    }
    *size = sz;
    return 1;
}

static u8 ed_everdrive_detect(void) {
    u32 version;
    ed_io_write(ED_REG_KEY, ED_REGKEY);
    version = ed_io_read(ED_REG_VERSION);
    if (version != ED3_VERSION && version != EDX_VERSION) {
        return 0; // V2.5, an emulator's open-bus, or a non-EverDrive cart
    }
    ed_io_write(ED_REG_SYSCFG, 0);
    ed_io_write(ED_REG_USBCFG, ED_USBMODE_RDNOP);
    if ((ed_io_read(ED_REG_USBCFG) & ED_USBSTAT_POWER) == 0) {
        return 0; // USB unit unpowered (X5 variant)
    }
    return 1;
}

/*********************************
          SC64 transport
*********************************/

#define SC64_REG_SR_CMD 0x1FFF0000
#define SC64_REG_DATA_0 0x1FFF0004
#define SC64_REG_DATA_1 0x1FFF0008
#define SC64_REG_IDENTIFIER 0x1FFF000C
#define SC64_REG_KEY 0x1FFF0010

#define SC64_SR_CMD_ERROR (1u << 30)
#define SC64_SR_CMD_BUSY (1u << 31)

#define SC64_V2_IDENTIFIER 0x53437632
#define SC64_KEY_RESET 0x00000000
#define SC64_KEY_UNLOCK_1 0x5F554E4C
#define SC64_KEY_UNLOCK_2 0x4F434B5F

#define SC64_CMD_CONFIG_SET 'C'
#define SC64_CMD_USB_WRITE_STATUS 'U'
#define SC64_CMD_USB_WRITE 'M'
#define SC64_CMD_USB_READ_STATUS 'u'
#define SC64_CMD_USB_READ 'm'

#define SC64_CFG_ROM_WRITE_ENABLE 1
#define SC64_USB_WRITE_STATUS_BUSY (1u << 31)
#define SC64_USB_READ_STATUS_BUSY (1u << 31)

// Scratch region in cart SDRAM used to stage USB data, reserving the top 8 MB
// (libdragon's DEBUG_ADDRESS_SIZE) of the 64 MB cart space: 0x10000000 +
// (0x04000000 - 0x800000). Safe as long as the DK64 ROM image is < 56 MB.
#define SC64_STAGING 0x13800000

// Execute one SC64 controller command. Returns 1 on error/timeout, 0 on success.
static u8 sc64_exec(u8 cmd, const u32 *args, u32 *result) {
    u32 sr;
    u32 start;
    if (args) {
        ed_io_write(SC64_REG_DATA_0, args[0]);
        ed_io_write(SC64_REG_DATA_1, args[1]);
    }
    ed_io_write(SC64_REG_SR_CMD, cmd);
    start = ed_c0_count();
    do {
        sr = ed_io_read(SC64_REG_SR_CMD);
        if (ed_count_elapsed(start, ED_TIMEOUT_MS)) {
            return 1;
        }
    } while (sr & SC64_SR_CMD_BUSY);
    if (result) {
        result[0] = ed_io_read(SC64_REG_DATA_0);
        result[1] = ed_io_read(SC64_REG_DATA_1);
    }
    return (sr & SC64_SR_CMD_ERROR) ? 1 : 0;
}

static void sc64_send(u8 datatype, const void *src, u32 size) {
    u32 args[2];
    u32 result[2];
    u32 start;
    u32 prev_writable;

    // Wait until any previous USB write has finished.
    start = ed_c0_count();
    do {
        if (sc64_exec(SC64_CMD_USB_WRITE_STATUS, 0, result)) {
            return;
        }
        if (ed_count_elapsed(start, ED_TIMEOUT_MS)) {
            return;
        }
    } while (result[0] & SC64_USB_WRITE_STATUS_BUSY);

    if (size) {
        dk_memcpy(ed_buffer, (void *)src, size);
    }

    // Enable SDRAM writes, stage the data, restore the previous setting.
    args[0] = SC64_CFG_ROM_WRITE_ENABLE;
    args[1] = 1;
    sc64_exec(SC64_CMD_CONFIG_SET, args, result);
    prev_writable = result[1];
    ed_dma_write(ed_buffer, SC64_STAGING, ALIGN2(size));
    args[0] = SC64_CFG_ROM_WRITE_ENABLE;
    args[1] = prev_writable;
    sc64_exec(SC64_CMD_CONFIG_SET, args, result);

    // Trigger the USB send: arg0 = staging address, arg1 = (datatype<<24)|size.
    args[0] = SC64_STAGING;
    args[1] = ((u32)datatype << 24) | (size & 0xFFFFFF);
    if (sc64_exec(SC64_CMD_USB_WRITE, args, 0)) {
        return;
    }

    start = ed_c0_count();
    do {
        if (sc64_exec(SC64_CMD_USB_WRITE_STATUS, 0, result)) {
            return;
        }
        if (ed_count_elapsed(start, ED_TIMEOUT_MS)) {
            return;
        }
    } while (result[0] & SC64_USB_WRITE_STATUS_BUSY);
}

// Returns 1 and fills datatype/size (payload in ed_buffer) if a command is
// pending, else 0.
static u8 sc64_recv(u8 *datatype, u32 *size) {
    u32 args[2];
    u32 result[2];
    u32 sz;
    u32 start;

    if (sc64_exec(SC64_CMD_USB_READ_STATUS, 0, result)) {
        return 0;
    }
    sz = result[1] & 0xFFFFFF;
    if (sz == 0) {
        return 0; // nothing pending
    }
    if (sz > ED_BUF_SIZE) {
        sz = ED_BUF_SIZE;
    }

    // Ask the SC64 to receive the pending data into the staging region.
    args[0] = SC64_STAGING;
    args[1] = sz;
    if (sc64_exec(SC64_CMD_USB_READ, args, 0)) {
        return 0;
    }
    start = ed_c0_count();
    do {
        if (sc64_exec(SC64_CMD_USB_READ_STATUS, 0, result)) {
            return 0;
        }
        if (ed_count_elapsed(start, ED_TIMEOUT_MS)) {
            return 0;
        }
    } while (result[0] & SC64_USB_READ_STATUS_BUSY);

    ed_dma_read(ed_buffer, SC64_STAGING, ALIGN2(sz));
    *datatype = result[0] & 0xFF;
    *size = sz;
    return 1;
}

static u8 sc64_detect(void) {
    ed_io_write(SC64_REG_KEY, SC64_KEY_RESET);
    ed_io_write(SC64_REG_KEY, SC64_KEY_UNLOCK_1);
    ed_io_write(SC64_REG_KEY, SC64_KEY_UNLOCK_2);
    return ed_io_read(SC64_REG_IDENTIFIER) == SC64_V2_IDENTIFIER;
}

/*********************************
          Command handler
*********************************/

static void cart_send(u8 datatype, const void *src, u32 size) {
    if (ed_cart == ED_CART_EVERDRIVE) {
        ed_everdrive_send(datatype, src, size);
    } else if (ed_cart == ED_CART_SC64) {
        sc64_send(datatype, src, size);
    }
}

static u8 cart_recv(u8 *datatype, u32 *size) {
    if (ed_cart == ED_CART_EVERDRIVE) {
        return ed_everdrive_recv(datatype, size);
    } else if (ed_cart == ED_CART_SC64) {
        return sc64_recv(datatype, size);
    }
    return 0;
}

// payload/size are the validated command body; payload lives in ed_buffer.
static void ed_handle_command(u8 datatype, const u8 *payload, u32 size) {
    if (datatype == ED_DATATYPE_RDRAM_READ && size >= 8) {
        u32 addr = ed_be32(payload) & 0x7FFFFFFF;
        u32 len = ed_be32(payload + 4);
        if (len > ED_MAX_XFER) {
            len = ED_MAX_XFER;
        }
        if (addr >= ED_RDRAM_SIZE) {
            len = 0;
        } else if (addr + len > ED_RDRAM_SIZE) {
            len = ED_RDRAM_SIZE - addr;
        }
        cart_send(ED_DATATYPE_RDRAM_DATA, (void *)(addr | 0x80000000), len);
    } else if (datatype == ED_DATATYPE_RDRAM_WRITE && size >= 8) {
        u32 addr = ed_be32(payload) & 0x7FFFFFFF;
        u32 len = ed_be32(payload + 4);
        u8 ack = 1;
        if (len > ED_MAX_XFER || (8 + len) > size) {
            ack = 0;
        } else if (addr + len > ED_RDRAM_SIZE) {
            ack = 0;
        } else if (len) {
            dk_memcpy((void *)(addr | 0x80000000), (void *)(payload + 8), len);
        }
        cart_send(ED_DATATYPE_RDRAM_ACK, &ack, 1);
    }
}

/*********************************
            Entry points
*********************************/

void everdrive_init(void) {
    ed_cart = ED_CART_NONE;

    // The RDP clock register reads 0 on emulators; bail so this stays a no-op
    // and the emulator memory-attach path is completely unaffected.
    if (*(volatile u32 *)0xA4100010 == 0) {
        return;
    }

    if (ed_everdrive_detect()) {
        ed_cart = ED_CART_EVERDRIVE;
    } else if (sc64_detect()) {
        ed_cart = ED_CART_SC64;
    } else {
        return; // unsupported cart / emulator open-bus
    }

    ed_buffer = (u8 *)(((u32)ed_buffer_raw + 0xF) & ~0xF);
}

void everdrive_service(void) {
    if (ed_cart == ED_CART_NONE) {
        return;
    }
    for (int i = 0; i < ED_MAX_CMDS_PER_FRAME; i++) {
        u8 datatype;
        u32 size;
        if (!cart_recv(&datatype, &size)) {
            return;
        }
        ed_handle_command(datatype, ed_buffer, size);
    }
}
