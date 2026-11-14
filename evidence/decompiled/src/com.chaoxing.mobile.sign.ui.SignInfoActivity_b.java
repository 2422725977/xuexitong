package com.chaoxing.mobile.sign.ui;
public class SignInfoActivity$b implements androidx.activity.result.ActivityResultCallback {
    public final synthetic com.chaoxing.mobile.sign.ui.SignInfoActivity a;

    public SignInfoActivity$b(com.chaoxing.mobile.sign.ui.SignInfoActivity p1)
    {
        this.a = p1;
        return;
    }

    public void a(com.chaoxing.android.scan.ScanResult p3)
    {
        if (p3 != null) {
            String v3_3 = p3.scans;
            if (v3_3 != null) {
                com.chaoxing.mobile.sign.ui.SignInfoActivity.R4(this.a, v3_3[0].content);
                return;
            }
        }
        this.a.setResult(0);
        this.a.finish();
        return;
    }

    public bridge synthetic void onActivityResult(Object p1)
    {
        this.a(((com.chaoxing.android.scan.ScanResult) p1));
        return;
    }
}
