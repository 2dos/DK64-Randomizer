#include "../include/common.h"

int* drawImageWithFilter(int* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int red, int green, int blue, int opacity) {
	dl = initDisplayList(dl);
	*(unsigned int*)(dl++) = 0xE200001C;
	*(unsigned int*)(dl++) = 0x00504240;
	gDPSetPrimColor(dl, 0, 0, red, green, blue, opacity);
	dl += 2;
	*(unsigned int*)(dl++) = 0xFCFF97FF;
	*(unsigned int*)(dl++) = 0xFF2CFE7F;
	*(unsigned int*)(dl++) = 0xE3001201;
	*(unsigned int*)(dl++) = 0x00000000;
	dl = displayImage(dl++, text_index, 0, codec_index, img_width, img_height, x, y, xScale, yScale, 0, 0.0f);
	return dl;
}

int* drawImage(int* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int opacity) {
	return drawImageWithFilter(dl, text_index, codec_index, img_width, img_height, x, y, xScale, yScale, 0xFF, 0xFF, 0xFF, opacity);
}

int* drawTri(int* dl, short x1, short y1, short x2, short y2, short x3, short y3, int red, int green, int blue, int alpha) {
	dl = initDisplayList(dl);
	// Set Combine
	*(unsigned int*)(dl++) = 0xFC7EA004;
	*(unsigned int*)(dl++) = 0x100C00F4;
	// Mtx
	*(unsigned int*)(dl++) = 0xDA380003;
	*(unsigned int*)(dl++) = 0x02000180;
	*(unsigned int*)(dl++) = 0xDA380007;
	*(unsigned int*)(dl++) = 0x02000080;
	// Vertex 0
	*(unsigned int*)(dl++) = 0x02180000;
	*(unsigned int*)(dl++) = (x1 << 16) | y1;
	*(unsigned int*)(dl++) = 0x02100000;
	*(unsigned int*)(dl++) = 0xFFFFFFFF;
	// Vertex 1
	*(unsigned int*)(dl++) = 0x02180002;
	*(unsigned int*)(dl++) = (x2 << 16) | y2;
	*(unsigned int*)(dl++) = 0x02100002;
	*(unsigned int*)(dl++) = 0xFFFFFFFF;
	// Vertex 2
	*(unsigned int*)(dl++) = 0x02180004;
	*(unsigned int*)(dl++) = (x3 << 16) | y3;
	*(unsigned int*)(dl++) = 0x02100004;
	*(unsigned int*)(dl++) = 0xFFFFFFFF;
	gDPSetPrimColor(dl, 0, 0, red, green, blue, alpha);
	dl += 2;
	// Draw Tri
	*(unsigned int*)(dl++) = 0x05000204;
	*(unsigned int*)(dl++) = 0x00000000;
	return dl;
}

int* drawPixelText(int* dl, int x, int y, char* str, int red, int green, int blue, int alpha) {
	*(unsigned int*)(dl++) = 0xE7000000;
    *(unsigned int*)(dl++) = 0x00000000;
    *(unsigned int*)(dl++) = 0xE3000A01;
    *(unsigned int*)(dl++) = 0x00000000;
    *(unsigned int*)(dl++) = 0xD9000000;
    *(unsigned int*)(dl++) = 0x00000000;
    *(unsigned int*)(dl++) = 0xD9FFFFFF;
    *(unsigned int*)(dl++) = 0x00200004;
    gDPSetPrimColor(dl, 0, 0, red, green, blue, alpha);
    dl += 2;
    *(unsigned int*)(dl++) = 0xFC119623;
    *(unsigned int*)(dl++) = 0xFF2FFFFF;
    *(unsigned int*)(dl++) = 0xE200001C;
    *(unsigned int*)(dl++) = 0x00504240;
    dl = textDraw(dl,2,x,y,str);
	return dl;
}

int* drawPixelTextContainer(int* dl, int x, int y, char* str, int red, int green, int blue, int alpha, int offset) {
	if (offset) {
		dl = drawPixelText(dl,x-offset,y+offset,str,0,0,0,alpha);
	}
	dl = drawPixelText(dl,x,y,str,red,green,blue,alpha);
	return dl;
}

int* displayCenteredText(int* dl, int y, char* str, int offset) {
	int center_x = 160;
	if (Rando.true_widescreen) {
		center_x = SCREEN_WD << 1;
	}
	int length = cstring_strlen(str);
	return drawPixelTextContainer(dl, center_x - (length << 2), y, str, 0xFF, 0xFF, 0xFF, 0xFF, offset);
}

