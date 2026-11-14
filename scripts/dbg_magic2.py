import struct
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
    print(n,i,"hsize70",hsize==0x70,"endian",endian==0x12345678,"sz",fsize>0x100,
          "fits",i+fsize<=len(d),"ord",(i<moff<fsize),"stroff",stroff==0x70)
