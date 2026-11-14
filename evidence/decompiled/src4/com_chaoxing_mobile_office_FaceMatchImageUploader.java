package com.chaoxing.mobile.office;
public class FaceMatchImageUploader implements com.chaoxing.facedetection.b, androidx.lifecycle.LifecycleOwner {
    public static final String h = "FaceMatchImageUploader";
    public final androidx.lifecycle.LifecycleOwner a;
    public final int b;
    public final com.chaoxing.facedetection.bean.FaceInfo c;
    public final androidx.lifecycle.LifecycleRegistry d;
    public final String e;
    public int f;
    public final android.os.Handler g;

    private androidx.lifecycle.LiveData k(androidx.lifecycle.LifecycleOwner p4, com.chaoxing.facedetection.UploadResult p5)
    {
        androidx.lifecycle.MutableLiveData v0_1 = new androidx.lifecycle.MutableLiveData();
        com.chaoxing.mobile.exam.persistence.a.d().g(p5.getObjectIdStr()).observe(p4, new com.chaoxing.mobile.office.e0(p5, v0_1));
        return v0_1;
    }

    private void g()
    {
        this.f = 0;
        this.g.removeCallbacksAndMessages(0);
        return;
    }

    static FaceMatchImageUploader()
    {
        return;
    }

    public FaceMatchImageUploader(int p3, String p4, com.chaoxing.facedetection.bean.FaceInfo p5)
    {
        this.g = new android.os.Handler(android.os.Looper.getMainLooper());
        this.a = this;
        this.b = p3;
        this.e = p4;
        this.f = 0;
        this.c = p5;
        androidx.lifecycle.LifecycleRegistry v3_2 = new androidx.lifecycle.LifecycleRegistry(this);
        this.d = v3_2;
        v3_2.markState(androidx.lifecycle.Lifecycle$State.RESUMED);
        v3_2.addObserver(new com.chaoxing.mobile.office.FaceMatchImageUploader$1(this));
        return;
    }

    public static synthetic void b(com.chaoxing.mobile.office.FaceMatchImageUploader p0, java.io.File p1)
    {
        p0.h(p1);
        return;
    }

