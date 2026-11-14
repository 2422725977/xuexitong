package com.chaoxing.mobile.main;
public class f {
    public androidx.appcompat.app.AppCompatActivity a;
    public androidx.fragment.app.Fragment b;
    public com.chaoxing.study.scan.JumpToScanActivity$e c;
    public android.os.Handler d;
    public com.chaoxing.mobile.resource.p e;

    public static void w(android.content.Context p3, String p4, String p5, String p6)
    {
        android.content.Intent v0_1 = new android.content.Intent(p3, com.chaoxing.mobile.resource.ui.AttentionByScanCodeActivity);
        android.os.Bundle v1_2 = new android.os.Bundle();
        v1_2.putString("uid", p4);
        v1_2.putString("puid", p5);
        v1_2.putString("from", p6);
        v0_1.putExtras(v1_2);
        if (!android.app.Activity.isInstance(p3)) {
            v0_1.addFlags(268435456);
        }
        p3.startActivity(v0_1);
        return;
    }

    public f(androidx.appcompat.app.AppCompatActivity p3)
    {
        this.d = new android.os.Handler(android.os.Looper.getMainLooper());
        this.e = new com.chaoxing.mobile.resource.p();
        this.a = p3;
        return;
    }

    public f(androidx.fragment.app.Fragment p3)
    {
        this.d = new android.os.Handler(android.os.Looper.getMainLooper());
        this.e = new com.chaoxing.mobile.resource.p();
        this.b = p3;
        return;
    }

    public f(com.chaoxing.study.scan.JumpToScanActivity$e p3)
    {
        this.d = new android.os.Handler(android.os.Looper.getMainLooper());
        this.e = new com.chaoxing.mobile.resource.p();
        this.a = p3.a;
        this.c = p3;
        return;
    }

    public static synthetic com.chaoxing.document.Book a(com.chaoxing.mobile.main.f p0, com.chaoxing.document.SsLibraryBook p1)
    {
        return p0.i(p1);
    }

    public static synthetic void b(com.chaoxing.mobile.main.f p0, android.content.Context p1, String p2, String p3, String p4)
    {
        p0.v(p1, p2, p3, p4);
        return;
    }

    public static synthetic com.chaoxing.study.scan.JumpToScanActivity$e c(com.chaoxing.mobile.main.f p0)
    {
        return p0.c;
    }

    public static synthetic void d(com.chaoxing.mobile.main.f p0, android.content.Context p1, String p2, String p3, java.util.List p4)
    {
        p0.x(p1, p2, p3, p4);
        return;
    }

    public static synthetic android.os.Handler e(com.chaoxing.mobile.main.f p0)
    {
        return p0.d;
    }

    public final com.chaoxing.document.Book i(com.chaoxing.document.SsLibraryBook p3)
    {
        com.chaoxing.document.Book v0_1 = new com.chaoxing.document.Book();
        v0_1.setTitle(p3.getBookname());
        v0_1.setSsid(p3.getSsid());
        v0_1.setCover(p3.getCover());
        v0_1.setBook_source(15);
        v0_1.setExtras(ne.a.g(p3));
        v0_1.setBookType(this.h(p3.getType()));
        v0_1.statisticExt = p3.getExt();
        v0_1.pdzUrl = p3.getPath();
        v0_1.bookProtocol = p3.getPath();
        return v0_1;
    }

    public final void v(android.content.Context p4, String p5, String p6, String p7)
    {
        android.content.Intent v0_1 = new android.content.Intent(this.j(), com.chaoxing.fanya.aphone.ui.chapter.detail.ui.ChapterDetailActivity);
        v0_1.putExtra("knowledgeId", p5);
        if (!ve.f.o(p7)) {
            v0_1.putExtra("courseId", p6);
            v0_1.putExtra("comefrom", "watch");
        } else {
            v0_1.putExtra("clazzId", p7);
            v0_1.putExtra("comefrom", "student");
        }
        p4.startActivity(v0_1);
        return;
    }

    public final void x(android.content.Context p8, String p9, String p10, java.util.List p11)
    {
        int v0_1;
        if (!(p8 instanceof android.app.Activity)) {
            v0_1 = 0;
        } else {
            v0_1 = ((android.app.Activity) p8).getWindow().getDecorView();
        }
        if (v0_1 != 0) {
            gg.a v1_1 = new gg.a();
            v1_1.C(p8, this.n(p11), "", 0, new com.chaoxing.mobile.main.f$d(this));
            com.chaoxing.mobile.main.f$e v8_1 = new com.chaoxing.mobile.main.f$e;
            gg.a v6_2 = v1_1;
            v8_1(this, p8, p9, p10, v6_2);
            gg.a v1_3 = v6_2;
            v1_3.x(v8_1);
            v1_3.z(v0_1);
            return;
        } else {
            return;
        }
    }

