package com.chaoxing.mobile.office.utils;
public class FaceCaptureRecognitionLifeOwner implements androidx.lifecycle.LifecycleOwner {
    public static final String g = "FaceCaptureRecognitionLifeOwner";
    public static final int h = 200;
    public final androidx.lifecycle.LifecycleRegistry a;
    public com.chaoxing.mobile.office.utils.f b;
    public boolean c;
    public String d;
    public final android.os.Handler e;
    public com.chaoxing.mobile.office.h0 f;

    private com.chaoxing.mobile.office.bean.ASQueryParams o(String p5)
    {
        String v5_3;
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
        String v3_3 = "";
        if (com.fanzhou.util.u.l(this.d)) {
            v5_3 = "";
        } else {
            v5_3 = "[remoteImage=";
        }
        String v5_6;
        v1_4.append(v5_3);
        if (com.fanzhou.util.u.l(this.d)) {
            v5_6 = "";
        } else {
            v5_6 = this.d;
        }
        v1_4.append(v5_6);
        if (!com.fanzhou.util.u.l(this.d)) {
            v3_3 = "]";
        }
        v1_4.append(v3_3);
        v1_4.append("[sign=officeApp]");
        v1_4.append("[uid=");
        v1_4.append(v0_1.getUid());
        v1_4.append("]");
        v1_4.append(com.chaoxing.mobile.office.utils.a2.a());
        v0_1.setEnc(vt.n.f(v1_4.toString()));
        return v0_1;
    }

    static FaceCaptureRecognitionLifeOwner()
    {
        return;
    }

    public FaceCaptureRecognitionLifeOwner()
    {
        androidx.lifecycle.LifecycleRegistry v0_1 = new androidx.lifecycle.LifecycleRegistry(this);
        this.a = v0_1;
        this.e = new android.os.Handler(android.os.Looper.getMainLooper());
        v0_1.markState(androidx.lifecycle.Lifecycle$State.CREATED);
        v0_1.addObserver(new com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner$1(this));
        return;
    }

