package com.chaoxing.mobile.office.utils;
public class FaceMatchClientRWWebPunchChecker implements androidx.lifecycle.LifecycleOwner {
    public static final String g = "FaceMatchClientRWWebPunchChecker";
    public static final int h = 200;
    public final androidx.lifecycle.LifecycleRegistry a;
    public com.chaoxing.mobile.office.i0 b;
    public String c;
    public int d;
    public com.chaoxing.mobile.office.utils.f e;
    public final android.os.Handler f;

    private void v(android.content.Context p7)
    {
        com.chaoxing.mobile.office.utils.z1.c().h(p7, p7.getResources().getString(com.chaoxing.mobile.R$string.collect_face_hint), 1, new com.chaoxing.mobile.office.utils.i0(this), new com.chaoxing.mobile.office.utils.j0(this));
        return;
    }

    private void r(android.content.Context p8, String p9, com.chaoxing.facedetection.bean.FaceInfo p10)
    {
        com.chaoxing.facedetection.bean.CollectConfig v4_1 = new com.chaoxing.facedetection.bean.CollectConfig();
        v4_1.setCollectType(2);
        v4_1.setCollectTimeoutType(1);
        v4_1.setSupportOpenUpload(0);
        com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker v2_0 = com.chaoxing.android.log.d.d().u();
        Class v3_1 = new StringBuilder();
        v3_1.append("openFaceImageCollector mFaceMatchActionNum=");
        v3_1.append(this.d);
        v2_0.m(v3_1.toString());
        if (this.d <= 0) {
            this.d = 2;
        }
        if (this.d > 4) {
            this.d = 4;
        }
        v4_1.setCollectStep(this.d);
        v4_1.setModel(0);
        com.chaoxing.facedetection.FaceCollector.g().d(p8, this, com.chaoxing.facedetection.compat.FaceDetectorCompatActivity, v4_1, new com.chaoxing.mobile.office.utils.h0(this, p8), new com.chaoxing.mobile.office.FaceMatchImageUploader(2, p9, p10));
        return;
    }

    private void l(android.content.Context p6, java.io.File p7)
    {
        try {
            Throwable v0_4 = okio.s0.e(okio.s0.t(p7));
            try {
                String v1_4 = com.chaoxing.mobile.util.d.b(v0_4.D());
                gl.i.d().c(this.n(v1_4), this.c, v1_4).observe(this, new com.chaoxing.mobile.office.utils.l0(this, p7, p6));
            } catch (Throwable v7_1) {
                if (v0_4 != null) {
                    try {
                        v0_4.close();
                    } catch (Throwable v0_1) {
                        v7_1.addSuppressed(v0_1);
                    }
                }
                throw v7_1;
            }
            v0_4.close();
            return;
        } catch (Throwable v7_2) {
            Throwable v0_3 = new StringBuilder();
            v0_3.append(p6.getResources().getString(com.chaoxing.mobile.R$string.face_match_error));
            v0_3.append(",");
            v0_3.append(v7_2.getLocalizedMessage());
            this.p(0, v0_3.toString());
            com.chaoxing.android.log.d.d().e("FaceMatchClientRWWebPunchChecker", 0, v7_2);
            return;
        }
    }

    private void i(android.content.Context p1, String p2, String p3, java.io.File p4)
    {
        this.f.postDelayed(new com.chaoxing.mobile.office.utils.k0(this, p3, p4), 200);
        return;
    }

