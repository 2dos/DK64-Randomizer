#include "../include/common.h"

Gfx* drawImageWithFilter(Gfx* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int red, int green, int blue, int opacity) {
	dl = initDisplayList(dl);
	gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
	gDPSetPrimColor(dl++, 0, 0, red, green, blue, opacity);
	gDPSetCombineLERP(dl++, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0);
	gDPSetTextureFilter(dl++, G_TF_POINT);
	return displayImage(dl++, text_index, 0, codec_index, img_width, img_height, x, y, xScale, yScale, 0, 0.0f);
}

Gfx* drawImage(Gfx* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int opacity) {
	return drawImageWithFilter(dl, text_index, codec_index, img_width, img_height, x, y, xScale, yScale, 0xFF, 0xFF, 0xFF, opacity);
}

Gfx* drawTri(Gfx* dl, short x1, short y1, short x2, short y2, short x3, short y3, int red, int green, int blue, int alpha) {
	dl = initDisplayList(dl);
	gDPSetCombineLERP(dl++, NOISE, TEXEL0, 0, COMBINED, TEXEL1, COMBINED, LOD_FRACTION, COMBINED, COMBINED, COMBINED, SHADE, PRIMITIVE, COMBINED, 1, PRIMITIVE, SHADE);
	gSPMatrix(dl++, 0x02000180, G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
	gSPMatrix(dl++, 0x02000080, G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_PROJECTION);
	// Vertex 0
	gSPModifyVertex(dl++, 0, G_MWO_POINT_XYSCREEN, (x1 << 16) | y1);
	gSPModifyVertex(dl++, 0, G_MWO_POINT_RGBA, 0xFFFFFFFF);
	// Vertex 1
	gSPModifyVertex(dl++, 1, G_MWO_POINT_XYSCREEN, (x2 << 16) | y2);
	gSPModifyVertex(dl++, 1, G_MWO_POINT_RGBA, 0xFFFFFFFF);
	// Vertex 2
	gSPModifyVertex(dl++, 2, G_MWO_POINT_XYSCREEN, (x3 << 16) | y3);
	gSPModifyVertex(dl++, 2, G_MWO_POINT_RGBA, 0xFFFFFFFF);
	gDPSetPrimColor(dl++, 0, 0, red, green, blue, alpha);
	// Draw Tri
	gSP1Triangle(dl++, 0, 1, 2, 0);
	return dl;
}

Gfx* drawPixelText(Gfx* dl, int x, int y, char* str, int red, int green, int blue, int alpha) {
	gDPPipeSync(dl++);
	gDPSetCycleType(dl++, G_CYC_1CYCLE);
	gSPClearGeometryMode(dl++, G_ZBUFFER | G_SHADE | G_CULL_BOTH | G_FOG | G_LIGHTING | G_TEXTURE_GEN | G_TEXTURE_GEN_LINEAR | G_LOD | G_SHADING_SMOOTH | G_CLIPPING | 0x0040F9FA);
	gSPSetGeometryMode(dl++, G_SHADE | G_SHADING_SMOOTH);
    gDPSetPrimColor(dl++, 0, 0, red, green, blue, alpha);
    gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
	gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
    return textDraw(dl,2,x,y,str);
}

Gfx* drawPixelTextContainer(Gfx* dl, int x, int y, char* str, int red, int green, int blue, int alpha, int offset) {
	if (offset) {
		dl = drawPixelText(dl,x-offset,y+offset,str,0,0,0,alpha);
	}
	return drawPixelText(dl,x,y,str,red,green,blue,alpha);
}

Gfx* displayCenteredText(Gfx* dl, int y, char* str, int offset) {
	int length = cstring_strlen(str);
	return drawPixelTextContainer(dl, 160 - (length << 2), y, str, 0xFF, 0xFF, 0xFF, 0xFF, offset);
}

Gfx* drawScreenRect(Gfx* dl, int x1, int y1, int x2, int y2, int red, int green, int blue, int alpha) {
	gDPPipeSync(dl++);
	gDPSetCycleType(dl++, G_CYC_FILL);
	gDPSetRenderMode(dl++, G_RM_NOOP, G_RM_NOOP2);
	gSPClearGeometryMode(dl++, G_ZBUFFER);
	gDPSetFillColor(dl++, ((red & 0x1F) << 11) | ((green & 0x1F) << 6) | ((blue & 0x1F) << 1) | (alpha & 0x1));
	gDPSetScissor(dl++, G_SC_NON_INTERLACE, 10, 10, 309, 229);
	gDPFillRectangle(dl++, x1 >> 2, y1 >> 2, x2 >> 2, y2 >> 2);
	return dl;
}

Gfx* drawString(Gfx* dl, int style, float x, float y, char* str) {
	float height = (float)getTextStyleHeight(style);
	float text_y = y - (height * 0x5);
	int centered = 0;
	if (style & 0x80) {
		centered = 0x80;
	}
	return displayText(dl, style & 0x7F, 4 * x, 4 * text_y, str, centered);
}

Gfx* drawText(Gfx* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity) {
	dl = initDisplayList(dl);
	int short_style = style & 0x7F;
	if (short_style == 1) {
		gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
		gSPMatrix(dl++, (int)&style128Mtx[0], G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
	} else {
		gSPDisplayList(dl++, 0x01000118);
		gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
		if (short_style == 6) {
			gSPMatrix(dl++, (int)&style6Mtx[0], G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
		} else if (short_style == 2) {
			gSPMatrix(dl++, (int)&style2Mtx[0], G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
		}
		gDPSetPrimColor(dl++, 0, 0, red, green, blue, opacity);
	}
	return drawString(dl,style,x,y,str);
}

Gfx* drawTextContainer(Gfx* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity, int background) {
	if (background) {
		dl = drawText(dl,style,x-background,y+background,str,0,0,0,opacity);
	}
	return drawText(dl,style,x,y,str,red,green,blue,opacity);
}

static char* character_recoloring_str = 0;
static char use_character_recoloring = 0;
static char char_color_data[0x40];
static unsigned char char_opacity_data[0x40];

void setCharacterRecoloring(int output, char* stored_str) {
	use_character_recoloring = output;
	character_recoloring_str = stored_str;
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