int* drawScreenRect(int* dl, int x1, int y1, int x2, int y2, int red, int green, int blue, int alpha) {
	*(unsigned int*)(dl++) = 0xE7000000;
	*(unsigned int*)(dl++) = 0x00000000;
	*(unsigned int*)(dl++) = 0xE3000A01;
	*(unsigned int*)(dl++) = 0x00300000;
	*(unsigned int*)(dl++) = 0xE200001C;
	*(unsigned int*)(dl++) = 0x00000000;
	*(unsigned int*)(dl++) = 0xD9FFFFFE;
	*(unsigned int*)(dl++) = 0x00000000;
	*(unsigned int*)(dl++) = 0xF7000000;
	*(unsigned int*)(dl++) = ((red & 0x1F) << 11) | ((green & 0x1F) << 6) | ((blue & 0x1F) << 1) | (alpha & 0x1);
	*(unsigned int*)(dl++) = 0xED000000 | (((0xA * 4) & 0xFFF) << 12) | ((4 * 0xA) & 0xFFF);
	if (Rando.true_widescreen) {
		*(unsigned int*)(dl++) = (((4 * (SCREEN_WD - 11)) & 0xFFF) << 12) | ((4 * (SCREEN_HD - 11)) & 0xFFF);
	} else {
		*(unsigned int*)(dl++) = (((4 * 0x135) & 0xFFF) << 12) | ((4 * 0xE5) & 0xFFF);
	}
	*(unsigned int*)(dl++) = 0xF6000000 | ((x2 & 0x3FF) << 12) | (y2 & 0x3FF);
	*(unsigned int*)(dl++) = ((x1 & 0x3FF) << 12) | (y1 & 0x3FF);
	return dl;
}

int* drawString(int* dl, int style, float x, float y, char* str) {
	float height = (float)getTextStyleHeight(style);
	float text_y = y - (height * 0x5);
	int centered = 0;
	if (style & 0x80) {
		centered = 0x80;
	}
	int* dl_copy = displayText(dl, style & 0x7F, 4 * x, 4 * text_y, str, centered);
	return dl_copy;
}

int* drawText(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity) {
	dl = initDisplayList(dl);
	int short_style = style & 0x7F;
	if (short_style == 1) {
		*(unsigned int*)(dl++) = 0xFC119623; // G_SETCOMBINE
		*(unsigned int*)(dl++) = 0xFF2FFFFF; // G_SETCIMG format: 1, 1, -1
		*(unsigned int*)(dl++) = 0xDA380003;
		*(unsigned int*)(dl++) = (int)&style128Mtx[0];
	} else {
		*(unsigned int*)(dl++) = 0xDE000000; // G_DL 0
		*(unsigned int*)(dl++) = 0x01000118; // G_VTX 0 11
		*(unsigned int*)(dl++) = 0xFC119623; // G_SETCOMBINE
		*(unsigned int*)(dl++) = 0xFF2FFFFF; // G_SETCIMG format: 1, 1, -1
		if (short_style == 6) {
			*(unsigned int*)(dl++) = 0xDA380003;
			*(unsigned int*)(dl++) = (int)&style6Mtx[0];
		} else if (short_style == 2) {
			*(unsigned int*)(dl++) = 0xDA380003;
			*(unsigned int*)(dl++) = (int)&style2Mtx[0];
		}
		gDPSetPrimColor(dl, 0, 0, red, green, blue, opacity);
		dl += 2;
	}
	dl = drawString(dl,style,x,y,str);
	return dl;
}

int* drawTextContainer(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity, int background) {
	if (background) {
		dl = drawText(dl,style,x-background,y+background,str,0,0,0,opacity);
	}
	dl = drawText(dl,style,x,y,str,red,green,blue,opacity);
	return dl;
}

static char* character_recoloring_str = 0;
static char use_character_recoloring = 0;
static char char_color_data[0x40];
static unsigned char char_opacity_data[0x40];

void setCharacterRecoloring(int output, char* stored_str) {
	use_character_recoloring = output;
	character_recoloring_str = stored_str;
	
	TestVariable = (int)&char_color_data[0];
}

void wipeTextColorData(void) {
	for (int i = 0; i < 0x40; i++) {
		char_color_data[i] = 0;
		char_opacity_data[i] = 0xFF;
	}
}

void setCharacterColor(int index, int value, int opacity) {
	char_color_data[index] = value;
	char_opacity_data[index] = opacity;
}

void applyHintRecoloring(letter_data* data, int index, int bitfield, char* char_address) {
	if ((!use_character_recoloring) || (!character_recoloring_str)) {
		recolorVertBlockText(data, index, bitfield);
		return;
	}
	int offset = char_address - character_recoloring_str;
	int color_value = base_text_color;
	int color_index = char_color_data[offset];
	int opacity = char_opacity_data[offset];
	if (color_index != 0) {
		color_value = emph_text_colors[color_index - 1];
	}
	for (int i = 0; i < 4; i++) {
		data->vtx_info[i].color = color_value | opacity;
	}
}