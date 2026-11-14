package com.chaoxing.mobile.sign.ui;
public class SignInfoActivity$f implements com.android.volley.Response$Listener {
    public final synthetic com.chaoxing.mobile.sign.ui.SignInfoActivity a;

    public SignInfoActivity$f(com.chaoxing.mobile.sign.ui.SignInfoActivity p1)
    {
        this.a = p1;
        return;
    }

    public void a(String p2)
    {
        android.os.Message v0_2 = com.chaoxing.mobile.sign.ui.SignInfoActivity.V4(this.a).obtainMessage();
        v0_2.obj = p2;
        com.chaoxing.mobile.sign.ui.SignInfoActivity.V4(this.a).sendMessage(v0_2);
        return;
    }

    public bridge synthetic void onResponse(Object p1)
    {
        this.a(((String) p1));
        return;
    }
}
