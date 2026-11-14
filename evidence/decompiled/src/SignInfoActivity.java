package com.chaoxing.mobile.sign.ui;
public class SignInfoActivity extends com.chaoxing.core.DefaultActivity {
    public static final int B = 51721;
    public android.os.Handler A;
    public android.content.Context a;
    public String b;
    public String c;
    public String d;
    public String e;
    public com.android.volley.RequestQueue f;
    public android.widget.LinearLayout g;
    public android.widget.LinearLayout h;
    public android.widget.LinearLayout i;
    public android.widget.LinearLayout j;
    public android.widget.LinearLayout k;
    public String l;
    public String m;
    public String n;
    public String o;
    public String p;
    public int q;
    public android.widget.TextView r;
    public android.widget.TextView s;
    public android.widget.TextView t;
    public android.widget.TextView u;
    public android.widget.TextView v;
    public android.widget.Button w;
    public android.widget.Button x;
    public android.widget.TextView y;
    public androidx.activity.result.ActivityResultLauncher z;

    private void o5()
    {
        this.z.launch(0);
        return;
    }

    private void initView()
    {
        this.f = com.android.volley.toolbox.Volley.newRequestQueue(this.a);
        this.u = ((android.widget.TextView) this.findViewById(com.chaoxing.mobile.R$id.sign_course));
        this.r = ((android.widget.TextView) this.findViewById(com.chaoxing.mobile.R$id.sign_time));
        this.s = ((android.widget.TextView) this.findViewById(com.chaoxing.mobile.R$id.sign_user));
        this.t = ((android.widget.TextView) this.findViewById(com.chaoxing.mobile.R$id.sign_tea));
        this.v = ((android.widget.TextView) this.findViewById(com.chaoxing.mobile.R$id.sign_fail_msg));
        this.w = ((android.widget.Button) this.findViewById(com.chaoxing.mobile.R$id.bt_again));
        android.widget.TextView v0_18 = ((android.widget.Button) this.findViewById(com.chaoxing.mobile.R$id.btnBack));
        this.x = v0_18;
        v0_18.setOnClickListener(new com.chaoxing.mobile.sign.ui.SignInfoActivity$e(this));
        this.g = ((android.widget.LinearLayout) this.findViewById(com.chaoxing.mobile.R$id.sign_success));
        this.h = ((android.widget.LinearLayout) this.findViewById(com.chaoxing.mobile.R$id.sign_false));
        this.i = ((android.widget.LinearLayout) this.findViewById(com.chaoxing.mobile.R$id.sign_loading));
        this.g.setVisibility(8);
        this.h.setVisibility(8);
        this.k = ((android.widget.LinearLayout) this.findViewById(com.chaoxing.mobile.R$id.ll_course));
        this.j = ((android.widget.LinearLayout) this.findViewById(com.chaoxing.mobile.R$id.ll_teacher));
        this.y = ((android.widget.TextView) this.findViewById(com.chaoxing.mobile.R$id.tv_message));
        return;
    }

    public SignInfoActivity()
    {
        this.p = "";
        this.A = new com.chaoxing.mobile.sign.ui.SignInfoActivity$c(this);
        return;
    }

    public static synthetic void R4(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, String p1)
    {
        p0.j5(p1);
        return;
    }

    public static synthetic int U4(com.chaoxing.mobile.sign.ui.SignInfoActivity p0)
    {
        return p0.q;
    }

    public static synthetic android.os.Handler V4(com.chaoxing.mobile.sign.ui.SignInfoActivity p0)
    {
        return p0.A;
    }

    public static synthetic int X4(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, int p1)
    {
        p0.q = p1;
        return p1;
    }

    public static synthetic void Y4(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, boolean p1, String p2)
    {
        p0.t5(p1, p2);
        return;
    }

    public static synthetic String b5(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, String p1)
    {
        p0.p = p1;
        return p1;
    }

    public static synthetic String c5(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, String p1)
    {
        p0.l = p1;
        return p1;
    }

    public static synthetic String d5(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, String p1)
    {
        p0.m = p1;
        return p1;
    }

    public static synthetic String f5(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, String p1)
    {
        p0.n = p1;
        return p1;
    }

    public static synthetic String g5(com.chaoxing.mobile.sign.ui.SignInfoActivity p0, String p1)
    {
        p0.o = p1;
        return p1;
    }

    public static synthetic android.content.Context h5(com.chaoxing.mobile.sign.ui.SignInfoActivity p0)
    {
        return p0.a;
    }

    public static synthetic void i5(com.chaoxing.mobile.sign.ui.SignInfoActivity p0)
    {
        p0.o5();
        return;
    }

    public final void j5(String p4)
    {
        String v0_0 = com.chaoxing.android.log.d.d();
        String v1_1 = new StringBuilder();
        v1_1.append("userId==");
        v1_1.append(this.d);
        v0_0.D(v1_1.toString());
        String v0_1 = this.d;
        if ((v0_1 != null) && (!android.text.TextUtils.isEmpty(v0_1))) {
            this.m5(p4, this.d);
            return;
        } else {
            com.chaoxing.android.widget.a.j(this, com.chaoxing.mobile.R$string.user_error).m(1).s();
            this.finish();
            return;
        }
    }

