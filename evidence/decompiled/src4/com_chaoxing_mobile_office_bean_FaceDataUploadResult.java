package com.chaoxing.mobile.office.bean;
public class FaceDataUploadResult implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
    private String msg;
    private String objectId;
    private int status;
    private int uploadStatus;

    static FaceDataUploadResult()
    {
        com.chaoxing.mobile.office.bean.FaceDataUploadResult.CREATOR = new com.chaoxing.mobile.office.bean.FaceDataUploadResult$a();
        return;
    }

    public FaceDataUploadResult()
    {
        return;
    }

    public FaceDataUploadResult(android.os.Parcel p2)
    {
        this.status = p2.readInt();
        this.uploadStatus = p2.readInt();
        this.msg = p2.readString();
        this.objectId = p2.readString();
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public String getMsg()
    {
        return this.msg;
    }

    public String getObjectId()
    {
        return this.objectId;
    }

    public int getStatus()
    {
        return this.status;
    }

    public int getUploadStatus()
    {
        return this.uploadStatus;
    }

    public void setMsg(String p1)
    {
        this.msg = p1;
        return;
    }

    public void setObjectId(String p1)
    {
        this.objectId = p1;
        return;
    }

    public void setStatus(int p1)
    {
        this.status = p1;
        return;
    }

    public void setUploadStatus(int p1)
    {
        this.uploadStatus = p1;
        return;
    }

    public void writeToParcel(android.os.Parcel p1, int p2)
    {
        p1.writeInt(this.status);
        p1.writeInt(this.uploadStatus);
        p1.writeString(this.msg);
        p1.writeString(this.objectId);
        return;
    }
}
