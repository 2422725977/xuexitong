package com.fanzhou.util;
public class j {

    public static String d(String p4)
    {
        if ((p4 != null) && (p4.length() != 0)) {
            try {
                StringBuffer v0_4 = java.security.MessageDigest.getInstance("MD5");
                v0_4.update(p4.getBytes());
                String v4_1 = v0_4.digest();
                StringBuffer v0_1 = new StringBuffer("");
                int v1_1 = 0;
            } catch (String v4_3) {
                v4_3.printStackTrace();
            }
            while (v1_1 < v4_1.length) {
                String v2_1 = v4_1[v1_1];
                if (v2_1 < null) {
                    v2_1 += 256;
                }
                if (v2_1 < 16) {
                    v0_1.append("0");
                }
                v0_1.append(Integer.toHexString(v2_1));
                v1_1++;
            }
            return v0_1.toString();
        }
        return 0;
    }

    public j()
    {
        return;
    }

    public static String a(String p1, String p2)
    {
        if (com.fanzhou.util.u.l(p1)) {
            return com.fanzhou.util.j.d(p2);
        } else {
            return com.fanzhou.util.j.d(p1);
        }
    }

    public static String b(String p7)
    {
        if (!com.fanzhou.util.w.s(p7)) {
            java.security.NoSuchAlgorithmException v7_1 = java.security.MessageDigest.getInstance("MD5").digest(p7.getBytes());
            int v0_1 = v7_1.length;
            int v2 = 0;
            String v3 = "";
            while (v2 < v0_1) {
                String v4_2 = Integer.toHexString((v7_1[v2] & 255));
                if (v4_2.length() == 1) {
                    StringBuilder v5_2 = new StringBuilder();
                    v5_2.append("0");
                    v5_2.append(v4_2);
                    v4_2 = v5_2.toString();
                }
                StringBuilder v5_4 = new StringBuilder();
                v5_4.append(v3);
                v5_4.append(v4_2);
                v3 = v5_4.toString();
                v2++;
            }
            return v3;
        } else {
            return "";
        }
    }

    public static String c(String p4)
    {
        if ((p4 != null) && (p4.length() != 0)) {
            try {
                int v0_5 = java.security.MessageDigest.getInstance("MD5");
                v0_5.update(p4.getBytes());
                String v4_1 = v0_5.digest();
                int v0_1 = new StringBuffer("");
                int v1_1 = 0;
            } catch (String v4_4) {
                v4_4.printStackTrace();
            }
            while (v1_1 < v4_1.length) {
                String v2_1 = v4_1[v1_1];
                if (v2_1 < null) {
                    v2_1 += 256;
                }
                if (v2_1 < 16) {
                    v0_1.append("0");
                }
                v0_1.append(Integer.toHexString(v2_1));
                v1_1++;
            }
            return v0_1.toString().substring(8, 24);
        }
        return 0;
    }

    public static String e(String p4)
    {
        if ((p4 != null) && (p4.length() != 0)) {
            try {
                StringBuffer v0_4 = java.security.MessageDigest.getInstance("MD5");
                v0_4.update(p4.getBytes(java.nio.charset.Charset.forName("GBK")));
                String v4_2 = v0_4.digest();
                StringBuffer v0_1 = new StringBuffer("");
                int v1_1 = 0;
            } catch (String v4_4) {
                v4_4.printStackTrace();
            }
            while (v1_1 < v4_2.length) {
                String v2_1 = v4_2[v1_1];
                if (v2_1 < null) {
                    v2_1 += 256;
                }
                if (v2_1 < 16) {
                    v0_1.append("0");
                }
                v0_1.append(Integer.toHexString(v2_1));
                v1_1++;
            }
            return v0_1.toString();
        }
        return 0;
    }
}
