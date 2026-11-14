package com.chaoxing.mobile.sign.ui;
public class SignInfoActivity$a extends androidx.activity.result.contract.ActivityResultContract {
    public final synthetic com.chaoxing.mobile.sign.ui.SignInfoActivity a;

    public SignInfoActivity$a(com.chaoxing.mobile.sign.ui.SignInfoActivity p1)
    {
        this.a = p1;
        return;
    }

    public android.content.Intent createIntent(android.content.Context p1, com.chaoxing.android.scan.ScanOptions p2)
    {
        return com.chaoxing.android.scan.c.a(p1, p2);
    }

    public com.chaoxing.android.scan.ScanResult parseResult(int p2, android.content.Intent p3)
    {
        if (p2 != -1) {
            return 0;
        } else {
            return ((com.chaoxing.android.scan.ScanResult) p3.getParcelableExtra("SCAN_RESULT"));
        }
    }

    public bridge synthetic android.content.Intent createIntent(android.content.Context p1, Object p2)
    {
        return this.createIntent(p1, ((com.chaoxing.android.scan.ScanOptions) p2));
    }

    public bridge synthetic Object parseResult(int p1, android.content.Intent p2)
    {
        return this.parseResult(p1, p2);
    }
}
