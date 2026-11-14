package gc;
public class b {
    public static String a = "http://mooc.chaoxing.com/";
    public static String b = "https://study-api.chaoxing.com/";
    public static String c = "https://robot.chaoxing.com/";
    public static String d = "https://mooc1-api.chaoxing.com/";
    public static int e = 0;
    public static String f = "http://course.fanya.chaoxing.com/";
    public static String g = "https://passport2-api.chaoxing.com/";
    public static String h = "https://detect.chaoxing.com/";
    public static String i = "https://fystat-ans.chaoxing.com/";
    public static String j = "https://fanyappfy.chaoxing.com/";
    public static String k = "https://mobilelearn.chaoxing.com/";
    public static String l = "https://x.chaoxing.com/";
    public static String m = "https://v0.chaoxing.com/";
    public static String n = "https://v1.chaoxing.com/";
    public static String o = "https://study-api.chaoxing.com/";
    public static String p = "chaoxing.com";
    public static final String q = "https://yz4.chaoxing.com/";
    public static final String r = "https://3wfy-ans.chaoxing.com/";
    public static String s = "https://mooc2-ans.chaoxing.com/";
    public static String t = "https://stat2-ans.chaoxing.com/";
    public static String u = "https://uc.chaoxing.com/";
    public static String v = "https://s99.ananas.chaoxing.com/";
    public static String w = "https://mooc-import-export-ans.chaoxing.com/";

    public static void c(boolean p0, String p1, String p2, String p3, String p4, String p5, String p6)
    {
        gc.b.e = p0;
        gc.b.a(p1);
        gc.b.d(p2);
        gc.b.e(p3);
        gc.b.f(p4);
        gc.b.g(p6);
        return;
    }

    public static void a(String p1)
    {
        if (com.fanzhou.util.u.l(p1)) {
            gc.b.f = "http://course.fanya.chaoxing.com/";
            return;
        } else {
            StringBuilder v0_2 = new StringBuilder();
            v0_2.append(p1);
            v0_2.append("/");
            gc.b.f = v0_2.toString();
            return;
        }
    }

    public static void d(String p1)
    {
        if (com.fanzhou.util.u.l(p1)) {
            gc.b.j = "https://fanyappfy.chaoxing.com/";
            return;
        } else {
            StringBuilder v0_2 = new StringBuilder();
            v0_2.append(p1);
            v0_2.append("/");
            gc.b.j = v0_2.toString();
            return;
        }
    }

    public static void e(String p3)
    {
        if (com.fanzhou.util.u.l(p3)) {
            gc.b.d = "https://mooc1-api.chaoxing.com/";
            gc.b.p = "chaoxing.com";
            return;
        } else {
            String v0_7 = new StringBuilder();
            v0_7.append(p3);
            v0_7.append("/");
            gc.b.d = v0_7.toString();
            String v0_3 = p3.indexOf(".");
            if (v0_3 > -1) {
                String v3_1 = p3.substring((v0_3 + 1));
                gc.b.p = v3_1;
                String v3_2 = v3_1.indexOf("/");
                if (v3_2 > -1) {
                    gc.b.p = gc.b.p.substring(0, v3_2);
                }
            }
            return;
        }
    }

    public static void f(String p1)
    {
        if (com.fanzhou.util.u.l(p1)) {
            gc.b.g = "https://passport2-api.chaoxing.com/";
            return;
        } else {
            StringBuilder v0_2 = new StringBuilder();
            v0_2.append(p1);
            v0_2.append("/");
            gc.b.g = v0_2.toString();
            return;
        }
    }

    public static void g(String p1)
    {
        if (com.fanzhou.util.u.l(p1)) {
            gc.b.i = "https://fystat-ans.chaoxing.com/";
            return;
        } else {
            StringBuilder v0_2 = new StringBuilder();
            v0_2.append(p1);
            v0_2.append("/");
            gc.b.i = v0_2.toString();
            return;
        }
    }

    static b()
    {
        return;
    }

    public b()
    {
        return;
    }

    public static void b(String p7, String p8, String p9, String p10, String p11, String p12)
    {
        gc.b.c(0, p7, p8, p9, p10, p11, p12);
        return;
    }
}