    private com.chaoxing.mobile.office.bean.ASQueryParams n(String p5)
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
        if (com.fanzhou.util.u.l(this.c)) {
            v5_3 = "";
        } else {
            v5_3 = "[remoteImage=";
        }
        String v5_6;
        v1_4.append(v5_3);
        if (com.fanzhou.util.u.l(this.c)) {
            v5_6 = "";
        } else {
            v5_6 = this.c;
        }
        v1_4.append(v5_6);
        if (!com.fanzhou.util.u.l(this.c)) {
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

    public FaceMatchClientRWWebPunchChecker()
    {
        androidx.lifecycle.LifecycleRegistry v0_1 = new androidx.lifecycle.LifecycleRegistry(this);
        this.a = v0_1;
        this.f = new android.os.Handler(android.os.Looper.getMainLooper());
        v0_1.markState(androidx.lifecycle.Lifecycle$State.CREATED);
        v0_1.addObserver(new com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker$1(this));
        return;
    }

    public static synthetic void a(com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker p3, android.content.Context p4, qe.b p5)
    {
        p3.getClass();
        if ((!com.chaoxing.mobile.office.utils.d1.b(p5)) || (!p5.f())) {
            if ((!com.chaoxing.mobile.office.utils.d1.b(p5)) || (!p5.g())) {
                if ((com.chaoxing.mobile.office.utils.d1.b(p5)) && (p5.d())) {
                    String v4_1 = p4.getResources();
                    Object[] v2_1 = new Object[1];
                    v2_1[0] = p5.d;
                    p3.j(v4_1.getString(com.chaoxing.mobile.R$string.request_server_error, v2_1));
                }
            } else {
                int v5_3 = ((com.chaoxing.library.data.DataModel) p5.c);
                if ((!com.chaoxing.mobile.office.utils.d1.b(v5_3)) || (v5_3.getResult() != 1)) {
                    if (com.chaoxing.mobile.office.utils.d1.b(v5_3)) {
                        String v4_3;
                        if (!com.fanzhou.util.u.l(v5_3.getErrorMsg())) {
                            v4_3 = v5_3.getErrorMsg();
                        } else {
                            v4_3 = p4.getResources().getString(com.chaoxing.mobile.R$string.not_face_data_and_retry);
                        }
                        p3.j(v4_3);
                    }
                } else {
                    String v0_13 = ((com.chaoxing.mobile.exam.bean.FaceData) v5_3.getData()).getObjectId();
                    p3.c = ((com.chaoxing.mobile.exam.bean.FaceData) v5_3.getData()).getHttp();
                    if (!ve.f.c(v0_13)) {
                        int v5_10 = new com.chaoxing.facedetection.bean.FaceInfo();
                        v5_10.setOpenUpload(0);
                        p3 = p3.r(p4, p3.c, v5_10);
                    } else {
                        p3 = p3.v(p4);
                    }
                }
                String v4_6 = com.chaoxing.android.log.d.d().u();
                int v5_12 = new StringBuilder();
                v5_12.append("checkServerFaceId remoteImage=");
                v5_12.append(p3.c);
                v4_6.m(v5_12.toString());
                return;
            }
        }
        return;
    }

    public static synthetic void b(com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker p2, String p3, java.io.File p4)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(p2.b)) {
            p2.b.f(0, p3);
        }
        p2.o(p4, p3);
        p2.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public static synthetic void c(com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker p4, android.content.Context p5, com.chaoxing.facedetection.CollectResult p6)
    {
        p4.getClass();
        if (p6.getLiveDetectionStatus() != -3) {
            boolean v0_0;
            if (com.fanzhou.util.u.l(p6.getImagePath())) {
                v0_0 = 0;
            } else {
                v0_0 = new java.io.File(p6.getImagePath());
            }
            if (!v0_0) {
                int v1_2 = p5.getResources().getString(com.chaoxing.mobile.R$string.rw_face_collect_failed);
                if (com.chaoxing.mobile.office.utils.d1.b(p6.getUploadResult())) {
                    v1_2 = p6.getUploadResult().getRawData();
                }
                p4.p(0, v1_2);
            }
            if ((!com.chaoxing.mobile.office.utils.d1.b(p6.getUploadResult())) || (p6.getUploadResult().getStatus() != 1)) {
                String v5_2 = p5.getResources().getString(com.chaoxing.mobile.R$string.face_match_failed);
                if (com.chaoxing.mobile.office.utils.d1.b(p6.getUploadResult())) {
                    v5_2 = p6.getUploadResult().getRawData();
                }
                p4.p(0, v5_2);
                return;
            } else {
                p4.l(p5, v0_0);
                return;
            }
        } else {
            String v5_6;
            if (!com.fanzhou.util.u.l(p4.c)) {
                v5_6 = "\u7528\u6237\u53d6\u6d88\u4eba\u8138\u8bc6\u522b";
            } else {
                v5_6 = "\u7528\u6237\u672a\u8fdb\u884c\u5f55\u5165\u4eba\u8138";
            }
            p4.p(0, v5_6);
            return;
        }
    }

    public static synthetic void d(com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker p1, android.view.View p2)
    {
        p1.getClass();
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventEnter(p2);
        if (p2.getId() == com.chaoxing.mobile.R$id.cancelTv) {
            String v2_1;
            if (!com.fanzhou.util.w.q(p1.c)) {
                v2_1 = "\u7528\u6237\u53d6\u6d88\u4eba\u8138\u8bc6\u522b";
            } else {
                v2_1 = "\u7528\u6237\u672a\u8fdb\u884c\u5f55\u5165\u4eba\u8138";
            }
            p1.p(0, v2_1);
            com.chaoxing.mobile.office.utils.z1.c().b();
        }
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventExit();
        return;
    }

