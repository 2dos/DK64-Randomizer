/* Rom Patcher JS - CRC32/MD5/SHA-1/checksums calculators v20200926 - Marc Robledo 2016-2020 - http://www.marcrobledo.com/license */

function padZeroes(intVal, nBytes){
	var hexString=intVal.toString(16);
	while (hexString.length<nBytes*2) {
        hexString='0'+hexString;
    }
	return hexString
}

/* CRC32 - from Alex - https://stackoverflow.com/a/18639999 */
const CRC32_TABLE=(function(){
	var c,crcTable=[];
	for(var n=0;n<256;n += 1){
		c=n;
		for (var k=0; k<8; k += 1) {
            c=((c&1)?(0xedb88320^(c>>>1)):(c>>>1));
        }
		crcTable[n]=c;
	}
	return crcTable;
}());
function crc32(marcFile, headerSize, ignoreLast4Bytes){
	var data=headerSize? new Uint8Array(marcFile._u8array.buffer, headerSize):marcFile._u8array;

	var crc=0^(-1);

	var len=ignoreLast4Bytes?data.length-4:data.length;
	for (var i=0; i<len; i += 1) {
        crc=(crc>>>8)^CRC32_TABLE[(crc^data[i])&0xff];
    }

	return ((crc^(-1))>>>0);
}
