package com.chaoxing.mobile.sign.util;
public class b {

    public b()
    {
        return;
    }

    public static android.location.Location b(android.content.Context p2)
    {
        int v2_5 = ((android.location.LocationManager) p2.getSystemService("location"));
        if (!v2_5.isProviderEnabled("network")) {
            if (!v2_5.isProviderEnabled("gps")) {
                return 0;
            } else {
                return v2_5.getLastKnownLocation("gps");
            }
        } else {
            return v2_5.getLastKnownLocation("network");
        }
    }

    public String a(android.content.Context p9)
    {
        String v0_1;
        String v0_3 = ((android.location.LocationManager) p9.getSystemService("location"));
        double v6 = 0;
        if (!v0_3.isProviderEnabled("gps")) {
            v0_3.requestLocationUpdates("network", 1000, 0, new com.chaoxing.mobile.sign.util.b$a(this));
            String v9_2 = v0_3.getLastKnownLocation("network");
            if (v9_2 == null) {
                v0_1 = 0;
            } else {
                v6 = v9_2.getLatitude();
                v0_1 = v9_2.getLongitude();
            }
        } else {
            String v9_4 = v0_3.getLastKnownLocation("gps");
            if (v9_4 == null) {
            } else {
                v6 = v9_4.getLatitude();
                v0_1 = v9_4.getLongitude();
            }
        }
        String v9_6 = new StringBuilder();
        v9_6.append("lat:");
        v9_6.append(Double.toString(v6));
        v9_6.append("lon");
        v9_6.append(Double.toString(v0_1));
        return v9_6.toString();
    }
}
