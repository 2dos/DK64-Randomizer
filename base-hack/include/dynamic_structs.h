/*
	This file is automatically written to by build_dynamic_bitfields.py
	Don't directly modify this file, instead modify the script
	Otherwise your changes will be overwritten on next build

	Thanks,
		Ballaam
*/


typedef struct RemovedBarriers {
	unsigned char five_dt_switches : 1; // 128 (OFFSET 0)
	unsigned char production_room_on : 1; // 64 
	unsigned char seasick_ship_spawned : 1; // 32 
	unsigned char igloo_pads_spawned : 1; // 16 
	unsigned char shipwreck_permanent : 1; // 8 
	unsigned char japes_coconut_gates : 1; // 4 
	unsigned char shellhive_gate : 1; // 2 
	unsigned char aztec_tunnel_door : 1; // 1 
	unsigned char factory_testing_gate : 1; // 128 (OFFSET 1)
	unsigned char lighthouse_gate : 1; // 64 
	unsigned char fungi_green_tunnel : 1; // 32 
	unsigned char fungi_yellow_tunnel : 1; // 16 
} RemovedBarriers;

typedef enum ENUM_RemovedBarriers {
	/* 0 */ REMOVEDBARRIERS_ENUM_FIVEDTSWITCHES,
	/* 1 */ REMOVEDBARRIERS_ENUM_PRODUCTIONROOMON,
	/* 2 */ REMOVEDBARRIERS_ENUM_SEASICKSHIPSPAWNED,
	/* 3 */ REMOVEDBARRIERS_ENUM_IGLOOPADSSPAWNED,
	/* 4 */ REMOVEDBARRIERS_ENUM_SHIPWRECKPERMANENT,
	/* 5 */ REMOVEDBARRIERS_ENUM_JAPESCOCONUTGATES,
	/* 6 */ REMOVEDBARRIERS_ENUM_SHELLHIVEGATE,
	/* 7 */ REMOVEDBARRIERS_ENUM_AZTECTUNNELDOOR,
	/* 8 */ REMOVEDBARRIERS_ENUM_FACTORYTESTINGGATE,
	/* 9 */ REMOVEDBARRIERS_ENUM_LIGHTHOUSEGATE,
	/* 10 */ REMOVEDBARRIERS_ENUM_FUNGIGREENTUNNEL,
	/* 11 */ REMOVEDBARRIERS_ENUM_FUNGIYELLOWTUNNEL,
} ENUM_RemovedBarriers;

typedef struct FasterChecks {
	unsigned char toy_monster : 1; // 128 (OFFSET 0)
	unsigned char piano : 1; // 64 
	unsigned char diddy_rnd : 1; // 32 
	unsigned char mech_fish : 1; // 16 
	unsigned char arcade_first_round : 1; // 8 
	unsigned char mermaid : 1; // 4 
	unsigned char owl_race : 1; // 2 
	unsigned char rabbit_race : 1; // 1 
	unsigned char ice_tomato : 1; // 128 (OFFSET 1)
	unsigned char castle_cart : 1; // 64 
	unsigned char jetpac : 1; // 32 
	unsigned char factory_car : 1; // 16 
	unsigned char castle_car : 1; // 8 
	unsigned char seal_race : 1; // 4 
} FasterChecks;

typedef enum ENUM_FasterChecks {
	/* 0 */ FASTERCHECKS_ENUM_TOYMONSTER,
	/* 1 */ FASTERCHECKS_ENUM_PIANO,
	/* 2 */ FASTERCHECKS_ENUM_DIDDYRND,
	/* 3 */ FASTERCHECKS_ENUM_MECHFISH,
	/* 4 */ FASTERCHECKS_ENUM_ARCADEFIRSTROUND,
	/* 5 */ FASTERCHECKS_ENUM_MERMAID,
	/* 6 */ FASTERCHECKS_ENUM_OWLRACE,
	/* 7 */ FASTERCHECKS_ENUM_RABBITRACE,
	/* 8 */ FASTERCHECKS_ENUM_ICETOMATO,
	/* 9 */ FASTERCHECKS_ENUM_CASTLECART,
	/* 10 */ FASTERCHECKS_ENUM_JETPAC,
	/* 11 */ FASTERCHECKS_ENUM_FACTORYCAR,
	/* 12 */ FASTERCHECKS_ENUM_CASTLECAR,
	/* 13 */ FASTERCHECKS_ENUM_SEALRACE,
} ENUM_FasterChecks;
