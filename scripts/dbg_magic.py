import struct, sys
d = open("chaoxing/out/snap3/r_29.bin","rb").read()
P = bytes.fromhex("6465780a30333500")
pos=0; n=0
while True:
    i=d.find(P,pos)
    if i<0: break
    pos=i+1
    n+=1
    g=lambda o: struct.unpack_from("<I",d,i+o)[0]
    fsize,hsize,endian,moff,stroff = g(0x20),g(0x24),g(0x28),g(0x34),g(0x3c)
    print("hit%-3d i=%-9d fsize=%-9d hsize=%-4d endian=%-10s moff=%-9d stroff=%-4d len=%d %s" % (
        n,i,fsize,hsize,hex(endian),moff,stroff,len(d),
        "PASS" if (hsize==0x70 and endian==0x12345678 and fsize>0x100 and i+fsize<=len(d) and i<moff<fsize and stroff==0x70) else "FILTERED"))
