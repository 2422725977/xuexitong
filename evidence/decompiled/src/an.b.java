package an;
public class b {
    public static final String a = "appProfile";
    public static final String b = "uniqueId";
    public static final String c = "SP_KEY_UNIQUE_INTEGER_ID";
    public static volatile String d;
    public static volatile int e;

    public static void a(android.content.Context p4)
    {
        if (an.b.d != null) {
            return;
        } else {
            if (an.b.d == null) {
                String v1_1 = r9.b.k(p4, "appProfile").h().getString("uniqueId", 0);
                if (v1_1 == null) {
                    v1_1 = r9.b.k(p4, "appProfile").getString("uniqueId", 0);
                } else {
                }
                if (v1_1 == null) {
                    v1_1 = java.util.UUID.randomUUID().toString().replaceAll("\\-", "");
                    r9.b.k(p4, "appProfile").h().g().f("uniqueId", v1_1).apply();
                } else {
                    if (v1_1.trim().length() < 8) {
                    }
                }
                an.b.d = v1_1;
            }
            return;
        }
    }

    public static void b(android.content.Context p4)
    {
        if (an.b.e != 0) {
            return;
        } else {
            if (an.b.e == 0) {
                int v1_1 = r9.b.k(p4, "appProfile").h().getInt("SP_KEY_UNIQUE_INTEGER_ID", 0);
                if (v1_1 == 0) {
                    v1_1 = r9.b.k(p4, "appProfile").getInt("SP_KEY_UNIQUE_INTEGER_ID", 0);
                } else {
                }
                if (v1_1 == 0) {
                    v1_1 = (java.util.UUID.randomUUID().toString().replaceAll("\\-", "").hashCode() & 2147483647);
                    r9.b.k(p4, "appProfile").h().g().d("SP_KEY_UNIQUE_INTEGER_ID", v1_1).apply();
                }
                an.b.e = v1_1;
            }
            return;
        }
    }

    public b()
    {
        return;
    }

    public static void c(android.content.Context p0)
    {
        an.b.a(p0);
        an.b.b(p0);
        return;
    }

    public static String d()
    {
        return an.b.d;
    }

    public static String e()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(an.b.e);
        v0_1.append("");
        return v0_1.toString();
    }

    public static int f()
    {
        return an.b.e;
    }
}