    public final int h(String p8)
    {
        if (com.fanzhou.util.w.s(p8)) {
            return 1;
        } else {
            p8.getClass();
            int v6 = -1;
            switch (p8.hashCode()) {
                case 110834:
                    if (p8.equals("pdf")) {
                        v6 = 0;
                    } else {
                    }
                case 110854:
                    if (p8.equals("pdz")) {
                        v6 = 1;
                    } else {
                    }
                    break;
                case 110925:
                    if (p8.equals("pgd")) {
                        v6 = 2;
                    } else {
                    }
                    break;
                case 115312:
                    if (p8.equals("txt")) {
                        v6 = 3;
                    } else {
                    }
                    break;
                case 3436594:
                    if (p8.equals("pdzx")) {
                        v6 = 4;
                    } else {
                    }
                    break;
                default:
            }
            switch (v6) {
                case 0:
                    return 2;
                case 1:
                    return 0;
                case 2:
                    return 3;
                case 3:
                    return 4;
                case 4:
                    return 5;
                default:
                    return 1;
            }
        }
    }

    public final Object l()
    {
        int v0_0 = this.a;
        if (v0_0 == 0) {
            int v0_1 = this.b;
            if (v0_1 == 0) {
                return 0;
            } else {
                return v0_1;
            }
        } else {
            return v0_0;
        }
    }

    public final android.content.Context j()
    {
        int v0_0 = this.l();
        if (!(v0_0 instanceof android.app.Activity)) {
            if (!(v0_0 instanceof androidx.fragment.app.Fragment)) {
                if (!(v0_0 instanceof android.app.Fragment)) {
                    return 0;
                } else {
                    return ((android.app.Fragment) v0_0).getActivity();
                }
            } else {
                return ((androidx.fragment.app.Fragment) v0_0).getContext();
            }
        } else {
            return ((android.app.Activity) v0_0);
        }
    }

    public final void f(String p2)
    {
        w9.f.l(p2).d().a().a().d(new com.chaoxing.mobile.main.f$b(this)).observeForever(new com.chaoxing.mobile.main.f$a(this));
        return;
    }

    public final void y(Object p2, android.content.Intent p3)
    {
        if (!(p2 instanceof android.app.Activity)) {
            if (!(p2 instanceof androidx.fragment.app.Fragment)) {
                if ((p2 instanceof android.app.Fragment)) {
                    ((android.app.Fragment) p2).startActivity(p3);
                }
                return;
            } else {
                ((androidx.fragment.app.Fragment) p2).startActivity(p3);
                return;
            }
        } else {
            ((android.app.Activity) p2).startActivity(p3);
            return;
        }
    }

    public final boolean u(android.content.Context p1)
    {
        if (!com.chaoxing.study.account.AccountManager.C().Z()) {
            return 0;
        } else {
            com.chaoxing.study.account.AccountManager.C().L0();
            return 1;
        }
    }

    public final java.util.HashMap r(String p11)
    {
        if (!com.fanzhou.util.w.q(p11)) {
            java.util.HashMap v0_2 = new java.util.HashMap();
            Exception v11_2 = p11.substring((p11.indexOf("?") + 1)).split("&");
            int v2_1 = v11_2.length;
            int v4 = 0;
            while (v4 < v2_1) {
                Exception v8_0;
                String v5_0 = v11_2[v4];
                int v6_1 = v5_0.indexOf("=");
                if (v6_1 <= 0) {
                    v8_0 = v5_0;
                } else {
                    v8_0 = java.net.URLDecoder.decode(v5_0.substring(0, v6_1), "UTF-8");
                }
                String v5_1;
                if (v6_1 <= 0) {
                    v5_1 = 0;
                } else {
                    int v6_2 = (v6_1 + 1);
                    if (v5_0.length() <= v6_2) {
                    } else {
                        v5_1 = java.net.URLDecoder.decode(v5_0.substring(v6_2), "UTF-8");
                    }
                }
                v0_2.put(v8_0, v5_1);
                v4++;
            }
            return v0_2;
        } else {
            return 0;
        }
    }

    public final int p(java.util.HashMap p3)
    {
        if ((p3 == 0) || ((p3.size() == 0) || (!p3.containsKey("_type")))) {
            return -50;
        } else {
            return Integer.parseInt(((String) p3.get("_type")));
        }
    }