    public final void t5(boolean p3, String p4)
    {
        this.i.setVisibility(8);
        if (p3 != null) {
            if (p3 != null) {
                this.g.setVisibility(0);
                this.h.setVisibility(8);
                com.chaoxing.mobile.webapp.ui.WebViewerUtil.c().g();
            }
            return;
        } else {
            this.g.setVisibility(8);
            this.h.setVisibility(0);
            this.w.setVisibility(0);
            if (ve.f.m(p4)) {
                this.y.setText(p4);
            }
            this.w.setOnClickListener(new com.chaoxing.mobile.sign.ui.SignInfoActivity$d(this));
            return;
        }
    }

    public final void m5(String p3, String p4)
    {
        try {
            String v1_2 = new org.json.JSONObject(p3);
            this.b = v1_2.getString("time");
            this.c = v1_2.getString("signId");
            this.e = an.b.d();
            org.json.JSONException v3_3 = new StringBuilder();
            v3_3.append(this.c);
            v3_3.append("-");
            v3_3.append(p4);
            v3_3.append("-");
            v3_3.append(this.b);
            v3_3.append("-");
            v3_3.append(this.e);
            org.json.JSONException v3_5 = com.fanzhou.util.j.d(v3_3.toString());
            int v0_3 = new StringBuilder();
            v0_3.append(wm.a.a);
            v0_3.append("signId=");
            v0_3.append(this.c);
            v0_3.append("&userId=");
            v0_3.append(p4);
            v0_3.append("&time=");
            v0_3.append(this.b);
            v0_3.append("&phoneId=");
            v0_3.append(this.e);
            v0_3.append("&enc=");
            v0_3.append(v3_5);
            v0_3.append("&ctype=stusign");
            org.json.JSONException v3_9 = v0_3.toString();
            com.chaoxing.android.log.d.d().D(v3_9);
            this.r5(v3_9);
            return;
        } catch (org.json.JSONException v3_10) {
            com.chaoxing.android.widget.a.j(this.a, com.chaoxing.mobile.R$string.json_unusual).s();
            v3_10.printStackTrace();
            return;
        }
    }

    public final void r5(String p4)
    {
        this.f.add(new com.android.volley.toolbox.StringRequest(p4, new com.chaoxing.mobile.sign.ui.SignInfoActivity$f(this), new com.chaoxing.mobile.sign.ui.SignInfoActivity$g(this)));
        return;
    }

    public boolean dispatchTouchEvent(android.view.MotionEvent p1)
    {
        com.networkbench.agent.impl.instrumentation.NBSGestureInstrument.dispatchTouchEvent(p1);
        return super.dispatchTouchEvent(p1);
    }

    public String k5(int p2)
    {
        if (p2 == 301) {
            return "\u7b7e\u5230\u5931\u8d25\uff08\u6570\u636e\u5e93\u63d2\u5165\u5931\u8d25\uff09";
        } else {
            switch (p2) {
                case 306:
                    return "enc\u9a8c\u8bc1\u9519\u8bef";
                case 307:
                    return "\u4e8c\u7ef4\u7801\u65f6\u95f4\u8fc7\u671f";
                case 308:
                    return "\u7b7e\u5230id\u4e0d\u5b58\u5728";
                case 309:
                    return "\u7528\u6237\u4e0d\u5b58\u5728";
                case 310:
                    return "\u7528\u6237\u5355\u4f4d\u4fe1\u606f\u9519\u8bef";
                case 311:
                    return "\u7528\u6237\u89d2\u8272\u9519\u8bef ";
                case 312:
                    return "\u7cfb\u7edf\u9519\u8bef";
                default:
                    return 0;
            }
        }
    }

    public void onCreate(android.os.Bundle p2)
    {
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityCreateBeginIns(this);
        super.onCreate(p2);
        this.setContentView(com.chaoxing.mobile.R$layout.activity_signinfo);
        this.a = this;
        this.d = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        this.initView();
        this.z = this.registerForActivityResult(new com.chaoxing.mobile.sign.ui.SignInfoActivity$a(this), new com.chaoxing.mobile.sign.ui.SignInfoActivity$b(this));
        this.o5();
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityCreateEndIns();
        return;
    }

    public boolean onKeyDown(int p1, android.view.KeyEvent p2)
    {
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onKeyDownAction(p1);
        return super.onKeyDown(p1, p2);
    }

    public void onRestart()
    {
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityRestartBeginIns(this);
        super.onRestart();
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityRestartEndIns();
        return;
    }

    public void onResume()
    {
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityResumeBeginIns(this);
        super.onResume();
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityResumeEndIns();
        return;
    }

    public void onStart()
    {
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityStartBeginIns(this);
        super.onStart();
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityStartEndIns();
        return;
    }

    public void onStop()
    {
        com.networkbench.agent.impl.instrumentation.NBSAppInstrumentation.activityStop(this);
        super.onStop();
        com.android.volley.RequestQueue v0 = this.f;
        if (v0 != null) {
            v0.cancelAll(this);
        }
        return;
    }
}
