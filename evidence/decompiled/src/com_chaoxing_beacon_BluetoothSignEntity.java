package com.chaoxing.beacon;
public class BluetoothSignEntity implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
    private java.util.List data;
    private int type;

    static BluetoothSignEntity()
    {
        com.chaoxing.beacon.BluetoothSignEntity.CREATOR = new com.chaoxing.beacon.BluetoothSignEntity$a();
        return;
    }

    private BluetoothSignEntity()
    {
        return;
    }

    public BluetoothSignEntity(android.os.Parcel p2)
    {
        this.type = p2.readInt();
        this.data = p2.createTypedArrayList(com.chaoxing.beacon.BluetoothDevices.CREATOR);
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public java.util.List getData()
    {
        if (this.data == null) {
            this.data = new java.util.ArrayList();
        }
        return this.data;
    }

    public int getType()
    {
        return this.type;
    }

    public void setData(java.util.List p1)
    {
        this.data = p1;
        return;
    }

    public void setType(int p1)
    {
        this.type = p1;
        return;
    }

    public void writeToParcel(android.os.Parcel p1, int p2)
    {
        p1.writeInt(this.type);
        p1.writeTypedList(this.data);
        return;
    }
}