    public final String m(java.util.HashMap p3)
    {
        if ((p3 == null) || ((p3.size() == 0) || (!p3.containsKey("inviteCode")))) {
            return 0;
        } else {
            return ((String) p3.get("inviteCode"));
        }
    }

    public final String[] q(java.util.HashMap p5)
    {
        String[] v0 = 0;
        if ((p5 != null) && ((p5.size() != 0) && (p5.containsKey("params")))) {
            String[] v2_0 = new String[2];
            try {
                int v1_2 = new org.json.JSONObject(java.net.URLDecoder.decode(((String) p5.get("params")), "UTF-8"));
                v2_0[0] = v1_2.optString("uid");
                v2_0[1] = v1_2.optString("puid");
            } catch (org.json.JSONException v5_8) {
                v5_8.printStackTrace();
            } catch (Exception) {
            }
            v0 = v2_0;
        }
        return v0;
    }

    public final String k(java.util.HashMap p3)
    {
        if ((p3 == null) || (!p3.containsKey("courseId"))) {
            return 0;
        } else {
            return ((String) p3.get("courseId"));
        }
    }

    public final String o(java.util.HashMap p3)
    {
        if ((p3 == null) || (!p3.containsKey("knowledgeId"))) {
            return 0;
        } else {
            return ((String) p3.get("knowledgeId"));
        }
    }

    public final void g(android.content.Context p7, String p8, String p9)
    {
        com.chaoxing.mobile.main.f$c v0_0 = hc.a.g2();
        com.fanzhou.loader.DataLoadThread v1_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        Object[] v2_1 = new Object[3];
        v2_1[0] = p8;
        v2_1[1] = "";
        v2_1[2] = v1_4;
        com.fanzhou.loader.DataLoadThread v1_1 = new com.fanzhou.loader.DataLoadThread(p7, 0, String.format(v0_0, v2_1));
        v1_1.setOnCompleteListener(new com.chaoxing.mobile.main.f$c(this, p7, p9, p8));
        com.chaoxing.study.scan.JumpToScanActivity$e v7_1 = this.c;
        if (v7_1 != null) {
            v7_1.c();
        }
        v1_1.loadData();
        return;
    }

    public final boolean t(android.net.Uri p2)
    {
        int v2_1 = p2.getHost();
        if ((!v2_1.contains("p.ananas.chaoxing.com")) && (!v2_1.contains("p.cldisk.com"))) {
            return 0;
        } else {
            return 1;
        }
    }

    public final void z(Object p2, android.content.Intent p3, int p4)
    {
        if (!(p2 instanceof android.app.Activity)) {
            if (!(p2 instanceof androidx.fragment.app.Fragment)) {
                if ((p2 instanceof android.app.Fragment)) {
                    ((android.app.Fragment) p2).startActivityForResult(p3, p4);
                }
                return;
            } else {
                ((androidx.fragment.app.Fragment) p2).startActivityForResult(p3, p4);
                return;
            }
        } else {
            ((android.app.Activity) p2).startActivityForResult(p3, p4);
            return;
        }
    }

    public final java.util.List n(java.util.List p5)
    {
        java.util.ArrayList v0_1 = new java.util.ArrayList();
        java.util.Iterator v5_1 = p5.iterator();
        while (v5_1.hasNext()) {
            String v1_0 = ((com.chaoxing.fanya.common.model.Clazz) v5_1.next());
            com.chaoxing.mobile.common.view.BottomItem v2_1 = new com.chaoxing.mobile.common.view.BottomItem();
            v2_1.setOption(v1_0.id);
            v2_1.setTitle(v1_0.name);
            v0_1.add(v2_1);
        }
        return v0_1;
    }

