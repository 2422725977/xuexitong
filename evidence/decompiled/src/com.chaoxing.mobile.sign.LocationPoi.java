package com.chaoxing.mobile.sign;
public class LocationPoi implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
    private String addr;
    private String name;

    static LocationPoi()
    {
        com.chaoxing.mobile.sign.LocationPoi.CREATOR = new com.chaoxing.mobile.sign.LocationPoi$a();
        return;
    }

    public LocationPoi()
    {
        return;
    }

    public LocationPoi(android.os.Parcel p2)
    {
        this.name = p2.readString();
        this.addr = p2.readString();
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public String getAddr()
    {
        return this.addr;
    }

    public String getName()
    {
        return this.name;
    }

    public void setAddr(String p1)
    {
        this.addr = p1;
        return;
    }

    public void setName(String p1)
    {
        this.name = p1;
        return;
    }

    public void writeToParcel(android.os.Parcel p1, int p2)
    {
        p1.writeString(this.name);
        p1.writeString(this.addr);
        return;
    }
}