    public static synthetic void a(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner p2, java.io.File p3, String p4, android.content.Context p5, qe.b p6)
    {
        p2.getClass();
        if ((!com.chaoxing.mobile.office.utils.d1.b(p6)) || (!p6.f())) {
            if ((!com.chaoxing.mobile.office.utils.d1.b(p6)) || ((!com.chaoxing.mobile.office.utils.d1.b(p6.c)) || (!com.chaoxing.mobile.office.utils.d1.b(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getData())))) {
                String v4_4 = new StringBuilder();
                v4_4.append(p5.getResources().getString(com.chaoxing.mobile.R$string.face_match_failed));
                v4_4.append("\u8bf7\u91cd\u8bd5!");
                p2.j(p5, v4_4.toString(), p3);
                return;
            } else {
                if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getData().getErrorCode() != 0) {
                    String v4_12;
                    if (!com.fanzhou.util.u.l(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg())) {
                        v4_12 = ((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg();
                    } else {
                        String v4_14 = new StringBuilder();
                        v4_14.append(p5.getResources().getString(com.chaoxing.mobile.R$string.face_match_failed));
                        v4_14.append(",\u8bf7\u91cd\u8bd5");
                        v4_12 = v4_14.toString();
                    }
                    p2.j(p5, v4_12, p3);
                    return;
                } else {
                    if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getData().getVerifyResult() != 1) {
                        p2.j(p5, p5.getResources().getString(com.chaoxing.mobile.R$string.live_detect_failed), p3);
                        return;
                    } else {
                        if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getData().getResult() != 1) {
                            String v4_2;
                            if (!com.fanzhou.util.u.l(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg())) {
                                v4_2 = ((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg();
                            } else {
                                v4_2 = p5.getResources().getString(com.chaoxing.mobile.R$string.face_match_failed);
                            }
                            p2.j(p5, v4_2, p3);
                            return;
                        } else {
                            p2.r(p3, p4);
                            return;
                        }
                    }
                }
            }
        } else {
            return;
        }
    }

    public static synthetic void b(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner p2, java.io.File p3, String p4, android.content.Context p5, com.chaoxing.mobile.office.bean.FaceDataUploadResult p6)
    {
        p2.getClass();
        if (!com.chaoxing.mobile.office.utils.d1.b(p6)) {
            String v4_7 = new StringBuilder();
            v4_7.append(p5.getResources().getString(com.chaoxing.mobile.R$string.upload_face_failed));
            v4_7.append(",\u8bf7\u91cd\u8bd5");
            p2.j(p5, v4_7.toString(), p3);
            return;
        } else {
            if (p6.getUploadStatus() != 1) {
                String v4_4;
                if (!com.fanzhou.util.u.l(p6.getMsg())) {
                    v4_4 = p6.getMsg();
                } else {
                    v4_4 = p5.getResources().getString(com.chaoxing.mobile.R$string.upload_face_failed);
                }
                p2.j(p5, v4_4, p3);
                return;
            } else {
                p2.s(p3, p4);
                return;
            }
        }
    }

    public static synthetic void c(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner p2, android.content.Context p3, java.io.File p4, String p5, qe.b p6)
    {
        p2.getClass();
        if ((!com.chaoxing.mobile.office.utils.d1.b(p6)) || (!p6.f())) {
            if ((!com.chaoxing.mobile.office.utils.d1.b(p6)) || ((!p6.g()) || ((!com.chaoxing.mobile.office.utils.d1.b(p6.c)) || (!com.chaoxing.mobile.office.utils.d1.b(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getData()))))) {
                String v5_2 = new StringBuilder();
                v5_2.append(p3.getResources().getString(com.chaoxing.mobile.R$string.live_detect_failed));
                v5_2.append("\u8bf7\u91cd\u8bd5!");
                p2.j(p3, v5_2.toString(), p4);
                return;
            } else {
                if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getData().getErrorCode() != 0) {
                    String v5_10;
                    if (!com.fanzhou.util.u.l(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg())) {
                        v5_10 = ((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg();
                    } else {
                        String v5_12 = new StringBuilder();
                        v5_12.append(p3.getResources().getString(com.chaoxing.mobile.R$string.live_detect_failed));
                        v5_12.append(",\u8bf7\u91cd\u8bd5");
                        v5_10 = v5_12.toString();
                    }
                    p2.j(p3, v5_10, p4);
                    return;
                } else {
                    if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getData().getVerifyResult() != 1) {
                        String v5_19;
                        if (!com.fanzhou.util.u.l(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg())) {
                            v5_19 = ((com.chaoxing.mobile.office.apiresponse.CommonResponse) p6.c).getMsg();
                        } else {
                            v5_19 = p3.getResources().getString(com.chaoxing.mobile.R$string.live_detect_failed);
                        }
                        p2.j(p3, v5_19, p4);
                        return;
                    } else {
                        p2.y(p3, p4).observe(p2, new com.chaoxing.mobile.office.utils.p(p2, p4, p5, p3));
                        return;
                    }
                }
            }
        } else {
            return;
        }
    }

    public static synthetic void d(android.content.Context p3, com.chaoxing.mobile.office.bean.FaceDataUploadResult p4, androidx.lifecycle.MutableLiveData p5, qe.b p6)
    {
        if ((!com.chaoxing.mobile.office.utils.d1.b(p6)) || (!p6.f())) {
            String v3_1 = p3.getResources().getString(com.chaoxing.mobile.R$string.collect_face_failed_and_retry);
            int v1_0 = 0;
            if ((com.chaoxing.mobile.office.utils.d1.b(p6)) && (p6.g())) {
                if ((com.chaoxing.mobile.office.utils.d1.b(p6.c)) && (((com.fanzhou.loader.Result) p6.c).getStatus() == 1)) {
                    v1_0 = 1;
                }
                if ((com.chaoxing.mobile.office.utils.d1.b(p6.c)) && (!com.fanzhou.util.u.l(((com.fanzhou.loader.Result) p6.c).getMessage()))) {
                    v3_1 = ((com.fanzhou.loader.Result) p6.c).getMessage();
                }
            }
            p4.setUploadStatus(v1_0);
            if (v1_0 != 1) {
                p4.setMsg(v3_1);
            }
            com.chaoxing.android.log.o v6_2 = com.chaoxing.android.log.d.d().u();
            boolean v0_16 = new StringBuilder();
            v0_16.append("updateFace status=");
            v0_16.append(v1_0);
            v0_16.append("msg=");
            v0_16.append(v3_1);
            v6_2.m(v0_16.toString());
            p5.postValue(p4);
            return;
        } else {
            return;
        }
    }

    public static synthetic void e(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner p1, android.view.View p2)
    {
        p1.getClass();
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventEnter(p2);
        if (p2.getId() == com.chaoxing.mobile.R$id.textTv) {
            com.chaoxing.mobile.office.utils.z1.c().b();
            if (com.chaoxing.mobile.office.utils.d1.b(p1.b)) {
                p1.b.m();
            }
        }
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventExit();
        return;
    }

    public static synthetic void f(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner p1, android.content.Context p2, String p3, java.io.File p4)
    {
        p1.getClass();
        com.chaoxing.mobile.office.utils.z1.c().j(p2, p3);
        p1.q(p4);
        return;
    }

    public static synthetic void g(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner p5, android.content.Context p6, qe.b p7)
    {
        p5.getClass();
        if ((!com.chaoxing.mobile.office.utils.d1.b(p7)) || (!p7.f())) {
            if ((!com.chaoxing.mobile.office.utils.d1.b(p7)) || (!p7.g())) {
                if ((com.chaoxing.mobile.office.utils.d1.b(p7)) && (p7.d())) {
                    int v0_4 = p6.getResources();
                    Object[] v1_0 = new Object[1];
                    v1_0[0] = p7.d;
                    p5.j(p6, v0_4.getString(com.chaoxing.mobile.R$string.request_server_error, v1_0), 0);
                }
            } else {
                String v7_4 = ((com.chaoxing.library.data.DataModel) p7.c);
                if ((!com.chaoxing.mobile.office.utils.d1.b(v7_4)) || (v7_4.getResult() != 1)) {
                    if (com.chaoxing.mobile.office.utils.d1.b(v7_4)) {
                        String v7_5;
                        if (!com.fanzhou.util.u.l(v7_4.getErrorMsg())) {
                            v7_5 = v7_4.getErrorMsg();
                        } else {
                            v7_5 = p6.getResources().getString(com.chaoxing.mobile.R$string.not_face_data_and_retry);
                        }
                        p5.j(p6, v7_5, 0);
                    }
                } else {
                    int v0_14 = ((com.chaoxing.mobile.exam.bean.FaceData) v7_4.getData()).getObjectId();
                    p5.d = ((com.chaoxing.mobile.exam.bean.FaceData) v7_4.getData()).getHttp();
                    if (!ve.f.c(v0_14)) {
                        if (com.chaoxing.mobile.office.utils.d1.b(p5.b)) {
                            p5.b.m();
                        }
                    } else {
                        p5.w(p6);
                    }
                }
                com.chaoxing.mobile.office.utils.f v6_5 = com.chaoxing.android.log.d.d().u();
                String v7_12 = new StringBuilder();
                v7_12.append("checkServerFaceId remoteImage=");
                v7_12.append(p5.d);
                v6_5.m(v7_12.toString());
                return;
            }
        }
        return;
    }

    public static synthetic void h(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner p4, android.content.Context p5, androidx.lifecycle.MediatorLiveData p6, Object p7)
    {
        p4.getClass();
        com.chaoxing.mobile.office.bean.FaceDataUploadResult v0_1 = new com.chaoxing.mobile.office.bean.FaceDataUploadResult();
        if ((p7 instanceof com.fanzhou.loader.Result)) {
            if (((com.fanzhou.loader.Result) p7).getStatus() == 1) {
                String v1_1 = ((com.chaoxing.mobile.clouddisk.bean.CloudDiskFile1) ((com.fanzhou.loader.Result) p7).getData());
                if (com.chaoxing.mobile.office.utils.d1.b(v1_1)) {
                    v0_1.setStatus(1);
                    v0_1.setObjectId(v1_1.getObjectId());
                }
            }
            v0_1.setMsg(((com.fanzhou.loader.Result) p7).getMessage());
            String v7_3 = com.chaoxing.android.log.d.d().u();
            String v1_4 = new StringBuilder();
            v1_4.append("uploadFaceData success status=");
            v1_4.append(v0_1.getStatus());
            v1_4.append("objectId=");
            v1_4.append(v0_1.getObjectId());
            v7_3.m(v1_4.toString());
        }
        if (v0_1.getStatus() != 0) {
            String v4_1 = p4.x(p5, p4, v0_1);
            java.util.Objects.requireNonNull(p6);
            p6.addSource(v4_1, new com.chaoxing.mobile.office.utils.j(p6));
            return;
        } else {
            String v4_7;
            String v4_3 = com.chaoxing.android.log.d.d().u();
            String v6_2 = new StringBuilder();
            v6_2.append("uploadFaceData failed status=");
            v6_2.append(v0_1.getStatus());
            v6_2.append("msg=");
            v6_2.append(v0_1.getMsg());
            v4_3.m(v6_2.toString());
            v0_1.setStatus(0);
            if (!com.fanzhou.util.u.l(v0_1.getMsg())) {
                v4_7 = v0_1.getMsg();
            } else {
                v4_7 = p5.getResources().getString(com.chaoxing.mobile.R$string.collect_face_failed_and_retry);
            }
            v0_1.setMsg(v4_7);
            return;
        }
    }

    public void r(java.io.File p4, String p5)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(this.f)) {
            this.f.x2(0, this.c, p5);
        }
        if ((com.chaoxing.mobile.office.utils.d1.b(p4)) && (p4.exists())) {
            p4.delete();
        }
        if (com.chaoxing.mobile.office.utils.d1.b(this.b)) {
            this.b.e();
        }
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public final void j(android.content.Context p3, String p4, java.io.File p5)
    {
        this.e.postDelayed(new com.chaoxing.mobile.office.utils.o(this, p3, p4, p5), 200);
        return;
    }

