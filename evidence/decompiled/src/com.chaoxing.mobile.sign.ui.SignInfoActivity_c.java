package com.chaoxing.mobile.sign.ui;
public class SignInfoActivity$c extends android.os.Handler {
    public transient com.networkbench.agent.impl.instrumentation.NBSRunnableInspect nbsHandler;
    final synthetic com.chaoxing.mobile.sign.ui.SignInfoActivity this$0;

    public SignInfoActivity$c(com.chaoxing.mobile.sign.ui.SignInfoActivity p2)
    {
        this.nbsHandler = new com.networkbench.agent.impl.instrumentation.NBSRunnableInspect();
        this.this$0 = p2;
        return;
    }

    public void handleMessage(android.os.Message p6)
    {
        com.networkbench.agent.impl.instrumentation.NBSRunnableInstrumentation.preRunMethod(this);
        boolean v6_5 = ((String) p6.obj);
        com.chaoxing.android.log.d.d().D(v6_5);
        try {
            com.chaoxing.mobile.sign.ui.SignInfoActivity v1_9 = new org.json.JSONObject(v6_5);
            com.chaoxing.mobile.sign.ui.SignInfoActivity.X4(this.this$0, v1_9.getInt("statusCode"));
        } catch (boolean v6_7) {
            com.chaoxing.mobile.sign.ui.SignInfoActivity.Y4(this.this$0, 0, "");
            com.chaoxing.android.widget.a.j(com.chaoxing.mobile.sign.ui.SignInfoActivity.h5(this.this$0), com.chaoxing.mobile.R$string.json_unusual).s();
            v6_7.printStackTrace();
            com.networkbench.agent.impl.instrumentation.NBSRunnableInstrumentation.sufRunMethod(this);
            return;
        }
        if (300 == com.chaoxing.mobile.sign.ui.SignInfoActivity.U4(this.this$0)) {
            boolean v6_6 = v1_9.getBoolean("status");
            String v2_4 = v1_9.getString("msg");
            com.chaoxing.mobile.sign.ui.SignInfoActivity.b5(this.this$0, v1_9.getString("stuName"));
            if (v6_6) {
                com.chaoxing.mobile.sign.ui.SignInfoActivity v1_0 = v1_9.getJSONObject("data");
                com.chaoxing.mobile.sign.ui.SignInfoActivity.c5(this.this$0, v1_0.getString("userName"));
                com.chaoxing.mobile.sign.ui.SignInfoActivity.d5(this.this$0, v1_0.getString("courseName"));
                com.chaoxing.mobile.sign.ui.SignInfoActivity.f5(this.this$0, v1_0.getString("className"));
                com.chaoxing.mobile.sign.ui.SignInfoActivity.g5(this.this$0, new java.text.SimpleDateFormat("yyyy-MM-dd HH:MM").format(new java.util.Date(v1_0.getJSONObject("addTime").getLong("time"))));
                com.chaoxing.mobile.sign.ui.SignInfoActivity.Y4(this.this$0, v6_6, v2_4);
                com.networkbench.agent.impl.instrumentation.NBSRunnableInstrumentation.sufRunMethod(this);
                return;
            } else {
                com.chaoxing.mobile.sign.ui.SignInfoActivity.Y4(this.this$0, v6_6, v2_4);
                com.networkbench.agent.impl.instrumentation.NBSRunnableInstrumentation.sufRunMethod(this);
                return;
            }
        } else {
            boolean v6_8 = this.this$0;
            com.chaoxing.mobile.sign.ui.SignInfoActivity.Y4(this.this$0, 0, v6_8.k5(com.chaoxing.mobile.sign.ui.SignInfoActivity.U4(v6_8)));
            com.networkbench.agent.impl.instrumentation.NBSRunnableInstrumentation.sufRunMethod(this);
            return;
        }
    }
}