    public void s(String p12)
    {
        if ((p12 != null) && (this.j() != null)) {
            String v4_5 = new android.content.Intent(this.j(), com.chaoxing.mobile.scan.CaptureISBNLoading);
            v4_5.putExtra("CaptureIsbn", p12);
            if (!p12.contains("BORROWMACHINE:")) {
                if (!p12.contains("GEDE:")) {
                    if (!p12.contains("QRMARK=SSLIBRARY")) {
                        if (!p12.startsWith("GROUP:")) {
                            if (!p12.startsWith("userInfoQR:")) {
                                if (!p12.startsWith("userInviteCodeQR:")) {
                                    if (!p12.startsWith("SIGNIN:")) {
                                        if (!p12.startsWith("seatQR:")) {
                                            if (!p12.startsWith("https://weixin.qq.com/q")) {
                                                if (!p12.startsWith("https://weixin.qq.com/q")) {
                                                    if (!p12.startsWith("INTELLIGENT_CLASSROOM:")) {
                                                        if (!com.fanzhou.util.o.f(p12)) {
                                                            if (!com.fanzhou.util.o.e(p12)) {
                                                                if (!com.fanzhou.util.o.b(p12)) {
                                                                    android.content.Context v0_56 = new android.content.Intent(this.j(), com.chaoxing.study.scan.ScanResultActivity);
                                                                    v0_56.putExtra("result", p12);
                                                                    this.j().startActivity(v0_56);
                                                                    return;
                                                                } else {
                                                                    android.content.Context v0_58 = new com.chaoxing.mobile.app.AppInfo();
                                                                    v0_58.setCataId("100000009");
                                                                    v0_58.setAppId(this.j().getString(com.chaoxing.mobile.R$string.site_id_scan));
                                                                    v0_58.setResourceType(0);
                                                                    v0_58.setAvailable(1);
                                                                    v0_58.setNeedLogin(1);
                                                                    v0_58.setLoginId(1);
                                                                    v0_58.setDescription(p12);
                                                                    v0_58.setAid(p12);
                                                                    java.util.ArrayList v12_38 = this.e;
                                                                    if (v12_38 == null) {
                                                                        return;
                                                                    } else {
                                                                        v12_38.i(this.j(), this.a, com.chaoxing.mobile.resource.ResourceClassBridge.a(v0_58));
                                                                        return;
                                                                    }
                                                                }
                                                            } else {
                                                            }
                                                        }
                                                        android.content.Context v0_2 = android.net.Uri.parse(p12);
                                                        java.util.ArrayList v2_1 = v0_2.getScheme();
                                                        if ((!"https".equalsIgnoreCase(v2_1)) && ((!"http".equalsIgnoreCase(v2_1)) && (!"ftp".equalsIgnoreCase(v2_1)))) {
                                                            try {
                                                                android.content.Context v0_4 = new android.content.Intent();
                                                                v0_4.setData(android.net.Uri.parse(p12));
                                                                v0_4.setAction("android.intent.action.VIEW");
                                                                v0_4.setFlags(268435456);
                                                                this.j().startActivity(v0_4);
                                                            } catch (android.content.Context v0_5) {
                                                                v0_5.printStackTrace();
                                                                com.chaoxing.mobile.study.util.c.c(this.j(), 0, p12);
                                                            }
                                                            return;
                                                        } else {
                                                            java.util.ArrayList v2_3 = this.r(p12);
                                                            String v4_6 = this.p(v2_3);
                                                            String v9 = this.m(v2_3);
                                                            if ((v4_6 != 1) || (com.fanzhou.util.w.q(v9))) {
                                                                if (v4_6 != 3) {
                                                                    if ((!this.t(v0_2)) || (!com.fanzhou.util.o.c(v0_2.toString()))) {
                                                                        android.content.Context v0_8 = new com.chaoxing.mobile.webapp.WebViewerParams();
                                                                        v0_8.setUseClientTool(1);
                                                                        v0_8.setUrl(p12);
                                                                        java.util.ArrayList v12_2 = new android.content.Intent(this.j(), com.chaoxing.mobile.webapp.ui.WebAppViewerActivity);
                                                                        v12_2.putExtra("webViewerParams", v0_8);
                                                                        this.y(this.l(), v12_2);
                                                                        return;
                                                                    } else {
                                                                        java.util.ArrayList v12_4 = new java.util.ArrayList();
                                                                        v12_4.add(v0_2.toString());
                                                                        com.chaoxing.mobile.group.ui.TopicImageViewerActivity.F5(this.j(), v12_4, 0, 1);
                                                                        return;
                                                                    }
                                                                } else {
                                                                    if (!this.u(this.j())) {
                                                                        this.g(this.j(), this.k(v2_3), this.o(v2_3));
                                                                        return;
                                                                    } else {
                                                                        return;
                                                                    }
                                                                }
                                                            } else {
                                                                if (!this.u(this.j())) {
                                                                    java.util.ArrayList v12_10 = this.q(v2_3);
                                                                    if ((v12_10 == null) || ((com.fanzhou.util.w.q(v12_10[0])) && (com.fanzhou.util.w.q(v12_10[1])))) {
                                                                        java.util.ArrayList v12_12 = new android.content.Intent(this.j(), com.chaoxing.mobile.resource.ui.ValidateUserCodeActivity);
                                                                        android.content.Context v0_19 = new android.os.Bundle();
                                                                        v0_19.putString("inviteCode", v9);
                                                                        v12_12.putExtra("args", v0_19);
                                                                        this.y(this.l(), v12_12);
                                                                        return;
                                                                    } else {
                                                                        com.chaoxing.mobile.main.f.w(this.j(), v12_10[0], v12_10[1], "scan");
                                                                        return;
                                                                    }
                                                                } else {
                                                                    return;
                                                                }
                                                            }
                                                        }
                                                    } else {
                                                        java.util.ArrayList v12_14 = p12.substring(22);
                                                        if (!com.fanzhou.util.w.q(v12_14)) {
                                                            java.util.ArrayList v12_16 = ((com.chaoxing.mobile.intelligentclassroom.bean.ScanInfo) ne.a.b(v12_14, com.chaoxing.mobile.intelligentclassroom.bean.ScanInfo));
                                                            if ((v12_16 != null) && (!v12_16.isStrictEmpty())) {
                                                                if (!v12_16.isEmpty()) {
                                                                    android.content.Context v0_28 = new android.content.Intent(this.j(), com.chaoxing.mobile.intelligentclassroom.ConfirmScreenActivity);
                                                                    v0_28.putExtra("scan_info", v12_16);
                                                                    this.y(this.l(), v0_28);
                                                                    return;
                                                                } else {
                                                                }
                                                            }
                                                            com.chaoxing.android.widget.a.j(this.j(), com.chaoxing.mobile.R$string.scan_error).s();
                                                            return;
                                                        } else {
                                                            com.chaoxing.android.widget.a.j(this.j(), com.chaoxing.mobile.R$string.scan_error).s();
                                                            return;
                                                        }
                                                    }
                                                } else {
                                                }
                                            }
                                            android.content.Context v0_32 = new android.content.Intent(this.j(), com.chaoxing.mobile.main.ui.ScanQrCodeMiddleActivity);
                                            String v1_13 = new android.os.Bundle();
                                            v1_13.putString("codeUrl", p12);
                                            v0_32.putExtras(v1_13);
                                            this.y(this.l(), v0_32);
                                            return;
                                        } else {
                                            java.util.ArrayList v12_23 = p12.replace("seatQR:", "");
                                            android.content.Context v0_34 = new android.content.Intent(this.j(), com.chaoxing.reserveseat.ui.QRcodeVerifyActivity);
                                            String v1_16 = new android.os.Bundle();
                                            v1_16.putString("codeInfo", v12_23);
                                            v0_34.putExtra("args", v1_16);
                                            this.y(this.l(), v0_34);
                                            return;
                                        }
                                    } else {
                                        try {
                                            android.content.Context v0_36 = new com.chaoxing.mobile.webapp.WebViewerParams();
                                            java.util.ArrayList v12_26 = com.chaoxing.mobile.s.I7(java.net.URLEncoder.encode(p12, "utf-8"), com.chaoxing.study.account.AccountManager.C().D().getPuid());
                                            v0_36.setUseClientTool(0);
                                            v0_36.setToolbarType(2);
                                            v0_36.setUrl(v12_26);
                                            java.util.ArrayList v12_28 = new android.content.Intent(this.j(), com.chaoxing.mobile.webapp.ui.WebAppCommonViewer);
                                            v12_28.putExtra("webViewerParams", v0_36);
                                            this.y(this.l(), v12_28);
                                        } catch (java.util.ArrayList v12_29) {
                                            v12_29.printStackTrace();
                                        }
                                        return;
                                    }
                                } else {
                                    if (!this.u(this.j())) {
                                        java.util.ArrayList v12_30 = p12.substring(17);
                                        android.content.Context v0_42 = new android.content.Intent(this.j(), com.chaoxing.mobile.resource.ui.ValidateUserCodeActivity);
                                        String v1_25 = new android.os.Bundle();
                                        v1_25.putString("inviteCode", v12_30);
                                        v0_42.putExtra("args", v1_25);
                                        this.y(this.l(), v0_42);
                                        return;
                                    } else {
                                        return;
                                    }
                                }
                            } else {
                                if (!this.u(this.j())) {
                                    ak.k.b(this.j(), p12.replace("userInfoQR:", ""));
                                    return;
                                } else {
                                    return;
                                }
                            }
                        } else {
                            android.content.Context v0_47 = new android.content.Intent(this.j(), com.chaoxing.mobile.group.ui.AddGroupByQRCodeActivity);
                            v0_47.putExtra("CaptureIsbn", p12);
                            this.y(this.l(), v0_47);
                            return;
                        }
                    } else {
                        this.f(p12);
                        return;
                    }
                } else {
                }
            }
            this.z(this.l(), v4_5, 993);
            java.util.ArrayList v12_35 = this.c;
            if (v12_35 != null) {
                v12_35.c();
                return;
            }
        }
        return;
    }
}
