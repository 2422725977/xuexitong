package com.chaoxing.mobile.webapp.jsprotocal.common;
public class j0 extends com.chaoxing.mobile.webapp.jsprotocal.a {
    public static final String n = "ClientSeatReserveSignInJsProtocalExecutor";
    public static final int o = 24576;
    public static final int p = 24577;
    public static final int q = 24578;
    public final io.reactivex.disposables.a k;
    public String l;
    public final android.os.Handler m;

    private void e0()
    {
        try {
            Exception v1_2 = new android.content.Intent();
            v1_2.setAction("android.settings.APPLICATION_DETAILS_SETTINGS");
            v1_2.setData(android.net.Uri.fromParts("package", this.j().getPackageName(), 0));
            this.D(v1_2, 24576);
            return;
        } catch (Exception v1_1) {
            com.chaoxing.android.log.d.d().e("ClientSeatReserveSignInJsProtocalExecutor", 0, v1_1);
            return;
        }
    }

    private void Y()
    {
        if ((!com.chaoxing.mobile.office.utils.a2.A()) || (com.chaoxing.mobile.office.utils.a2.C(this.j().getApplicationContext()))) {
            this.c0();
            return;
        } else {
            this.g0();
            return;
        }
    }

    private void i0()
    {
        com.chaoxing.core.widget.CustomerDialog v0_1 = new com.chaoxing.core.widget.CustomerDialog(this.j());
        v0_1.u(com.chaoxing.mobile.R$string.request_permission);
        v0_1.z(com.chaoxing.mobile.R$string.request_permission_bluetooth);
        v0_1.L(com.chaoxing.mobile.R$string.go_settings, new com.chaoxing.mobile.webapp.jsprotocal.common.c0(this));
        v0_1.G(17039360, new com.chaoxing.mobile.webapp.jsprotocal.common.d0(this));
        v0_1.setCanceledOnTouchOutside(0);
        v0_1.setCancelable(0);
        v0_1.show();
        return;
    }

    private void j0()
    {
        com.chaoxing.core.widget.CustomerDialog v0_1 = new com.chaoxing.core.widget.CustomerDialog(this.j());
        v0_1.u(com.chaoxing.mobile.R$string.request_permission);
        v0_1.z(com.chaoxing.mobile.R$string.request_permission_location);
        v0_1.L(com.chaoxing.mobile.R$string.go_settings, new com.chaoxing.mobile.webapp.jsprotocal.common.e0(this));
        v0_1.G(17039360, new com.chaoxing.mobile.webapp.jsprotocal.common.u(this));
        v0_1.setCanceledOnTouchOutside(0);
        v0_1.setCancelable(0);
        v0_1.show();
        return;
    }

    private void g0()
    {
        com.chaoxing.core.widget.CustomerDialog v0_1 = new com.chaoxing.core.widget.CustomerDialog(this.j());
        v0_1.u(com.chaoxing.mobile.R$string.request_permission);
        v0_1.C("\u5b66\u4e60\u901a\u8bf7\u6c42\u5f00\u542f\u9ad8\u7cbe\u5ea6\u4f4d\u7f6e\u4fe1\u606f\u670d\u52a1");
        v0_1.L(com.chaoxing.mobile.R$string.go_settings, new com.chaoxing.mobile.webapp.jsprotocal.common.a0(this));
        v0_1.G(17039360, new com.chaoxing.mobile.webapp.jsprotocal.common.b0(this));
        v0_1.setCanceledOnTouchOutside(0);
        v0_1.setCancelable(0);
        v0_1.show();
        return;
    }

    private void f0()
    {
        this.D(new android.content.Intent("android.bluetooth.adapter.action.REQUEST_ENABLE"), 24577);
        return;
    }

