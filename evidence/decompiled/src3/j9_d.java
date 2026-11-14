package j9;
public class d extends android.webkit.WebChromeClient {
    public android.app.Activity a;
    public android.view.ViewGroup b;
    public int c;
    public int d;
    public android.webkit.WebChromeClient$CustomViewCallback e;
    public j9.h f;

    public d(android.app.Activity p1)
    {
        this.a = p1;
        return;
    }

    public static synthetic void a(android.webkit.JsResult p0, android.content.DialogInterface p1, int p2)
    {
        p0.cancel();
        p1.dismiss();
        return;
    }

    public static synthetic void b(android.webkit.JsResult p0, android.content.DialogInterface p1, int p2)
    {
        p0.confirm();
        p1.dismiss();
        return;
    }

    public static synthetic void c(android.webkit.JsResult p0, android.content.DialogInterface p1, int p2)
    {
        p0.confirm();
        p1.dismiss();
        return;
    }

    public void onHideCustomView()
    {
        if (this.b != null) {
            int v0_5 = ((android.widget.FrameLayout) this.a.getWindow().getDecorView());
            this.b.removeAllViews();
            v0_5.setBackgroundColor(0);
            v0_5.removeView(this.b);
            this.b = 0;
            this.a.getWindow().getDecorView().setSystemUiVisibility(this.c);
            this.a.setRequestedOrientation(this.d);
            this.e = 0;
            return;
        } else {
            return;
        }
    }

    public void d()
    {
        android.webkit.WebChromeClient$CustomViewCallback v0 = this.e;
        if (v0 != null) {
            v0.onCustomViewHidden();
        }
        return;
    }

    public void e(j9.h p1)
    {
        this.f = p1;
        return;
    }

    public android.graphics.Bitmap getDefaultVideoPoster()
    {
        try {
            return android.graphics.Bitmap.createBitmap(1, 1, android.graphics.Bitmap$Config.ARGB_8888);
        } catch (Exception) {
            return super.getDefaultVideoPoster();
        }
    }

    public boolean onConsoleMessage(android.webkit.ConsoleMessage p1)
    {
        return super.onConsoleMessage(p1);
    }

    public void onGeolocationPermissionsShowPrompt(String p3, android.webkit.GeolocationPermissions$Callback p4)
    {
        p4.invoke(p3, 1, 0);
        super.onGeolocationPermissionsShowPrompt(p3, p4);
        return;
    }

    public boolean onJsAlert(android.webkit.WebView p1, String p2, String p3, android.webkit.JsResult p4)
    {
        int v1_4 = this.a.getParent();
        if (v1_4 == 0) {
            v1_4 = this.a;
        }
        new android.app.AlertDialog$Builder(v1_4).setMessage(p3).setCancelable(0).setPositiveButton(17039370, new j9.a(p4)).show();
        return 1;
    }

    public boolean onJsConfirm(android.webkit.WebView p4, String p5, String p6, android.webkit.JsResult p7)
    {
        String v4_0 = "";
        try {
            int v5_4 = new org.json.JSONObject(p6);
            j9.c v6_5 = v5_4.optString("message");
            boolean v0_8 = v5_4.optString("btnOk");
            try {
                int v5_3;
                String v4_1 = v5_4.optString("btnCancel");
            } catch (Exception) {
                int v5_2 = v4_1;
                v4_0 = v0_8;
                v5_3 = v4_0;
                v4_1 = v5_2;
                new android.app.AlertDialog$Builder(this.a).setMessage(v6_5).setCancelable(0).setPositiveButton(v5_3, new j9.b(p7)).setNegativeButton(v4_1, new j9.c(p7)).show();
                return 1;
            }
            if (!android.text.TextUtils.isEmpty(v0_8)) {
                v5_3 = v0_8;
            } else {
                v5_3 = "\u786e\u5b9a";
            }
            try {
                if (!android.text.TextUtils.isEmpty(v4_1)) {
                    new android.app.AlertDialog$Builder(this.a).setMessage(v6_5).setCancelable(0).setPositiveButton(v5_3, new j9.b(p7)).setNegativeButton(v4_1, new j9.c(p7)).show();
                    return 1;
                } else {
                    v4_1 = "\u53d6\u6d88";
                    new android.app.AlertDialog$Builder(this.a).setMessage(v6_5).setCancelable(0).setPositiveButton(v5_3, new j9.b(p7)).setNegativeButton(v4_1, new j9.c(p7)).show();
                    return 1;
                }
            } catch (Exception) {
                v5_2 = v4_1;
                v4_0 = v5_3;
            }
        } catch (Exception) {
            v5_2 = "";
        }
    }

    public void onPermissionRequest(android.webkit.PermissionRequest p1)
    {
        super.onPermissionRequest(p1);
        return;
    }

    public void onPermissionRequestCanceled(android.webkit.PermissionRequest p1)
    {
        super.onPermissionRequestCanceled(p1);
        return;
    }

    public void onProgressChanged(android.webkit.WebView p1, int p2)
    {
        super.onProgressChanged(p1, p2);
        return;
    }

    public void onReceivedTitle(android.webkit.WebView p3, String p4)
    {
        if (p4 != null) {
            boolean v0_3 = p3.getUrl();
            if (!p4.equals(v0_3)) {
                if (!p4.equals(v0_3.substring((new java.net.URL(v0_3).getProtocol().length() + 3)))) {
                    super.onReceivedTitle(p3, p4);
                    boolean v0_4 = this.f;
                    if (v0_4) {
                        v0_4.g(p3, p4);
                    }
                    return;
                } else {
                }
            }
            p4 = "";
        }
    }

    public void onShowCustomView(android.view.View p4, android.webkit.WebChromeClient$CustomViewCallback p5)
    {
        if (this.b == null) {
            this.b = new j9.d$a(p4.getContext());
            this.c = this.a.getWindow().getDecorView().getSystemUiVisibility();
            this.d = this.a.getRequestedOrientation();
            this.e = p5;
            int v5_4 = ((android.widget.FrameLayout) this.a.getWindow().getDecorView());
            android.widget.FrameLayout$LayoutParams v0_7 = new android.widget.FrameLayout$LayoutParams(-1, -1);
            android.widget.FrameLayout$LayoutParams v2_1 = new android.widget.FrameLayout$LayoutParams(-1, -1);
            if (k9.a.g(this.a)) {
                v2_1.leftMargin = k9.a.b(this.a);
            }
            this.b.addView(p4, v2_1);
            this.b.setBackgroundColor(-16777216);
            v5_4.addView(this.b, v0_7);
            this.a.getWindow().getDecorView().setSystemUiVisibility(3846);
            this.a.setRequestedOrientation(0);
            return;
        } else {
            android.app.Activity v4_7 = this.e;
            if (v4_7 == null) {
                this.onHideCustomView();
                return;
            } else {
                v4_7.onCustomViewHidden();
                return;
            }
        }
    }
}
