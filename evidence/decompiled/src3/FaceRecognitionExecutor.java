package com.chaoxing.mobile.webapp.jsprotocal.exam;
public class FaceRecognitionExecutor extends com.chaoxing.mobile.webapp.jsprotocal.a implements androidx.lifecycle.LifecycleOwner {
    public static ss.b r;
    public static ss.o s;
    public androidx.lifecycle.LifecycleRegistry k;
    public String l;
    public String m;
    public String n;
    public int o;
    public android.os.Handler p;
    public int q;

    public FaceRecognitionExecutor(android.app.Activity p2, com.fanzhou.ui.WebClient p3)
    {
        super(p2, p3);
        super.o = 0;
        super.p = new android.os.Handler(android.os.Looper.getMainLooper());
        super.d = p3;
        qi.g v2_2 = new androidx.lifecycle.LifecycleRegistry(super);
        super.k = v2_2;
        v2_2.markState(androidx.lifecycle.Lifecycle$State.RESUMED);
        com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor.r = qi.c.a();
        com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor.s = qi.g.a();
        return;
    }

    public static synthetic void G(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p4, com.chaoxing.facedetection.UploadResult p5, androidx.lifecycle.MutableLiveData p6, qe.b p7)
    {
        p4.getClass();
        if (!p7.f()) {
            com.chaoxing.facedetection.bean.FaceInfo v0_1 = p5.getFaceInfo();
            int v2 = 0;
            if (!p7.g()) {
                p4.b0(p7);
            } else {
                int v1_0 = p7.c;
                if ((v1_0 != 0) && (((com.fanzhou.loader.Result) v1_0).getStatus() == 1)) {
                    v2 = 1;
                }
                if (v2 == 0) {
                    p4.b0(p7);
                }
            }
            if (v2 == 1) {
                v0_1.setCollectedObjectStr(p5.getObjectIdStr());
            }
            v0_1.setUpdateFaceStatus(v2);
            p5.setStatus(v2);
            p6.postValue(p5);
            return;
        } else {
            return;
        }
    }

    public static synthetic void H(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p2, com.chaoxing.facedetection.CollectResult p3)
    {
        p2.getClass();
        String v3_2 = p3.getUploadResult();
        if ((v3_2 != null) && (v3_2.getStatus() == 1)) {
            com.chaoxing.mobile.webapp.e.a().c(v3_2.getRawData());
            p2.q(v3_2.getRawData());
        }
        return;
    }

    public static synthetic com.fanzhou.ui.WebClient I(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0)
    {
        return p0.d;
    }

    public static synthetic com.fanzhou.ui.WebClient J(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0)
    {
        return p0.d;
    }

    public static synthetic void K(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0, com.chaoxing.facedetection.bean.CollectFile p1, int p2, com.chaoxing.facedetection.UploadResult p3, int p4)
    {
        p0.X(p1, p2, p3, p4);
        return;
    }

    public static synthetic void L(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0, int p1, boolean p2, int p3, com.chaoxing.facedetection.bean.FaceInfo p4)
    {
        p0.U(p1, p2, p3, p4);
        return;
    }

    public static synthetic void M(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0, com.chaoxing.facedetection.CollectResult p1, int p2, int p3)
    {
        p0.Y(p1, p2, p3);
        return;
    }

    public static synthetic String N(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0)
    {
        return p0.l;
    }

    public static synthetic String O(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0)
    {
        return p0.m;
    }

    public static synthetic void P(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0, androidx.lifecycle.LifecycleOwner p1, com.chaoxing.mobile.clouddisk.upload.CloudUploadConfig p2, java.io.File p3, com.chaoxing.facedetection.bean.FaceInfo p4, int p5, int p6, com.chaoxing.facedetection.bean.CollectFile p7)
    {
        p0.a0(p1, p2, p3, p4, p5, p6, p7);
        return;
    }

    public static synthetic int Q(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0)
    {
        return p0.o;
    }

    public static synthetic androidx.lifecycle.LiveData R(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0, androidx.lifecycle.LifecycleOwner p1, com.chaoxing.facedetection.UploadResult p2)
    {
        return p0.c0(p1, p2);
    }

    public static synthetic android.app.Activity S(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor p0)
    {
        return p0.a;
    }

    public final void b0(qe.b p3)
    {
        this.p.post(new com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$d(this, p3));
        return;
    }

    public final void X(com.chaoxing.facedetection.bean.CollectFile p3, int p4, com.chaoxing.facedetection.UploadResult p5, int p6)
    {
        com.chaoxing.facedetection.CollectResult v0_1 = new com.chaoxing.facedetection.CollectResult();
        v0_1.setSenseDetectResult(p3.getSenseDetectResult());
        v0_1.setFaceLog(p3.getFaceLog());
        v0_1.setLiveDetectionStatus(p3.getCollectState());
        v0_1.setUploadResult(p5);
        v0_1.setCollectType(p6);
        v0_1.setImagePath(p3.getPath());
        this.Y(v0_1, p6, p4);
        return;
    }

