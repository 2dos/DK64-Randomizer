#define writeFunction(a,b) *(int*)(a) = 0x0C000000 | ((((int)(b)) & 0xFFFFFF) >> 2);
#define loadSingularHook(a,b) *(int*)(a) = 0x08000000 | ((((int)(b)) & 0xFFFFFF) >> 2); *(int*)(a+4)=0;