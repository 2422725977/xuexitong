package com.chaoxing.facedetection.bean;
public class FaceInfo implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
    private String collectedObjectStr;
    private int openUpload;
    private int updateFaceStatus;

    static FaceInfo()
    {
        com.chaoxing.facedetection.bean.FaceInfo.CREATOR = new com.chaoxing.facedetection.bean.FaceInfo$a();
        return;
    }

    public FaceInfo()
    {
        return;
    }

    public FaceInfo(android.os.Parcel p2)
    {
        this.openUpload = p2.readInt();
        this.collectedObjectStr = p2.readString();
        this.updateFaceStatus = p2.readInt();
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public String getCollectedObjectStr()
    {
        return this.collectedObjectStr;
    }

    public int getOpenUpload()
    {
        return this.openUpload;
    }

    public int getUpdateFaceStatus()
    {
        return this.updateFaceStatus;
    }

    public void setCollectedObjectStr(String p1)
    {
        this.collectedObjectStr = p1;
        return;
    }

    public void setOpenUpload(int p1)
    {
        this.openUpload = p1;
        return;
    }

    public void setUpdateFaceStatus(int p1)
    {
        this.updateFaceStatus = p1;
        return;
    }

    public void writeToParcel(android.os.Parcel p1, int p2)
    {
        p1.writeInt(this.openUpload);
        p1.writeString(this.collectedObjectStr);
        p1.writeInt(this.updateFaceStatus);
        return;
    }
}
