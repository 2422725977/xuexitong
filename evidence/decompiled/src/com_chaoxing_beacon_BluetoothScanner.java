package com.chaoxing.beacon;
public class BluetoothScanner implements androidx.lifecycle.LifecycleOwner {
    public static final String n = "BluetoothScanner";
    public static final int o = 10;
    public static final int p = 10;
    public static final int q = 3;
    public static final int r = 13;
    public final androidx.lifecycle.LifecycleRegistry a;
    public int b;
    public final android.content.Context c;
    public boolean d;
    public boolean e;
    public java.util.concurrent.ExecutorService f;
    public final android.os.Handler g;
    public final java.util.List h;
    public com.chaoxing.beacon.i i;
    public int j;
    public final java.util.HashMap k;
    public final android.bluetooth.le.ScanCallback l;
    public final Runnable m;

    static BluetoothScanner()
    {
        return;
    }

    public BluetoothScanner(android.content.Context p4)
    {
        androidx.lifecycle.LifecycleRegistry v0_1 = new androidx.lifecycle.LifecycleRegistry(this);
        this.a = v0_1;
        this.b = 0;
        this.g = new android.os.Handler(android.os.Looper.getMainLooper());
        this.h = new java.util.ArrayList();
        this.k = new java.util.HashMap();
        this.l = new com.chaoxing.beacon.BluetoothScanner$a(this);
        this.m = new com.chaoxing.beacon.BluetoothScanner$b(this);
        this.c = p4;
        v0_1.markState(androidx.lifecycle.Lifecycle$State.CREATED);
        v0_1.addObserver(new com.chaoxing.beacon.BluetoothScanner$1(this));
        return;
    }

    public static synthetic boolean a(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.e;
    }

    public static synthetic int b(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.j;
    }

    public static synthetic String[] c(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.r();
    }

    public static synthetic void d(com.chaoxing.beacon.BluetoothScanner p0, android.bluetooth.le.ScanResult p1)
    {
        p0.s(p1);
        return;
    }

    public static synthetic android.os.Handler e(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.g;
    }

    public static synthetic java.util.concurrent.ExecutorService f(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.f;
    }

    public static synthetic boolean g(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.d;
    }

    public static synthetic int h(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.b;
    }

    public static synthetic int i(com.chaoxing.beacon.BluetoothScanner p2)
    {
        int v0 = p2.b;
        p2.b = (v0 + 1);
        return v0;
    }

    public static synthetic java.util.List j(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.h;
    }

    public static synthetic com.chaoxing.beacon.i k(com.chaoxing.beacon.BluetoothScanner p0)
    {
        return p0.i;
    }

    public static synthetic boolean l(com.chaoxing.beacon.BluetoothScanner p0, Object p1)
    {
        return p0.u(p1);
    }

    public static synthetic boolean m(com.chaoxing.beacon.BluetoothScanner p0, android.bluetooth.le.ScanResult p1)
    {
        return p0.p(p1);
    }

    public static synthetic String[] n(com.chaoxing.beacon.BluetoothScanner p0, android.bluetooth.le.ScanResult p1)
    {
        return p0.o(p1);
    }

    public final String[] r()
    {
        String[] v0_1 = new String[2];
        v0_1[0] = "";
        v0_1[1] = "";
        if (!com.chaoxing.beacon.g.a(this.h)) {
            com.chaoxing.beacon.BluetoothDeviceEntity v2_2 = ((com.chaoxing.beacon.BluetoothDeviceEntity) this.h.get(0));
            if (v2_2 != null) {
                v0_1[0] = v2_2.getName();
                v0_1[1] = v2_2.getMacAddress();
            }
        }
        return v0_1;
    }

    public final void s(android.bluetooth.le.ScanResult p3)
    {
        if (this.u(p3)) {
            java.util.List v3_5 = p3.getDevice();
            if ((this.u(v3_5)) && ((!android.text.TextUtils.isEmpty(v3_5.getName())) && (!v3_5.getName().equalsIgnoreCase("N/A")))) {
                com.chaoxing.beacon.BluetoothDeviceEntity v0_5 = new com.chaoxing.beacon.BluetoothDeviceEntity();
                v0_5.setName(v3_5.getName());
                v0_5.setMacAddress(v3_5.getAddress());
                if (!this.h.contains(v0_5)) {
                    this.h.add(v0_5);
                }
            }
        }
        return;
    }

    public final boolean u(Object p1)
    {
        if (p1 == 0) {
            return 0;
        } else {
            return 1;
        }
    }

    public final boolean p(android.bluetooth.le.ScanResult p3)
    {
        if ((!this.u(p3.getDevice())) || (this.k.get(p3.getDevice().getAddress()) == null)) {
            return 0;
        } else {
            return 1;
        }
    }

    public final String[] o(android.bluetooth.le.ScanResult p5)
    {
        String[] v0_1 = new String[2];
        v0_1[0] = "";
        v0_1[1] = "";
        if (this.u(p5.getDevice())) {
            String v5_4 = ((com.chaoxing.beacon.BluetoothDevices) this.k.get(p5.getDevice().getAddress()));
            if (v5_4 != null) {
                v0_1[0] = v5_4.getName();
                v0_1[1] = v5_4.getMacAddress();
            }
        }
        return v0_1;
    }