    public final void U(int p13, boolean p14, int p15, com.chaoxing.facedetection.bean.FaceInfo p16)
    {
        com.chaoxing.facedetection.bean.CollectConfig v7_1 = new com.chaoxing.facedetection.bean.CollectConfig();
        com.chaoxing.facedetection.FaceCollector v0_0 = 1;
        v7_1.setCollectType(1);
        if (p13 != 1) {
            if (p13 != 3) {
                if (p13 == 4) {
                    v7_1.setSupportOpenUpload(1);
                    v7_1.setCollectTimeoutType(1);
                }
            } else {
                v7_1.setForceOpenUpload(p14);
                v7_1.setCollectTimeoutType(2);
            }
        } else {
            if ((p16 == null) || (p16.getOpenUpload() != 1)) {
                com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$f v6_1 = 0;
            } else {
                v6_1 = 1;
            }
            v7_1.setSupportOpenUpload(v6_1);
            v7_1.setCollectTimeoutType(2);
        }
        if (p15 != 1) {
            v0_0 = 0;
        }
        v7_1.setModel(v0_0);
        com.chaoxing.facedetection.FaceCollector.g().d(this.k().getContext(), this.k(), com.chaoxing.facedetection.compat.FaceDetectorCompatActivity, v7_1, new com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$c(this, p13, p15), new com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$f(this, this, p15, p13, this.n, p16));
        return;
    }

    public final void Y(com.chaoxing.facedetection.CollectResult p17, int p18, int p19)
    {
        String v5_4;
        String v2_10;
        String v2_11 = p17.getUploadResult();
        ss.o v4_2 = 0;
        if (v2_11 == null) {
            v5_4 = "";
            v2_10 = 0;
        } else {
            if (!com.fanzhou.util.w.s(v2_11.getObjectIdStr())) {
                v5_4 = v2_11.getObjectIdStr();
            } else {
                v5_4 = "";
            }
            v2_10 = v2_11.getStatus();
        }
        if (p17.getLiveDetectionStatus() != -1) {
            if (p17.getLiveDetectionStatus() != 1) {
                if (p17.getLiveDetectionStatus() == -3) {
                    v4_2 = -3;
                }
            } else {
                v4_2 = 1;
            }
        } else {
            v4_2 = -1;
        }
        int v6_4 = new java.util.HashMap();
        int v7_3 = new org.json.JSONObject();
        if ((p18 != 1) && (p18 != 3)) {
            if (p18 == 2) {
                v7_3.put("LiveDetectionStatus", v4_2);
            }
        } else {
            v7_3.put("currentFaceId", v5_4);
            v7_3.put("collectStatus", v2_10);
            v7_3.put("LiveDetectionStatus", v4_2);
            v6_4.put("currentFaceId", v5_4);
            boolean v0_15 = new StringBuilder();
            v0_15.append(v2_10);
            v0_15.append("");
            v6_4.put("collectStatus", v0_15.toString());
            boolean v0_18 = new StringBuilder();
            v0_18.append(v4_2);
            v0_18.append("");
            v6_4.put("LiveDetectionStatus", v0_18.toString());
            if (p19 == 1) {
                v7_3.put("recogType", p19);
                String v2_14 = new StringBuilder();
                v2_14.append(p19);
                v2_14.append("");
                v6_4.put("recogType", v2_14.toString());
                String v2_16 = p17.getSenseDetectResult();
                if (v2_16 != null) {
                    ss.o v4_4 = new StringBuilder();
                    v4_4.append(v2_16.getResult());
                    v4_4.append("");
                    v6_4.put("SenseDetectionStatus", v4_4.toString());
                    v7_3.put("SenseDetectionStatus", v2_16.getResult());
                    v6_4.put("sessionId", v2_16.getSessionId());
                    v7_3.put("sessionId", v2_16.getSessionId());
                    ss.o v4_0 = new org.json.JSONObject();
                    v4_0.put("errCode", v2_16.getErrCode());
                    v4_0.put("errMsg", v2_16.getErrMsg());
                    v7_3.put("extraData", v4_0.toString());
                }
            }
            if (p17.getFaceLog() != null) {
                v7_3.put("extraData", ne.a.g(p17.getFaceLog()));
            }
        }
        if (!v6_4.containsKey("currentFaceId")) {
            v6_4.put("currentFaceId", "");
        }
        if (!v6_4.containsKey("collectStatus")) {
            v6_4.put("collectStatus", "0");
        }
        if (!v6_4.containsKey("LiveDetectionStatus")) {
            v6_4.put("LiveDetectionStatus", "0");
        }
        if (p19 == 1) {
            if (!v6_4.containsKey("recogType")) {
                v6_4.put("recogType", "0");
            }
            if (!v7_3.has("recogType")) {
                v7_3.put("recogType", p19);
            }
            if (!v6_4.containsKey("sessionId")) {
                v6_4.put("sessionId", "");
            }
            if (!v7_3.has("sessionId")) {
                v7_3.put("sessionId", "");
            }
            if (!v6_4.containsKey("SenseDetectionStatus")) {
                v6_4.put("SenseDetectionStatus", "0");
            }
            if (!v7_3.has("SenseDetectionStatus")) {
                v7_3.put("SenseDetectionStatus", "0");
            }
        }
        boolean v0_11 = System.currentTimeMillis();
        v7_3.put("signToken", ss.c.a().b(com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor.r, com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor.s, Long.toString(v0_11), v6_4));
        v7_3.put("cxcid", com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor.r.get());
        v7_3.put("cxtime", Long.toString(v0_11));
        try {
            this.q(v7_3.toString());
            return;
        } catch (boolean v0_10) {
            v0_10.printStackTrace();
            return;
        }
    }

