package com.chaoxing.facedetection;
public class UploadResult implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
    private com.chaoxing.facedetection.bean.FaceInfo faceInfo;
    private String objectIdStr;
    private String rawData;
    private int status;

    static UploadResult()
    {
        com.chaoxing.facedetection.UploadResult.CREATOR = new com.chaoxing.facedetection.UploadResult$a();
        return;
    }

    public UploadResult()
    {
        return;
    }

    public UploadResult(android.os.Parcel p2)
    {
        this.status = p2.readInt();
        this.objectIdStr = p2.readString();
        this.rawData = p2.readString();
        this.faceInfo = ((com.chaoxing.facedetection.bean.FaceInfo) p2.readParcelable(com.chaoxing.facedetection.bean.FaceInfo.getClassLoader()));
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public com.chaoxing.facedetection.bean.FaceInfo getFaceInfo()
    {
        return this.faceInfo;
    }

    public String getObjectIdStr()
    {
        return this.objectIdStr;
    }

    public String getRawData()
    {
        return this.rawData;
    }

    public int getStatus()
    {
        return this.status;
    }

    public void setFaceInfo(com.chaoxing.facedetection.bean.FaceInfo p1)
    {
        this.faceInfo = p1;
        return;
    }

    public void setObjectIdStr(String p1)
    {
        this.objectIdStr = p1;
        return;
    }

    public void setRawData(String p1)
    {
        this.rawData = p1;
        return;
    }

    public void setStatus(int p1)
    {
        this.status = p1;
        return;
    }

    public void writeToParcel(android.os.Parcel p2, int p3)
    {
        p2.writeInt(this.status);
        p2.writeString(this.objectIdStr);
        p2.writeString(this.rawData);
        p2.writeParcelable(this.faceInfo, p3);
        return;
    }
}