    public static synthetic void c(com.chaoxing.mobile.office.FaceMatchImageUploader p1, androidx.lifecycle.MediatorLiveData p2, androidx.lifecycle.LiveData p3, com.chaoxing.facedetection.UploadResult p4, String p5, java.io.File p6, qe.b p7)
    {
        p1.getClass();
        if ((!com.chaoxing.mobile.office.utils.d1.b(p7)) || (!p7.f())) {
            p2.removeSource(p3);
            if ((!com.chaoxing.mobile.office.utils.d1.b(p7)) || ((!com.chaoxing.mobile.office.utils.d1.b(p7.c)) || (!com.chaoxing.mobile.office.utils.d1.b(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p7.c).getData())))) {
                p4.setStatus(0);
                p1.j(p4, p6, p2);
                return;
            } else {
                String v3_10 = ((com.chaoxing.mobile.office.apiresponse.CommonResponse) p7.c).getData().getErrorCode();
                if (v3_10 != null) {
                    if (v3_10 > 111) {
                        if (v3_10 >= 222000) {
                            p4.setStatus(0);
                            p4.setRawData(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p7.c).getMsg());
                            p2.postValue(p4);
                        }
                    } else {
                        p4.setStatus(0);
                        p4.setRawData(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p7.c).getMsg());
                        p1.j(p4, p6, p2);
                        return;
                    }
                } else {
                    if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p7.c).getData().getResult() != 1) {
                        p4.setStatus(0);
                        p4.setRawData(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p7.c).getMsg());
                    } else {
                        p4.setStatus(1);
                        p4.setRawData(p5);
                    }
                    p2.postValue(p4);
                    return;
                }
            }
        }
        return;
    }

    public static synthetic void d(com.chaoxing.facedetection.UploadResult p4, androidx.lifecycle.MutableLiveData p5, qe.b p6)
    {
        if ((!com.chaoxing.mobile.office.utils.d1.b(p6)) || (!p6.f())) {
            com.chaoxing.facedetection.bean.FaceInfo v0_2 = p4.getFaceInfo();
            int v2 = 0;
            if ((com.chaoxing.mobile.office.utils.d1.b(p6)) && ((p6.g()) && ((com.chaoxing.mobile.office.utils.d1.b(p6.c)) && (((com.fanzhou.loader.Result) p6.c).getStatus() == 1)))) {
                v2 = 1;
            }
            if (v2 != 1) {
                p4.setRawData("\u4e0a\u4f20\u4eba\u8138\u6570\u636e\u5931\u8d25");
            } else {
                v0_2.setCollectedObjectStr(p4.getObjectIdStr());
            }
            v0_2.setUpdateFaceStatus(v2);
            p5.postValue(p4);
            return;
        } else {
            return;
        }
    }

    public static synthetic void e(com.chaoxing.mobile.office.FaceMatchImageUploader p3, androidx.lifecycle.MediatorLiveData p4, com.chaoxing.facedetection.bean.CollectFile p5, Object p6)
    {
        p3.getClass();
        com.chaoxing.facedetection.UploadResult v0_1 = new com.chaoxing.facedetection.UploadResult();
        if (((p6 instanceof com.fanzhou.loader.Result)) && (((com.fanzhou.loader.Result) p6).getStatus() == 1)) {
            String v6_2 = ((com.chaoxing.mobile.clouddisk.bean.CloudDiskFile1) ((com.fanzhou.loader.Result) p6).getData());
            if (com.chaoxing.mobile.office.utils.d1.b(v6_2)) {
                v0_1.setStatus(1);
                v0_1.setObjectIdStr(v6_2.getObjectId());
            }
        }
        if (v0_1.getStatus() != 0) {
            v0_1.setFaceInfo(p3.c);
            if ((p3.c.getOpenUpload() != 1) || (p5.getCollectState() != 1)) {
                p4.postValue(v0_1);
                p3.d.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
                return;
            } else {
                androidx.lifecycle.LiveData v3_2 = p3.k(p3.a, v0_1);
                java.util.Objects.requireNonNull(p4);
                p4.addSource(v3_2, new com.chaoxing.mobile.office.c0(p4));
                return;
            }
        } else {
            v0_1.setStatus(0);
            v0_1.setRawData("\u4eba\u8138\u91c7\u96c6\u6210\u529f,\u4e0a\u4f20\u4e91\u76d8\u5931\u8d25");
            p4.postValue(v0_1);
            return;
        }
    }

    public static synthetic void f(com.chaoxing.mobile.office.FaceMatchImageUploader p0)
    {
        p0.g();
        return;
    }

    public final androidx.lifecycle.MediatorLiveData h(java.io.File p9)
    {
        com.chaoxing.facedetection.UploadResult v4_1 = new com.chaoxing.facedetection.UploadResult();
        androidx.lifecycle.MediatorLiveData v2_1 = new androidx.lifecycle.MediatorLiveData();
        try {
            okio.BufferedSource v7 = okio.s0.e(okio.s0.t(p9));
            try {
                String v5 = com.chaoxing.mobile.util.d.b(v7.D());
                int v3_1 = gl.i.d().a(this.i(v5), this.e, v5);
                v2_1.addSource(v3_1, new com.chaoxing.mobile.office.d0(this, v2_1, v3_1, v4_1, v5, p9));
            } catch (Throwable v0_3) {
                Throwable v9_1 = v0_3;
                if (v7 != null) {
                    try {
                        v7.close();
                    } catch (Throwable v0_4) {
                        v9_1.addSuppressed(v0_4);
                    }
                }
                throw v9_1;
            }
            v7.close();
            return v2_1;
        } catch (Throwable v0_5) {
            Throwable v9_2 = v0_5;
            v4_1.setStatus(0);
            v4_1.setRawData("");
            v2_1.postValue(v4_1);
            com.chaoxing.android.log.d.d().e(com.chaoxing.mobile.office.FaceMatchImageUploader.h, 0, v9_2);
            return v2_1;
        }
    }

    public final void j(com.chaoxing.facedetection.UploadResult p3, java.io.File p4, androidx.lifecycle.MediatorLiveData p5)
    {
        long v0_1 = (this.f + 1);
        this.f = v0_1;
        if (v0_1 >= 3) {
            p5.postValue(p3);
            return;
        } else {
            this.g.postDelayed(new com.chaoxing.mobile.office.f0(this, p4), 1000);
            return;
        }
    }

    public final androidx.lifecycle.LiveData l(com.chaoxing.facedetection.bean.CollectFile p6)
    {
        if ((!com.chaoxing.mobile.office.utils.d1.b(p6)) || (!ve.f.m(p6.getPath()))) {
            android.net.Uri v0_1 = 0;
        } else {
            v0_1 = new java.io.File(p6.getPath());
        }
        if ((!com.chaoxing.mobile.office.utils.d1.a(v0_1)) && ((v0_1.exists()) && (v0_1.isFile()))) {
            if ((this.b != 1) || ((!com.chaoxing.mobile.office.utils.d1.b(this.c)) || (this.c.getOpenUpload() != 1))) {
                return this.h(v0_1);
            } else {
                androidx.lifecycle.MediatorLiveData v1_10 = new androidx.lifecycle.MediatorLiveData();
                com.chaoxing.mobile.clouddisk.upload.c.q().C(this.a, android.net.Uri.fromFile(v0_1), new com.chaoxing.mobile.office.g0(this, v1_10, p6));
                return v1_10;
            }
        } else {
            androidx.lifecycle.MediatorLiveData v6_3 = new androidx.lifecycle.MutableLiveData();
            android.net.Uri v0_5 = new com.chaoxing.facedetection.UploadResult();
            v0_5.setStatus(0);
            v6_3.postValue(v0_5);
            return v6_3;
        }
    }

    public final com.chaoxing.mobile.office.bean.ASQueryParams i(String p5)
    {
        com.chaoxing.mobile.office.bean.ASQueryParams v0_1 = new com.chaoxing.mobile.office.bean.ASQueryParams();
        v0_1.setDateTime(com.chaoxing.mobile.office.utils.w1.p(System.currentTimeMillis()));
        v0_1.setDeptId(dl.a2.a());
        v0_1.setUid(com.chaoxing.study.account.AccountManager.C().D().getPuid());
        StringBuilder v1_4 = new StringBuilder();
        v1_4.append("[datetime=");
        v1_4.append(v0_1.getDateTime());
        v1_4.append("]");
        v1_4.append("[deptId=");
        v1_4.append(v0_1.getDeptId());
        v1_4.append("]");
        v1_4.append("[image=");
        v1_4.append(p5);
        v1_4.append("]");
        v1_4.append("[remoteImage=");
        v1_4.append(this.e);
        v1_4.append("]");
        v1_4.append("[sign=officeApp]");
        v1_4.append("[uid=");
        v1_4.append(v0_1.getUid());
        v1_4.append("]");
        v1_4.append(com.chaoxing.mobile.office.utils.a2.a());
        v0_1.setEnc(vt.n.f(v1_4.toString()));
        return v0_1;
    }

    public androidx.lifecycle.LiveData a(com.chaoxing.facedetection.bean.CollectFile p3)
    {
        if ((!com.chaoxing.mobile.office.utils.d1.a(this.a)) && (this.a.getLifecycle().getCurrentState() != androidx.lifecycle.Lifecycle$State.DESTROYED)) {
            if (this.b != 2) {
                return this.l(p3);
            } else {
                androidx.lifecycle.LiveData v3_3 = new androidx.lifecycle.MutableLiveData();
                com.chaoxing.facedetection.UploadResult v0_4 = new com.chaoxing.facedetection.UploadResult();
                v0_4.setStatus(1);
                v3_3.postValue(v0_4);
                return v3_3;
            }
        } else {
            androidx.lifecycle.LiveData v3_5 = new androidx.lifecycle.MutableLiveData();
            com.chaoxing.facedetection.UploadResult v0_6 = new com.chaoxing.facedetection.UploadResult();
            v0_6.setStatus(0);
            v3_5.postValue(v0_6);
            return v3_5;
        }
    }

    public androidx.lifecycle.Lifecycle getLifecycle()
    {
        return this.d;
    }
}
