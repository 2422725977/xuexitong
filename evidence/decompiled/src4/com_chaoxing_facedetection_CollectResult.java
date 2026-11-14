package com.chaoxing.facedetection;
public class CollectResult implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR = None;
    public static final int LIVE_STATUS_BACK = 253;
    public static final int LIVE_STATUS_FAIL = 0;
    public static final int LIVE_STATUS_SKIP = 255;
    public static final int LIVE_STATUS_SUCCESS = 1;
    public static final int LIVE_STATUS_UNKNOWN = 254;
    private int collectType;
    private com.chaoxing.facedetection.FaceLog faceLog;
    private String imagePath;
    private int liveDetectionStatus;
    private android.graphics.RectF rect;
    private int result;
    private com.chaoxing.facedetection.bean.SenseDetectResult senseDetectResult;
    private com.chaoxing.facedetection.UploadResult uploadResult;

    static CollectResult()
    {
        com.chaoxing.facedetection.CollectResult.CREATOR = new com.chaoxing.facedetection.CollectResult$a();
        return;
    }

    public CollectResult()
    {
        return;
    }

    public CollectResult(android.os.Parcel p2)
    {
        this.result = p2.readInt();
        this.collectType = p2.readInt();
        this.liveDetectionStatus = p2.readInt();
        this.imagePath = p2.readString();
        this.rect = ((android.graphics.RectF) p2.readParcelable(android.graphics.RectF.getClassLoader()));
        this.uploadResult = ((com.chaoxing.facedetection.UploadResult) p2.readParcelable(com.chaoxing.facedetection.UploadResult.getClassLoader()));
        this.senseDetectResult = ((com.chaoxing.facedetection.bean.SenseDetectResult) p2.readParcelable(com.chaoxing.facedetection.bean.SenseDetectResult.getClassLoader()));
        this.faceLog = ((com.chaoxing.facedetection.FaceLog) p2.readParcelable(com.chaoxing.facedetection.FaceLog.getClassLoader()));
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public int getCollectType()
    {
        return this.collectType;
    }

    public com.chaoxing.facedetection.FaceLog getFaceLog()
    {
        return this.faceLog;
    }

    public String getImagePath()
    {
        return this.imagePath;
    }

    public int getLiveDetectionStatus()
    {
        return this.liveDetectionStatus;
    }

    public android.graphics.RectF getRect()
    {
        return this.rect;
    }

    public int getResult()
    {
        return this.result;
    }

    public com.chaoxing.facedetection.bean.SenseDetectResult getSenseDetectResult()
    {
        return this.senseDetectResult;
    }

    public com.chaoxing.facedetection.UploadResult getUploadResult()
    {
        return this.uploadResult;
    }

    public void setCollectType(int p1)
    {
        this.collectType = p1;
        return;
    }

    public void setFaceLog(com.chaoxing.facedetection.FaceLog p1)
    {
        this.faceLog = p1;
        return;
    }

    public void setImagePath(String p1)
    {
        this.imagePath = p1;
        return;
    }

    public void setLiveDetectionStatus(int p1)
    {
        this.liveDetectionStatus = p1;
        return;
    }

    public void setRect(android.graphics.RectF p1)
    {
        this.rect = p1;
        return;
    }

    public void setResult(int p1)
    {
        this.result = p1;
        return;
    }

    public void setSenseDetectResult(com.chaoxing.facedetection.bean.SenseDetectResult p1)
    {
        this.senseDetectResult = p1;
        return;
    }

    public void setUploadResult(com.chaoxing.facedetection.UploadResult p1)
    {
        this.uploadResult = p1;
        return;
    }

    public String toString()
    {
        String v0_1 = new StringBuilder();
        v0_1.append("CollectResult{result=");
        v0_1.append(this.result);
        v0_1.append(",liveDetectionStatus=");
        v0_1.append(this.liveDetectionStatus);
        v0_1.append(", imagePath=\'");
        v0_1.append(this.imagePath);
        v0_1.append(39);
        v0_1.append(", rect=");
        v0_1.append(this.rect);
        v0_1.append(", uploadResult=");
        v0_1.append(this.uploadResult);
        v0_1.append(125);
        return v0_1.toString();
    }

    public void writeToParcel(android.os.Parcel p2, int p3)
    {
        p2.writeInt(this.result);
        p2.writeInt(this.collectType);
        p2.writeInt(this.liveDetectionStatus);
        p2.writeString(this.imagePath);
        p2.writeParcelable(this.rect, p3);
        p2.writeParcelable(this.uploadResult, p3);
        p2.writeParcelable(this.senseDetectResult, p3);
        p2.writeParcelable(this.faceLog, p3);
        return;
    }
}