    private void a0()
    {
        io.reactivex.disposables.b v0_2 = new b40.c(this.k());
        this.k.c(v0_2.s(new String[] {"android.permission.ACCESS_COARSE_LOCATION", "android.permission.ACCESS_FINE_LOCATION"})).subscribe(new com.chaoxing.mobile.webapp.jsprotocal.common.v(this, v0_2)));
        return;
    }

    private void d0()
    {
        int v0_2 = com.chaoxing.mobile.webapp.jsprotocal.common.j0$b.a[this.X().ordinal()];
        if (v0_2 == 1) {
            this.a0();
            return;
        } else {
            if (v0_2 == 3) {
                this.f0();
                return;
            } else {
                return;
            }
        }
    }

    public j0(android.app.Activity p1, com.fanzhou.ui.WebClient p2)
    {
        super(p1, p2);
        super.k = new io.reactivex.disposables.a();
        super.m = new android.os.Handler(android.os.Looper.getMainLooper());
        return;
    }

    public static synthetic void G(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0, android.content.DialogInterface p1, int p2)
    {
        p0.e0();
        return;
    }

    public static synthetic void H(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p1, android.content.DialogInterface p2, int p3)
    {
        com.chaoxing.android.widget.a.j(p1.j(), com.chaoxing.mobile.R$string.request_permission_bluetooth_failed).s();
        try {
            com.chaoxing.android.log.o v2_4 = new org.json.JSONObject();
            v2_4.put("result", 0);
            v2_4.put("data", ne.a.g(new java.util.ArrayList()));
            v2_4.put("errorMsg", "\u83b7\u53d6\u84dd\u7259\u8bbe\u5907\u5931\u8d25,\u8bf7\u5f00\u542f\u9644\u8fd1\u8bbe\u5907\u6743\u9650");
            p1.m.post(new com.chaoxing.mobile.webapp.jsprotocal.common.z(p1, v2_4));
            return;
        } catch (Exception v1_1) {
            com.chaoxing.android.log.d.d().e("ClientSeatReserveSignInJsProtocalExecutor", 0, v1_1);
            return;
        }
    }

    public static synthetic void I(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p1, org.json.JSONObject p2)
    {
        p1.r(p1.c, p2.toString());
        return;
    }

    public static synthetic void J(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p1, org.json.JSONObject p2)
    {
        p1.r(p1.c, p2.toString());
        return;
    }

    public static synthetic void K(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p1, Exception p2)
    {
        p1.r(p1.c, p2.getLocalizedMessage());
        return;
    }

    public static synthetic void L(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p1, org.json.JSONObject p2)
    {
        p1.r(p1.c, p2.toString());
        return;
    }

    public static synthetic void M(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p1, b40.b p2)
    {
        p1.getClass();
        if (!p2.b) {
            if (!p2.c) {
                p1.i0();
                return;
            } else {
                p1.i0();
                return;
            }
        } else {
            p1.Y();
            return;
        }
    }

    public static synthetic void N(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p1, android.content.DialogInterface p2, int p3)
    {
        com.chaoxing.android.widget.a.j(p1.j(), com.chaoxing.mobile.R$string.request_permission_location_failed).s();
        try {
            com.chaoxing.android.log.o v2_4 = new org.json.JSONObject();
            v2_4.put("result", 0);
            v2_4.put("data", ne.a.g(new java.util.ArrayList()));
            v2_4.put("errorMsg", "\u83b7\u53d6\u84dd\u7259\u8bbe\u5907\u5931\u8d25,\u8bf7\u5f00\u542f\u4f4d\u7f6e\u6743\u9650");
            p1.m.post(new com.chaoxing.mobile.webapp.jsprotocal.common.x(p1, v2_4));
            return;
        } catch (Exception v1_1) {
            com.chaoxing.android.log.d.d().e("ClientSeatReserveSignInJsProtocalExecutor", 0, v1_1);
            return;
        }
    }

    public static synthetic void O(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p2, b40.c p3, b40.b p4)
    {
        p2.getClass();
        if (!p4.b) {
            if (!p4.c) {
                p2.j0();
                return;
            } else {
                p2.j0();
                return;
            }
        } else {
            if (android.os.Build$VERSION.SDK_INT < 31) {
                p2.Y();
                return;
            } else {
                p2.k.c(p3.s(new String[] {"android.permission.BLUETOOTH_SCAN", "android.permission.BLUETOOTH_ADVERTISE", "android.permission.BLUETOOTH_CONNECT"})).subscribe(new com.chaoxing.mobile.webapp.jsprotocal.common.w(p2)));
                return;
            }
        }
    }

    public static synthetic void P(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0, android.content.DialogInterface p1, int p2)
    {
        p0.c0();
        return;
    }

    public static synthetic void Q(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0, android.content.DialogInterface p1, int p2)
    {
        p0.b0();
        return;
    }

    public static synthetic void R(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0, android.content.DialogInterface p1, int p2)
    {
        p0.e0();
        return;
    }

    public static synthetic android.os.Handler S(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0)
    {
        return p0.m;
    }

    public static synthetic String T(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0)
    {
        return p0.c;
    }

    public static synthetic String U(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0)
    {
        return p0.c;
    }

    public static synthetic String V(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0)
    {
        return p0.c;
    }

    public static synthetic String W(com.chaoxing.mobile.webapp.jsprotocal.common.j0 p0)
    {
        return p0.c;
    }

    public final void c0()
    {
        try {
            com.chaoxing.beacon.a.a(this.j().getApplicationContext()).c(this.l, new com.chaoxing.mobile.webapp.jsprotocal.common.j0$a(this));
            return;
        } catch (Exception v0_1) {
            this.m.post(new com.chaoxing.mobile.webapp.jsprotocal.common.y(this, v0_1));
            com.chaoxing.android.log.d.d().e("ClientSeatReserveSignInJsProtocalExecutor", 0, v0_1);
            return;
        }
    }

    public void b0()
    {
        this.D(new android.content.Intent("android.settings.LOCATION_SOURCE_SETTINGS"), 24578);
        return;
    }

    public com.chaoxing.beacon.BluetoothState X()
    {
        if (this.j().getApplicationContext().getPackageManager().hasSystemFeature("android.hardware.bluetooth_le")) {
            com.chaoxing.beacon.BluetoothState v0_4 = ((android.bluetooth.BluetoothManager) this.j().getApplicationContext().getSystemService("bluetooth"));
            if (v0_4 == null) {
                return com.chaoxing.beacon.BluetoothState.BluetoothStatePowerOff;
            } else {
                if (!v0_4.getAdapter().isEnabled()) {
                    return com.chaoxing.beacon.BluetoothState.BluetoothStatePowerOff;
                } else {
                    return com.chaoxing.beacon.BluetoothState.BluetoothStatePowerOn;
                }
            }
        } else {
            return com.chaoxing.beacon.BluetoothState.BluetoothStateNotSupported;
        }
    }

    public final void h0()
    {
        try {
            Exception v0_1 = new org.json.JSONObject();
            v0_1.put("result", 0);
            v0_1.put("data", ne.a.g(new java.util.ArrayList()));
            v0_1.put("errorMsg", "\u8bf7\u5f00\u542f\u84dd\u7259");
            this.m.post(new com.chaoxing.mobile.webapp.jsprotocal.common.t(this, v0_1));
            return;
        } catch (Exception v0_2) {
            com.chaoxing.android.log.d.d().e("ClientSeatReserveSignInJsProtocalExecutor", 0, v0_2);
            return;
        }
    }

    public void a(int p1, int p2, android.content.Intent p3)
    {
        super.a(p1, p2, p3);
        if (p1 != 24577) {
            if (p1 != 24576) {
                if (p1 == 24578) {
                    this.c0();
                }
                return;
            } else {
                this.a0();
                return;
            }
        } else {
            if (p2 == -1) {
                this.a0();
                return;
            } else {
                com.chaoxing.android.widget.a.k(this.j().getApplicationContext(), "\u8bf7\u5f00\u542f\u84dd\u7259").s();
                this.h0();
                return;
            }
        }
    }

    public void destory()
    {
        try {
            com.chaoxing.beacon.a.a(this.j().getApplicationContext()).b();
            this.k.e();
            this.m.removeCallbacksAndMessages(0);
        } catch (Exception v1_1) {
            com.chaoxing.android.log.d.d().e("ClientSeatReserveSignInJsProtocalExecutor", 0, v1_1);
        }
        super.destory();
        return;
    }

    public void execute(String p2)
    {
        if ((!this.a.isFinishing()) && (!com.fanzhou.util.w.q(p2))) {
            this.l = p2;
            this.d0();
        }
        return;
    }
}
