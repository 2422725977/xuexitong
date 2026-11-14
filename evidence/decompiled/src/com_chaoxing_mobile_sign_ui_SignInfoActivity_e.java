package com.chaoxing.mobile.sign.ui;
public class SignInfoActivity$e implements android.view.View$OnClickListener {
    public final synthetic com.chaoxing.mobile.sign.ui.SignInfoActivity a;

    public SignInfoActivity$e(com.chaoxing.mobile.sign.ui.SignInfoActivity p1)
    {
        this.a = p1;
        return;
    }

    public void onClick(android.view.View p1)
    {
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventEnter(p1);
        this.a.onBackPressed();
        com.networkbench.agent.impl.instrumentation.NBSActionInstrumentation.onClickEventExit();
        return;
    }
}
