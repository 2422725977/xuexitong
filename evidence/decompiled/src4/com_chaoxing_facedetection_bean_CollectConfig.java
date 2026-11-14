package com.chaoxing.facedetection.bean;
public class CollectConfig implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR = None;
    public static final String TAG = "collect_config";
    public static final int TIMEOUT_COLLECT = 2;
    public static final int TIMEOUT_RETRY = 1;
    private int collectStep;
    private int collectTimeoutType;
    private int collectType;
    private boolean isForceOpenUpload;
    private boolean isSupportOpenUpload;
    private int model;
    private String uploadTips;

    static CollectConfig()
    {
        com.chaoxing.facedetection.bean.CollectConfig.CREATOR = new com.chaoxing.facedetection.bean.CollectConfig$a();
        return;
    }

    public CollectConfig()
    {
        this.collectStep = 1;
        return;
    }

    public CollectConfig(android.os.Parcel p4)
    {
        byte v1_3;
        int v0 = 1;
        this.collectStep = 1;
        this.model = p4.readInt();
        this.collectType = p4.readInt();
        this.collectStep = p4.readInt();
        this.collectTimeoutType = p4.readInt();
        if (p4.readByte() == 0) {
            v1_3 = 0;
        } else {
            v1_3 = 1;
        }
        this.isSupportOpenUpload = v1_3;
        if (p4.readByte() == 0) {
            v0 = 0;
        }
        this.isForceOpenUpload = v0;
        this.uploadTips = p4.readString();
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public int getCollectStep()
    {
        return this.collectStep;
    }

    public int getCollectTimeoutType()
    {
        return this.collectTimeoutType;
    }

    public int getCollectType()
    {
        return this.collectType;
    }

    public int getModel()
    {
        return this.model;
    }

    public String getUploadTips()
    {
        return this.uploadTips;
    }

    public boolean isForceOpenUpload()
    {
        return this.isForceOpenUpload;
    }

    public boolean isSupportOpenUpload()
    {
        return this.isSupportOpenUpload;
    }

    public void setCollectStep(int p1)
    {
        this.collectStep = p1;
        return;
    }

    public void setCollectTimeoutType(int p1)
    {
        this.collectTimeoutType = p1;
        return;
    }

    public void setCollectType(int p1)
    {
        this.collectType = p1;
        return;
    }

    public void setForceOpenUpload(boolean p1)
    {
        this.isForceOpenUpload = p1;
        return;
    }

    public void setModel(int p1)
    {
        this.model = p1;
        return;
    }

    public void setSupportOpenUpload(boolean p1)
    {
        this.isSupportOpenUpload = p1;
        return;
    }

    public void setUploadTips(String p1)
    {
        this.uploadTips = p1;
        return;
    }

    public void writeToParcel(android.os.Parcel p1, int p2)
    {
        p1.writeInt(this.model);
        p1.writeInt(this.collectType);
        p1.writeInt(this.collectStep);
        p1.writeInt(this.collectTimeoutType);
        p1.writeByte(((byte) this.isSupportOpenUpload));
        p1.writeByte(((byte) this.isForceOpenUpload));
        p1.writeString(this.uploadTips);
        return;
    }
}