    public void y()
    {
        this.e = 1;
        this.b = 0;
        this.h.clear();
        this.a.markState(androidx.lifecycle.Lifecycle$State.RESUMED);
        android.os.Handler v0_2 = ((android.bluetooth.BluetoothManager) this.c.getSystemService("bluetooth"));
        if ((v0_2 != null) && (v0_2.getAdapter() != null)) {
            android.os.Handler v0_5 = v0_2.getAdapter().getBluetoothLeScanner();
            if (v0_5 != null) {
                v0_5.stopScan(this.l);
            }
        }
        android.os.Handler v0_6 = this.f;
        if (v0_6 != null) {
            v0_6.shutdown();
        }
        this.g.removeCallbacks(this.m);
        this.g.removeCallbacksAndMessages(0);
        return;
    }

    public final void t(String p4)
    {
        if (!android.text.TextUtils.isEmpty(p4)) {
            try {
                java.util.Iterator v4_6 = ((com.chaoxing.beacon.BluetoothSignEntity) com.alibaba.fastjson.g.parseObject(p4, com.chaoxing.beacon.BluetoothSignEntity));
            } catch (java.util.Iterator v4_3) {
                android.util.Log.e(com.chaoxing.beacon.BluetoothScanner.n, android.util.Log.getStackTraceString(v4_3));
                return;
            }
            if (this.u(v4_6)) {
                com.chaoxing.beacon.BluetoothDevices v0_1 = v4_6.getType();
                this.j = v0_1;
                if ((v0_1 == 1) || (v0_1 == 2)) {
                    this.k.clear();
                    java.util.Iterator v4_2 = v4_6.getData().iterator();
                    while (v4_2.hasNext()) {
                        com.chaoxing.beacon.BluetoothDevices v0_7 = ((com.chaoxing.beacon.BluetoothDevices) v4_2.next());
                        this.k.put(v0_7.getMacAddress(), v0_7);
                    }
                }
            }
        }
        return;
    }

    public void w(boolean p1)
    {
        this.d = p1;
        return;
    }

    public void v(com.chaoxing.beacon.i p1)
    {
        this.i = p1;
        return;
    }

    public androidx.lifecycle.Lifecycle getLifecycle()
    {
        return this.a;
    }

    public void q()
    {
        this.y();
        return;
    }

    public void x(String p10, com.chaoxing.beacon.i p11)
    {
        this.a.markState(androidx.lifecycle.Lifecycle$State.RESUMED);
        this.t(p10);
        this.e = 0;
        this.w(1);
        this.v(p11);
        this.f = java.util.concurrent.Executors.newFixedThreadPool(10);
        android.bluetooth.le.BluetoothLeScanner v10_5 = ((android.bluetooth.BluetoothManager) this.c.getSystemService("bluetooth"));
        if ((v10_5 != null) && (v10_5.getAdapter() != null)) {
            android.bluetooth.le.BluetoothLeScanner v10_7 = v10_5.getAdapter().getBluetoothLeScanner();
            if (v10_7 != null) {
                java.util.ArrayList v11_5 = new java.util.ArrayList();
                android.bluetooth.le.ScanSettings v0_8 = new android.bluetooth.le.ScanFilter$Builder().setServiceData(android.os.ParcelUuid.fromString("00001802-0000-1000-8000-00805f9b34fb"), 0).build();
                android.bluetooth.le.ScanCallback v1_9 = new android.bluetooth.le.ScanFilter$Builder().setServiceData(android.os.ParcelUuid.fromString("0000fff0-0000-1000-8000-00805f9b34fb"), 0).build();
                android.bluetooth.le.ScanFilter v3_5 = new android.bluetooth.le.ScanFilter$Builder().setServiceData(android.os.ParcelUuid.fromString("0000fff1-0000-1000-8000-00805f9b34fb"), 0).build();
                android.bluetooth.le.ScanFilter v4_5 = new android.bluetooth.le.ScanFilter$Builder().setServiceData(android.os.ParcelUuid.fromString("0000fda5-0000-1000-8000-00805f9b34fb"), 0).build();
                android.bluetooth.le.ScanFilter v5_5 = new android.bluetooth.le.ScanFilter$Builder().setServiceData(android.os.ParcelUuid.fromString("0000ab81-0000-1000-8000-00805f9b34fb"), 0).build();
                android.bluetooth.le.ScanFilter v6_5 = new android.bluetooth.le.ScanFilter$Builder().setServiceData(android.os.ParcelUuid.fromString("0000ffe1-0000-1000-8000-00805f9b34fb"), 0).build();
                android.bluetooth.le.ScanFilter v2_2 = new android.bluetooth.le.ScanFilter$Builder().setServiceData(android.os.ParcelUuid.fromString("0000ffd1-0000-1000-8000-00805f9b34fb"), 0).build();
                v11_5.add(v0_8);
                v11_5.add(v1_9);
                v11_5.add(v3_5);
                v11_5.add(v4_5);
                v11_5.add(v5_5);
                v11_5.add(v6_5);
                v11_5.add(v2_2);
                android.bluetooth.le.ScanSettings v0_3 = new android.bluetooth.le.ScanSettings$Builder().setScanMode(2);
                v0_3.setReportDelay(0);
                v10_7.startScan(v11_5, v0_3.build(), this.l);
            }
        }
        this.g.post(this.m);
        return;
    }
}