    public final void a0(androidx.lifecycle.LifecycleOwner p13, com.chaoxing.mobile.clouddisk.upload.CloudUploadConfig p14, java.io.File p15, com.chaoxing.facedetection.bean.FaceInfo p16, int p17, int p18, com.chaoxing.facedetection.bean.CollectFile p19)
    {
        long v0_1 = (this.q + 1);
        this.q = v0_1;
        if (v0_1 <= 3) {
            long v0_2;
            if (v0_1 != 2) {
                if (v0_1 != 3) {
                    v0_2 = 60000;
                } else {
                    v0_2 = 600000;
                }
            } else {
                v0_2 = 300000;
            }
            if ((p13 != null) && (p13.getLifecycle().getCurrentState() == androidx.lifecycle.Lifecycle$State.RESUMED)) {
                this.p.postDelayed(new com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$e(this, p13, p14, p15, p16, p17, p18, p19), v0_2);
            }
        }
        return;
    }

    public final androidx.lifecycle.LiveData c0(androidx.lifecycle.LifecycleOwner p4, com.chaoxing.facedetection.UploadResult p5)
    {
        androidx.lifecycle.MutableLiveData v0_1 = new androidx.lifecycle.MutableLiveData();
        com.chaoxing.mobile.exam.persistence.a.d().g(p5.getObjectIdStr()).observe(p4, new com.chaoxing.mobile.webapp.jsprotocal.exam.l(this, p5, v0_1));
        return v0_1;
    }

    public final void V()
    {
        com.chaoxing.facedetection.bean.CollectConfig v4_1 = new com.chaoxing.facedetection.bean.CollectConfig();
        v4_1.setModel(0);
        v4_1.setCollectType(0);
        com.chaoxing.facedetection.FaceCollector.g().d(this.k().getContext(), this.k(), com.chaoxing.facedetection.compat.FaceDetectorCompatActivity, v4_1, new com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$a(this), new com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$g(this.k(), this.n, this));
        return;
    }

    public final void T(int p4)
    {
        com.chaoxing.mobile.exam.persistence.a.d().c(com.chaoxing.study.account.AccountManager.C().D().getPuid()).observe(new com.chaoxing.mobile.webapp.jsprotocal.exam.j(this), new com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor$b(this, p4));
        return;
    }

    public final void W(String p9, String p10, int p11, int p12)
    {
        com.chaoxing.mobile.webapp.e.a().d(this.b.getContext(), this, p9, p10, p11, p12, new com.chaoxing.mobile.webapp.jsprotocal.exam.k(this));
        return;
    }

    public void destory()
    {
        this.k.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor.r = 0;
        com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor.s = 0;
        super.destory();
        return;
    }

    public void execute(String p7)
    {
        if (!com.fanzhou.util.w.s(p7)) {
            String v0_2 = new org.json.JSONObject(p7);
            com.chaoxing.facedetection.bean.FaceInfo v7_12 = v0_2.optInt("funTag", -1);
            int v2_0 = 0;
            int v1_0 = v0_2.optInt("recogType", 0);
            this.l = v0_2.optString("uploadParams");
            this.m = v0_2.optString("faceUploadParam");
            this.n = v0_2.optString("uploadConfig");
            boolean v3_7 = v0_2.optJSONObject("funData");
            if (v7_12 != null) {
                if (v7_12 != 1) {
                    if (v7_12 != 2) {
                        if (v7_12 != 3) {
                            if (v7_12 == 4) {
                                com.chaoxing.facedetection.bean.FaceInfo v7_2 = v0_2.optString("recInterface");
                                String v0_3 = "";
                                if (v3_7) {
                                    v0_3 = v3_7.optString("tipMsg");
                                    v2_0 = v3_7.optInt("skipConfirm");
                                }
                                if (!ve.f.c(v7_2)) {
                                    this.W(v7_2, v0_3, v2_0, v1_0);
                                }
                            }
                        } else {
                            if (v3_7) {
                                this.o = v3_7.optInt("ignoreFaceId", 0);
                            }
                            if (this.o == 0) {
                                v2_0 = 1;
                            }
                            this.U(3, v2_0, v1_0, new com.chaoxing.facedetection.bean.FaceInfo());
                            return;
                        }
                    } else {
                        this.U(2, 0, v1_0, new com.chaoxing.facedetection.bean.FaceInfo());
                        return;
                    }
                } else {
                    this.T(v1_0);
                    return;
                }
            } else {
                this.V();
                return;
            }
        }
        return;
    }

    public androidx.lifecycle.Lifecycle getLifecycle()
    {
        return this.k;
    }
}
