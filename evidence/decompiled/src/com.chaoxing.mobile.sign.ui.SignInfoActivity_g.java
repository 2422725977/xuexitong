package com.chaoxing.mobile.sign.ui;
public class SignInfoActivity$g implements com.android.volley.Response$ErrorListener {
    public final synthetic com.chaoxing.mobile.sign.ui.SignInfoActivity a;

    public SignInfoActivity$g(com.chaoxing.mobile.sign.ui.SignInfoActivity p1)
    {
        this.a = p1;
        return;
    }

    public void onErrorResponse(com.android.volley.VolleyError p3)
    {
        com.chaoxing.android.widget.a.j(com.chaoxing.mobile.sign.ui.SignInfoActivity.h5(this.a), com.chaoxing.mobile.R$string.request_unusual).m(1).s();
        com.chaoxing.mobile.sign.ui.SignInfoActivity.Y4(this.a, 0, "");
        return;
    }
}