    public static synthetic void e(com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker p1, String p2)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(p1.b)) {
            p1.b.g(p2);
        }
        p1.p(0, p2);
        p1.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public static synthetic void f(com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker p2, java.io.File p3, android.content.Context p4, qe.b p5)
    {
        p2.getClass();
        if ((!com.chaoxing.mobile.office.utils.d1.b(p5)) || (!p5.f())) {
            if ((!com.chaoxing.mobile.office.utils.d1.b(p5)) || ((!com.chaoxing.mobile.office.utils.d1.b(p5.c)) || (!com.chaoxing.mobile.office.utils.d1.b(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getData())))) {
                String v3_2 = new StringBuilder();
                v3_2.append(p4.getResources().getString(com.chaoxing.mobile.R$string.face_match_failed));
                v3_2.append("\u8bf7\u91cd\u8bd5!");
                p2.p(0, v3_2.toString());
                return;
            } else {
                if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getData().getErrorCode() != 0) {
                    String v3_10;
                    if (!com.fanzhou.util.u.l(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getMsg())) {
                        v3_10 = ((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getMsg();
                    } else {
                        String v3_12 = new StringBuilder();
                        v3_12.append(p4.getResources().getString(com.chaoxing.mobile.R$string.face_match_failed));
                        v3_12.append(",\u8bf7\u91cd\u8bd5");
                        v3_10 = v3_12.toString();
                    }
                    p2.p(0, v3_10);
                    return;
                } else {
                    if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getData().getVerifyResult() != 1) {
                        p2.i(p4, p4.getResources().getString(com.chaoxing.mobile.R$string.live_detect_failed), mw.d.a().D(p5.c), p3);
                        return;
                    } else {
                        if (((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getData().getResult() != 1) {
                            String v0_3;
                            if (!com.fanzhou.util.u.l(((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getMsg())) {
                                v0_3 = ((com.chaoxing.mobile.office.apiresponse.CommonResponse) p5.c).getMsg();
                            } else {
                                v0_3 = p4.getResources().getString(com.chaoxing.mobile.R$string.face_match_failed);
                            }
                            p2.i(p4, v0_3, mw.d.a().D(p5.c), p3);
                            return;
                        } else {
                            p2.q(p3, mw.d.a().D(p5.c));
                            return;
                        }
                    }
                }
            }
        } else {
            return;
        }
    }

    public static synthetic void g(com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker p1, android.view.View p2)
    {
        p1.getClass();
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventEnter(p2);
        if (p2.getId() == com.chaoxing.mobile.R$id.textTv) {
            com.chaoxing.mobile.office.utils.z1.c().b();
            if (com.chaoxing.mobile.office.utils.d1.b(p1.e)) {
                p1.e.m();
            }
        }
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventExit();
        return;
    }

    public final void j(String p5)
    {
        this.f.postDelayed(new com.chaoxing.mobile.office.utils.m0(this, p5), 200);
        return;
    }

    public void o(java.io.File p3, String p4)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(this.b)) {
            this.b.f(0, p4);
        }
        if ((com.chaoxing.mobile.office.utils.d1.b(p3)) && (p3.exists())) {
            p3.delete();
        }
        if (com.chaoxing.mobile.office.utils.d1.b(this.e)) {
            this.e.e();
        }
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public void p(java.io.File p2, String p3)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(this.b)) {
            this.b.g(p3);
        }
        if ((com.chaoxing.mobile.office.utils.d1.b(p2)) && (p2.exists())) {
            p2.delete();
        }
        if (com.chaoxing.mobile.office.utils.d1.b(this.e)) {
            this.e.e();
        }
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public void q(java.io.File p3, String p4)
    {
        if (com.chaoxing.mobile.office.utils.d1.b(this.b)) {
            this.b.d(0, p4);
        }
        if ((com.chaoxing.mobile.office.utils.d1.b(p3)) && (p3.exists())) {
            p3.delete();
        }
        if (com.chaoxing.mobile.office.utils.d1.b(this.e)) {
            this.e.e();
        }
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public androidx.lifecycle.Lifecycle getLifecycle()
    {
        return this.a;
    }

    public void h(android.content.Context p3)
    {
        this.a.markState(androidx.lifecycle.Lifecycle$State.RESUMED);
        com.chaoxing.mobile.exam.persistence.a.d().c(com.chaoxing.study.account.AccountManager.C().D().getPuid()).observe(this, new com.chaoxing.mobile.office.utils.n0(this, p3));
        return;
    }

    public void k()
    {
        com.chaoxing.mobile.office.utils.z1.c().b();
        this.c = 0;
        this.f.removeCallbacksAndMessages(0);
        return;
    }

    public void m()
    {
        this.a.markState(androidx.lifecycle.Lifecycle$State.DESTROYED);
        return;
    }

    public com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker s(int p1)
    {
        this.d = p1;
        return this;
    }

    public void t(com.chaoxing.mobile.office.i0 p1)
    {
        this.b = p1;
        return;
    }

    public com.chaoxing.mobile.office.utils.FaceMatchClientRWWebPunchChecker u(com.chaoxing.mobile.office.utils.f p1)
    {
        this.e = p1;
        return this;
    }
}
