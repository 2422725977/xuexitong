package com.chaoxing.facedetection.sensetime.bean;
public class SenseLiveResult implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
    private java.util.List actionImages;
    private String defakeScore;
    private boolean liveness;
    private String livenessScore;
    private boolean multiFace;
    private java.util.List qualityImages;

    static SenseLiveResult()
    {
        com.chaoxing.facedetection.sensetime.bean.SenseLiveResult.CREATOR = new com.chaoxing.facedetection.sensetime.bean.SenseLiveResult$a();
        return;
    }

    public SenseLiveResult()
    {
        return;
    }

    public SenseLiveResult(android.os.Parcel p5)
    {
        byte v1_0;
        android.os.Parcelable$Creator v0 = com.chaoxing.facedetection.sensetime.bean.SenseImage.CREATOR;
        this.actionImages = p5.createTypedArrayList(v0);
        this.defakeScore = p5.readString();
        int v2 = 0;
        if (p5.readByte() == 0) {
            v1_0 = 0;
        } else {
            v1_0 = 1;
        }
        this.liveness = v1_0;
        this.livenessScore = p5.readString();
        if (p5.readByte() != 0) {
            v2 = 1;
        }
        this.multiFace = v2;
        this.qualityImages = p5.createTypedArrayList(v0);
        return;
    }

    public int describeContents()
    {
        return 0;
    }

    public java.util.List getActionImages()
    {
        return this.actionImages;
    }

    public String getDefakeScore()
    {
        return this.defakeScore;
    }

    public String getLivenessScore()
    {
        return this.livenessScore;
    }

    public java.util.List getQualityImages()
    {
        return this.qualityImages;
    }

    public boolean isLiveness()
    {
        return this.liveness;
    }

    public boolean isMultiFace()
    {
        return this.multiFace;
    }

    public void setActionImages(java.util.List p1)
    {
        this.actionImages = p1;
        return;
    }

    public void setDefakeScore(String p1)
    {
        this.defakeScore = p1;
        return;
    }

    public void setLiveness(boolean p1)
    {
        this.liveness = p1;
        return;
    }

    public void setLivenessScore(String p1)
    {
        this.livenessScore = p1;
        return;
    }

    public void setMultiFace(boolean p1)
    {
        this.multiFace = p1;
        return;
    }

    public void setQualityImages(java.util.List p1)
    {
        this.qualityImages = p1;
        return;
    }

    public void writeToParcel(android.os.Parcel p1, int p2)
    {
        p1.writeTypedList(this.actionImages);
        p1.writeString(this.defakeScore);
        p1.writeByte(((byte) this.liveness));
        p1.writeString(this.livenessScore);
        p1.writeByte(((byte) this.multiFace));
        p1.writeTypedList(this.qualityImages);
        return;
    }
}
