/*
	This file is automatically written to by build_dynamic_bitfields.py
	Don't directly modify this file, instead modify the script
	Otherwise your changes will be overwritten on next build

	Thanks,
		Ballaam
*/


typedef struct RemovedBarriers {
	unsigned char five_dt_switches : 1; // 0x80 (OFFSET 0)
	unsigned char production_room_on : 1; // 0x40 
	unsigned char seasick_ship_spawned : 1; // 0x20 
	unsigned char igloo_pads_spawned : 1; // 0x10 
	unsigned char unused_4 : 1; // 0x8 
	unsigned char japes_coconut_gates : 1; // 0x4 
	unsigned char shellhive_gate : 1; // 0x2 
	unsigned char aztec_tunnel_door : 1; // 0x1 
	unsigned char factory_testing_gate : 1; // 0x80 (OFFSET 1)
	unsigned char lighthouse_gate : 1; // 0x40 
	unsigned char fungi_green_tunnel : 1; // 0x20 
	unsigned char fungi_yellow_tunnel : 1; // 0x10 
	unsigned char shipwreck_gate : 1; // 0x8 
	unsigned char llama_switches : 1; // 0x4 
} RemovedBarriers;

typedef enum ENUM_RemovedBarriers {
	/* 0 */ REMOVEDBARRIERS_ENUM_FIVEDTSWITCHES,
	/* 1 */ REMOVEDBARRIERS_ENUM_PRODUCTIONROOMON,
	/* 2 */ REMOVEDBARRIERS_ENUM_SEASICKSHIPSPAWNED,
	/* 3 */ REMOVEDBARRIERS_ENUM_IGLOOPADSSPAWNED,
	/* 4 */ REMOVEDBARRIERS_ENUM_UNUSED4,
	/* 5 */ REMOVEDBARRIERS_ENUM_JAPESCOCONUTGATES,
	/* 6 */ REMOVEDBARRIERS_ENUM_SHELLHIVEGATE,
	/* 7 */ REMOVEDBARRIERS_ENUM_AZTECTUNNELDOOR,
	/* 8 */ REMOVEDBARRIERS_ENUM_FACTORYTESTINGGATE,
	/* 9 */ REMOVEDBARRIERS_ENUM_LIGHTHOUSEGATE,
	/* 10 */ REMOVEDBARRIERS_ENUM_FUNGIGREENTUNNEL,
	/* 11 */ REMOVEDBARRIERS_ENUM_FUNGIYELLOWTUNNEL,
	/* 12 */ REMOVEDBARRIERS_ENUM_SHIPWRECKGATE,
	/* 13 */ REMOVEDBARRIERS_ENUM_LLAMASWITCHES,
} ENUM_RemovedBarriers;

typedef struct FasterChecks {
	unsigned char piano : 1; // 0x80 (OFFSET 0)
	unsigned char diddy_rnd : 1; // 0x40 
	unsigned char mech_fish : 1; // 0x20 
	unsigned char arcade_first_round : 1; // 0x10 
	unsigned char rabbit_race : 1; // 0x8 
	unsigned char castle_cart : 1; // 0x4 
	unsigned char arcade_second_round : 1; // 0x2 
} FasterChecks;

typedef enum ENUM_FasterChecks {
	/* 0 */ FASTERCHECKS_ENUM_PIANO,
	/* 1 */ FASTERCHECKS_ENUM_DIDDYRND,
	/* 2 */ FASTERCHECKS_ENUM_MECHFISH,
	/* 3 */ FASTERCHECKS_ENUM_ARCADEFIRSTROUND,
	/* 4 */ FASTERCHECKS_ENUM_RABBITRACE,
	/* 5 */ FASTERCHECKS_ENUM_CASTLECART,
	/* 6 */ FASTERCHECKS_ENUM_ARCADESECONDROUND,
} ENUM_FasterChecks;
