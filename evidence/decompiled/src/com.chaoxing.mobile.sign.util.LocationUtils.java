package com.chaoxing.mobile.sign.util;
public class LocationUtils {
    public static final boolean f = True;
    public static final String g = "LocationUtils";
    public static final String h = "sp_my_location_data";
    public static com.chaoxing.mobile.sign.util.LocationUtils i;
    public com.baidu.location.BDLocation a;
    public android.content.Context b;
    public com.baidu.location.LocationClient c;
    public com.chaoxing.mobile.sign.util.LocationUtils$b d;
    public com.chaoxing.mobile.sign.util.LocationUtils$a e;

    public LocationUtils(android.content.Context p2)
    {
        this.a = 0;
        this.b = p2.getApplicationContext();
        return;
    }

    public static synthetic android.content.Context a(com.chaoxing.mobile.sign.util.LocationUtils p0)
    {
        return p0.b;
    }

    public static synthetic com.chaoxing.mobile.sign.util.LocationUtils$a b(com.chaoxing.mobile.sign.util.LocationUtils p0)
    {
        return p0.e;
    }

    public static synthetic com.chaoxing.mobile.sign.util.LocationUtils$a c(com.chaoxing.mobile.sign.util.LocationUtils p0, com.chaoxing.mobile.sign.util.LocationUtils$a p1)
    {
        p0.e = p1;
        return p1;
    }

    public static synthetic com.baidu.location.BDLocation d(com.chaoxing.mobile.sign.util.LocationUtils p0, com.baidu.location.BDLocation p1)
    {
        p0.a = p1;
        return p1;
    }

    public static com.chaoxing.mobile.sign.util.LocationUtils g(android.content.Context p1)
    {
        if (com.chaoxing.mobile.sign.util.LocationUtils.i == null) {
            com.chaoxing.mobile.sign.util.LocationUtils.i = new com.chaoxing.mobile.sign.util.LocationUtils(p1);
        }
        return com.chaoxing.mobile.sign.util.LocationUtils.i;
    }

    public boolean j()
    {
        int v0 = 0;
        try {
            if (android.provider.Settings$Secure.getInt(this.b.getContentResolver(), "location_mode") != 0) {
                v0 = 1;
            }
        } catch (android.provider.Settings$SettingNotFoundException v1_3) {
            v1_3.printStackTrace();
            return 0;
        }
        return v0;
    }

    public final boolean f(String p2)
    {
        if (androidx.core.content.ContextCompat.checkSelfPermission(this.b, p2) != 0) {
            return 0;
        } else {
            return 1;
        }
    }

    public final void i()
    {
        com.baidu.location.LocationClientOption v0_1 = new com.baidu.location.LocationClientOption();
        v0_1.setLocationMode(com.baidu.location.LocationClientOption$LocationMode.Battery_Saving);
        v0_1.setCoorType("bd09ll");
        v0_1.setScanSpan(3000);
        v0_1.setIsNeedAddress(1);
        v0_1.setOpenGps(1);
        v0_1.setOpenGnss(1);
        v0_1.setLocationNotify(1);
        v0_1.setIsNeedLocationDescribe(1);
        v0_1.setIsNeedLocationPoiList(1);
        v0_1.setIgnoreKillProcess(1);
        v0_1.SetIgnoreCacheException(0);
        v0_1.setEnableSimulateGps(0);
        v0_1.setEnableSimulateGnss(0);
        v0_1.setIsNeedAltitude(1);
        v0_1.setFirstLocType(com.baidu.location.LocationClientOption$FirstLocType.ACCURACY_IN_FIRST_LOC);
        v0_1.setTimeOut(25);
        this.c.setLocOption(v0_1);
        return;
    }

    public boolean e()
    {
        if (this.j()) {
            if ((!this.f("android.permission.ACCESS_FINE_LOCATION")) && (!this.f("android.permission.ACCESS_COARSE_LOCATION"))) {
                return 0;
            } else {
                return 1;
            }
        } else {
            return 0;
        }
    }

    public com.baidu.location.BDLocation h()
    {
        com.chaoxing.android.log.d.d().d("LocationUtils", "get location");
        return this.a;
    }

    public void k(androidx.lifecycle.LifecycleOwner p1, com.chaoxing.mobile.sign.util.LocationUtils$a p2)
    {
        this.e = p2;
        if (p1 != null) {
            p1.getLifecycle().addObserver(new com.chaoxing.mobile.sign.util.LocationUtils$1(this));
        }
        return;
    }

    public void l()
    {
        com.chaoxing.android.log.d.d().d("LocationUtils", "start monitor location");
        com.chaoxing.android.log.o v0_15 = this.c;
        if (v0_15 != null) {
            String v1_4 = this.d;
            if (v1_4 != null) {
                if (v0_15 != null) {
                    v0_15.unRegisterLocationListener(v1_4);
                }
                this.d = 0;
            }
        } else {
            try {
                this.c = new com.baidu.location.LocationClient(this.b);
            } catch (com.chaoxing.android.log.o v0_4) {
                v0_4.printStackTrace();
            }
        }
        if (this.c != null) {
            this.i();
            com.chaoxing.android.log.o v0_7 = new com.chaoxing.mobile.sign.util.LocationUtils$b(this);
            this.d = v0_7;
            this.c.registerLocationListener(v0_7);
            if (!this.c.isStarted()) {
                this.c.start();
            }
            if (!this.c.isStarted()) {
                com.chaoxing.android.log.d.d().d("LocSDK3", "locClient is null or not started");
            } else {
                this.c.requestLocation();
            }
        }
        return;
    }

    public void m()
    {
        com.chaoxing.android.log.d.d().d("LocationUtils", "stop monitor location");
        com.baidu.location.LocationClient v0_2 = this.c;
        if ((v0_2 != null) && (v0_2.isStarted())) {
            this.c.stop();
        }
        return;
    }
}