    public void s(java.io.File p4, String p5)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(this.f)) {
            this.f.x2(1, this.c, p5);
        }
        if ((com.chaoxing.mobile.office.utils.d1.b(p4)) && (p4.exists())) {
            p4.delete();
        }
        if (com.chaoxing.mobile.office.utils.d1.b(this.b)) {
            this.b.e();
        }
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public final androidx.lifecycle.LiveData y(android.content.Context p4, java.io.File p5)
    {
        androidx.lifecycle.MediatorLiveData v0_1 = new androidx.lifecycle.MediatorLiveData();
        com.chaoxing.mobile.clouddisk.upload.c.q().C(this, android.net.Uri.fromFile(p5), new com.chaoxing.mobile.office.utils.n(this, p4, v0_1));
        return v0_1;
    }

    public void q(java.io.File p4)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(this.f)) {
            this.f.j4(0, this.c);
        }
        if ((com.chaoxing.mobile.office.utils.d1.b(p4)) && (p4.exists())) {
            p4.delete();
        }
        if (com.chaoxing.mobile.office.utils.d1.b(this.b)) {
            this.b.e();
        }
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public final void w(android.content.Context p4)
    {
        com.chaoxing.mobile.office.utils.z1.c().f(p4, p4.getResources().getString(com.chaoxing.mobile.R$string.collect_face_hint), new com.chaoxing.mobile.office.utils.m(this));
        return;
    }

    public final androidx.lifecycle.LiveData x(android.content.Context p4, androidx.lifecycle.LifecycleOwner p5, com.chaoxing.mobile.office.bean.FaceDataUploadResult p6)
    {
        androidx.lifecycle.MutableLiveData v0_1 = new androidx.lifecycle.MutableLiveData();
        com.chaoxing.mobile.exam.persistence.a.d().g(p6.getObjectId()).observe(p5, new com.chaoxing.mobile.office.utils.l(p4, p6, v0_1));
        return v0_1;
    }

    public com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner v(boolean p1)
    {
        this.c = p1;
        return this;
    }

    public final void l(android.content.Context p5, java.io.File p6)
    {
        try {
            Throwable v0_3 = okio.s0.e(okio.s0.t(p6));
            try {
                Throwable v1_6 = com.chaoxing.mobile.util.d.b(v0_3.D());
                gl.i.d().b(this.o(v1_6), v1_6).observe(this, new com.chaoxing.mobile.office.utils.i(this, p5, p6, v1_6));
            } catch (Throwable v1_0) {
                if (v0_3 != null) {
                    try {
                        v0_3.close();
                    } catch (Throwable v0_1) {
                        v1_0.addSuppressed(v0_1);
                    }
                }
                throw v1_0;
            }
            v0_3.close();
            return;
        } catch (Throwable v0_2) {
            Throwable v1_2 = new StringBuilder();
            v1_2.append(p5.getResources().getString(com.chaoxing.mobile.R$string.face_verify_error));
            v1_2.append(",");
            v1_2.append(v0_2.getLocalizedMessage());
            this.j(p5, v1_2.toString(), p6);
            com.chaoxing.android.log.d.d().e(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner.g, 0, v0_2);
            return;
        }
    }

    public final void m(android.content.Context p6, java.io.File p7)
    {
        try {
            Throwable v0_3 = okio.s0.e(okio.s0.t(p7));
            try {
                Throwable v1_6 = com.chaoxing.mobile.util.d.b(v0_3.D());
                gl.i.d().c(this.o(v1_6), this.d, v1_6).observe(this, new com.chaoxing.mobile.office.utils.h(this, p7, v1_6, p6));
            } catch (Throwable v1_0) {
                if (v0_3 != null) {
                    try {
                        v0_3.close();
                    } catch (Throwable v0_1) {
                        v1_0.addSuppressed(v0_1);
                    }
                }
                throw v1_0;
            }
            v0_3.close();
            return;
        } catch (Throwable v0_2) {
            Throwable v1_2 = new StringBuilder();
            v1_2.append(p6.getResources().getString(com.chaoxing.mobile.R$string.face_match_error));
            v1_2.append(",");
            v1_2.append(v0_2.getLocalizedMessage());
            this.j(p6, v1_2.toString(), p7);
            com.chaoxing.android.log.d.d().e(com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner.g, 0, v0_2);
            return;
        }
    }

    public androidx.lifecycle.Lifecycle getLifecycle()
    {
        return this.a;
    }

    public void i(android.content.Context p3)
    {
        this.a.markState(androidx.lifecycle.Lifecycle$State.RESUMED);
        com.chaoxing.mobile.exam.persistence.a.d().c(com.chaoxing.study.account.AccountManager.C().D().getPuid()).observe(this, new com.chaoxing.mobile.office.utils.k(this, p3));
        return;
    }

    public void k()
    {
        this.e.removeCallbacksAndMessages(0);
        this.d = 0;
        this.v(0);
        return;
    }

    public void n()
    {
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public void p(android.content.Intent p4, android.content.Context p5, com.chaoxing.mobile.office.viewmodel.PunchViewModel p6)
    {
        java.io.File v4_1;
        java.io.File v4_7 = ((com.chaoxing.mobile.group.bean.JCameraResult) p4.getParcelableExtra("data"));
        if ((!com.chaoxing.mobile.office.utils.d1.b(v4_7)) || (v4_7.getOptMode() != 1)) {
            v4_1 = 0;
            p6.y(0);
            if ((com.chaoxing.mobile.office.utils.d1.b(v4_1)) && (v4_1.exists())) {
                p6.y(1);
                this.a.markState(androidx.lifecycle.Lifecycle$State.RESUMED);
                boolean v6_3 = com.chaoxing.android.log.d.d().u();
                String v0_9 = new StringBuilder();
                v0_9.append("handlerFile remoteImage=");
                v0_9.append(this.d);
                v6_3.m(v0_9.toString());
                if (!com.fanzhou.util.u.l(this.d)) {
                    this.m(p5, v4_1);
                } else {
                    this.l(p5, v4_1);
                    return;
                }
            }
        } else {
            java.io.File v4_2 = v4_7.getImageUris();
            if ((!com.chaoxing.mobile.office.utils.d1.a(v4_2)) && (!v4_2.isEmpty())) {
                v4_1 = this.b.h(p5, ((android.net.Uri) v4_2.get(0)).toString());
            }
        }
        return;
    }

    public com.chaoxing.mobile.office.utils.FaceCaptureRecognitionLifeOwner t(com.chaoxing.mobile.office.utils.f p1)
    {
        this.b = p1;
        return this;
    }

    public void u(com.chaoxing.mobile.office.h0 p1)
    {
        this.f = p1;
        return;
    }
}
