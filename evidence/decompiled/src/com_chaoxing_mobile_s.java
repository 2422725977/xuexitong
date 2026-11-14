package com.chaoxing.mobile;
public class s {
    public static final String A = "https://contactsyd.chaoxing.com/";
    public static final String B = "https://structureyd.chaoxing.com/";
    public static final String C = "https://money.chaoxing.com";
    public static final String D = "https://specie.chaoxing.com/";
    public static final String a = "20220629";
    public static final String b = "https://passport2.chaoxing.com/";
    public static final String c = "https://passport2-api.chaoxing.com/";
    public static final String d = "https://mobilelearn.chaoxing.com/";
    public static final String e = "https://resource.chaoxing.com/";
    public static final String f = "https://live.chaoxing.com/";
    public static final String g = "https://groupweb.chaoxing.com/";
    public static final String h = "https://yz4.chaoxing.com/";
    public static final String i = "https://fystat-ans.chaoxing.com/";
    public static final String j = "https://zhibo.chaoxing.com/";
    public static final String k = "https://xuexitong.chaoxing.com/";
    public static final String l = "https://x.chaoxing.com/";
    public static final String m = "https://ke.chaoxing.com/";
    public static final String n = "https://learn.chaoxing.com/";
    public static final String o = "https://learn.chaoxing.com/";
    public static final String p = "https://study-api.chaoxing.com/";
    public static final String q = "https://im.chaoxing.com/";
    public static final String r = "https://special.rhky.com/";
    public static final String s = "https://useryd.chaoxing.com/";
    public static final String t = "https://fanya.zyk2.chaoxing.com/";
    public static final String u = "https://v1.chaoxing.com/";
    public static String v = "https://mooc1-api.chaoxing.com/";
    public static final String w = "274";
    public static final String x = "https://img1.16q.cn/";
    public static final String y = "https://lcyd.chaoxing.com/";
    public static final String z = "https://learn.chaoxing.com/";

    public static String f9(String p2, String[] p3, String[] p4, boolean p5)
    {
        if (p5 == null) {
            if ((p3 != null) && (p3.length != 0)) {
                StringBuilder v5_3 = new StringBuilder(p2);
                int v2_1 = 0;
                while (v2_1 < p3.length) {
                    String v0_0 = p4[v2_1];
                    if (v0_0 == null) {
                        v0_0 = "";
                    }
                    v5_3.append(p3[v2_1]);
                    v5_3.append("=");
                    v5_3.append(v0_0);
                    if (v2_1 < (p3.length - 1)) {
                        v5_3.append("&");
                    }
                    v2_1++;
                }
                p2 = v5_3.toString();
            }
            return p2;
        } else {
            return com.chaoxing.mobile.s.A8(p2, p3, p4);
        }
    }

    public static String x8(String p1)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(p1);
        v0_1.append(com.fanzhou.util.y.X());
        return v0_1.toString();
    }

    public static String A8(String p1, String[] p2, String[] p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(p1);
        v0_1.append(com.fanzhou.util.y.W(p2, p3));
        return v0_1.toString();
    }

    public static String Bc(String p4, String p5, int p6, String p7)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p7));
        v0_1.append("apis/topic/getTopic?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"topicId", "puid", "maxW", "version"}), new String[] {p4, p5, String.valueOf(p6), "20180323"}));
    }

    public static String y8(String p1, java.util.List p2)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(p1);
        v0_1.append(com.fanzhou.util.y.U(p2));
        return v0_1.toString();
    }

    public static String z8(String p1, String[] p2, Object[] p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(p1);
        v0_1.append(com.fanzhou.util.y.V(p2, p3));
        return v0_1.toString();
    }

    public static String F4(String p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/circle/getCircle?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "puid", "maxW"}), new String[] {p4, p5, v2_2.toString()}));
    }

    public static String e9(String p1, String[] p2, String[] p3)
    {
        return com.chaoxing.mobile.s.f9(p1, p2, p3, 1);
    }

    public static String C9(String p8, String p9, int p10, int p11, String p12, int p13, String p14)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/getCircleList?");
        String v0_2 = v0_1.toString();
        String v3 = "page";
        String v5 = "kw";
        String.valueOf(p10);
        String.valueOf(p11);
        String.valueOf(p13);
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"uid", "categoryId"}), new String[] {p8, p14}));
    }

    public static String F3(String p7, String p8, int p9, String p10)
    {
        int v0_3 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.d.b().a(p7));
        v1_2.append("apis/topic_folder/addTopicFolder?");
        String v1_0 = v1_2.toString();
        Integer v9_1 = Integer.valueOf(p9);
        Object[] v3_2 = new Object[5];
        v3_2[0] = v0_3;
        v3_2[1] = p7;
        v3_2[2] = p8;
        v3_2[3] = v9_1;
        v3_2[4] = p10;
        return com.chaoxing.mobile.s.z8(v1_0, new String[] {"puid", "circleId", "name", "pid", "ftag"}), v3_2);
    }

    public static String J9(int p4, String p5, long p6, int p8)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        String v6_1 = v2_1.toString();
        StringBuilder v7_1 = new StringBuilder();
        v7_1.append(p8);
        v7_1.append("");
        return com.chaoxing.mobile.s.f9("https://resource.chaoxing.com/apis/cloud/getRecs.jspx?", new String[] {"ownertype", "ownerId", "pid", "recType"}), new String[] {v1_1, p5, v6_1, v7_1.toString()}), 1);
    }

    public static String M9(String p1)
    {
        if (com.fanzhou.util.w.q(p1)) {
            p1 = "";
        }
        return p1;
    }

    public static String K3(String p8, String p9, int p10, int p11)
    {
        return com.chaoxing.mobile.s.W3("-1", p8, "custom", "", "", p9, p10, p11);
    }

    public static String W3(String p13, String p14, String p15, String p16, String p17, String p18, int p19, int p20)
    {
        int v2 = "fid";
        String v4 = "level";
        String v6 = "pageSize";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append("");
        v1_1.append(p19);
        v1_1.toString();
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append("");
        v1_3.append(p20);
        v1_3.toString();
        String v10 = "2";
        v6 = p16;
        String v11 = p18;
        return com.chaoxing.mobile.s.f9("https://contactsyd.chaoxing.com/apis/dept/getDepts?", new String[] {"puid", "addHideUserTag"}), new String[] {p14, "1"}), 1);
    }

    public static String P7(android.content.Context p6, int p7)
    {
        String v0_1 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v7_1 = com.fanzhou.document.c.b(p7);
        Integer v2_0 = Integer.valueOf(1);
        Integer v3_1 = Integer.valueOf(20000);
        Object[] v4_1 = new Object[4];
        v4_1[0] = v0_1;
        v4_1[1] = v7_1;
        v4_1[2] = v2_0;
        v4_1[3] = v3_1;
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/scribe/getUserScribes?", new String[] {"uid", "st", "cpage", "pageSize"}), v4_1);
    }

    public static String pa(android.content.Context p6, int p7, String p8, int p9, int p10)
    {
        return com.chaoxing.mobile.s.A9(com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getFid(), p7, p9, p8, p10);
    }

    public static String U3(String p6, String p7, int p8)
    {
        int v0_3 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.d.b().a(p6));
        v1_2.append("apis/topic_folder/deleteTopicFolder?");
        String v1_0 = v1_2.toString();
        Integer v8_1 = Integer.valueOf(p8);
        Object[] v3_2 = new Object[4];
        v3_2[0] = v0_3;
        v3_2[1] = p6;
        v3_2[2] = p7;
        v3_2[3] = v8_1;
        return com.chaoxing.mobile.s.z8(v1_0, new String[] {"puid", "circleId", "folderId", "delAll"}), v3_2);
    }

    public static varargs String L1(String p0, Object[] p1)
    {
        return String.format(p0, p1);
    }

    public static String Z1(int p4, int p5, int p6, int p7)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        int v5_1 = v2_1.toString();
        StringBuilder v2_4 = new StringBuilder();
        v2_4.append(p6);
        v2_4.append("");
        String v6_1 = v2_4.toString();
        StringBuilder v2_6 = new StringBuilder();
        v2_6.append(p7);
        v2_6.append("");
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/v2apis/friend/getFollowers?", new String[] {"isfollower", "topsign", "page", "pageSize"}), new String[] {v1_1, v5_1, v6_1, v2_6.toString()}), 1);
    }

    public static String X3(android.content.Context p13, String p14, String p15, int p16, int p17, String p18)
    {
        com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v11 = "pageSize";
        String v7 = "deptid";
        String v9 = "uid";
        com.chaoxing.study.account.AccountManager.C().D().getFid();
        int v0_3 = new StringBuilder();
        v0_3.append(p16);
        v0_3.append("");
        v0_3.toString();
        int v0_5 = new StringBuilder();
        v0_5.append(p17);
        v0_5.append("");
        v0_5.toString();
        String v3 = p15;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/v2apis/roster/getUsers?", new String[] {"type", "mcode"}), new String[] {"bycata", p18}), 1);
    }

    public static String g4(String[] p1, String[] p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/updateCustomFolder.jspx?", p1, p2);
    }

    public static String ka(String p3, String p4, String p5, String p6)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/topic_folder/addTopicToFolder?");
        String v6_1 = v0_1.toString();
        Object[] v1_2 = new Object[3];
        v1_2[0] = p3;
        v1_2[1] = p4;
        v1_2[2] = p5;
        return com.chaoxing.mobile.s.z8(v6_1, new String[] {"puid", "uuid", "folderId"}), v1_2);
    }

    public static String A9(String p16, String p17, int p18, int p19, String p20, int p21)
    {
        String v4_1 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(v4_1)) {
            String v3_2 = new StringBuilder();
            v3_2.append(pk.a.e);
            v3_2.append("apis/circle/myJoinCircles4?");
            String v8 = v3_2.toString();
            String v11 = "maxW";
            String v13 = "fields";
            String v3_4 = new StringBuilder();
            v3_4.append(p18);
            v3_4.append("");
            v3_4.toString();
            String v0_2 = new StringBuilder();
            v0_2.append(p19);
            v0_2.append("");
            v0_2.toString();
            String v0_4 = new StringBuilder();
            v0_4.append(p21);
            v0_4.append("");
            v0_4.toString();
            String v5 = p20;
            return com.chaoxing.mobile.s.A8(v8, new String[] {"uid", "order"}), new String[] {p16, "4"}));
        } else {
            String v3_7 = new StringBuilder();
            v3_7.append(pk.a.e);
            v3_7.append("apis/circle/myJoinCircles4?");
            String v3_9 = v3_7.toString();
            String[] v9 = "maxW";
            v11 = "fields";
            String v5_2 = new StringBuilder();
            v5_2.append(p18);
            v5_2.append("");
            v5_2.toString();
            String v5_4 = new StringBuilder();
            v5_4.append(p19);
            v5_4.append("");
            v5_4.toString();
            String v1_3 = new StringBuilder();
            v1_3.append(p21);
            v1_3.append("");
            v1_3.toString();
            v8 = p20;
            return com.chaoxing.mobile.s.A8(v3_9, new String[] {"puid", "order"}), new String[] {v4_1, "4"}));
        }
    }

    public static String t1(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/topic/deleteTopic?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"circleId", "puid", "topicId"}), new String[] {p4, p5, p6}));
    }

    public static String w3(String[] p1, String[] p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/addCustomFolder.jspx?", p1, p2);
    }

    public static String Kb()
    {
        return com.chaoxing.mobile.s.x8("https://money.chaoxing.com/purse/api/ds/selectMoney?");
    }

    static s()
    {
        return;
    }

    public s()
    {
        return;
    }

    public static String A(String p3)
    {
        return com.chaoxing.mobile.s.f9("https://contactsyd.chaoxing.com/apis/dept/addUserDept4Server?", new String[] {"deptid"}), new String[] {p3}), 1);
    }

    public static String A0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/testPaper/preAddQuestion?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String A1(String p2, String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/updateDept?", new String[] {"name", "deptid"}), new String[] {p2, p3}), 1);
    }

    public static String A2(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://live.chaoxing.com/liveAPI/allLivingByChatId?chatId=%s", v0_1);
    }

    public static String A3()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/addCircle2?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String A4(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "showChatRoom"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "showChatRoom"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String A5(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://x.chaoxing.com/course/begin?classId=%s", v0_1);
    }

    public static String A6(android.content.Context p14, int p15, String p16, boolean p17, String p18, int p19, int p20)
    {
        String v6 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v14_5 = new StringBuilder();
        v14_5.append(pk.a.f);
        v14_5.append("apis/notice/getReaders?");
        String v14_1 = v14_5.toString();
        String v9 = "isread";
        String v11 = "page";
        String[] v0_2 = new StringBuilder();
        v0_2.append(p15);
        v0_2.append("");
        String[] v0_3 = v0_2.toString();
        // Both branches of the condition point to the same code.
        // if (!p17) {
            String v3_1 = new StringBuilder();
            v3_1.append(p19);
            v3_1.append("");
            v3_1.toString();
            String v3_3 = new StringBuilder();
            v3_3.append(p20);
            v3_3.append("");
            v3_3.toString();
            String v1 = p16;
            return com.chaoxing.mobile.s.A8(v14_1, new String[] {"noticeId", "puid"}), new String[] {v0_3, v6}));
        // }
    }

    public static String A7()
    {
        return "https://mooc1.chaoxing.com/ananas/ueditor/dialogs/insertziliao/ziliao/teachingResourceLibrary.html#";
    }

    public static String Aa(int p10, String p11, String p12, int p13, int p14, int p15, int p16, String p17)
    {
        if (!com.fanzhou.util.w.s(p17)) {
            String v0_7 = new StringBuilder();
            v0_7.append(pk.a.f);
            v0_7.append("apis/notice/getReplys?");
            String v8_0 = v0_7.toString();
            String v2 = "puid";
            String v4 = "pageSize";
            String v0_2 = String.valueOf(p10);
            String.valueOf(p13);
            String.valueOf(p14);
            String.valueOf(p15);
            String.valueOf(p16);
            String v1 = p11;
            return com.chaoxing.mobile.s.A8(v8_0, new String[] {"noticeId", "from"}), new String[] {v0_2, p17}));
        } else {
            String v0_5 = new StringBuilder();
            v0_5.append(pk.a.f);
            v0_5.append("apis/notice/getReplys?");
            String v0_6 = v0_5.toString();
            String v3 = "puid";
            String v5 = "pageSize";
            String v2_1 = String.valueOf(p10);
            String.valueOf(p13);
            String.valueOf(p14);
            String.valueOf(p15);
            v4 = p12;
            return com.chaoxing.mobile.s.A8(v0_6, new String[] {"noticeId", "maxW"}), new String[] {v2_1, String.valueOf(p16)}));
        }
    }

    public static String Ab()
    {
        return com.chaoxing.mobile.s.x8("https://mobilelearn.chaoxing.com/newdiscuss/saveDiscussForCli?");
    }

    public static String Ac(String p3, String p4, String p5, int p6, String p7)
    {
        if (!com.fanzhou.util.w.s(p4)) {
            String v3_5 = new StringBuilder();
            v3_5.append(pk.d.b().a(p7));
            v3_5.append("apis/topic/getTopic?");
            return com.chaoxing.mobile.s.A8(v3_5.toString(), new String[] {"uuid", "puid", "maxW", "version"}), new String[] {p4, p5, String.valueOf(p6), "20180323"}));
        } else {
            return com.chaoxing.mobile.s.Bc(p3, p5, p6, p7);
        }
    }

    public static String Ad(java.util.List p1)
    {
        return com.chaoxing.mobile.s.y8("https://passport2-api.chaoxing.com/api/xxtforset?", p1);
    }

    public static String B()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.d);
        v0_1.append("apis/usersgroup/addUsersGroup?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String B0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/testPaper/preAddQuestion?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String B1(long p5, String p7)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.e);
        v1_2.append("apis/circle_folder/updateCircleFolder?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"uid", "id", "name"}), new String[] {v0_2, String.valueOf(p5), p7}));
    }

    public static String B2(String p2, String p3)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/right/checkResdataRights.jspx?", new String[] {"key", "cataid"}), new String[] {p2, p3}));
    }

    public static String B3(String p11, int p12, String p13, String p14, int p15, int p16, int p17, int p18)
    {
        String v1 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.e);
        v0_4.append("apis/circle/addCircle?");
        String v0_1 = v0_4.toString();
        String v4 = "check";
        String v6 = "introduce";
        String v8 = "isShowCircleCloud";
        String v2_3 = new StringBuilder();
        v2_3.append(p12);
        v2_3.append("");
        v2_3.toString();
        String v2_5 = new StringBuilder();
        v2_5.append(p15);
        v2_5.append("");
        v2_5.toString();
        StringBuilder v15_2 = new StringBuilder();
        v15_2.append(p16);
        v15_2.append("");
        v15_2.toString();
        StringBuilder v15_4 = new StringBuilder();
        v15_4.append(p17);
        v15_4.append("");
        v15_4.toString();
        StringBuilder v15_6 = new StringBuilder();
        v15_6.append(p18);
        v15_6.append("");
        v4 = p13;
        return com.chaoxing.mobile.s.A8(v0_1, new String[] {"puid", "showQrcode"}), new String[] {v1, v15_6.toString()}));
    }

    public static String B4(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "showGroupChat"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "showGroupChat"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String B5(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://x.chaoxing.com/scannerPage?classId=%s", v0_1);
    }

    public static String B6(android.content.Context p24, String p25, int p26, String p27, String p28, int p29, String p30, int p31, int p32, String p33, String p34, String p35, int p36, int p37)
    {
        com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.f);
        v0_4.append("apis/notice/myNotices_v2?");
        String v0_1 = v0_4.toString();
        String v12 = "kw";
        String v14 = "contSize";
        String v16 = "page";
        String v18 = "puid";
        String v20 = "read";
        String[] v1_2 = new StringBuilder();
        v1_2.append(p26);
        v1_2.append("");
        v1_2.toString();
        String v3_1 = new StringBuilder();
        v3_1.append(p29);
        v3_1.append("");
        v3_1.toString();
        String v3_3 = new StringBuilder();
        v3_3.append(p31);
        v3_3.append("");
        v3_3.toString();
        String v3_5 = new StringBuilder();
        v3_5.append(p32);
        v3_5.append("");
        v3_5.toString();
        String v3_7 = new StringBuilder();
        v3_7.append(p36);
        v3_7.append("");
        v3_7.toString();
        String v3_9 = new StringBuilder();
        v3_9.append(p37);
        v3_9.append("");
        String v4 = p28;
        String v10 = p33;
        v12 = p35;
        return com.chaoxing.mobile.s.A8(v0_1, new String[] {"type", "folderId"}), new String[] {p25, v3_9.toString()}));
    }

    public static String B7(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://yz4.chaoxing.com/circlemarket/index?channelId=1000000616&name=%s&fid=%s", v0_1);
    }

    public static String B8(String p4, String p5, int p6, int p7, String p8)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/topic/getTopicCheck?");
        String v8_1 = v0_1.toString();
        Integer v6_1 = Integer.valueOf(p6);
        Integer v7_1 = Integer.valueOf(p7);
        Object[] v1_2 = new Object[4];
        v1_2[0] = p5;
        v1_2[1] = p4;
        v1_2[2] = v6_1;
        v1_2[3] = v7_1;
        return com.chaoxing.mobile.s.z8(v8_1, new String[] {"uuid", "puid", "maxW", "checkStatus"}), v1_2);
    }

    public static String B9(String p7, String p8, int p9, String p10)
    {
        if (p10 == null) {
            p10 = "";
        }
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.e);
        v1_2.append("apis/circle/myJoinCircles5?");
        String v1_0 = v1_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"puid", "fid", "order", "maxW", "sign"}), new String[] {p7, p8, "4", v3_2.toString(), p10}));
    }

    public static String Ba()
    {
        return "https://mobilelearn.chaoxing.com/widget/teachingPlan/cloudPptBeginClass";
    }

    public static String Bb()
    {
        return com.chaoxing.mobile.s.x8("https://mobilelearn.chaoxing.com/widget/apis/renwu/setRenWuTitleAndContent?");
    }

    public static String Bd(String p6, String p7, int p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "isShowCompanyValue"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "isShowCompanyValue"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String C(int p2, String p3)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p2);
        v1_3.append("");
        return com.chaoxing.mobile.s.f9("https://resource.chaoxing.com/apis/cloud/getFolderHierarchy.jspx?", new String[] {"ownertype", "ownerId"}), new String[] {v1_3.toString(), p3}), 1);
    }

    public static String C0()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/subscribe/addCustomFolder.jspx?");
    }

    public static String C1()
    {
        return com.chaoxing.mobile.s.x8("https://resource.chaoxing.com/apis/cloud/editFolder.jspx?");
    }

    public static String C2(String p3, String p4, String p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("api/crcStorageStatus?puid=%s&crc=%s&_token=%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[3];
        v1_3[0] = p3;
        v1_3[1] = p4;
        v1_3[2] = p5;
        return String.format(v0_2, v1_3);
    }

    public static String C3(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/sendNotice?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "uuid"}), new String[] {p3, p4}));
    }

    public static String C4(String p3, String p4, String p5, int p6)
    {
        if (!com.fanzhou.util.w.s(p4)) {
            String v3_5 = new StringBuilder();
            v3_5.append(pk.d.b().a(p4));
            v3_5.append("apis/circle/getCircle?");
            String v3_1 = v3_5.toString();
            StringBuilder v1_2 = new StringBuilder();
            v1_2.append(p6);
            v1_2.append("");
            return com.chaoxing.mobile.s.A8(v3_1, new String[] {"bbsid", "puid", "maxW"}), new String[] {p4, p5, v1_2.toString()}));
        } else {
            return com.chaoxing.mobile.s.F4(p3, p5, p6);
        }
    }

    public static String C5(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://x.chaoxing.com/scannerPage?courseId=%s", v0_1);
    }

    public static String C6(android.content.Context p4, String p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/getNoticeSendAuth?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "sourceType", "noticeId"}), new String[] {v4_4, p5, p6}));
    }

    public static String C7()
    {
        return com.chaoxing.mobile.s.x8("https://mc.m.5read.com/apis/rss/rssCataList.jspx");
    }

    public static String C8(String p8, String p9, int p10, String p11, String p12, int p13, String p14)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/topic/getTopicCheckListWithPoff?");
        String v0_2 = v0_1.toString();
        int v3 = "maxW";
        String v5 = "kw";
        Integer v10_1 = Integer.valueOf(p10);
        Integer v13_1 = Integer.valueOf(p13);
        Object[] v2_1 = new Object[7];
        v2_1[0] = p8;
        v2_1[1] = p9;
        v2_1[2] = v10_1;
        v2_1[3] = p11;
        v2_1[4] = p12;
        v2_1[5] = v13_1;
        v2_1[6] = p14;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"bbsid", "lastValue"}), v2_1);
    }

    public static String Ca(String p5, String p6, int p7, int p8)
    {
        if (p8 == -1) {
            Integer v7_2 = Integer.valueOf(p7);
            Object[] v8_2 = new Object[3];
            v8_2[0] = p5;
            v8_2[1] = p6;
            v8_2[2] = v7_2;
            return String.format("https://x.chaoxing.com/apis/toScreen/courseChapterToScreen?courseId=%s&chapterId=%s&opt=%d", v8_2);
        } else {
            Integer v7_1 = Integer.valueOf(p7);
            Object[] v8_1 = Integer.valueOf(1);
            Object[] v0_2 = new Object[4];
            v0_2[0] = p5;
            v0_2[1] = p6;
            v0_2[2] = v7_1;
            v0_2[3] = v8_1;
            return String.format("https://x.chaoxing.com/apis/toScreen/courseChapterToScreen?courseId=%s&chapterId=%s&opt=%d&openInCurrent=%d", v0_2);
        }
    }

    public static String Cb(int p6, String p7, String p8, long p9)
    {
        if (p6 != null) {
            StringBuilder v10_1 = new StringBuilder();
            v10_1.append(p6);
            v10_1.append("");
            return com.chaoxing.mobile.s.A8("https://mobilelearn.chaoxing.com/ppt/taskAPI/saveAndFindPlantId?", new String[] {"type", "courseId", "uid"}), new String[] {v10_1.toString(), p7, p8}));
        } else {
            StringBuilder v1_2 = new StringBuilder();
            v1_2.append(p6);
            v1_2.append("");
            String v6_4 = v1_2.toString();
            StringBuilder v1_4 = new StringBuilder();
            v1_4.append(p9);
            v1_4.append("");
            return com.chaoxing.mobile.s.A8("https://mobilelearn.chaoxing.com/ppt/taskAPI/saveAndFindPlantId?", new String[] {"type", "courseId", "uid", "planId"}), new String[] {v6_4, p7, p8, v1_4.toString()}));
        }
    }

    public static String Cc(String p14, String p15, String p16, int p17, int p18, String p19, int p20, String p21, String p22)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p16));
        v0_1.append("apis/label/getLabelTopicByPoff?");
        String v0_2 = v0_1.toString();
        String v7 = "bbsid";
        String v9 = "order";
        String v11 = "pageSize";
        String.valueOf(p17);
        String v2_1 = new StringBuilder();
        v2_1.append(p18);
        v2_1.append("");
        v2_1.toString();
        String.valueOf(p20);
        v7 = p19;
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "tags"}), new String[] {p14, p22}));
    }

    public static String Cd(android.content.Context p2)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("apis/other/uploadFile?");
        return com.chaoxing.mobile.s.e9(v0_2.toString(), new String[] {"puid"}), new String[] {v2_4}));
    }

    public static String D(String p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/user/atToMes?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid"}), new String[] {p2}));
    }

    public static String D0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/selection/preAddSelect?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String D1()
    {
        return "https://mobilelearn.chaoxing.com/widget/coursewareActive/changeActiveName?";
    }

    public static String D2(String p2, String p3, String p4, String p5)
    {
        if (!ve.f.o(p2)) {
            p2 = pk.a.a;
        }
        Object[] v0_4 = new StringBuilder();
        v0_4.append(p2);
        v0_4.append("api/crcStorageStatus?puid=%s&crc=%s&_token=%s");
        String v2_1 = v0_4.toString();
        Object[] v0_2 = new Object[3];
        v0_2[0] = p3;
        v0_2[1] = p4;
        v0_2[2] = p5;
        return String.format(v2_1, v0_2);
    }

    public static String D3()
    {
        return "https://homewh.chaoxing.com/home/tools/more?type=chuangzuo";
    }

    public static String D4(java.util.List p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p3));
        v0_1.append("apis/circle/getCircle?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String D5(android.content.Context p5, int p6, String p7)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/pptTestPaper/preAddQuestion?", new String[] {"tid", "uid", "appType", "courseId"}), new String[] {v5_4, v0_0, v2_2.toString(), p7}), 0);
    }

    public static String D6(String p2, int p3)
    {
        Integer v3_1 = Integer.valueOf(p3);
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = v3_1;
        return String.format("https://x.chaoxing.com/apis/toScreen/noticeToScreen?idCode=%s&opt=%s", v0_1);
    }

    public static String D7()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/scribe/getScribeRssRecomm");
    }

    public static String D8(String p8, String p9, int p10, String p11, String p12, int p13, String p14)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/topic/getTopicCheckListWithPoff2?");
        String v0_2 = v0_1.toString();
        int v3 = "maxW";
        String v5 = "kw";
        Integer v10_1 = Integer.valueOf(p10);
        Integer v13_1 = Integer.valueOf(p13);
        Object[] v2_1 = new Object[7];
        v2_1[0] = p8;
        v2_1[1] = p9;
        v2_1[2] = v10_1;
        v2_1[3] = p11;
        v2_1[4] = p12;
        v2_1[5] = v13_1;
        v2_1[6] = p14;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"bbsid", "lastValue"}), v2_1);
    }

    public static String D9(String p7, String p8, int p9, int p10, int p11, String p12)
    {
        return com.chaoxing.mobile.s.C9(p7, p8, p9, p10, "", p11, p12);
    }

    public static String Da(String p6, String p7, int p8, int p9, int p10)
    {
        if (p10 == -1) {
            Integer v8_2 = Integer.valueOf(p8);
            Integer v9_1 = Integer.valueOf(p9);
            Object[] v10_1 = new Object[4];
            v10_1[0] = p6;
            v10_1[1] = p7;
            v10_1[2] = v8_2;
            v10_1[3] = v9_1;
            return String.format("https://x.chaoxing.com/apis/toScreen/courseChapterToScreen?courseId=%s&chapterId=%s&num=%d&opt=%d", v10_1);
        } else {
            Integer v8_1 = Integer.valueOf(p8);
            Integer v9_2 = Integer.valueOf(p9);
            Object[] v10_2 = Integer.valueOf(1);
            Object[] v0_2 = new Object[5];
            v0_2[0] = p6;
            v0_2[1] = p7;
            v0_2[2] = v8_1;
            v0_2[3] = v9_2;
            v0_2[4] = v10_2;
            return String.format("https://x.chaoxing.com/apis/toScreen/courseChapterToScreen?courseId=%s&chapterId=%s&num=%d&opt=%d&openInCurrent=%d", v0_2);
        }
    }

    public static String Db()
    {
        return "https://mobilelearn.chaoxing.com/ppt/activeAPI/copyActive?";
    }

    public static String Dc(String p21, String p22, String p23, int p24, String p25, int p26, String p27, String p28, String p29, int p30, int p31)
    {
        String v6_0;
        if (android.text.TextUtils.isEmpty(p29)) {
            v6_0 = p29;
        } else {
            v6_0 = p29;
            if (p29.equals("0")) {
                String v2_1 = new StringBuilder();
                v2_1.append(pk.d.b().a(p21));
                v2_1.append("apis/topic/getTopicListWithPoff?");
                String v9_1 = v2_1.toString();
                String v12 = "puid";
                String v14 = "maxW";
                String v16 = "pageSize";
                String.valueOf(p24);
                String.valueOf(p26);
                String v2_3 = new StringBuilder();
                v2_3.append(p30);
                v2_3.append("");
                String v2 = p22;
                String v5 = p25;
                return com.chaoxing.mobile.s.A8(v9_1, new String[] {"bbsid", "order"}), new String[] {p21, v2_3.toString()}));
            }
        }
        if (android.text.TextUtils.isEmpty(v6_0)) {
            String v3_5 = new StringBuilder();
            v3_5.append(pk.d.b().a(p21));
            v3_5.append("apis/topic/getTopicListWithPoff?");
            String v10_2 = v3_5.toString();
            String v13 = "puid";
            String v15 = "maxW";
            String v17 = "pageSize";
            String.valueOf(p24);
            String.valueOf(p26);
            String v3_8 = new StringBuilder();
            v3_8.append(p30);
            v3_8.append("");
            v3_8.toString();
            String v1_2 = new StringBuilder();
            v1_2.append(p31);
            v1_2.append("");
            String v3 = p23;
            String v1 = p27;
            return com.chaoxing.mobile.s.A8(v10_2, new String[] {"bbsid", "searchType"}), new String[] {p21, v1_2.toString()}));
        } else {
            String v3_10 = new StringBuilder();
            v3_10.append(pk.d.b().a(p21));
            v3_10.append("apis/topic/getTopicListWithPoff?");
            String v10_3 = v3_10.toString();
            v13 = "puid";
            v15 = "maxW";
            v17 = "pageSize";
            String.valueOf(p24);
            String.valueOf(p26);
            String v3_13 = new StringBuilder();
            v3_13.append(p30);
            v3_13.append("");
            v3_13.toString();
            String v1_4 = new StringBuilder();
            v1_4.append(p31);
            v1_4.append("");
            v3 = p23;
            String v7 = p28;
            return com.chaoxing.mobile.s.A8(v10_3, new String[] {"bbsid", "searchType"}), new String[] {p21, v1_4.toString()}));
        }
    }

    public static String Dd(android.content.Context p2)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("apis/other/uploadMedia?");
        return com.chaoxing.mobile.s.e9(v0_2.toString(), new String[] {"puid"}), new String[] {v2_4}));
    }

    public static String E(String p6, String p7, String p8, String p9)
    {
        if (!com.fanzhou.util.w.q(p7)) {
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/friend/addUserFollowEachOther?", new String[] {"puid", "followedPuid", "from", "noSendMsg"}), new String[] {p6, p7, p9, "1"}));
        } else {
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/friend/addUserFollowEachOther?", new String[] {"puid", "followedUid", "from", "noSendMsg"}), new String[] {p6, p8, p9, "1"}));
        }
    }

    public static String E0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/noticeselection/produceview?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String E1()
    {
        return "https://yz4.chaoxing.com/selfBuiltProject/addOrUpdateFolder";
    }

    public static String E2(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://fanya.zyk2.chaoxing.com/mobile/prep/searchMoocName?title=%s&type=8&courseid=%s#INNER", v0_1);
    }

    public static String E3(String p6, String p7, String p8, int p9, String p10)
    {
        if (!com.fanzhou.util.w.s(p7)) {
            String v6_9 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
            String v0_1 = new StringBuilder();
            v0_1.append(pk.d.b().a(p7));
            v0_1.append("apis/topic_folder/addTopicFolder?");
            String v0_2 = v0_1.toString();
            Integer v9_1 = Integer.valueOf(p9);
            Object[] v2_2 = new Object[5];
            v2_2[0] = v6_9;
            v2_2[1] = p7;
            v2_2[2] = p8;
            v2_2[3] = v9_1;
            v2_2[4] = p10;
            return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "bbsid", "name", "pid", "ftag"}), v2_2);
        } else {
            return com.chaoxing.mobile.s.F3(p6, p8, p9, p10);
        }
    }

    public static String E4(String p5, String p6, int p7, int p8, String p9, String p10)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p10));
        v0_1.append("apis/circle/getCircle2?");
        String v10_1 = v0_1.toString();
        String v1_2 = new StringBuilder();
        v1_2.append(p7);
        v1_2.append("");
        String v1_3 = v1_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p8);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v10_1, new String[] {"info", "uid", "maxW", "stype", "sinfo"}), new String[] {p5, p6, v1_3, v2_2.toString(), p9}));
    }

    public static String E5(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p3;
        v0_1[1] = p2;
        return String.format("https://mobilelearn.chaoxing.com/task/getStuWorkAndExamSkipUrl?courseId=%s&classId=%s#INNER", v0_1);
    }

    public static String E6()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/scribe/getScribeNpRecs");
    }

    public static String E7(android.content.Context p5, String p6, int p7, int p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_note/getOpenedNote?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p7);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p8);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "s_noteId", "from", "maxW"}), new String[] {v5_4, p6, v2_3, v3_2.toString()}));
    }

    public static String E8(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/topic_folder/getTopicFolderTree?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"circleId", "ftags", "puid"}), new String[] {p4, p5, p6}));
    }

    public static String E9(String p9, String p10, String p11, int p12, int p13, int p14)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p10));
        v0_1.append("apis/circle/circleMems?");
        String v0_2 = v0_1.toString();
        String v3 = "uid";
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p12);
        v2_1.append("");
        v2_1.toString();
        String.valueOf(p13);
        String v5 = p11;
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "pageSize"}), new String[] {p9, String.valueOf(p14)}));
    }

    public static String Ea()
    {
        return "https://x.chaoxing.com/apis/toScreen/sendCmdToClient";
    }

    public static String Eb(String p10, String p11, String p12, String p13, int p14, int p15, int p16)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p11));
        v0_1.append("apis/circle/circleMems?");
        String v0_2 = v0_1.toString();
        String v3 = "uid";
        String v5 = "order";
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p14);
        v2_1.append("");
        v2_1.toString();
        String.valueOf(p15);
        v5 = p12;
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "pageSize"}), new String[] {p10, String.valueOf(p16)}));
    }

    public static String Ec(int p11, String p12, String p13, int p14, int p15, int p16, int p17, String p18, String p19)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/topic/getTopicList?");
        String v0_2 = v0_1.toString();
        String v3 = "uid";
        String v5 = "maxW";
        String v7 = "page";
        String v2 = String.valueOf(p11);
        String.valueOf(p14);
        String.valueOf(p15);
        String.valueOf(p16);
        String.valueOf(p17);
        String v4 = p12;
        v3 = p18;
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "tags"}), new String[] {v2, p19}));
    }

    public static String Ed(android.content.Context p21, String p22, String p23, String p24, int p25, int p26, double p27, boolean p29, String p30, String p31, int p32, String p33, String p34, String p35, String p36, String p37, String p38, int p39)
    {
        String[] v1_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.c);
        v0_4.append("apis/note_notebook/uploadNotebook?");
        String v0_1 = v0_4.toString();
        String v4 = "name";
        String v6 = "openedState";
        String v8 = "sort";
        String v10 = "friendsGroupIds";
        String v12 = "version";
        String v14 = "usersGroupId";
        String v16 = "tag";
        String v3_1 = new StringBuilder();
        v3_1.append(p22);
        v3_1.append("");
        v3_1.toString();
        String v5_1 = new StringBuilder();
        v5_1.append(p25);
        v5_1.append("");
        v5_1.toString();
        String v6_2 = new StringBuilder();
        v6_2.append(p26);
        v6_2.append("");
        v6_2.toString();
        String v7_2 = new StringBuilder();
        v7_2.append(p27);
        v7_2.append("");
        v7_2.toString();
        // Both branches of the condition point to the same code.
        // if (!p29) {
            String v9_1 = new StringBuilder();
            v9_1.append(p32);
            v9_1.append("");
            v9_1.toString();
            String v9_3 = new StringBuilder();
            v9_3.append(p39);
            v9_3.append("");
            String v9 = p30;
            v12 = p33;
            v14 = p35;
            v16 = p37;
            String v3 = p23;
            return com.chaoxing.mobile.s.A8(v0_1, new String[] {"puid", "category"}), new String[] {v1_0, v9_3.toString()}));
        // }
    }

    public static String F(String p2, String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/bindDeptCircleid?", new String[] {"deptid", "circleid"}), new String[] {p2, p3}), 1);
    }

    public static String F0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/sign/produceSignView?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String F1(String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/closeDeptIncode?", new String[] {"deptid"}), new String[] {p3}), 1);
    }

    public static String F2()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/getsemesterlist");
        return v0_1.toString();
    }

    public static String F5(int p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = Integer.valueOf(p2);
        return String.format("https://fystat-ans.chaoxing.com/flowerApi/findFlowerScoreStatus?type=%d", v0_1);
    }

    public static String F6()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/im/creatChatGroups?");
    }

    public static String F7()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("edit/phone/save?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String F8(String p12, String p13, String p14, int p15, String p16, int p17, String p18, String p19, String p20, int p21)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p12));
        v0_1.append("apis/pp/topic_getTopicListWithPoff?");
        String v0_2 = v0_1.toString();
        String v3 = "puid";
        String v5 = "maxW";
        String v7 = "pageSize";
        String.valueOf(p15);
        String.valueOf(p17);
        v5 = p14;
        v3 = p18;
        String v10 = p20;
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"bbsid", "topicType"}), new String[] {p12, String.valueOf(p21)}));
    }

    public static String F9(String p7, String p8, String p9, String p10, String p11, int p12, int p13)
    {
        if (android.text.TextUtils.isEmpty(p8)) {
            String v8_3 = new StringBuilder();
            v8_3.append(pk.d.b().a(p7));
            v8_3.append("apis/circle/circleMems2?");
            String v0_1 = v8_3.toString();
            String v3 = "lastJoinTime";
            String.valueOf(p12);
            return com.chaoxing.mobile.s.A8(v0_1, new String[] {"circleId", "pageSize"}), new String[] {p7, String.valueOf(p13)}));
        } else {
            String v7_4 = new StringBuilder();
            v7_4.append(pk.d.b().a(p8));
            v7_4.append("apis/circle/circleMems2?");
            String v7_5 = v7_4.toString();
            String v2 = "lastJoinTime";
            String.valueOf(p12);
            return com.chaoxing.mobile.s.A8(v7_5, new String[] {"bbsid", "pageSize"}), new String[] {p8, String.valueOf(p13)}));
        }
    }

    public static String Fa(String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/createDeptIncode?", new String[] {"deptid"}), new String[] {p3}), 1);
    }

    public static String Fb(String p8, String p9, String p10, String p11, String p12, String p13, int p14, int p15)
    {
        if (android.text.TextUtils.isEmpty(p9)) {
            String v9_3 = new StringBuilder();
            v9_3.append(pk.d.b().a(p8));
            v9_3.append("apis/circle/circleMems2?");
            String v0_1 = v9_3.toString();
            String v3 = "name";
            String v5 = "lastId";
            String.valueOf(p13);
            String.valueOf(p14);
            return com.chaoxing.mobile.s.A8(v0_1, new String[] {"circleId", "pageSize"}), new String[] {p8, String.valueOf(p15)}));
        } else {
            String v8_4 = new StringBuilder();
            v8_4.append(pk.d.b().a(p9));
            v8_4.append("apis/circle/circleMems2?");
            String v8_5 = v8_4.toString();
            String v2 = "name";
            String v4 = "lastId";
            String.valueOf(p13);
            String.valueOf(p14);
            return com.chaoxing.mobile.s.A8(v8_5, new String[] {"bbsid", "pageSize"}), new String[] {p9, String.valueOf(p15)}));
        }
    }

    public static String Fc(String p3, String p4, long p5, String p7)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p7));
        v0_1.append("apis/user/userAuth?");
        String v7_1 = v0_1.toString();
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p5);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8(v7_1, new String[] {"uid", "circleId", "topicId"}), new String[] {p3, p4, v1_2.toString()}));
    }

    public static String Fd(String p3, String p4, String p5)
    {
        if (com.fanzhou.util.w.s(p5)) {
            return com.chaoxing.mobile.s.A8("https://useryd.chaoxing.com/apis/user/getUser?", new String[] {"myPuid", "uid"}), new String[] {p4, p3}));
        } else {
            return com.chaoxing.mobile.s.A8("https://useryd.chaoxing.com/apis/user/getUser?", new String[] {"myPuid", "puid"}), new String[] {p4, p5}));
        }
    }

    public static String G(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://passport2-api.chaoxing.com/v5/login?fid=%S&status=openid4&type=2", v0_1);
    }

    public static String G0(android.content.Context p6, int p7, String p8, String p9)
    {
        String v6_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p7);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/sign/produceSignView?", new String[] {"tid", "uid", "appType", "bbsid", "groupId"}), new String[] {v6_4, v0_0, v2_2.toString(), p8, p9}), 0);
    }

    public static String G1()
    {
        return "https://special.rhky.com/mobile/mooc/tocourse/101723775";
    }

    public static String G2(android.content.Context p2)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("apis/circle/getCirclesByGroupChat?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid"}), new String[] {v2_4}));
    }

    public static String G3(java.util.List p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p3));
        v0_1.append("apis/topic/addTopic?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String G4(android.content.Context p3)
    {
        String v3_8 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(v0_0)) {
            String v0_2 = new StringBuilder();
            v0_2.append(pk.a.e);
            v0_2.append("apis/circle/updateMyCircleSort?");
            return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"uid"}), new String[] {v3_8}));
        } else {
            String v3_5 = new StringBuilder();
            v3_5.append(pk.a.e);
            v3_5.append("apis/circle/updateMyCircleSort?");
            return com.chaoxing.mobile.s.A8(v3_5.toString(), new String[] {"puid"}), new String[] {v0_0}));
        }
    }

    public static String G5()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("phone/moocAnalysis/tch/stuTrack");
        return v0_1.toString();
    }

    public static String G6(int p3, String p4)
    {
        Object[] v1_2 = new Object[2];
        v1_2[0] = Integer.valueOf(p3);
        v1_2[1] = p4;
        return com.chaoxing.mobile.s.z8("https://mobilelearn.chaoxing.com/widget/sign/api/findPuidsByActiveId?", new String[] {"signType", "activeId"}), v1_2);
    }

    public static String G7(String p5, String p6, String p7, String p8, String p9, String[] p10)
    {
        String v10_1 = new StringBuilder();
        v10_1.append(gc.b.d);
        v10_1.append("edit/phone/save?");
        String v10_2 = v10_1.toString();
        String v1_1 = new StringBuilder();
        v1_1.append(p5);
        v1_1.append("");
        String v1_2 = v1_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        String v6_1 = v2_2.toString();
        StringBuilder v2_4 = new StringBuilder();
        v2_4.append(p7);
        v2_4.append("");
        return com.chaoxing.mobile.s.A8(v10_2, new String[] {"cardid", "courseid", "knowledgeid", "title", "content"}), new String[] {v1_2, v6_1, v2_4.toString(), p8, p9}));
    }

    public static String G8(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "topicNeedCheck"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "topicNeedCheck"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String G9(String p4, int p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/check/joinCheck?");
        String v0_2 = v0_1.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        String v2_2 = v2_1.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p6);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"uid", "page", "pageSize"}), new String[] {p4, v2_2, v3_2.toString()}));
    }

    public static String Ga(String p2)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://learn.chaoxing.com/mobilelib/app/index?dxfid=");
        v0_1.append(p2);
        return v0_1.toString();
    }

    public static String Gb(android.content.Context p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.e9("https://structureyd.chaoxing.com/apis/roster/searchRosterUser4Client?", new String[] {"fids", "puid", "keyword", "page", "searchMode"}), new String[] {p6, com.chaoxing.study.account.AccountManager.C().D().getPuid(), p7, "1", "1"}));
    }

    public static String Gc(String p5, String p6, int p7, int p8, String p9, String p10)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p10));
        v0_1.append("apis/invitation/getTopicReplys?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uuid", "puid", "maxW", "order", "tags"}), new String[] {p5, p6, String.valueOf(p7), String.valueOf(p8), p9}));
    }

    public static String Gd()
    {
        return "https://passport2-api.chaoxing.com/v11/register";
    }

    public static String H(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://passport2-api.chaoxing.com/v5/login?fid=%s&status=bind&type=1", v0_1);
    }

    public static String H0(String p3)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("phone/coursecontroller/create?opertaion=%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[1];
        v1_3[0] = p3;
        return String.format(v0_2, v1_3);
    }

    public static String H1()
    {
        return "https://m.chaoxing.com/pages/discover/index/searchbox.jsp";
    }

    public static String H2(android.content.Context p2)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("apis/circle/getCirclesGroupChat?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid"}), new String[] {v2_4}));
    }

    public static String H3(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://useryd.chaoxing.com/apis/user/getUser?", new String[] {"puid"}), new String[] {p2}));
    }

    public static String H4(String p2, String p3, String p4, int p5)
    {
        Integer v5_1 = Integer.valueOf(p5);
        Object[] v0_1 = new Object[4];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        v0_1[3] = v5_1;
        return String.format("https://live.chaoxing.com/zhibo/noteLive?uid=%s&tid=%s&circleId=%s&appType=17", v0_1);
    }

    public static String H5()
    {
        return "https://fystat-ans.chaoxing.com/scoreApi/findScoreList";
    }

    public static String H6()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/im/addUsers2Chatgroup?");
    }

    public static String H7(java.util.List p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("edit/phone/save?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String H8(String p8, String p9, String p10, int p11, int p12, String p13)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (!com.fanzhou.util.w.s(p9)) {
            String v8_2 = new StringBuilder();
            v8_2.append(pk.d.b().a(p13));
            v8_2.append("apis/topic/getTopicReadPerson2?");
            String v8_3 = v8_2.toString();
            StringBuilder v1_2 = new StringBuilder();
            v1_2.append(p11);
            v1_2.append("");
            String v11_1 = v1_2.toString();
            StringBuilder v1_4 = new StringBuilder();
            v1_4.append(p12);
            v1_4.append("");
            return com.chaoxing.mobile.s.A8(v8_3, new String[] {"puid", "uuid", "lastValue", "pageSize", "page"}), new String[] {v0_2, p9, p10, v11_1, v1_4.toString()}));
        } else {
            String[] v9_3 = new StringBuilder();
            v9_3.append(pk.d.b().a(p13));
            v9_3.append("apis/topic/getTopicReadPerson2?");
            String[] v9_4 = v9_3.toString();
            StringBuilder v1_7 = new StringBuilder();
            v1_7.append(p11);
            v1_7.append("");
            String v11_2 = v1_7.toString();
            StringBuilder v1_9 = new StringBuilder();
            v1_9.append(p12);
            v1_9.append("");
            return com.chaoxing.mobile.s.A8(v9_4, new String[] {"puid", "topicId", "lastValue", "pageSize", "page"}), new String[] {v0_2, p8, p10, v11_2, v1_9.toString()}));
        }
    }

    public static String H9(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("apis/topic/getUpdateTopicCount?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "circleIds"}), new String[] {v3_4, p4}));
    }

    public static String Ha()
    {
        return "https://oa.chaoxing.com/";
    }

    public static String Hb(String p3, int p4, int p5)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/searchUser?", new String[] {"kw", "page", "pageSize"}), new String[] {p3, v1_1, v2_1.toString()}));
    }

    public static String Hc(String p5, long p6)
    {
        String v0_3 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (!com.fanzhou.util.w.s(p5)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.a.e);
            v6_2.append("apis/topic/topCancel?");
            String v6_3 = v6_2.toString();
            StringBuilder v1_1 = new StringBuilder();
            v1_1.append(p5);
            v1_1.append("");
            String v5_1 = v1_1.toString();
            StringBuilder v1_3 = new StringBuilder();
            v1_3.append(v0_3);
            v1_3.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"uuid", "puid"}), new String[] {v5_1, v1_3.toString()}));
        } else {
            String v5_5 = new StringBuilder();
            v5_5.append(pk.a.e);
            v5_5.append("apis/topic/topCancel?");
            String v5_6 = v5_5.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p6);
            v2_1.append("");
            String v6_4 = v2_1.toString();
            String[] v7_4 = new StringBuilder();
            v7_4.append(v0_3);
            v7_4.append("");
            return com.chaoxing.mobile.s.A8(v5_6, new String[] {"topicId", "puid"}), new String[] {v6_4, v7_4.toString()}));
        }
    }

    public static String Hd()
    {
        return com.chaoxing.mobile.s.x8("https://money.chaoxing.com/apis/pay/alipayNotify_client?");
    }

    public static String I()
    {
        return "https://passport2-api.chaoxing.com/v5/login?status=bind&retainStatus=1";
    }

    public static String I0(android.content.Context p3, int p4)
    {
        String v3_6 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        Integer v4_1 = Integer.valueOf(p4);
        Object[] v1_1 = new Object[3];
        v1_1[0] = v3_6;
        v1_1[1] = v0_0;
        v1_1[2] = v4_1;
        return String.format("https://mobilelearn.chaoxing.com/thesis/teacher/start?tid=%s&uid=%s&appType=%d", v1_1);
    }

    public static String I1()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("help.jsp");
        return v0_1.toString();
    }

    public static String I2()
    {
        return "https://passport2.chaoxing.com/org/allcity";
    }

    public static String I3(String p3, String p4, String p5)
    {
        return com.chaoxing.mobile.s.A8("https://useryd.chaoxing.com/apis/user/getUser?", new String[] {"uid", "puid", "myPuid"}), new String[] {p3, p4, p5}));
    }

    public static String I4(String p5, String p6, String p7, String p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p7));
        v0_1.append("apis/circle/getUserCircleTopicStats?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "circleId", "bbsid", "tags"}), new String[] {p5, p6, p7, p8}));
    }

    public static String I5(String p3, String p4, String p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("work/task-list?courseId=%s&classId=%s&cpi=%s#INNER");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[3];
        v1_3[0] = p4;
        v1_3[1] = p3;
        v1_3[2] = p5;
        return String.format(v0_2, v1_3);
    }

    public static String I6(android.content.Context p7, String p8, int p9, int p10, int p11, int p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.c);
        v7_5.append("apis/note_note/getOpenedNote?");
        String v7_1 = v7_5.toString();
        String v3 = "from";
        String v1_3 = new StringBuilder();
        v1_3.append(p9);
        v1_3.append("");
        v1_3.toString();
        String v1_5 = new StringBuilder();
        v1_5.append(p10);
        v1_5.append("");
        v1_5.toString();
        StringBuilder v10_2 = new StringBuilder();
        v10_2.append(p11);
        v10_2.append("");
        v10_2.toString();
        StringBuilder v10_4 = new StringBuilder();
        v10_4.append(p12);
        v10_4.append("");
        return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "maxW"}), new String[] {v0, v10_4.toString()}));
    }

    public static String I7(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://mobilelearn.chaoxing.com/newsign/studentSign?rcode=%s&uid=%s", v0_1);
    }

    public static String I8(String p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p5));
        v0_1.append("apis/circle/updateCircleExtend?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "bbsid", "replyNeedCheck"}), new String[] {p4, p5, v2_2.toString()}));
    }

    public static String I9(int p1, String p2, long p3)
    {
        return com.chaoxing.mobile.s.J9(p1, p2, p3, 0);
    }

    public static String Ia()
    {
        return "https://learn.chaoxing.com/apis/user/currentUser?backurl=https%3A%2F%2Flive.superlib.com%2FrecommendList";
    }

    public static String Ib(String p3, int p4, int p5)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/searchUserWithCnt?", new String[] {"kw", "page", "pageSize"}), new String[] {p3, v1_1, v2_1.toString()}));
    }

    public static String Ic()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/subscribe/cancelSubscribe.jspx?");
    }

    public static String Id(String p2, String p3)
    {
        String v2_1 = com.chaoxing.mobile.s.M9(p2);
        String v3_1 = com.chaoxing.mobile.s.M9(p3);
        Object[] v0_1 = new Object[2];
        v0_1[0] = v2_1;
        v0_1[1] = v3_1;
        return String.format("https://live.chaoxing.com/liveAPI/getOnlineCount?streamName=%s&vdoid=%s", v0_1);
    }

    public static String J(String p3, int p4, int p5)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://special.chaoxing.com/apis/special/getChapterBookmarksList?", new String[] {"uid", "page", "pageSize"}), new String[] {p3, v1_1, v2_1.toString()}));
    }

    public static String J0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/votePhone/preAddVote?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String J1(String p9, String p10, String p11, int p12, int p13, int p14)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/getCircleList?");
        String v0_2 = v0_1.toString();
        String v3 = "kw";
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p12);
        v2_1.append("");
        v2_1.toString();
        StringBuilder v2_3 = new StringBuilder();
        v2_3.append(p13);
        v2_3.append("");
        v2_3.toString();
        StringBuilder v13_2 = new StringBuilder();
        v13_2.append(p14);
        v13_2.append("");
        String v5 = p11;
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"uid", "pageSize"}), new String[] {p9, v13_2.toString()}));
    }

    public static String J2(String p3)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassPhoneManage/phone/toParticipateCls?inviteCode=%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[1];
        v1_3[0] = p3;
        return String.format(v0_2, v1_3);
    }

    public static String J3(String p1, int p2, int p3)
    {
        return com.chaoxing.mobile.s.K3(p1, "", p2, p3);
    }

    public static String J4(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://mobilelearn.chaoxing.com/widget/apis/renwu/getRenWuTitleAndContent?", new String[] {"key"}), new String[] {p2}));
    }

    public static String J5()
    {
        return "https://homewh.chaoxing.com/home/tools/more";
    }

    public static String J6(android.content.Context p11, String p12, String p13, String p14, String p15, int p16, int p17, int p18, int p19)
    {
        String v1 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.d);
        v0_4.append("apis/activity/noteActivity?");
        String v0_0 = v0_4.toString();
        String v4 = "notebookCid";
        String v6 = "kw";
        String v8 = "maxW";
        if (p16 != 0) {
            String v3_1 = new StringBuilder();
            v3_1.append(p16);
            v3_1.append("");
            v3_1.toString();
        }
        String v11_3 = new StringBuilder();
        v11_3.append(p17);
        v11_3.append("");
        v11_3.toString();
        String v11_5 = new StringBuilder();
        v11_5.append(p18);
        v11_5.append("");
        v11_5.toString();
        String v11_7 = new StringBuilder();
        v11_7.append(p19);
        v11_7.append("");
        String v3 = p13;
        String v5 = p15;
        return com.chaoxing.mobile.s.f9(v0_0, new String[] {"puid", "pageSize"}), new String[] {v1, v11_7.toString()}), 1);
    }

    public static String J7(String p3)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("screen/file_%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[1];
        v1_3[0] = p3;
        return String.format(v0_2, v1_3);
    }

    public static String J8(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://groupweb.chaoxing.com/screen/discuss/inv_detail?uuid=%s", v0_1);
    }

    public static String Ja(String p7, String p8, int p9, int p10, String p11, String p12)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p7));
        v0_1.append("apis/topic/getOpenedTopTopicList?");
        String v0_2 = v0_1.toString();
        String v3 = "maxW";
        String.valueOf(p9);
        String.valueOf(p10);
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"bbsid", "tags"}), new String[] {p7, p12}));
    }

    public static String Jb(String p4, int p5, int p6, String p7)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p5);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("http://uc1-ans.chaoxing.com/apis/phone/user/getperson?", new String[] {"keyword", "fid", "offset", "limit"}), new String[] {p4, p7, v1_1, v2_1.toString()}));
    }

    public static String Jc(String p6, String p7, int p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "onlyManagerReply"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "onlyManagerReply"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String Jd(String p2, String p3, String p4)
    {
        String v2_1 = com.chaoxing.mobile.s.M9(p2);
        String v3_1 = com.chaoxing.mobile.s.M9(p3);
        String v4_1 = com.chaoxing.mobile.s.M9(p4);
        Object[] v0_1 = new Object[3];
        v0_1[0] = v2_1;
        v0_1[1] = v3_1;
        v0_1[2] = v4_1;
        return String.format("https://live.chaoxing.com/chatRoomApi/goChatroom?liveId=%s&puid=%s&vdoid=%s", v0_1);
    }

    public static String K(String p9, String p10, String p11, String p12)
    {
        String v2 = "cfid";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(com.fanzhou.util.n.a);
        v1_1.append("");
        v1_1.toString();
        String v5 = p11;
        return com.chaoxing.mobile.s.A8("https://yz4.chaoxing.com/selfBuiltProject/buildSelfSubject?", new String[] {"uid", "version"}), new String[] {p9, com.fanzhou.util.n.c}));
    }

    public static String K0(android.content.Context p2, String p3)
    {
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/delFolder?", new String[] {"puid", "id"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid(), p3}));
    }

    public static String K1(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/folderOrder?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "folderOrders"}), new String[] {v3_4, p4}));
    }

    public static String K2(String p2, String p3, String p4)
    {
        Object[] v0_1 = new Object[3];
        v0_1[0] = p3;
        v0_1[1] = p2;
        v0_1[2] = p4;
        return String.format("https://mobilelearn.chaoxing.com/widget/CWareDataController/createStuFeedback?classId=%s&courseId=%s&uid=%s", v0_1);
    }

    public static String K4(String p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("app/circle/checkCircle?inviteCode=");
        v0_1.append(p2);
        v0_1.append("&params=");
        v0_1.append(p3);
        return v0_1.toString();
    }

    public static String K5()
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/moveFolderUserSubs.jspx?", new String[] {"version"}), new String[] {com.fanzhou.util.n.c}));
    }

    public static String K6(android.content.Context p12, String p13, String p14, String p15, int p16, String p17, int p18, int p19, int p20, int p21)
    {
        String v1 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.c);
        v0_4.append("apis/note_note/getOpenedNoteList?");
        String v0_0 = v0_4.toString();
        String v4 = "notebookCid";
        String v6 = "getDetail";
        String v8 = "contSize";
        String v2_3 = new StringBuilder();
        v2_3.append(p16);
        v2_3.append("");
        v2_3.toString();
        if (p18 != 0) {
            String v2_5 = new StringBuilder();
            v2_5.append(p18);
            v2_5.append("");
            v2_5.toString();
        }
        String v12_3 = new StringBuilder();
        v12_3.append(p19);
        v12_3.append("");
        v12_3.toString();
        String v12_5 = new StringBuilder();
        v12_5.append(p20);
        v12_5.append("");
        v12_5.toString();
        String v12_7 = new StringBuilder();
        v12_7.append(p21);
        v12_7.append("");
        String v3 = p14;
        v6 = p17;
        return com.chaoxing.mobile.s.f9(v0_0, new String[] {"puid", "pageSize"}), new String[] {v1, v12_7.toString()}), 1);
    }

    public static String K7(int p2)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/scribe/getScribeCatas?", new String[] {"st"}), new String[] {com.fanzhou.document.c.b(p2)}));
    }

    public static String K8()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/report/addReportNew?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String K9(int p4, String p5, long p6, int p8)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        String v6_1 = v2_1.toString();
        StringBuilder v7_1 = new StringBuilder();
        v7_1.append(p8);
        v7_1.append("");
        return com.chaoxing.mobile.s.f9("https://resource.chaoxing.com/apis/cloud/getRecsV2.jspx?", new String[] {"ownertype", "ownerId", "pid", "recType"}), new String[] {v1_1, p5, v6_1, v7_1.toString()}), 1);
    }

    public static String Ka(String p10, String p11, String p12, int p13, String p14, int p15, String p16, String p17)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p10));
        v0_1.append("apis/topic/getOpenedTopicListWithPoff?");
        String v0_2 = v0_1.toString();
        String v3 = "puid";
        String v5 = "maxW";
        String.valueOf(p13);
        String.valueOf(p15);
        v5 = p12;
        v3 = p16;
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"bbsid", "tags"}), new String[] {p10, p17}));
    }

    public static String Kc(String p6, String p7, int p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircle?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "lock_add"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircle?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "lock_add"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String Kd()
    {
        return "https://zhibo.chaoxing.com/apis/live/whetherExistNoClassRoomLiving";
    }

    public static String L(String p5, String p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("comm/apis/praise/cancelReplyPraise?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"replyUuid", "puid", "sid1"}), new String[] {p5, v0_2, p6}));
    }

    public static String L0(String p3, String p4, int p5)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p5);
        v1_2.append("");
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/delFromFolder?", new String[] {"folderId", "msgId", "type"}), new String[] {p3, p4, v1_2.toString()}));
    }

    public static String L2(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p3;
        v0_1[1] = p2;
        return String.format("https://mobilelearn.chaoxing.com/widget/renwu/newCg?classId=%s&courseId=%s", v0_1);
    }

    public static String L3(String p3, String p4)
    {
        return com.chaoxing.mobile.s.A8("https://useryd.chaoxing.com/apis/user/getUser?", new String[] {"puid", "myPuid", "fields"}), new String[] {p3, p4, "topicCount,replyCount"}));
    }

    public static String L4(android.content.Context p5, String p6, int p7, int p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.d);
        v0_2.append("apis/usersgroup/getGroupUsers?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p7);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p8);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "usersGroupId", "page", "pageSize"}), new String[] {v5_4, p6, v2_3, v3_2.toString()}));
    }

    public static String L5(android.content.Context p4, long p5, String p7, String p8)
    {
        String v0_3 = new StringBuilder();
        v0_3.append(p5);
        v0_3.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/moveFolderUserSubs.jspx?", new String[] {"cfid", "key", "cataid", "uid", "version"}), new String[] {v0_3.toString(), p7, p8, com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.util.n.c}));
    }

    public static String L6(String p5, String p6, int p7, int p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/note_note/getOpenedNoteList2?");
        String v0_2 = v0_1.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        String v2_2 = v2_1.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p8);
        v3_2.append("");
        return com.chaoxing.mobile.s.f9(v0_2, new String[] {"puid", "noteCids", "contSize", "maxW"}), new String[] {p5, p6, v2_2, v3_2.toString()}), 1);
    }

    public static String L7(String p4, int p5)
    {
        Integer v5_1 = Integer.valueOf(p5);
        Integer v1_2 = Integer.valueOf(24);
        Object[] v2_1 = new Object[3];
        v2_1[0] = p4;
        v2_1[1] = v5_1;
        v2_1[2] = v1_2;
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/scribe/getScribeNpSearch?", new String[] {"sw", "cpage", "pagesize"}), v2_1);
    }

    public static String L8(String p2, String p3, int p4)
    {
        Integer v4_1 = Integer.valueOf(p4);
        Object[] v0_1 = new Object[3];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = v4_1;
        return String.format("https://x.chaoxing.com/apis/toScreen/topicToScreen?uuid=%s&topicId=%s&opt=%s", v0_1);
    }

    public static String L9(String p3, String p4)
    {
        return com.chaoxing.mobile.s.f9("https://resource.chaoxing.com/apis/cloud/searchRecs.jspx?", new String[] {"ownertype", "ownerId", "kw"}), new String[] {"1", p3, p4}), 1);
    }

    public static String La(String p15, String p16, int p17, int p18, int p19, int p20, String p21)
    {
        String v7;
        if (!com.fanzhou.util.w.q(p21)) {
            v7 = p21;
        } else {
            v7 = "";
        }
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.e);
        v0_4.append("apis/topic/getUidTopicList?");
        String v0_1 = v0_4.toString();
        String v10 = "maxW";
        String v12 = "page";
        String.valueOf(p17);
        String.valueOf(p18);
        String.valueOf(p19);
        String.valueOf(p20);
        return com.chaoxing.mobile.s.A8(v0_1, new String[] {"uid", "kw"}), new String[] {p15, v7}));
    }

    public static String Lb(String p4, String p5, int p6, String p7, String p8)
    {
        if (!android.text.TextUtils.isEmpty(p8)) {
            String v5_3 = new StringBuilder();
            v5_3.append(pk.d.b().a(p8));
            v5_3.append("apis/cmem/joinCircle?");
            String v5_1 = v5_3.toString();
            StringBuilder v1_1 = new StringBuilder();
            v1_1.append(p6);
            v1_1.append("");
            return com.chaoxing.mobile.s.A8(v5_1, new String[] {"uid", "bbsid", "type"}), new String[] {p4, p8, v1_1.toString()}));
        } else {
            String[] v7_6 = new StringBuilder();
            v7_6.append(pk.d.b().a(p5));
            v7_6.append("apis/cmem/joinCircle?");
            String[] v7_7 = v7_6.toString();
            StringBuilder v1_4 = new StringBuilder();
            v1_4.append(p6);
            v1_4.append("");
            return com.chaoxing.mobile.s.A8(v7_7, new String[] {"uid", "circleId", "type"}), new String[] {p4, p5, v1_4.toString()}));
        }
    }

    public static String Lc(String p6, String p7, String p8, int p9, long p10)
    {
        if (android.text.TextUtils.isEmpty(p8)) {
            String v8_3 = new StringBuilder();
            v8_3.append(pk.d.b().a(p7));
            v8_3.append("apis/circle/updateCircleExtend?");
            String v8_1 = v8_3.toString();
            StringBuilder v1_2 = new StringBuilder();
            v1_2.append(p9);
            v1_2.append("");
            String v9_1 = v1_2.toString();
            StringBuilder v1_4 = new StringBuilder();
            v1_4.append(p10);
            v1_4.append("");
            return com.chaoxing.mobile.s.A8(v8_1, new String[] {"puid", "circleId", "sign_ban", "sign_ban_startTime"}), new String[] {p6, p7, v9_1, v1_4.toString()}));
        } else {
            String v7_2 = new StringBuilder();
            v7_2.append(pk.d.b().a(p8));
            v7_2.append("apis/circle/updateCircleExtend?");
            String v7_3 = v7_2.toString();
            StringBuilder v1_6 = new StringBuilder();
            v1_6.append(p9);
            v1_6.append("");
            String v9_2 = v1_6.toString();
            StringBuilder v1_8 = new StringBuilder();
            v1_8.append(p10);
            v1_8.append("");
            return com.chaoxing.mobile.s.A8(v7_3, new String[] {"puid", "bbsid", "sign_ban", "sign_ban_startTime"}), new String[] {p6, p8, v9_2, v1_8.toString()}));
        }
    }

    public static String M(int p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/cmem/showCircleActivity?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"circleId", "uid", "showActivity"}), new String[] {String.valueOf(p4), p5, String.valueOf(p6)}));
    }

    public static String M0(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/cmem/delCmems?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"circleId", "uid", "uids"}), new String[] {p4, p5, p6}));
    }

    public static String M1(String p3, int p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/share/addShare?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"uid", "action"}), new String[] {p3, v2_1.toString()}));
    }

    public static String M2(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://mobilelearn.chaoxing.com/classroomapi/classtheme/info?chatId=%s", v0_1);
    }

    public static String M3(android.content.Context p3)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("apis/circle/getSchoolCircle?");
        return com.chaoxing.mobile.s.f9(v0_2.toString(), new String[] {"uid"}), new String[] {v3_4}), 1);
    }

    public static String M4()
    {
        String[] v1_4 = new StringBuilder();
        v1_4.append(com.fanzhou.util.n.a);
        v1_4.append("");
        String[] v1_1 = v1_4.toString();
        StringBuilder v4_1 = new StringBuilder();
        v4_1.append(com.fanzhou.util.n.b);
        v4_1.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/getGuestSubscirbe.jspx?", new String[] {"productId", "version", "clientType"}), new String[] {v1_1, com.fanzhou.util.n.c, v4_1.toString()}));
    }

    public static String M5(String p6, int p7, String p8, String p9, String p10)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p10));
        v0_1.append("apis/topic_folder/updateTopicFolder?");
        String v0_2 = v0_1.toString();
        Integer v7_1 = Integer.valueOf(p7);
        Object[] v2_2 = new Object[5];
        v2_2[0] = p6;
        v2_2[1] = v7_1;
        v2_2[2] = p8;
        v2_2[3] = p9;
        v2_2[4] = p10;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"folder_uuid", "pid", "name", "puid", "bbsid"}), v2_2);
    }

    public static String M6(int p8, int p9, String p10, String p11, int p12, int p13)
    {
        String v2 = "puid";
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append(p8);
        v1_3.append("");
        v2 = v1_3.toString();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p9);
        v1_1.append("");
        v1_1.toString();
        int v9_2 = new StringBuilder();
        v9_2.append(p12);
        v9_2.append("");
        v9_2.toString();
        int v9_4 = new StringBuilder();
        v9_4.append(p13);
        v9_4.append("");
        String v5 = p11;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/v2apis/friend/getFollowers?", new String[] {"isfollower", "pageSize"}), new String[] {v2, v9_4.toString()}), 1);
    }

    public static String M7(String p5, int p6)
    {
        int v6_3 = com.fanzhou.document.c.b(p6);
        Integer v1_1 = Integer.valueOf(20);
        Object[] v2_1 = new Object[5];
        v2_1[0] = p5;
        v2_1[1] = v6_3;
        v2_1[2] = "p_a_g_e";
        v2_1[3] = v1_1;
        v2_1[4] = "android";
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/scribe/getScribeCataRes?", new String[] {"cataid", "st", "cpage", "pagesize", "type"}), v2_1);
    }

    public static String M8(String p3, String p4, int p5)
    {
        Integer v5_1 = Integer.valueOf(p5);
        Object[] v1_2 = new Object[3];
        v1_2[0] = p3;
        v1_2[1] = p4;
        v1_2[2] = v5_1;
        return com.chaoxing.mobile.s.z8("https://specie.chaoxing.com/apis/message/getPraiseListWithPoff?", new String[] {"puid", "lastValue", "pageSize"}), v1_2);
    }

    public static String Ma()
    {
        return com.chaoxing.mobile.s.x8("https://passport2-api.chaoxing.com/v11/loginregister?");
    }

    public static String Mb(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/sendNoticeAttachment?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "tocircles", "uuid"}), new String[] {p4, p5, p6}));
    }

    public static String Mc(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://im.chaoxing.com/apis/message/updateChatAttachment?", new String[] {"chat_id"}), new String[] {p2}));
    }

    public static String N(String p5, String p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/praise/cancelNoteReplyPraise?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"replyUuid", "puid", "relationId"}), new String[] {p5, v0_2, p6}));
    }

    public static String N0(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_note/deleteNote?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "cid"}), new String[] {v3_4, p4}));
    }

    public static String N1(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://learn.chaoxing.com/html/activityGraph/count.html?puid=%s&tid=%s", v0_1);
    }

    public static String N2(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(gc.b.d);
        v0_2.append("gas/clazz?userid=%s&id=%s&fields=isteacher,id,bbsid,chatid,name,course.fields(id,name,teacherfactor,imageurl)&view=json");
        String v0_0 = v0_2.toString();
        Object[] v1_2 = new Object[2];
        v1_2[0] = v3_4;
        v1_2[1] = p4;
        return String.format(v0_0, v1_2);
    }

    public static String N3()
    {
        return "https://home-yd.chaoxing.com/home/getcxHomePage?incode=public2&v=1";
    }

    public static String N4(android.content.Context p2)
    {
        String v2_3 = new java.text.DecimalFormat("img00000000000000000000000000000");
        StringBuilder v0_2 = new StringBuilder();
        v0_2.append("https://img1.16q.cn/");
        v0_2.append(v2_3.format(Integer.valueOf(com.chaoxing.study.account.AccountManager.C().D().getUid())));
        return v0_2.toString();
    }

    public static String N5()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/v2apis/roster/getUserUnitList?");
    }

    public static String N6(long p1, int p3)
    {
        String v1_1 = Long.valueOf(p1);
        Integer v2 = Integer.valueOf(p3);
        Object[] v3_2 = new Object[2];
        v3_2[0] = v1_1;
        v3_2[1] = v2;
        return String.format("https://mobilelearn.chaoxing.com/widget/pptSource/previewPPT?parentId=%s&isPreview=%s", v3_2);
    }

    public static String N7(String p5, int p6, int p7)
    {
        int v6_2 = com.fanzhou.document.c.b(p6);
        Integer v7_1 = Integer.valueOf(p7);
        Integer v1_2 = Integer.valueOf(20);
        Object[] v2_1 = new Object[5];
        v2_1[0] = p5;
        v2_1[1] = v6_2;
        v2_1[2] = v7_1;
        v2_1[3] = v1_2;
        v2_1[4] = "android";
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/scribe/getScribeCataRes?", new String[] {"cataid", "st", "cpage", "pagesize", "type"}), v2_1);
    }

    public static String N8(android.content.Context p4, String p5, String p6)
    {
        if (p5 == null) {
            p5 = "";
        }
        String v1_2 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(com.fanzhou.util.n.a);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/app/unbindApp.jspx?", new String[] {"uid", "aid", "cataid", "productId"}), new String[] {v1_2, p6, p5, v2_1.toString()}));
    }

    public static String N9(String p2)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("work/phone/workLib?courseId=");
        v0_1.append(p2);
        return v0_1.toString();
    }

    public static String Na(String p4, String p5, int p6, String p7)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p6);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://passport2.chaoxing.com/xxt/loginregisternew?", new String[] {"uname", "code", "loginType", "roleSelect"}), new String[] {p4, p5, v1_2.toString(), p7}));
    }

    public static String Nb(android.content.Context p6, int p7, String p8, String p9, String p10)
    {
        String v6_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/remind/sendRemind?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p7);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "sourceType", "sourceId", "sourceName", "sendRemindType"}), new String[] {v6_4, v2_2.toString(), p8, p9, p10}));
    }

    public static String Nc(String p4, String p5, String p6, int p7)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p7);
        v1_2.append("");
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/updatetChatGroupsInfo?", new String[] {"groupid", "groupname", "desc", "maxusers"}), new String[] {p4, p5, p6, v1_2.toString()}), 1);
    }

    public static String O(int p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/replyCancelTop?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"replyId", "puid"}), new String[] {String.valueOf(p3), p4}));
    }

    public static String O0(boolean p3, String p4, String p5)
    {
        if (p3 == null) {
            return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/delUsersToGroupBatch?", new String[] {"groupid", "members"}), new String[] {p4, p5}), 1);
        } else {
            return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/delUsersToGroupBatchFor104?", new String[] {"groupid", "members"}), new String[] {p4, p5}), 1);
        }
    }

    public static String O1(android.content.Context p2, String p3)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        Object[] v0_1 = new Object[2];
        v0_1[0] = p3;
        v0_1[1] = v2_4;
        return String.format("https://mobilelearn.chaoxing.com/teachingPlanAPI/noFinishActiveCount?chatId=%s&tuid=%s", v0_1);
    }

    public static String O2(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://x.chaoxing.com/course/getClassInvitecode?classId=%s&fid=%s", v0_1);
    }

    public static String O3(android.content.Context p2)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_notebook/getDefaultNotebooks?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid"}), new String[] {v2_4}));
    }

    public static String O4()
    {
        return "https://special.rhky.com/mobile/mooc/tocourse/96637676";
    }

    public static String O5(String p2, String p3)
    {
        return com.chaoxing.mobile.s.f9("https://contactsyd.chaoxing.com/apis/roster/getUserUnitList?", new String[] {"puid", "from"}), new String[] {p2, p3}), 1);
    }

    public static String O6(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://money.chaoxing.com/apis/packet/packetPayStatus?", new String[] {"id"}), new String[] {p2}));
    }

    public static String O7(android.content.Context p1)
    {
        return com.chaoxing.mobile.s.P7(p1, -1);
    }

    public static String O8(String p3)
    {
        Object[] v1_2 = new StringBuilder();
        v1_2.append(p3);
        v1_2.append(com.chaoxing.mobile.secrets.Keys.KEY_22);
        String v0_2 = com.fanzhou.util.j.d(v1_2.toString());
        Object[] v1_1 = new Object[2];
        v1_1[0] = p3;
        v1_1[1] = v0_2;
        return String.format("https://passport2-api.chaoxing.com/api/extenduserinfo?uid=%s&enc=%s&last=1", v1_1);
    }

    public static String O9()
    {
        return "https://mooc1-api.chaoxing.com/phone/data/addnoteresource";
    }

    public static String Oa(int p2, String p3, String p4, String p5, String p6)
    {
        Object[] v0_1 = new Object[5];
        v0_1[0] = Integer.valueOf(p2);
        v0_1[1] = p3;
        v0_1[2] = p4;
        v0_1[3] = p5;
        v0_1[4] = p6;
        return String.format("https://data-xxt.aichaoxing.com/analysis/ac_event?state=%s&userId=%s&request_path=%s&time=%s&enc=%s", v0_1);
    }

    public static String Ob(String p2, String p3, int p4)
    {
        String v0_3 = new StringBuilder();
        v0_3.append(p4);
        v0_3.append("");
        return com.chaoxing.mobile.s.A8("https://specie.chaoxing.com/apis/message/updateMessageReadStatus?", new String[] {"puid", "id", "status"}), new String[] {p3, v0_3.toString(), "1"}));
    }

    public static String Oc(android.content.Context p4, int p5, String p6, int p7)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_1 = new StringBuilder();
        v1_1.append(p5);
        v1_1.append("");
        String v1_2 = v1_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/updateChatStatus?", new String[] {"puid", "type", "msgId", "status"}), new String[] {v4_4, v1_2, p6, v2_1.toString()}));
    }

    public static String P(android.content.Context p4, int p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/cancelNoticeTop?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "noticeId", "sid"}), new String[] {v4_4, v2_2.toString(), p6}));
    }

    public static String P0(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/im/delUnFidUsersFromGroup?", new String[] {"groupid"}), new String[] {p2}));
    }

    public static String P1(String p4, long p5, int p7)
    {
        StringBuilder v1_4 = new StringBuilder();
        v1_4.append(p5);
        v1_4.append("");
        String v6 = v1_4.toString();
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p7);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/addExternalSubscribe.jspx?", new String[] {"uid", "cfid", "source", "version"}), new String[] {p4, v6, v1_2.toString(), com.fanzhou.util.n.c}));
    }

    public static String P2(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(gc.b.d);
        v0_2.append("gas/clazz?userid=%s&id=%s&fields=isteacher");
        String v0_0 = v0_2.toString();
        Object[] v1_2 = new Object[2];
        v1_2[0] = v3_4;
        v1_2[1] = p4;
        return String.format(v0_0, v1_2);
    }

    public static String P3(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/right/quitIncode.jspx?", new String[] {"invitecode"}), new String[] {p2}));
    }

    public static String P4(String p5, String p6)
    {
        Integer v2_1 = Integer.valueOf(1);
        Object[] v3_0 = new Object[4];
        v3_0[0] = p5;
        v3_0[1] = p6;
        v3_0[2] = com.fanzhou.util.n.c;
        v3_0[3] = v2_1;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/subscribe/getSubscribeByUid.jspx?", new String[] {"uid", "puid", "version", "splitData"}), v3_0);
    }

    public static String P5(String p6, String p7, String p8, int p9, int p10)
    {
        if (com.fanzhou.util.w.q(p7)) {
            p7 = "";
        }
        if (com.fanzhou.util.w.q(p8)) {
            p8 = "";
        }
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p9);
        v2_2.append("");
        String v9_1 = v2_2.toString();
        StringBuilder v2_4 = new StringBuilder();
        v2_4.append(p10);
        v2_4.append("");
        return com.chaoxing.mobile.s.A8("https://special.chaoxing.com/apis/special/getHisSpecialList?", new String[] {"puid", "hisUid", "hisPuid", "pageNo", "pageSize"}), new String[] {p6, p8, p7, v9_1, v2_4.toString()}));
    }

    public static String P6()
    {
        if (!n9.b.b()) {
            return com.chaoxing.mobile.s.x8("https://money.chaoxing.com/apis/pay/signature?");
        } else {
            return com.chaoxing.mobile.s.A8("https://money.chaoxing.com/apis/pay/signature?", new String[] {"versionType"}), new String[] {"2"}));
        }
    }

    public static String P8(String p12, String p13, String p14, long p15, int p17, String p18)
    {
        String v2 = "fid";
        String v4 = "level";
        String v6 = "pageSize";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p14);
        v1_1.append("");
        v1_1.toString();
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append("");
        v1_3.append(p15);
        v1_3.toString();
        StringBuilder v1_5 = new StringBuilder();
        v1_5.append("");
        v1_5.append(p17);
        v1_5.toString();
        String v9 = "2";
        v6 = "";
        String v10 = p18;
        return com.chaoxing.mobile.s.f9("https://contactsyd.chaoxing.com/apis/dept/getDepts?", new String[] {"puid", "addHideUserTag"}), new String[] {p12, "1"}), 1);
    }

    public static String P9()
    {
        return "https://mooc1-api.chaoxing.com/phone/data/addnoteresource";
    }

    public static String Pa(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/praise/addNotePraise?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"relationId", "puid"}), new String[] {p4, v3_4}));
    }

    public static String Pb(String p4, String p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/friend/sendValidate?", new String[] {"uid", "friendid", "friendPuid", "msg"}), new String[] {p4, p5, p6, p7}));
    }

    public static String Pc(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "onlyMgrScore"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "onlyMgrScore"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String Q(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/praise/cancelNotePraise?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"relationId", "puid"}), new String[] {p4, v3_4}));
    }

    public static String Q0(android.content.Context p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/delUserFollowV2?", new String[] {"uid", "puid", "followedUid", "followedPuid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid(), p6, p7}), 1);
    }

    public static String Q1()
    {
        return "https://fystat-ans.chaoxing.com/scoreApi/addScore";
    }

    public static String Q2(android.content.Context p3, String p4)
    {
        Object[] v1_1 = new Object[3];
        v1_1[0] = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        v1_1[1] = "1";
        v1_1[2] = p4;
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/user/delUserValidateMsgV2?", new String[] {"receive", "op", "cataids"}), v1_1);
    }

    public static String Q3(long p3, android.content.Context p5)
    {
        String v0_3 = new StringBuilder();
        v0_3.append(p3);
        v0_3.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/delCustomFolder.jspx?", new String[] {"cfid", "type", "uid", "version"}), new String[] {v0_3.toString(), "2", com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.util.n.c}));
    }

    public static String Q4(String p3, int p4)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/praise/cancelUserPraise?", new String[] {"type", "targetid", "utype"}), new String[] {"1", p3, String.valueOf(p4)}));
    }

    public static String Q5(android.content.Context p4, String p5, int p6, String p7)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p6);
        v1_1.append("");
        return com.chaoxing.mobile.s.A8("https://appswh.chaoxing.com/apis/vclass/myClassList?", new String[] {"puid", "lastId", "pageSize", "kw"}), new String[] {v4_4, p5, v1_1.toString(), p7}));
    }

    public static String Q6(android.content.Context p4, String p5, int p6, int p7)
    {
        String v6_1;
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v1_0 = "";
        if (p6 != null) {
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p6);
            v2_1.append("");
            v6_1 = v2_1.toString();
        } else {
            v6_1 = "";
        }
        if (p7 != 0) {
            StringBuilder v2_3 = new StringBuilder();
            v2_3.append(p7);
            v2_3.append("");
            v1_0 = v2_3.toString();
        }
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/getUserFriendGroup?", new String[] {"uid", "gid", "cpage", "pageSize"}), new String[] {v4_4, p5, v6_1, v1_0}), 1);
    }

    public static String Q7(String p9, String p10, String p11, int p12, int p13, String p14)
    {
        // Both branches of the condition point to the same code.
        // if (!com.fanzhou.util.w.q(p10)) {
            if (com.fanzhou.util.w.q(p11)) {
                p11 = "";
            }
            String v4 = "hisPuid";
            StringBuilder v2_2 = new StringBuilder();
            v2_2.append(p12);
            v2_2.append("");
            v2_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p13);
            v2_4.append("");
            v2_4.toString();
            p10 = p11;
            return com.chaoxing.mobile.s.A8("https://special.chaoxing.com/apis/special/getHisSpecialList?", new String[] {"puid", "kw"}), new String[] {p9, p14}));
        // }
    }

    public static String Q8(String p13, String p14, String p15, long p16, int p18, String p19)
    {
        int v2 = "fid";
        String v4 = "level";
        String v6 = "pageSize";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append("");
        v1_1.append(p16);
        v1_1.toString();
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append("");
        v1_3.append(p18);
        v1_3.toString();
        String v10 = "2";
        String v7 = "";
        String v5 = p15;
        return com.chaoxing.mobile.s.f9("https://structureyd.chaoxing.com/apis/dept/getDepts4Client?", new String[] {"puid", "addHideUserTag"}), new String[] {p13, "1"}), 1);
    }

    public static String Q9()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("edit/phone/insertnewchapter?");
        Object[] v1_3 = new Object[0];
        return String.format(v0_1.toString(), v1_3);
    }

    public static String Qa(String p4, int p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/praise/getNotePraises?");
        String v0_2 = v0_1.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        String v2_2 = v2_1.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p6);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"relationId", "page", "pageSize"}), new String[] {p4, v2_2, v3_2.toString()}));
    }

    public static String Qb(java.util.List p1)
    {
        return com.chaoxing.mobile.s.y8("https://learn.chaoxing.com/apis/friend/updateAlias?", p1);
    }

    public static String Qc(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "memberShowRank"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "memberShowRank"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String R(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/praise/cancelReplyPraise?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "uuid", "bbsid"}), new String[] {p4, v2_2.toString(), p6}));
    }

    public static String R0()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/friend/delUserFriendGroup?");
    }

    public static String R1(android.content.Context p4, int p5, String p6, String p7)
    {
        if ((p5 != 2) && ((p5 != 3) && (p5 != 4))) {
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/scribe/addScribe?", new String[] {"uid", "st", "uuid", "cataid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.document.c.b(p5), p6, p7}));
        } else {
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/scribe/addScribe?", new String[] {"uid", "st", "dxid", "cataid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.document.c.b(p5), p6, p7}));
        }
    }

    public static String R2(String p2)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://mooc1-api.chaoxing.com/ananas/audiostatus/");
        v0_1.append(p2);
        return v0_1.toString();
    }

    public static String R3(String p2, String p3)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/facade/deleteResources.jspx?", new String[] {"key", "cataid"}), new String[] {p2, p3}));
    }

    public static String R4(String p3, int p4)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/praise/addUserPraise?", new String[] {"type", "targetid", "utype"}), new String[] {"1", p3, String.valueOf(p4)}));
    }

    public static String R5(String p3, int p4, int p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("gas/clazz?id=%s&fields=name,person.fields(userId,username,avatarurl).offset(%d).limit(%d)&isteachcourse=true&view=json");
        String v0_2 = v0_1.toString();
        Integer v4_1 = Integer.valueOf(p4);
        Integer v5_1 = Integer.valueOf(p5);
        Object[] v1_1 = new Object[3];
        v1_1[0] = p3;
        v1_1[1] = v4_1;
        v1_1[2] = v5_1;
        return String.format(v0_2, v1_1);
    }

    public static String R6(String p2, int p3, int p4, String p5, String p6, String p7)
    {
        Integer v3_1 = Integer.valueOf(p3);
        Integer v4_1 = Integer.valueOf(p4);
        Object[] v0_1 = new Object[6];
        v0_1[0] = p2;
        v0_1[1] = v3_1;
        v0_1[2] = v4_1;
        v0_1[3] = p5;
        v0_1[4] = p6;
        v0_1[5] = p7;
        return String.format("https://mobilelearn.chaoxing.com/ppt/activeAPI/personalActiveLibraryV2?uid=%s&pageSize=%s&page=%s&classId=%s&courseid=%s&courseId=%s", v0_1);
    }

    public static String R7(String p7, String p8, String p9, String p10, int p11, int p12)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.d);
        v0_1.append("apis/activity/getActivity?");
        String v0_2 = v0_1.toString();
        String v3 = "puid";
        String.valueOf(p11);
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"myPuid", "pageSize"}), new String[] {p7, String.valueOf(p12)}));
    }

    public static String R8(String p5, String p6, int p7, long p8, String p10)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p7);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p8);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9("https://contactsyd.chaoxing.com/apis/log/getUnitDeptUserLogs?", new String[] {"puid", "fid", "pageSize", "offsetValue", "offsetAuxValue"}), new String[] {p5, p6, v1_1, v2_1.toString(), p10}), 1);
    }

    public static String R9(String p3, int p4, int p5)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/market/getInviteUser?", new String[] {"reference", "orderby", "pageSize"}), new String[] {p3, v1_1, v2_1.toString()}));
    }

    public static String Ra(String p4, String p5, int p6, int p7, String p8)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/praise/addOrCancelCirclePraise?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"circleId", "uid", "isPraise", "type"}), new String[] {p4, p5, String.valueOf(p6), String.valueOf(p7)}));
    }

    public static String Rb(String p5, String p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.d.b().a(p5));
        v1_2.append("apis/cmem/setCreaterWithAuth?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"bbsid", "puid", "newCreaterPuid"}), new String[] {p5, v0_2, p6}));
    }

    public static String Rc(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "showManager"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "showManager"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String S(String p2, String p3, String p4)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/praise/cancelPraise?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uuid", "puid"}), new String[] {p2, p3}));
    }

    public static String S0()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/persongroup/deleteUserFromPersonGroup?");
    }

    public static String S1(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/getUserJoinCircles?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "myUid"}), new String[] {p3, p4}));
    }

    public static String S2()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("api/newfle?");
        return v0_1.toString();
    }

    public static String S3(String p3, String p4, String p5)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p5));
        v0_1.append("apis/topic/deleteTopicWithCheck?");
        String v5_1 = v0_1.toString();
        Object[] v1_2 = new Object[2];
        v1_2[0] = p3;
        v1_2[1] = p4;
        return com.chaoxing.mobile.s.z8(v5_1, new String[] {"puid", "uuid"}), v1_2);
    }

    public static String S4(String p3, int p4)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/praise/getUserPraiseCntAndStatus?", new String[] {"type", "targetid", "utype"}), new String[] {"1", p3, String.valueOf(p4)}));
    }

    public static String S5(android.content.Context p3)
    {
        return com.chaoxing.mobile.s.pa(p3, 100, 0, 0, 0);
    }

    public static String S6(String p3, String p4, String p5)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/getUserRights?", new String[] {"uid", "puid", "rights"}), new String[] {p3, p4, p5}));
    }

    public static String S7(String p3, int p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/getSendNoticeParams?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "noticeId"}), new String[] {p3, v2_1.toString()}));
    }

    public static String S8(String p5, String p6, int p7, long p8, String p10)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p7);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p8);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9("https://structureyd.chaoxing.com/apis/log/getUnitDeptUserLogs?", new String[] {"puid", "fid", "pageSize", "offsetValue", "offsetAuxValue"}), new String[] {p5, p6, v1_1, v2_1.toString(), p10}), 1);
    }

    public static String S9(String p2, String p3)
    {
        return com.chaoxing.mobile.s.e9("https://learn.chaoxing.com/v2apis/friend/isFollower?", new String[] {"followedUid", "followedPuid"}), new String[] {p2, p3}));
    }

    public static String Sa(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/praise/addReplyPraise?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "uuid", "bbsid"}), new String[] {p4, v2_2.toString(), p6}));
    }

    public static String Sb(String p5, String p6, String p7, int p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p5));
        v0_1.append("apis/cmem/setManager?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p8);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "uid", "uids", "manager"}), new String[] {p5, p6, p7, v2_2.toString()}));
    }

    public static String Sc()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassManage/updateClassFiled");
        return v0_1.toString();
    }

    public static String T()
    {
        return "https://yz4.chaoxing.com/selfBuiltProject/cancleTopsign";
    }

    public static String T0(android.content.Context p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/persongroup/deletePersonGroup?", new String[] {"tid", "puid", "gid", "gids"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid(), p6, p7}), 1);
    }

    public static String T1(String p6, String p7, int p8, int p9, int p10)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/getUserJoinCircles?");
        String v0_2 = v0_1.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        String v2_2 = v2_1.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p7);
        v3_2.append("");
        String v7_1 = v3_2.toString();
        StringBuilder v3_4 = new StringBuilder();
        v3_4.append(p8);
        v3_4.append("");
        String v8_1 = v3_4.toString();
        StringBuilder v3_6 = new StringBuilder();
        v3_6.append(p9);
        v3_6.append("");
        String v9_1 = v3_6.toString();
        StringBuilder v3_8 = new StringBuilder();
        v3_8.append(p10);
        v3_8.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"myPuid", "puid", "type", "page", "pageSize"}), new String[] {v2_2, v7_1, v8_1, v9_1, v3_8.toString()}));
    }

    public static String T2(String p2)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("belonger/");
        v0_1.append(p2);
        return v0_1.toString();
    }

    public static String T3(String p4, String p5, String p6, String p7, int p8)
    {
        if ((!com.fanzhou.util.w.s(p5)) && (!com.fanzhou.util.w.s(p7))) {
            String v4_1 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p5));
            v6_2.append("apis/topic_folder/deleteTopicFolder?");
            String v6_3 = v6_2.toString();
            Integer v8_1 = Integer.valueOf(p8);
            Object[] v1_2 = new Object[4];
            v1_2[0] = v4_1;
            v1_2[1] = p5;
            v1_2[2] = p7;
            v1_2[3] = v8_1;
            return com.chaoxing.mobile.s.z8(v6_3, new String[] {"puid", "bbsid", "folder_uuid", "delAll"}), v1_2);
        } else {
            return com.chaoxing.mobile.s.U3(p4, p6, p8);
        }
    }

    public static String T4()
    {
        return "https://x.chaoxing.com/apis/resControl/imageMove";
    }

    public static String T5(int p9, int p10, int p11, String p12, int p13, int p14)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/myManageCircle?");
        String v0_2 = v0_1.toString();
        String v3 = "mems_magnitude";
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p9);
        v2_1.append("");
        v3 = v2_1.toString();
        StringBuilder v2_3 = new StringBuilder();
        v2_3.append(p10);
        v2_3.append("");
        v2_3.toString();
        StringBuilder v10_2 = new StringBuilder();
        v10_2.append(p11);
        v10_2.append("");
        v10_2.toString();
        StringBuilder v10_4 = new StringBuilder();
        v10_4.append(p13);
        v10_4.append("");
        v10_4.toString();
        StringBuilder v10_6 = new StringBuilder();
        v10_6.append(p14);
        v10_6.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "pageSize"}), new String[] {v3, v10_6.toString()}));
    }

    public static String T6()
    {
        String v0_1 = new StringBuilder();
        v0_1.append("https://learn.chaoxing.com/v2apis/user/getUser4C?");
        v0_1.append(com.fanzhou.util.y.X());
        return v0_1.toString();
    }

    public static String T7(android.content.Context p10, int p11, int p12, int p13, int p14, int p15, int p16, String p17, String p18)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v10_5 = new StringBuilder();
        v10_5.append(pk.a.f);
        v10_5.append("apis/notice/sendNoticeRemind?");
        String v10_1 = v10_5.toString();
        String v3 = "send_msg_email";
        String v5 = "send_msg_voice";
        String v7 = "send_msg_wx";
        String v1_3 = new StringBuilder();
        v1_3.append(p11);
        v1_3.append("");
        v1_3.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p12);
        v2_1.append("");
        v2_1.toString();
        StringBuilder v12_2 = new StringBuilder();
        v12_2.append(p13);
        v12_2.append("");
        v12_2.toString();
        StringBuilder v12_4 = new StringBuilder();
        v12_4.append(p14);
        v12_4.append("");
        v12_4.toString();
        StringBuilder v12_6 = new StringBuilder();
        v12_6.append(p15);
        v12_6.append("");
        v12_6.toString();
        StringBuilder v12_8 = new StringBuilder();
        v12_8.append(p16);
        v12_8.append("");
        v12_8.toString();
        v7 = p17;
        return com.chaoxing.mobile.s.A8(v10_1, new String[] {"puid", "un_puids"}), new String[] {v0, p18}));
    }

    public static String T8(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return com.chaoxing.mobile.s.L1("https://passport2.chaoxing.com/org/froms?cityid=%s&pid=%s", v0_1);
    }

    public static String T9(String p2, String p3)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/friend/isFriend2C?", new String[] {"friendid", "friendPuid"}), new String[] {p2, p3}));
    }

    public static String Ta(String p2, String p3, String p4)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/praise/addPraise?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uuid", "puid"}), new String[] {p2, p3}));
    }

    public static String Tb(String p4, String p5, String p6, int p7, String p8, String p9)
    {
        String v0 = com.chaoxing.mobile.secrets.Keys.KEY_21;
        StringBuilder v5_1 = com.fanzhou.util.y.C(v0, p5);
        if (p7 != null) {
            String v6_2 = com.fanzhou.util.y.C(v0, p6);
            try {
                String v8_1 = java.net.URLEncoder.encode(p8, "UTF-8");
            } catch (Object[] v7_1) {
                v7_1.printStackTrace();
            }
            Object[] v7_3 = new Object[4];
            v7_3[0] = p4;
            v7_3[1] = v6_2;
            v7_3[2] = v5_1;
            v7_3[3] = v8_1;
            String v4_3 = String.format("https://passport2-api.chaoxing.com/api/renew-pwd?name=%s&pwd=%s&newPwd=%s&hddUid=%s", v7_3);
            if (!com.fanzhou.util.w.q(p9)) {
                StringBuilder v5_4 = new StringBuilder();
                v5_4.append(v4_3);
                v5_4.append("&schoolid=");
                v5_4.append(p9);
                v4_3 = v5_4.toString();
            }
            return v4_3;
        } else {
            String v6_1 = new Object[2];
            v6_1[0] = p4;
            v6_1[1] = v5_1;
            return String.format("https://passport2.chaoxing.com/api/renew-pwd?name=%s&newPwd=%s", v6_1);
        }
    }

    public static String Tc(android.content.Context p2, String p3, int p4, String p5)
    {
        String v2_6 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        Integer v4_1 = Integer.valueOf(p4);
        Object[] v0_1 = new Object[4];
        v0_1[0] = p3;
        v0_1[1] = v2_6;
        v0_1[2] = v4_1;
        v0_1[3] = p5;
        return String.format("https://mobilelearn.chaoxing.com/classroomapi/classtheme/update?chatId=%s&uid=%s&type=%d&classId=%s", v0_1);
    }

    public static String U(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/cancelSubscribe.jspx?", new String[] {"uid", "version"}), new String[] {p2, com.fanzhou.util.n.c}));
    }

    public static String U0(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://special.chaoxing.com/apis/special/deleteChapterBookmarks?", new String[] {"uid", "op"}), new String[] {p2, "1"}));
    }

    public static String U1(String p2, String p3, String p4)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://data-xxt.aichaoxing.com/analysis/tab?u=");
        v0_1.append(p2);
        v0_1.append("&m=");
        v0_1.append(p3);
        v0_1.append("&enc=");
        v0_1.append(p4);
        return v0_1.toString();
    }

    public static String U2(String p2, String p3, String p4)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://mobilelearn.chaoxing.com/cloudApi/fileList?uid=");
        v0_1.append(p2);
        v0_1.append("&tid=");
        v0_1.append(p3);
        v0_1.append("&dpath=");
        v0_1.append(p4);
        return v0_1.toString();
    }

    public static String U4()
    {
        return "https://x.chaoxing.com/apis/resControl/imageControlByGes";
    }

    public static String U5(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://yz4.chaoxing.com/selfBuiltProject/indexList?creatorId=%s", v0_1);
    }

    public static String U6(String p5, String p6, int p7, long p8, String p10)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p7);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p8);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9("https://contactsyd.chaoxing.com/apis/dept/getUsersDepts?", new String[] {"puid", "fid", "pageSize", "offsetValue", "offsetAuxValue"}), new String[] {p5, p6, v1_1, v2_1.toString(), p10}), 1);
    }

    public static String U7(String p4, String p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/circleGroupChat3?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "circleId", "autoJoin"}), new String[] {p4, p5, "0"}));
    }

    public static String U8(android.content.Context p6, String p7, String p8, String p9, String p10)
    {
        String v6_5 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.d.b().a(p9));
        v0_2.append("apis/topic_folder/updateTopicFolder?");
        String v0_0 = v0_2.toString();
        Object[] v2_2 = new Object[5];
        v2_2[0] = p7;
        v2_2[1] = p8;
        v2_2[2] = v6_5;
        v2_2[3] = p9;
        v2_2[4] = p10;
        return com.chaoxing.mobile.s.z8(v0_0, new String[] {"folder_uuid", "name", "puid", "bbsid", "pid"}), v2_2);
    }

    public static String U9(String p5, String p6, String p7)
    {
        if (!android.text.TextUtils.isEmpty(p7)) {
            String v6_3 = new StringBuilder();
            v6_3.append(pk.d.b().a(p7));
            v6_3.append("apis/cmem/joinCircle?");
            return com.chaoxing.mobile.s.A8(v6_3.toString(), new String[] {"puid", "bbsid", "type"}), new String[] {p5, p7, "1"}));
        } else {
            String v7_2 = new StringBuilder();
            v7_2.append(pk.d.b().a(p6));
            v7_2.append("apis/cmem/joinCircle?");
            return com.chaoxing.mobile.s.A8(v7_2.toString(), new String[] {"puid", "circleId", "type"}), new String[] {p5, p6, "1"}));
        }
    }

    public static String Ua(long p5, String p7, int p8, int p9, int p10, String p11)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p11));
        v0_1.append("apis/praise/getPraises2?");
        String v11_1 = v0_1.toString();
        String v5_1 = String.valueOf(p5);
        String v6 = String.valueOf(p8);
        String v8_1 = String.valueOf(p9);
        String v9_2 = new StringBuilder();
        v9_2.append("");
        v9_2.append(p10);
        return com.chaoxing.mobile.s.A8(v11_1, new String[] {"topicId", "lastValue", "pageSize", "order", "page"}), new String[] {v5_1, p7, v6, v8_1, v9_2.toString()}));
    }

    public static String Ub(String p3, int p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.d);
        v0_1.append("apis/userprivacy/setActivityTimeLimit?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "time"}), new String[] {p3, v2_1.toString()}));
    }

    public static String Uc(java.util.List p1)
    {
        return com.chaoxing.mobile.s.y8("https://lcyd.chaoxing.com/apis/comment/updateComment?", p1);
    }

    public static String V(String p4, String p5)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p5)) {
            String v5_2 = new StringBuilder();
            v5_2.append(pk.d.b().a(p4));
            v5_2.append("apis/circle/topCancel?");
            return com.chaoxing.mobile.s.A8(v5_2.toString(), new String[] {"circleId", "puid"}), new String[] {p4, v0_2}));
        } else {
            String v4_4 = new StringBuilder();
            v4_4.append(pk.d.b().a(p5));
            v4_4.append("apis/circle/topCancel?");
            return com.chaoxing.mobile.s.A8(v4_4.toString(), new String[] {"bbsid", "puid"}), new String[] {p5, v0_2}));
        }
    }

    public static String V0(String p2, int p3)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p3);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://special.chaoxing.com/apis/special/deleteChapterBookmarks?", new String[] {"uid", "mid"}), new String[] {p2, v1_2.toString()}));
    }

    public static String V1()
    {
        return "https://app.chaoxing.com/t";
    }

    public static String V2(String p3, String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("api/media/info?puid=%s&fleid=%s&objectid=%s&_token=%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[4];
        v1_3[0] = p3;
        v1_3[1] = p4;
        v1_3[2] = p5;
        v1_3[3] = p6;
        return String.format(v0_2, v1_3);
    }

    public static String V3(android.content.Context p3, String p4, String p5)
    {
        Object[] v1_1 = new Object[3];
        v1_1[0] = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        v1_1[1] = p4;
        v1_1[2] = p5;
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/user/delUserValidateMsgV2?", new String[] {"receive", "mid", "cataids"}), v1_1);
    }

    public static String V4()
    {
        return "https://x.chaoxing.com/apis/resControl/imageRotate";
    }

    public static String V5(android.content.Context p14, int p15, String p16, String p17, int p18, int p19, String p20, String p21, String p22, int p23, String p24, String p25)
    {
        int v1_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.d);
        v0_4.append("apis/activity/getNewestNote3?");
        String v0_0 = v0_4.toString();
        String v4 = "uids";
        String v6 = "order";
        String v8 = "kw";
        String v10 = "circleFolderId";
        String v2_3 = new StringBuilder();
        v2_3.append(p15);
        v2_3.append("");
        v2_3.toString();
        if (p18 != 0) {
            String v4_1 = new StringBuilder();
            v4_1.append(p18);
            v4_1.append("");
            v4_1.toString();
        }
        String v14_3 = new StringBuilder();
        v14_3.append(p19);
        v14_3.append("");
        v14_3.toString();
        String v14_5 = new StringBuilder();
        v14_5.append(p23);
        v14_5.append("");
        v14_5.toString();
        String v3 = p16;
        String v7 = p20;
        String v9 = p22;
        return com.chaoxing.mobile.s.f9(v0_0, new String[] {"puid", "index_Id"}), new String[] {v1_0, p25}), 1);
    }

    public static String V6(String p5, String p6, int p7, long p8, String p10)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p7);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p8);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9("https://structureyd.chaoxing.com/apis/dept/getUsersDepts4Client?", new String[] {"puid", "fid", "pageSize", "offsetValue", "offsetAuxValue"}), new String[] {p5, p6, v1_1, v2_1.toString(), p10}), 1);
    }

    public static String V7(String p3, String p4, int p5)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p5);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/friend/updateFriendTopsign?", new String[] {"uid", "friend", "topsign"}), new String[] {p3, p4, v1_2.toString()}));
    }

    public static String V8(android.content.Context p5, String p6, int p7, int p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_note/getUpdateNote?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p7);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p8);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "resId", "type", "maxW"}), new String[] {v5_4, p6, v2_3, v3_2.toString()}));
    }

    public static String V9(String p6, String p7, String p8, String p9)
    {
        if (!android.text.TextUtils.isEmpty(p9)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p9));
            v7_3.append("apis/cmem/joinCircle?");
            return com.chaoxing.mobile.s.A8(v7_3.toString(), new String[] {"puid", "bbsid", "type", "folderId"}), new String[] {p6, p9, "1", p8}));
        } else {
            String v9_2 = new StringBuilder();
            v9_2.append(pk.d.b().a(p7));
            v9_2.append("apis/cmem/joinCircle?");
            return com.chaoxing.mobile.s.A8(v9_2.toString(), new String[] {"puid", "circleId", "type", "folderId"}), new String[] {p6, p7, "1", p8}));
        }
    }

    public static String Va()
    {
        return "https://mobilelearn.chaoxing.com/active/publishActiveNotice?";
    }

    public static String Vb(int p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/replySetTop?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"replyId", "puid"}), new String[] {String.valueOf(p3), p4}));
    }

    public static String Vc(String p6, String p7, String p8, int p9, String p10)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/invitation/updateCommonReply?");
        String v0_2 = v0_1.toString();
        String v2_0 = "";
        if (p9 != 0) {
            StringBuilder v3_2 = new StringBuilder();
            v3_2.append(p9);
            v3_2.append("");
            v2_0 = v3_2.toString();
        }
        return com.chaoxing.mobile.s.f9(v0_2, new String[] {"puid", "replyUuid", "replyId", "maxW", "relationId"}), new String[] {p6, p7, p8, v2_0, p10}), 1);
    }

    public static String W(android.content.Context p8, String p9, String p10, String p11, String p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v6 = "tids";
        String v4 = "ogid";
        String v3 = p10;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/persongroup/changeUser2UserFriendGroup?", new String[] {"tid", "puids"}), new String[] {v0, p12}), 1);
    }

    public static String W0(String p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://mobilelearn.chaoxing.com/cloudApi/delFile?userId=");
        v0_1.append(p2);
        v0_1.append("&filePath=");
        v0_1.append(p3);
        return v0_1.toString();
    }

    public static String W1()
    {
        return "https://app.chaoxing.com";
    }

    public static String W2(String p4, String p5)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.a);
        v1_2.append("api/extfilesInfo?resids=%s&puid=%s&_token=%s");
        String v1_0 = v1_2.toString();
        Object[] v2_2 = new Object[3];
        v2_2[0] = p4;
        v2_2[1] = v0_2;
        v2_2[2] = p5;
        return String.format(v1_0, v2_2);
    }

    public static String W4()
    {
        return "https://x.chaoxing.com/apis/resControl/imageZoom";
    }

    public static String W5(android.content.Context p7, int p8, String p9, int p10, String p11, String p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.d);
        v7_5.append("apis/activity/getActivitys_all?");
        String v7_1 = v7_5.toString();
        String v3 = "kw";
        String v1_3 = new StringBuilder();
        v1_3.append(p8);
        v1_3.append("");
        v1_3.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p10);
        v2_1.append("");
        v2_1.toString();
        String v2 = p9;
        return com.chaoxing.mobile.s.f9(v7_1, new String[] {"puid", "index_Id"}), new String[] {v0, p12}), 1);
    }

    public static String W6()
    {
        return "https://mobilelearn.chaoxing.com/widget/teachingPlan/openScreenPpt";
    }

    public static String W7(String p5, String p6, String p7, String p8, int p9)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p9);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/friend/updateFollowTopsign?", new String[] {"puid", "uid", "followedPuid", "followedUid", "topsign"}), new String[] {p5, p6, p7, p8, v1_2.toString()}));
    }

    public static String W8(String p6, String p7, int p8, String p9)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (!com.fanzhou.util.w.s(p6)) {
            String v7_2 = new StringBuilder();
            v7_2.append(pk.d.b().a(p9));
            v7_2.append("apis/topic/getUpdateTopic?");
            String v7_3 = v7_2.toString();
            StringBuilder v1_2 = new StringBuilder();
            v1_2.append(p8);
            v1_2.append("");
            return com.chaoxing.mobile.s.A8(v7_3, new String[] {"puid", "uuid", "maxW"}), new String[] {v0_2, p6, v1_2.toString()}));
        } else {
            String v6_4 = new StringBuilder();
            v6_4.append(pk.d.b().a(p9));
            v6_4.append("apis/topic/getUpdateTopic?");
            String v6_5 = v6_4.toString();
            StringBuilder v1_5 = new StringBuilder();
            v1_5.append(p8);
            v1_5.append("");
            return com.chaoxing.mobile.s.A8(v6_5, new String[] {"puid", "topicId", "maxW"}), new String[] {v0_2, p7, v1_5.toString()}));
        }
    }

    public static String W9()
    {
        return "https://home-yd.chaoxing.com/home/getcxHomePage?incode=resourcecenter";
    }

    public static String Wa(long p2)
    {
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p2);
        v1_1.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/circle/createCircle.jspx?", new String[] {"sourceFolderId"}), new String[] {v1_1.toString()}));
    }

    public static String Wb(android.content.Context p4, int p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/setNoticeTop?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "noticeId", "sid"}), new String[] {v4_4, v2_2.toString(), p6}));
    }

    public static String Wc(String p13, String p14, String p15, String p16, String p17, String p18)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(p15);
        v0_1.append("A*1~Gq0L):_&8^e!@s");
        com.fanzhou.util.j.b(v0_1.toString());
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("comm/apis/reply/updateCommonReply?");
        String[] v8 = "sid1";
        String v10 = "enc";
        String v3 = p15;
        String v6 = p17;
        return com.chaoxing.mobile.s.f9(v0_2.toString(), new String[] {"puid", "notePartContent"}), new String[] {p13, p18}), 1);
    }

    public static String X(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://m.chaoxing.com/msearch.jsp?sw=%s", v0_1);
    }

    public static String X0(String p6, String p7)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/invitation/deleteCommonReply?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"replyUuid", "puid", "noteCid", "relationId"}), new String[] {p6, v0_2, p7, p7}));
    }

    public static String X1(String p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/cmem/attentionCircle?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "uid", "attention"}), new String[] {p4, p5, v2_2.toString()}));
    }

    public static String X2()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("upload/uploadfile?");
        return v0_1.toString();
    }

    public static String X4()
    {
        return "https://passport2.chaoxing.com/v11/importcourse";
    }

    public static String X5(android.content.Context p20, int p21, String p22, int p23, String p24, String p25, int p26)
    {
        int v1_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getUnitConfigInfo().getUnitPrivate();
        String v2_1 = new StringBuilder();
        v2_1.append(pk.a.d);
        v2_1.append("apis/activity/getActivitys_attention?");
        String v10 = v2_1.toString();
        String v13 = "kw";
        String v15 = "index_updateTime";
        String v17 = "version";
        String v2_3 = new StringBuilder();
        v2_3.append(p21);
        v2_3.append("");
        v2_3.toString();
        String v4_1 = new StringBuilder();
        v4_1.append(p23);
        v4_1.append("");
        v4_1.toString();
        String v5_2 = new StringBuilder();
        v5_2.append(v0_2);
        v5_2.append("");
        v5_2.toString();
        String v0_5 = new StringBuilder();
        v0_5.append(p26);
        v0_5.append("");
        String v3 = p22;
        String v6 = p25;
        return com.chaoxing.mobile.s.f9(v10, new String[] {"puid", "queryPrivate"}), new String[] {v1_0, v0_5.toString()}), 1);
    }

    public static String X6(String p17, String p18, String p19, String p20, String p21)
    {
        String v0_0 = android.os.Build.MANUFACTURER;
        if (!com.fanzhou.util.w.s(v0_0)) {
            v0_0.toUpperCase();
        }
        String v0_1;
        if (!n9.b.b()) {
            v0_1 = "RELEASE";
        } else {
            v0_1 = "BETA";
        }
        String v8 = v0_1;
        String v11 = "schoolId";
        String v13 = "m_token";
        String[] v1_2 = new StringBuilder();
        v1_2.append(3);
        v1_2.append("");
        v1_2.toString();
        String v3 = p19;
        String v5 = p21;
        return com.chaoxing.mobile.s.f9("https://message.chaoxing.com/apis/pmsg/register?", new String[] {"uid", "editions"}), new String[] {p17, v8}), 1);
    }

    public static String X7(String p2)
    {
        Object[] v0_1 = new StringBuilder();
        v0_1.append("https://zhibo.chaoxing.com/");
        v0_1.append(p2);
        Object[] v0_3 = new Object[0];
        return String.format(v0_1.toString(), v0_3);
    }

    public static String X8()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/topic_folder/updateTopicFolderSort?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String X9()
    {
        return "https://live.chaoxing.com/liveTelecast";
    }

    public static String Xa()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("work/phone/publishWorkAndCheck");
        return v0_1.toString();
    }

    public static String Xb()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/friend/updateUserFollowAlias?");
    }

    public static String Xc(String p3, String p4, int p5)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p5);
        v1_2.append("");
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/updateFolder?", new String[] {"id", "name", "ignored"}), new String[] {p3, p4, v1_2.toString()}));
    }

    public static String Y(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://mooc1-api.chaoxing.com/gas/course?id=%s&fields=id,name,mappingcourseid,imageurl,teacherfactor,unfinishedJobcount,jobcount,state,knowledge.fields(id,name,indexOrder,parentnodeid,status,layer,label,card.fields(id,title,cardorder,knowledgeid))&view=json", v0_1);
    }

    public static String Y0(String p6, String p7, String p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("comm/apis/reply/deleteCommonReply?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"replyUuid", "puid", "sid1", "productName"}), new String[] {p6, v0_2, p7, p8}));
    }

    public static String Y1(int p2, int p3)
    {
        return com.chaoxing.mobile.s.Z1(p2, p3, 1, 9000);
    }

    public static String Y2()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("api/token/uservalid");
        Object[] v1_3 = new Object[0];
        return String.format(v0_1.toString(), v1_3);
    }

    public static String Y3(android.content.Context p6, String p7, String p8, String p9)
    {
        return com.chaoxing.mobile.s.X3(p6, p7, p8, 1, 9999, p9);
    }

    public static String Y4()
    {
        return "https://homewh.chaoxing.com/home/tools/more?type=hudong";
    }

    public static String Y5(android.content.Context p8, String p9, int p10, String p11, int p12, String p13, String p14)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v8_5 = new StringBuilder();
        v8_5.append(pk.a.d);
        v8_5.append("apis/activity/getActivitys_friendsGroup?");
        String v8_1 = v8_5.toString();
        String v3 = "pageSize";
        String v5 = "maxW";
        String v1_3 = new StringBuilder();
        v1_3.append(p10);
        v1_3.append("");
        v1_3.toString();
        String v1_5 = new StringBuilder();
        v1_5.append(p12);
        v1_5.append("");
        v1_5.toString();
        String v1 = p9;
        v5 = p13;
        return com.chaoxing.mobile.s.f9(v8_1, new String[] {"puid", "index_Id"}), new String[] {v0, p14}), 1);
    }

    public static String Y6(String p15, String p16, String p17, String p18)
    {
        String[] v0_0 = android.os.Build.MANUFACTURER;
        if (!com.fanzhou.util.w.s(v0_0)) {
            v0_0.toUpperCase();
        }
        String[] v0_1;
        if (!n9.b.b()) {
            v0_1 = "RELEASE";
        } else {
            v0_1 = "BETA";
        }
        String v7 = v0_1;
        String v10 = "productId";
        String v12 = "clientType";
        int v1_2 = new StringBuilder();
        v1_2.append(3);
        v1_2.append("");
        v1_2.toString();
        String v3 = p17;
        return com.chaoxing.mobile.s.f9("https://message.chaoxing.com/apis/pmsg/registerUmeng?", new String[] {"puid", "editions"}), new String[] {p15, v7}), 1);
    }

    public static String Y7(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://yz4.chaoxing.com/selfBuiltProject/shareFolder?", new String[] {"cfid"}), new String[] {p2}));
    }

    public static String Y8(java.util.List p1)
    {
        return com.chaoxing.mobile.s.y8("https://learn.chaoxing.com/apis/user/updateUser?", p1);
    }

    public static String Y9(String p2)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://zhibo.chaoxing.com/live/getCourseware?streamName=");
        v0_1.append(p2);
        return v0_1.toString();
    }

    public static String Ya(String p5, String p6, String p7)
    {
        String[] v0_5 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p7)) {
            if (android.text.TextUtils.isEmpty(v0_5)) {
                String v7_3 = new StringBuilder();
                v7_3.append(pk.d.b().a(p6));
                v7_3.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v7_3.toString(), new String[] {"uid", "circleId"}), new String[] {p5, p6}));
            } else {
                String v5_4 = new StringBuilder();
                v5_4.append(pk.d.b().a(p6));
                v5_4.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v5_4.toString(), new String[] {"puid", "circleId"}), new String[] {v0_5, p6}));
            }
        } else {
            if (android.text.TextUtils.isEmpty(v0_5)) {
                String[] v6_4 = new StringBuilder();
                v6_4.append(pk.d.b().a(p7));
                v6_4.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v6_4.toString(), new String[] {"uid", "bbsid"}), new String[] {p5, p7}));
            } else {
                String v5_10 = new StringBuilder();
                v5_10.append(pk.d.b().a(p7));
                v5_10.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v5_10.toString(), new String[] {"puid", "bbsid"}), new String[] {v0_5, p7}));
            }
        }
    }

    public static String Yb(String p2, long p3)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p3);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/updateUserRights?", new String[] {"uid", "code"}), new String[] {p2, v1_2.toString()}));
    }

    public static String Yc()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/batchReOrder");
        return v0_1.toString();
    }

    public static String Z()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassPhoneManage/phone/checkClazzNameExists");
        return v0_1.toString();
    }

    public static String Z0(String p8, String p9, long p10, int p12, String p13)
    {
        String v8_1 = com.chaoxing.mobile.s.M9(p8);
        String v9_1 = com.chaoxing.mobile.s.M9(p9);
        if (!com.fanzhou.util.w.s(p13)) {
            String v0_1 = new StringBuilder();
            v0_1.append(gc.b.d);
            v0_1.append("mycourse/leftSlip?courseId=%s&classId=%s&catalogId=%d&type=%d&cpi=%s");
            String v0_2 = v0_1.toString();
            if (v9_1 == null) {
                v9_1 = "";
            }
            Long v10_1 = Long.valueOf(p10);
            Integer v11_0 = Integer.valueOf(p12);
            Object[] v12_2 = new Object[5];
            v12_2[0] = v8_1;
            v12_2[1] = v9_1;
            v12_2[2] = v10_1;
            v12_2[3] = v11_0;
            v12_2[4] = p13;
            return String.format(v0_2, v12_2);
        } else {
            String v13_2 = new StringBuilder();
            v13_2.append(gc.b.d);
            v13_2.append("mycourse/leftSlip?courseId=%s&classId=%s&catalogId=%d&type=%d");
            String v13_3 = v13_2.toString();
            if (v9_1 == null) {
                v9_1 = "";
            }
            Long v10_2 = Long.valueOf(p10);
            Integer v11_1 = Integer.valueOf(p12);
            Object[] v12_3 = new Object[4];
            v12_3[0] = v8_1;
            v12_3[1] = v9_1;
            v12_3[2] = v10_2;
            v12_3[3] = v11_1;
            return String.format(v13_3, v12_3);
        }
    }

    public static String Z2(android.content.Context p6, int p7, int p8, String p9, String p10)
    {
        String v6_9 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        int v2 = "pageSize";
        int v7_1 = Integer.valueOf(p7);
        Integer v8_1 = Integer.valueOf(p8);
        Object[] v1_1 = new Object[6];
        v1_1[0] = v6_9;
        v1_1[1] = v7_1;
        v1_1[2] = v8_1;
        v1_1[3] = "0,1,-1,2,-2,3,4";
        v1_1[4] = p9;
        v1_1[5] = p10;
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/user/getUserValidateMsgs?", new String[] {"puid", "clearMsgByCataid"}), v1_1);
    }

    public static String Z3(android.content.Context p13, String p14, String p15, String p16, String p17)
    {
        com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v11 = "pageSize";
        String v7 = "deptid";
        String v9 = "uid";
        int v0_1 = new StringBuilder();
        v0_1.append(p17);
        v0_1.append("");
        v0_1.toString();
        String v5 = "1";
        String v3 = p15;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/v2apis/roster/getUsers?", new String[] {"type", "mcode"}), new String[] {"bycata", p16}), 1);
    }

    public static String Z4(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/right/getHomeConfigByUid.jspx?", new String[] {"uid"}), new String[] {p2}));
    }

    public static String Z5(android.content.Context p7, int p8, String p9, int p10, String p11, String p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.d);
        v7_5.append("apis/activity/getActivitys_me?");
        String v7_1 = v7_5.toString();
        String v3 = "kw";
        String v1_3 = new StringBuilder();
        v1_3.append(p8);
        v1_3.append("");
        v1_3.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p10);
        v2_1.append("");
        v2_1.toString();
        String v2 = p9;
        return com.chaoxing.mobile.s.f9(v7_1, new String[] {"puid", "index_Id"}), new String[] {v0, p12}), 1);
    }

    public static String Z6(String p9, String p10, String p11, String p12, String p13)
    {
        String v2 = "schoolId";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(3);
        v1_1.append("");
        String v5 = p11;
        String v7 = p13;
        return com.chaoxing.mobile.s.f9("https://message.chaoxing.com/apis/pmsg/logoff?", new String[] {"uid", "clientType"}), new String[] {p9, v1_1.toString()}), 1);
    }

    public static String Z7(String p5, String p6, int p7, int p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.d);
        v0_1.append("apis/activity/dataActivity?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "puid", "page", "pageSize"}), new String[] {p5, p6, String.valueOf(p7), String.valueOf(p8)}));
    }

    public static String Z8(String p2, String p3)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/apk/apkInfos.jspx?", new String[] {"apkid", "puid"}), new String[] {p2, p3}));
    }

    public static String Z9(String p2)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://apps.chaoxing.com/apis/mright/createRandomIncode.jspx?codeType=LIVE&srcVal=");
        v0_1.append(p2);
        return v0_1.toString();
    }

    public static String Za(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/cmem/quitCircle2Creater?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "circleId"}), new String[] {p3, p4}));
    }

    public static String Zb(String p5, long p6, int p8, String p9)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p9));
        v0_1.append("apis/invitation/replySetTop?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "replyId", "top", "bbsid"}), new String[] {p5, String.valueOf(p6), String.valueOf(p8), p9}));
    }

    public static String Zc(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "autoClearStatus"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "autoClearStatus"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String a(java.util.List p1)
    {
        return com.chaoxing.mobile.s.y8("https://lcyd.chaoxing.com/apis/comment/addComment?", p1);
    }

    public static String a0(android.content.Context p3)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_notebook/checkOrCreateNotebook?");
        return com.chaoxing.mobile.s.f9(v0_2.toString(), new String[] {"puid"}), new String[] {v3_4}), 1);
    }

    public static String a1(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassPhoneManage/phone/deleteAssistantOrTeacher2?courseId=%s&teacherId=%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[2];
        v1_3[0] = p3;
        v1_3[1] = p4;
        return String.format(v0_2, v1_3);
    }

    public static String a2(String p3, int p4)
    {
        if (!com.fanzhou.util.w.s(p3)) {
            try {
                p3 = java.net.URLDecoder.decode(p3, "UTF-8");
            } catch (Exception v0_3) {
                v0_3.printStackTrace();
            }
        }
        String v1_1 = new StringBuilder();
        v1_1.append(p4);
        v1_1.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/scribe/getScribeAudioSearch?", new String[] {"sw", "cpage", "type"}), new String[] {p3, v1_1.toString(), "android"}));
    }

    public static String a3(String p5, int p6, int p7, String p8, String p9, String p10)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p6);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9(p5, new String[] {"pageSize", "page", "mark", "name", "title"}), new String[] {v1_1, v2_1.toString(), p8, p9, p10}), 1);
    }

    public static String a4(String p13, String p14, String p15, String p16, String p17, String p18, String p19, String p20, String p21, String p22)
    {
        String v2 = "deptid";
        String v4 = "puid";
        String v6 = "pageSize";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p18);
        v1_1.append("");
        v1_1.toString();
        String v7 = p13;
        v6 = p16;
        String v8 = p19;
        String v11 = p21;
        return com.chaoxing.mobile.s.f9("https://contactsyd.chaoxing.com/apis/roster/getUsers?", new String[] {"type", "offsetAuxValue"}), new String[] {p14, p22}), 1);
    }

    public static String a5(String p4, String p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("gas/knowledge?");
        String v0_2 = v0_1.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        String v2_2 = v2_1.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p5);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"id", "courseid", "fields"}), new String[] {v2_2, v3_2.toString(), "id,name,card.fields(id,description,title,cardorder)"}));
    }

    public static String a6(android.content.Context p7, int p8, String p9, int p10, String p11, String p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.d);
        v7_5.append("apis/activity/getActivitysMeRead?");
        String v7_1 = v7_5.toString();
        String v3 = "kw";
        String v1_3 = new StringBuilder();
        v1_3.append(p8);
        v1_3.append("");
        v1_3.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p10);
        v2_1.append("");
        v2_1.toString();
        String v2 = p9;
        return com.chaoxing.mobile.s.f9(v7_1, new String[] {"puid", "index_Id"}), new String[] {v0, p12}), 1);
    }

    public static String a7(String p4, String p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.f9("https://message.chaoxing.com/apis/pmsg/logoffUmeng?", new String[] {"puid", "schoolId", "productId", "m_token"}), new String[] {p4, p5, p6, p7}), 1);
    }

    public static String a8(String p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.d);
        v0_1.append("apis/user/updateShieldingUser?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "psuids", "status"}), new String[] {p4, p5, v2_1.toString()}));
    }

    public static String a9(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/uploadhead?", new String[] {"uid"}), new String[] {p2}));
    }

    public static String aa()
    {
        return "https://live.chaoxing.com/front/mobile/zhibo/images/logo.png";
    }

    public static String ab(String p5, String p6, String p7)
    {
        String[] v0_5 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p7)) {
            if (android.text.TextUtils.isEmpty(v0_5)) {
                String v7_3 = new StringBuilder();
                v7_3.append(pk.d.b().a(p6));
                v7_3.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v7_3.toString(), new String[] {"uid", "circleId"}), new String[] {p5, p6}));
            } else {
                String v5_4 = new StringBuilder();
                v5_4.append(pk.d.b().a(p6));
                v5_4.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v5_4.toString(), new String[] {"puid", "circleId"}), new String[] {v0_5, p6}));
            }
        } else {
            if (android.text.TextUtils.isEmpty(v0_5)) {
                String[] v6_4 = new StringBuilder();
                v6_4.append(pk.d.b().a(p7));
                v6_4.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v6_4.toString(), new String[] {"uid", "bbsid"}), new String[] {p5, p7}));
            } else {
                String v5_10 = new StringBuilder();
                v5_10.append(pk.d.b().a(p7));
                v5_10.append("apis/cmem/quitCircle?");
                return com.chaoxing.mobile.s.A8(v5_10.toString(), new String[] {"puid", "bbsid"}), new String[] {v0_5, p7}));
            }
        }
    }

    public static String ac(String p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/cmem/showCircleActivity?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "uid", "showActivity"}), new String[] {p4, p5, v2_1.toString()}));
    }

    public static String ad(android.content.Context p4, String p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/updateFolder?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "folder_uuid", "folder_name"}), new String[] {v4_4, p5, p6}));
    }

    public static String b()
    {
        return com.chaoxing.mobile.s.x8("https://commendyd.chaoxing.com/apis/commend/addCommend?");
    }

    public static String b0(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://passport2-api.chaoxing.com/api/verifybindstatus?enc=%s&uid=%s", v0_1);
    }

    public static String b1()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/batchDelete");
        return v0_1.toString();
    }

    public static String b2(int p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = Integer.valueOf(p2);
        return String.format("https://authen.chaoxing.com/authsign/show?certifyType=%d", v0_1);
    }

    public static String b3(android.content.Context p5, String p6, int p7, int p8)
    {
        String v7_1;
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_note/getOpenedNoteList2?");
        String v0_0 = v0_2.toString();
        if (p7 != null) {
            StringBuilder v3_2 = new StringBuilder();
            v3_2.append(p7);
            v3_2.append("");
            v7_1 = v3_2.toString();
        } else {
            v7_1 = "";
        }
        StringBuilder v3_4 = new StringBuilder();
        v3_4.append(p8);
        v3_4.append("");
        return com.chaoxing.mobile.s.f9(v0_0, new String[] {"puid", "noteCids", "contSize", "maxW"}), new String[] {v5_4, p6, v7_1, v3_4.toString()}), 1);
    }

    public static String b4(String p13, String p14, String p15, String p16, String p17, String p18, String p19, String p20, String p21, String p22)
    {
        String v2 = "deptid";
        String v4 = "puid";
        String v6 = "pageSize";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p18);
        v1_1.append("");
        v1_1.toString();
        String v7 = p13;
        v6 = p16;
        String v8 = p19;
        String v11 = p21;
        return com.chaoxing.mobile.s.f9("https://structureyd.chaoxing.com/apis/roster/getUsers4Client?", new String[] {"type", "offsetAuxValue"}), new String[] {p14, p22}), 1);
    }

    public static String b5(String p4, int p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("courseapi/msg-list?");
        String v0_2 = v0_1.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9(v0_2, new String[] {"clazzid", "limit", "offset"}), new String[] {p4, "20", v2_1.toString()}), 0);
    }

    public static String b6(android.content.Context p9, int p10, String p11, int p12, String p13, String p14)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        com.chaoxing.study.account.AccountManager.C().D().getFid();
        String v9_2 = new StringBuilder();
        v9_2.append(pk.a.d);
        v9_2.append("apis/activity/getActivitys_unit?");
        String v9_3 = v9_2.toString();
        String v4 = "pageSize";
        String v6 = "maxW";
        String v2_4 = new StringBuilder();
        v2_4.append(p10);
        v2_4.append("");
        v2_4.toString();
        String v3_1 = new StringBuilder();
        v3_1.append(p12);
        v3_1.append("");
        v3_1.toString();
        String v3 = p11;
        return com.chaoxing.mobile.s.f9(v9_3, new String[] {"puid", "index_Id"}), new String[] {v0, p14}), 1);
    }

    public static String b7(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/service/quitGridCode?", new String[] {"uid"}), new String[] {p2}));
    }

    public static String b8(android.content.Context p5, int p6, int p7, int p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("/apis/circle/hideActivityCircles?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p7);
        v3_2.append("");
        String v7_1 = v3_2.toString();
        StringBuilder v3_4 = new StringBuilder();
        v3_4.append(p8);
        v3_4.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "page", "pageSize", "maxW"}), new String[] {v5_4, v2_3, v7_1, v3_4.toString()}));
    }

    public static String b9(String p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/note_note/uploadNote?");
        return com.chaoxing.mobile.s.e9(v0_1.toString(), new String[] {"cid"}), new String[] {p2}));
    }

    public static String ba()
    {
        return "https://live.chaoxing.com/liveAPI/getOneOrMoreLiveStatusNew";
    }

    public static String bb(android.content.Context p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/persongroup/updatePersonGroup?", new String[] {"tid", "puid", "gid", "name"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid(), p6, p7}), 1);
    }

    public static String bc()
    {
        return com.chaoxing.mobile.s.x8("https://resource.chaoxing.com/apis/cloud/updateNorder.jspx?");
    }

    public static String bd(android.content.Context p5, String p6, String p7, int p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/updateFolder?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p8);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "folder_uuid", "folder_name", "top"}), new String[] {v5_4, p6, p7, v2_2.toString()}));
    }

    public static String c(android.content.Context p4, String p5, String p6, int p7)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p7);
        v1_1.append("");
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/addFolder?", new String[] {"puid", "name", "pid", "ignored"}), new String[] {v4_4, p5, p6, v1_1.toString()}));
    }

    public static String c0(android.content.Context p2, String p3)
    {
        return com.chaoxing.mobile.s.f9("https://specie.chaoxing.com/apis/message/clearNoRead?", new String[] {"puid", "specieIds"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid(), p3}), 1);
    }

    public static String c1(android.content.Context p4, String p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/deleteFolder?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "folder_uuids", "noticeIds"}), new String[] {v4_4, p5, p6}));
    }

    public static String c2()
    {
        return "https://sso.chaoxing.com/apis/login/userLogin.do";
    }

    public static String c3()
    {
        return "https://homewh.chaoxing.com/home/tools/more/v2";
    }

    public static String c4(android.content.Context p10, String p11, String p12)
    {
        com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v8 = "cpage";
        String v6 = "name";
        String v2 = p12;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/v2apis/roster/getUsers?", new String[] {"type", "pageSize"}), new String[] {"byuid", "9999"}), 1);
    }

    public static String c5()
    {
        return "https://app-1.chaoxing.com/app1/index";
    }

    public static String c6(String p11, int p12, int p13, String p14, int p15, String p16, String p17, String p18, String p19)
    {
        String v2 = "page";
        String v4 = "maxW";
        String v6 = "puid";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p12);
        v1_1.append("");
        v1_1.toString();
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append(p13);
        v1_3.append("");
        v1_3.toString();
        String v13_2 = new StringBuilder();
        v13_2.append(p15);
        v13_2.append("");
        v13_2.toString();
        String v7 = p16;
        String v9 = p18;
        return com.chaoxing.mobile.s.f9("https://commendyd.chaoxing.com/apis/commend/queryCommend?", new String[] {"keyword", "tags"}), new String[] {p11, p19}), 1);
    }

    public static String c7(android.content.Context p11, String p12, String p13, String p14, String p15, String p16, int p17, int p18)
    {
        String v11_5 = com.chaoxing.study.account.AccountManager.C().D().getUnitConfigInfo().getUnitPrivate();
        String v2 = "number";
        String v4 = "tagnumber";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p17);
        v1_1.append("");
        v1_1.toString();
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append(p18);
        v1_3.append("");
        v1_3.toString();
        StringBuilder v1_5 = new StringBuilder();
        v1_5.append(v11_5);
        v1_5.append("");
        String v5 = p14;
        String v7 = p16;
        return com.chaoxing.mobile.s.f9("https://commendyd.chaoxing.com/apis/commend/randCommend?", new String[] {"type", "unitPrivate"}), new String[] {p12, v1_5.toString()}), 1);
    }

    public static String c8(android.content.Context p4, int p5, int p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.e);
        v0_2.append("/apis/user/getShieldingUsers?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p6);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "page", "pageSize"}), new String[] {v4_4, v2_3, v3_2.toString()}));
    }

    public static String c9()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/note_note/uploadNote?");
        return v0_1.toString();
    }

    public static String ca()
    {
        return "https://live.chaoxing.com/liveAPI/getNewLiveStatusList";
    }

    public static String cb(android.content.Context p4, int p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/readNotice?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"noticeId", "sid", "puid"}), new String[] {v2_2.toString(), p6, v4_4}));
    }

    public static String cc(android.content.Context p4, String p5)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/persongroup/updatePersonGroupNorder?", new String[] {"tid", "puid", "gids"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid(), p5}), 1);
    }

    public static String cd(String p4, String p5)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p4)) {
            String v4_2 = new StringBuilder();
            v4_2.append(pk.d.b().a(p5));
            v4_2.append("apis/circle/uploadCircleLogo?");
            return com.chaoxing.mobile.s.A8(v4_2.toString(), new String[] {"puid", "circleId"}), new String[] {v0_2, p5}));
        } else {
            String[] v5_3 = new StringBuilder();
            v5_3.append(pk.d.b().a(p4));
            v5_3.append("apis/circle/uploadCircleLogo?");
            return com.chaoxing.mobile.s.A8(v5_3.toString(), new String[] {"puid", "bbsid"}), new String[] {v0_2, p4}));
        }
    }

    public static String d(String p5, String p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("comm/apis/praise/addReplyPraise?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"replyUuid", "puid", "sid1"}), new String[] {p5, v0_2, p6}));
    }

    public static String d0(android.content.Context p4, String p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/clearNoticeRedDot?");
        return com.chaoxing.mobile.s.f9(v0_2.toString(), new String[] {"puid", "noticeId", "idCodes"}), new String[] {v4_4, p5, p6}), 1);
    }

    public static String d1(android.content.Context p2, String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/delUserFriendGroup?", new String[] {"uid", "gid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), p3}), 1);
    }

    public static String d2(String p5, String p6, String p7, String p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/score/addReplyScoreBatch?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "uuids", "score", "bbsid"}), new String[] {p5, p6, p7, p8}));
    }

    public static String d3(String p3, int p4, int p5)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/contact/getContactMembers?", new String[] {"id", "cpage", "pageSize"}), new String[] {p3, v1_1, v2_1.toString()}));
    }

    public static String d4(String p2)
    {
        String v1_2 = new StringBuilder();
        v1_2.append(p2);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://mobilelearn.chaoxing.com/widget/active/getActiveInfo?", new String[] {"id"}), new String[] {v1_2.toString()}));
    }

    public static String d5(int p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = Integer.valueOf(p2);
        return String.format("https://mobilelearn.chaoxing.com/widget/active/getLiveActiveInfo?id=%s", v0_1);
    }

    public static String d6(android.content.Context p5, String p6, String p7, String p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_notebook/getNotebookList2?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "lastUpdateTime", "page", "pageSize"}), new String[] {v5_4, p6, p7, p8}));
    }

    public static String d7()
    {
        return "https://rec.chaoxing.com/static/readreport";
    }

    public static String d8()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("phone/api/haveElectiveCourse?view=json");
        return v0_1.toString();
    }

    public static String d9(String p2)
    {
        try {
            String v2_2 = java.net.URLEncoder.encode(p2, "UTF-8");
        } catch (Object[] v0_1) {
            v0_1.printStackTrace();
        }
        Object[] v0_3 = new Object[1];
        v0_3[0] = v2_2;
        return String.format("https://mobilewx.chaoxing.com/widget/weixin/formatWeixinQrcode?wxQrcodeValue=%s", v0_3);
    }

    public static String da(long p2)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p2);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/getSourcesByUid.jspx?", new String[] {"cfid", "version"}), new String[] {v1_2.toString(), com.fanzhou.util.n.c}));
    }

    public static String db(android.content.Context p4, int p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/recallNotice?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"noticeId", "sid", "puid"}), new String[] {v2_2.toString(), p6, v4_4}));
    }

    public static String dc()
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/moveSubscribeOrder.jspx?", new String[] {"version"}), new String[] {com.fanzhou.util.n.c}));
    }

    public static String dd(String p4, String p5, int p6)
    {
        String v5_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.d.b().a(p4));
        v0_2.append("apis/circle/updateCircleExtend?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "bbsid", "isShowCircleChat"}), new String[] {v5_2, p4, v2_2.toString()}));
    }

    public static String e(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/addFolder?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "folder_name"}), new String[] {v3_4, p4}));
    }

    public static String e0(String p2)
    {
        if (p2 == null) {
            p2 = "";
        }
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/getAppCataInfo.jspx?", new String[] {"mcode"}), new String[] {p2}));
    }

    public static String e1(String p4)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.e);
        v1_2.append("apis/circle_folder/deleteCircleFolder?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"puid", "id"}), new String[] {v0_2, p4}));
    }

    public static String e2(android.content.Context p4, String p5)
    {
        int v0_3 = Integer.valueOf(com.fanzhou.util.n.a);
        String v1_1 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        Object[] v2_1 = new Object[3];
        v2_1[0] = v0_3;
        v2_1[1] = p5;
        v2_1[2] = v1_1;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/app/bindApp.jspx?", new String[] {"productId", "aid", "uid"}), v2_1);
    }

    public static String e3(android.content.Context p2)
    {
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/getFolders?", new String[] {"puid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid()}));
    }

    public static String e4(long p4, String p6, int p7, android.content.Context p8)
    {
        String v0_5 = new StringBuilder();
        v0_5.append(p4);
        v0_5.append("");
        String v5 = v0_5.toString();
        String v0_3 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p7);
        v1_2.append("");
        return com.chaoxing.mobile.s.g4(new String[] {"cfid", "cfname", "uid", "shareType", "version"}), new String[] {v5, p6, v0_3, v1_2.toString(), com.fanzhou.util.n.c}));
    }

    public static String e5(String p2, String p3, String p4, int p5)
    {
        Integer v5_1 = Integer.valueOf(p5);
        Object[] v0_1 = new Object[4];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        v0_1[3] = v5_1;
        return String.format("https://live.chaoxing.com/taskpagelive/gonewlive?courseId=%s&classId=%s&puid=%s&source=%s", v0_1);
    }

    public static String e6(android.content.Context p7, String p8, String p9, int p10, int p11, int p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.c);
        v7_5.append("apis/note_rtfnote/getNoteList?");
        String v7_1 = v7_5.toString();
        String v3 = "kw";
        String v1_3 = new StringBuilder();
        v1_3.append(p10);
        v1_3.append("");
        v1_3.toString();
        String v1_5 = new StringBuilder();
        v1_5.append(p11);
        v1_5.append("");
        v1_5.toString();
        StringBuilder v11_2 = new StringBuilder();
        v11_2.append(p12);
        v11_2.append("");
        String v2 = p9;
        return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "maxW"}), new String[] {v0, v11_2.toString()}));
    }

    public static String e7(String p3, String p4, String p5)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/log/getUserOperLogSection.jspx?", new String[] {"uid", "key", "cataid"}), new String[] {p3, p4, p5}));
    }

    public static String e8(String p3, String p4)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/isFriend2C?", new String[] {"friendid", "friendPuid", "vs"}), new String[] {p3, p4, "1"}), 1);
    }

    public static String ea(String p6, String p7, int p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircle?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "check"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircle?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "check"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String eb(int p2, int p3)
    {
        String v2_1 = Integer.valueOf(p2);
        Integer v3_1 = Integer.valueOf(p3);
        Object[] v0_1 = new Object[2];
        v0_1[0] = v2_1;
        v0_1[1] = v3_1;
        return String.format("https://home-yd.chaoxing.com/apis/data/getIdxSourceVoByPoolId?poolId=tushu&incode=000000&page=%s&pageSize=%s", v0_1);
    }

    public static String ec()
    {
        return "https://yz4.chaoxing.com/selfBuiltProject/backSort";
    }

    public static String ed(String p4, String p5, int p6)
    {
        String v5_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.d.b().a(p4));
        v0_2.append("apis/circle/updateCircleExtend?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "bbsid", "isShowCircleCloud"}), new String[] {v5_2, p4, v2_2.toString()}));
    }

    public static String f()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassPhoneManage/phone/addClsMultiMember");
        return v0_1.toString();
    }

    public static String f0(String p2)
    {
        if (p2 == null) {
            p2 = "";
        }
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/getSubscribeIncrement.jspx?", new String[] {"updateTime"}), new String[] {p2}));
    }

    public static String f1()
    {
        return com.chaoxing.mobile.s.x8("https://resource.chaoxing.com/apis/cloud/deleteRecs.jspx?");
    }

    public static String f2(String p8, String p9, String p10, int p11, String p12)
    {
        String v1 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v4 = "noteBookName";
        String v2_1 = new StringBuilder();
        v2_1.append(p11);
        v2_1.append("");
        v2_1.toString();
        String v2 = p8;
        v4 = p10;
        return com.chaoxing.mobile.s.A8("https://bookyd.chaoxing.com/apis/notebook/getBookNoteBook?", new String[] {"puid", "tag"}), new String[] {v1, p12}));
    }

    public static String f3(android.content.Context p9, String p10, int p11, int p12, int p13, int p14, int p15, int p16)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v9_5 = new StringBuilder();
        v9_5.append(pk.a.c);
        v9_5.append("apis/note_note/getOpenedNote?");
        String v9_1 = v9_5.toString();
        String v3 = "from";
        String v5 = "version";
        String v1_3 = new StringBuilder();
        v1_3.append(p11);
        v1_3.append("");
        v1_3.toString();
        String v1_5 = new StringBuilder();
        v1_5.append(p12);
        v1_5.append("");
        v1_5.toString();
        StringBuilder v12_2 = new StringBuilder();
        v12_2.append(p13);
        v12_2.append("");
        v12_2.toString();
        StringBuilder v12_4 = new StringBuilder();
        v12_4.append(p14);
        v12_4.append("");
        v12_4.toString();
        StringBuilder v12_6 = new StringBuilder();
        v12_6.append(p15);
        v12_6.append("");
        v12_6.toString();
        StringBuilder v12_8 = new StringBuilder();
        v12_8.append(p16);
        v12_8.append("");
        return com.chaoxing.mobile.s.A8(v9_1, new String[] {"puid", "checkCooperate"}), new String[] {v0, v12_8.toString()}));
    }

    public static String f4(long p3, String p5, android.content.Context p6)
    {
        String v0_3 = new StringBuilder();
        v0_3.append(p3);
        v0_3.append("");
        return com.chaoxing.mobile.s.g4(new String[] {"cfid", "cfname", "uid", "version"}), new String[] {v0_3.toString(), p5, com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.util.n.c}));
    }

    public static String f5(String p2, String p3, String p4)
    {
        Object[] v0_1 = new Object[3];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        return String.format("https://live.chaoxing.com/liveAPI/getOnlineCount?puid=%s&vdoid=%s&streamName=%s", v0_1);
    }

    public static String f6(String p5, int p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("pc/note_note/getNoteDetail?");
        String v1_0 = v1_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p6);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"puid", "cid", "needCoopResource"}), new String[] {v0_2, p5, v3_2.toString()}));
    }

    public static String f7(android.content.Context p5, String p6, String p7, int p8, String p9)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p8);
        v1_1.append("");
        return com.chaoxing.mobile.s.f9("https://appswh.chaoxing.com/apis/speech/getRecognizedSpeech?", new String[] {"puid", "file_url", "fileId", "rate", "format"}), new String[] {v5_4, p6, p7, v1_1.toString(), p9}), 1);
    }

    public static String f8()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/service/appConfig?");
    }

    public static String fa()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/batchMove");
        return v0_1.toString();
    }

    public static String fb(String p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/getCircleList?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "categoryId", "page", "pageSize"}), new String[] {p5, "1", "1", "100"}));
    }

    public static String fc()
    {
        return com.chaoxing.mobile.s.x8("https://mobilelearn.chaoxing.com/newdiscuss/savebegindiscussForCli?");
    }

    public static String fd()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/updateCircle?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String g()
    {
        return "https://fystat1.fy.chaoxing.com/teachClass/addClsMultiMember";
    }

    public static String g0(android.content.Context p8, String p9, int p10, int p11, int p12, int p13)
    {
        com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v8_5 = new StringBuilder();
        v8_5.append(pk.a.c);
        v8_5.append("apis/invitation/getCommonReplys?");
        String v8_1 = v8_5.toString();
        String v4 = "page";
        String v0_2 = new StringBuilder();
        v0_2.append(p10);
        v0_2.append("");
        v0_2.toString();
        String v0_4 = new StringBuilder();
        v0_4.append(p11);
        v0_4.append("");
        v0_4.toString();
        StringBuilder v11_2 = new StringBuilder();
        v11_2.append(p12);
        v11_2.append("");
        v11_2.toString();
        StringBuilder v11_4 = new StringBuilder();
        v11_4.append(p13);
        v11_4.append("");
        return com.chaoxing.mobile.s.A8(v8_1, new String[] {"relationId", "maxW"}), new String[] {p9, v11_4.toString()}));
    }

    public static String g1(int p4, String p5, String p6, int p7)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9("https://resource.chaoxing.com/apis/cloud/deleteRecs.jspx?", new String[] {"ownertype", "ownerId", "recIds", "type"}), new String[] {v1_1, p5, p6, v2_1.toString()}), 1);
    }

    public static String g2(String p3)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(p3);
        v0_1.append(com.chaoxing.mobile.secrets.Keys.KEY_20);
        String v0_3 = com.fanzhou.util.j.d(v0_1.toString());
        Object[] v1_0 = new Object[2];
        v1_0[0] = p3;
        v1_0[1] = v0_3;
        return String.format("https://passport2.chaoxing.com/api/boolean-modified?name=%s&enc=%s", v1_0);
    }

    public static String g3(String p4)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/cooperate/getCooperateContent?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"puid", "cids"}), new String[] {v0_2, p4}));
    }

    public static String g5(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://live.chaoxing.com/liveAPI/getLivePariseCount?streamName=%s&vdoid=%s", v0_1);
    }

    public static String g6(android.content.Context p7, String p8, String p9, int p10, int p11, int p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.c);
        v7_5.append("apis/note_note/getNoteList?");
        String v7_1 = v7_5.toString();
        String v3 = "kw";
        String v1_3 = new StringBuilder();
        v1_3.append(p10);
        v1_3.append("");
        v1_3.toString();
        String v1_5 = new StringBuilder();
        v1_5.append(p11);
        v1_5.append("");
        v1_5.toString();
        StringBuilder v11_2 = new StringBuilder();
        v11_2.append(p12);
        v11_2.append("");
        String v2 = p9;
        return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "maxW"}), new String[] {v0, v11_2.toString()}));
    }

    public static String g7(String p1, int p2)
    {
        String v2_1 = new StringBuilder();
        v2_1.append(pk.a.e);
        v2_1.append("/apis/circle/recomCircleList2?");
        return com.chaoxing.mobile.s.A8(v2_1.toString(), new String[] {"puid"}), new String[] {p1}));
    }

    public static String g8()
    {
        return "https://live.chaoxing.com/taskpagelive/newliveForCli";
    }

    public static String g9()
    {
        return "https://learn.chaoxing.com/apis/user/getUser4CByEmailOrPhone?";
    }

    public static String ga(String p4, String p5, long p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle_folder/addCircleToFolder?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "circleId", "folderId"}), new String[] {p4, p5, String.valueOf(p6)}));
    }

    public static String gb(String p5, int p6, int p7, int p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/recomCircleList?");
        String v0_2 = v0_1.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        String v2_2 = v2_1.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p7);
        v3_2.append("");
        String v7_1 = v3_2.toString();
        StringBuilder v3_4 = new StringBuilder();
        v3_4.append(p8);
        v3_4.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"uid", "maxW", "page", "pageSize"}), new String[] {p5, v2_2, v7_1, v3_4.toString()}));
    }

    public static String gc()
    {
        return "https://yz4.chaoxing.com/selfBuiltProject/topsign";
    }

    public static String gd(String p5, int p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.d.b().a(p5));
        v1_2.append("apis/circle/updateCircleExtend?");
        String v1_0 = v1_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p6);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"puid", "bbsid", "showDelReason"}), new String[] {v0_2, p5, v3_2.toString()}));
    }

    public static String h()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/cmem/addCmems2?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String h0(String p3, int p4, int p5)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/log/getUserOperLogs.jspx?", new String[] {"uid", "page", "pageSize"}), new String[] {p3, v1_1, v2_1.toString()}));
    }

    public static String h1(int p4, String p5, String p6, int p7)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p4);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9("https://resource.chaoxing.com/apis/cloud/deleteRecs.jspx?", new String[] {"ownertype", "ownerId", "folderIds", "type"}), new String[] {v1_1, p5, p6, v2_1.toString()}), 1);
    }

    public static String h2(android.content.Context p12, String p13)
    {
        String v12_3 = p12.getResources().getDisplayMetrics().densityDpi;
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v3 = "fid";
        int v5 = "pageSize";
        Integer v7 = "version";
        Integer v9 = "uid";
        int v2_1 = Integer.valueOf(com.fanzhou.util.n.a);
        String v3_2 = com.chaoxing.study.account.AccountManager.C().D().getDxfid();
        String v4_2 = com.chaoxing.study.account.AccountManager.C().D().getFid();
        Integer v6 = Integer.valueOf(1);
        Integer v7_1 = Integer.valueOf(20000);
        Integer v8_1 = Integer.valueOf(com.fanzhou.util.n.b);
        Integer v9_3 = Integer.valueOf(com.chaoxing.study.account.AccountManager.C().D().getRights());
        String v12_4 = Integer.valueOf(v12_3);
        Object[] v10_1 = new Object[11];
        v10_1[0] = v2_1;
        v10_1[1] = v3_2;
        v10_1[2] = v4_2;
        v10_1[3] = v6;
        v10_1[4] = v7_1;
        v10_1[5] = p13;
        v10_1[6] = com.fanzhou.util.n.c;
        v10_1[7] = v8_1;
        v10_1[8] = v0_0;
        v10_1[9] = v9_3;
        v10_1[10] = v12_4;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/app/boundApps.jspx?", new String[] {"productId", "dpi"}), v10_1);
    }

    public static String h3()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("api/crc2fle");
        return v0_1.toString();
    }

    public static String h4(java.util.List p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p3));
        v0_1.append("apis/topic/updateTopic?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String h5(String p2, String p3, String p4)
    {
        Object[] v0_1 = new Object[3];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        return String.format("https://live.chaoxing.com/liveAPI/setLivePariseCount?streamName=%s&vdoid=%s&puid=%s", v0_1);
    }

    public static String h6()
    {
        return com.chaoxing.mobile.s.x8("https://mobilelearn.chaoxing.com/ppt/jx/gettext?");
    }

    public static String h7(int p6, int p7, int p8, int p9, long p10)
    {
        String v2 = "pageSize";
        int v9_2 = Integer.valueOf(p9);
        String v6_1 = Integer.valueOf(p6);
        int v7_1 = Integer.valueOf(p7);
        Integer v8_1 = Integer.valueOf(p8);
        Long v10_1 = Long.valueOf(p10);
        Object[] v11_1 = new Object[6];
        v11_1[0] = v9_2;
        v11_1[1] = v6_1;
        v11_1[2] = v7_1;
        v11_1[3] = v8_1;
        v11_1[4] = v10_1;
        v11_1[5] = com.fanzhou.util.n.c;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/app/recommendRes.jspx?", new String[] {"cpid", "version"}), v11_1);
    }

    public static String h8(String p4, String p5, String p6, long p7)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p7);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/stickSubscribe.jspx?", new String[] {"uid", "key", "cataid", "cfid"}), new String[] {p4, p5, p6, v1_2.toString()}));
    }

    public static String h9(String p3, String p4, String p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassPhoneManage/phone/fetchStuDetail?ut=t&classId=%s&courseId=%s&loginName=%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[3];
        v1_3[0] = p3;
        v1_3[1] = p4;
        v1_3[2] = p5;
        return String.format(v0_2, v1_3);
    }

    public static String ha()
    {
        return com.chaoxing.mobile.s.x8("https://resource.chaoxing.com/apis/cloud/moveRecs.jspx?");
    }

    public static String hb(String p3, int p4, int p5)
    {
        String[] v0_1 = new Object[1];
        v0_1[0] = p3;
        String v3_3 = String.format("https://rec.chaoxing.com/api/subject/recommend2/%s?", v0_1);
        String v1_1 = new StringBuilder();
        v1_1.append(p4);
        v1_1.append("");
        String v1_2 = v1_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v3_3, new String[] {"cpage", "size"}), new String[] {v1_2, v2_1.toString()}));
    }

    public static String hc(String p5, long p6)
    {
        String v0_3 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (!com.fanzhou.util.w.s(p5)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.a.e);
            v6_2.append("apis/topic/topSet?");
            String v6_3 = v6_2.toString();
            StringBuilder v1_1 = new StringBuilder();
            v1_1.append(v0_3);
            v1_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"uuid", "puid"}), new String[] {p5, v1_1.toString()}));
        } else {
            String v5_4 = new StringBuilder();
            v5_4.append(pk.a.e);
            v5_4.append("apis/topic/topSet?");
            String v5_5 = v5_4.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p6);
            v2_1.append("");
            String v6_4 = v2_1.toString();
            String[] v7_4 = new StringBuilder();
            v7_4.append(v0_3);
            v7_4.append("");
            return com.chaoxing.mobile.s.A8(v5_5, new String[] {"topicId", "puid"}), new String[] {v6_4, v7_4.toString()}));
        }
    }

    public static String hd(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle_folder/updateCircleFolderOrder?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "folderId"}), new String[] {p3, p4}));
    }

    public static String i(int p6, String p7, String p8, String p9)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        return com.chaoxing.mobile.s.e9("https://im.chaoxing.com/apis/message/addMessage?", new String[] {"isGroup", "hxMsgId", "tuid", "chatManId", "groupType"}), new String[] {v2_1.toString(), p8, v0_2, p7, p9}));
    }

    public static String i0(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://mobilelearn.chaoxing.com/ppt/groupAPI/getActiveCount?uid=%s", v0_1);
    }

    public static String i1(android.content.Context p4, int p5, String p6, String p7)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p5);
        v1_1.append("");
        return com.chaoxing.mobile.s.e9("https://im.chaoxing.com/apis/message/revokeMessage?", new String[] {"isGroup", "hxMsgId", "tuid", "chatManId"}), new String[] {v1_1.toString(), p7, v4_4, p6}));
    }

    public static String i2(String p2, String p3)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/isExistsSharedSubscribe.jspx?", new String[] {"uid", "puid"}), new String[] {p2, p3}));
    }

    public static String i3(String p2)
    {
        if (!ve.f.o(p2)) {
            p2 = pk.a.a;
        }
        StringBuilder v0_2 = new StringBuilder();
        v0_2.append(p2);
        v0_2.append("api/crc2fle");
        return v0_2.toString();
    }

    public static String i4(int p3)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/getmyfiledcourse?rss=1&partCoruse=%d");
        String v0_2 = v0_1.toString();
        Object[] v1_1 = new Object[1];
        v1_1[0] = Integer.valueOf(p3);
        return String.format(v0_2, v1_1);
    }

    public static String i5(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://live.chaoxing.com/zhibo/liveReview?streamName=%s", v0_1);
    }

    public static String i6(String p2)
    {
        String v1_2 = new StringBuilder();
        v1_2.append(p2);
        v1_2.append("");
        return com.chaoxing.mobile.s.e9("https://sharewh.chaoxing.com/apis/parse/parsePage?", new String[] {"url"}), new String[] {v1_2.toString()}));
    }

    public static String i7(android.content.Context p2)
    {
        return com.chaoxing.mobile.s.A8("https://money.chaoxing.com/apis/packet/getRedPacketBless?", new String[] {"puid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid()}));
    }

    public static String i8(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://zhibo.chaoxing.com/%s", v0_1);
    }

    public static String i9(android.content.Context p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/persongroup/getPersonGroup?", new String[] {"tid", "puid", "page", "pageSize"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid(), p6, p7}), 1);
    }

    public static String ia()
    {
        return "https://yz4.chaoxing.com/selfBuiltProject/batchMove";
    }

    public static String ib(String p3)
    {
        return com.chaoxing.mobile.s.A8("https://special.chaoxing.com/apis/special/getSpecial?", new String[] {"courseId", "fields", "version"}), new String[] {p3, "mooc_courseId,subCount", "1"}));
    }

    public static String ic(String p2, String p3)
    {
        String v2_1 = com.chaoxing.mobile.s.M9(p2);
        String v3_1 = com.chaoxing.mobile.s.M9(p3);
        Object[] v0_1 = new Object[2];
        v0_1[0] = v2_1;
        v0_1[1] = v3_1;
        return String.format("https://live.chaoxing.com/liveAPI/getlivestatus?streamName=%s&vdoid=%s", v0_1);
    }

    public static String id(java.util.List p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p3));
        v0_1.append("apis/circle/updateCircle?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String j(String p4, int p5)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p5);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8("https://im.chaoxing.com/apis/message/addMessageTransInfo?", new String[] {"puid", "chat_id", "chat_type"}), new String[] {v0_2, p4, v2_1.toString()}));
    }

    public static String j0(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://mobilelearn.chaoxing.com/ppt/activeAPI/classTaskCount?puid=%s", v0_1);
    }

    public static String j1(String p3, String p4, String p5)
    {
        if (android.text.TextUtils.isEmpty(p5)) {
            String v5_3 = new StringBuilder();
            v5_3.append(pk.d.b().a(p4));
            v5_3.append("/apis/cmem/clearNonCXCmems?");
            return com.chaoxing.mobile.s.A8(v5_3.toString(), new String[] {"puid", "circleId"}), new String[] {p3, p4}));
        } else {
            String v4_2 = new StringBuilder();
            v4_2.append(pk.d.b().a(p5));
            v4_2.append("/apis/cmem/clearNonCXCmems?");
            return com.chaoxing.mobile.s.A8(v4_2.toString(), new String[] {"puid", "bbsid"}), new String[] {p3, p5}));
        }
    }

    public static String j2(android.content.Context p4, int p5, String p6, String p7)
    {
        if ((p5 != 2) && ((p5 != 3) && (p5 != 4))) {
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/scribe/cancelScribe?", new String[] {"uid", "st", "uuid", "cataid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.document.c.b(p5), p6, p7}));
        } else {
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/scribe/cancelScribe?", new String[] {"uid", "st", "dxid", "cataid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.document.c.b(p5), p6, p7}));
        }
    }

    public static String j3(String p2, String p3, int p4)
    {
        Integer v4_1 = Integer.valueOf(p4);
        Object[] v0_1 = new Object[3];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = v4_1;
        return String.format("https://mobilelearn.chaoxing.com/phoneactivehistory/phonetimelist?courseId=%s&classId=%s&from=%d", v0_1);
    }

    public static String j4(int p2, String p3, int p4, long p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/reLeftSlip?type=%d&courseId=%s&handle=%s&catalogId=%d");
        String v0_2 = v0_1.toString();
        String v2_5 = Integer.valueOf(p2);
        Integer v4_1 = Integer.valueOf(p4);
        Long v5_1 = Long.valueOf(p5);
        Object[] v6_1 = new Object[4];
        v6_1[0] = v2_5;
        v6_1[1] = p3;
        v6_1[2] = v4_1;
        v6_1[3] = v5_1;
        return String.format(v0_2, v6_1);
    }

    public static String j5(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = p3;
        return String.format("https://zhibo.chaoxing.com/live/mobileSharePageLive?streamName=%s&vdoid=%s", v0_1);
    }

    public static String j6(android.content.Context p3, String p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_note/getNoteList2?");
        return com.chaoxing.mobile.s.e9(v0_2.toString(), new String[] {"puid", "notebookCid"}), new String[] {v3_4, p4}));
    }

    public static String j7(android.content.Context p3)
    {
        return com.chaoxing.mobile.s.A8("https://money.chaoxing.com/apis/packet/getVipRedPacketCfg?", new String[] {"uid", "puid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid()}));
    }

    public static String j8(String p8, String p9, String p10, long p11, int p13)
    {
        String v2 = "key";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p11);
        v1_1.append("");
        v1_1.toString();
        StringBuilder v12_1 = new StringBuilder();
        v12_1.append(p13);
        v12_1.append("");
        v12_1.toString();
        String v4 = p10;
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/addSubscribe.jspx?", new String[] {"uid", "version"}), new String[] {p8, com.fanzhou.util.n.c}));
    }

    public static String j9(android.content.Context p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/persongroup/getPersonUserGroup?", new String[] {"tid", "puid", "page", "pagesize"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid(), p6, p7}), 1);
    }

    public static String ja(String p2, String p3, String p4, String p5, String p6)
    {
        if (!com.fanzhou.util.w.s(p5)) {
            String v4_3 = new StringBuilder();
            v4_3.append(pk.d.b().a(p6));
            v4_3.append("apis/topic_folder/addTopicToFolder?");
            String v4_1 = v4_3.toString();
            Object[] v0_3 = new Object[3];
            v0_3[0] = p2;
            v0_3[1] = p3;
            v0_3[2] = p5;
            return com.chaoxing.mobile.s.z8(v4_1, new String[] {"puid", "uuid", "folder_uuid"}), v0_3);
        } else {
            return com.chaoxing.mobile.s.ka(p2, p3, p4, p6);
        }
    }

    public static String jb(int p2, int p3)
    {
        int v0_1 = new StringBuilder();
        v0_1.append(p2);
        v0_1.append("");
        int v0_3 = v0_1.toString();
        int v1_2 = new StringBuilder();
        v1_2.append(p3);
        v1_2.append("");
        String v2_1 = v1_2.toString();
        Object[] v3_2 = new Object[2];
        v3_2[0] = v0_3;
        v3_2[1] = v2_1;
        return String.format("https://home-yd.chaoxing.com/apis/data/getIdxSourceVoByPoolId?poolId=tuijian&incode=000000&page=%s&pageSize=%s", v3_2);
    }

    public static String jc(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://special.rhky.com/mobile/mooc/toinfo/%s", v0_1);
    }

    public static String jd(String p6, String p7, int p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircle?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "isShow"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircle?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "isShow"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String k(String p5, String p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/praise/addNoteReplyPraise?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"replyUuid", "puid", "relationId"}), new String[] {p5, v0_2, p6}));
    }

    public static String k0(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivecount?puid=%s&source=15", v0_1);
    }

    public static String k1(android.content.Context p3, int p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/deleteNotice?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p4);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"noticeId", "puid"}), new String[] {v2_2.toString(), v3_4}));
    }

    public static String k2(String p4, String p5, String p6, long p7)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p7);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/cancelStickSubscribe.jspx?", new String[] {"uid", "key", "cataid", "cfid"}), new String[] {p4, p5, p6, v1_2.toString()}));
    }

    public static String k3()
    {
        String v0_1 = new Object[0];
        return String.format("https://x.chaoxing.com/apis/toScreen/courseCatalogToScreen", v0_1);
    }

    public static String k4()
    {
        return "https://ke.chaoxing.com/api/xxt/iCourseList";
    }

    public static String k5(String p2, String p3, String p4, String p5, String p6, String p7, String p8, String p9)
    {
        Object[] v0_1 = new Object[8];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        v0_1[3] = p5;
        v0_1[4] = p6;
        v0_1[5] = p7;
        v0_1[6] = p8;
        v0_1[7] = p9;
        return com.chaoxing.mobile.s.L1("https://passport2-api.chaoxing.com/oauth2/qq/openid?access_token=%s&expires_in=%s&refresh_token=%s&fid=%s&openid1=%s&refer=%s&enc=%s&version=1&unionid=%s", v0_1);
    }

    public static String k6(String p7, String p8, int p9, int p10)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/praise/getNotePraisesWithPoff?");
        String v1_0 = v1_2.toString();
        String v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        String v3_3 = v3_2.toString();
        StringBuilder v4_2 = new StringBuilder();
        v4_2.append(p10);
        v4_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"noteCid", "puid", "lastValue", "pageSize", "page"}), new String[] {p7, v0_2, p8, v3_3, v4_2.toString()}));
    }

    public static String k7(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/topic/addTopicWithCheck?");
        String v0_2 = v0_1.toString();
        Object[] v2_2 = new Object[3];
        v2_2[0] = p4;
        v2_2[1] = p5;
        v2_2[2] = p6;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "uuid", "bbsid"}), v2_2);
    }

    public static String k8(android.content.Context p7, long p8)
    {
        String v7_8 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getFid();
        Object[] v3 = "fid";
        int v8_1 = Long.valueOf(p8);
        Integer v9_1 = Integer.valueOf(com.fanzhou.util.n.a);
        Integer v2_1 = Integer.valueOf(com.fanzhou.util.n.b);
        Object[] v3_1 = new Object[6];
        v3_1[0] = v8_1;
        v3_1[1] = v7_8;
        v3_1[2] = v0_0;
        v3_1[3] = v9_1;
        v3_1[4] = com.fanzhou.util.n.c;
        v3_1[5] = v2_1;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/app/getRecMarkets.jspx?", new String[] {"pid", "clientType"}), v3_1);
    }

    public static String k9(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://statisticyd.chaoxing.com/apis/statistic/getUserStatistic?", new String[] {"puid"}), new String[] {p2}));
    }

    public static String kb(String p2, int p3)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p3);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://money.chaoxing.com/redpacket/split?", new String[] {"id", "flag"}), new String[] {p2, v1_2.toString()}));
    }

    public static String kc(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://mooc1-api.chaoxing.com/chapterlist?courseId=%s", v0_1);
    }

    public static String kd(String p6, String p7, int p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircle?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "showQrcode"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircle?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "showQrcode"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String l(android.content.Context p4, String p5, String p6)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/addNoticeToFolder?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "folder_uuid", "noticeIds"}), new String[] {v4_4, p5, p6}));
    }

    public static String l0(String p10, String p11, String p12, String p13, String p14, String p15)
    {
        String v2 = "public";
        String v4 = "approval";
        String v6 = "invite";
        String v5 = "false";
        v6 = p12;
        String v8 = p14;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/creatCustomDeptChatGroups?", new String[] {"owner", "desc"}), new String[] {p10, p15}), 1);
    }

    public static String l1(int p4, int p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/replyDelete?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"noticeId", "replyId", "puid"}), new String[] {String.valueOf(p4), String.valueOf(p5), p6}));
    }

    public static String l2(String p4, String p5, String p6)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/cancelSubscribe.jspx?", new String[] {"uid", "key", "cataid", "version"}), new String[] {p4, p5, p6, com.fanzhou.util.n.c}));
    }

    public static String l3()
    {
        return "https://passport2-api.chaoxing.com/v11/importcourse?trust=true";
    }

    public static String l4()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("visit/phone/isOpenFace");
        return v0_1.toString();
    }

    public static String l5(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = com.fanzhou.util.y.j0(p2);
        return com.chaoxing.mobile.s.L1("https://sso.chaoxing.com/apis/login/userLogin4Try.do?enc=%s", v0_1);
    }

    public static String l6(String p7, String p8, int p9, int p10)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/read/getNoteReadPersonsWithPoff?");
        String v1_0 = v1_2.toString();
        String v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        String v3_3 = v3_2.toString();
        StringBuilder v4_2 = new StringBuilder();
        v4_2.append(p10);
        v4_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"puid", "noteCid", "lastValue", "pageSize", "page"}), new String[] {v0_2, p7, p8, v3_3, v4_2.toString()}));
    }

    public static String l7(android.content.Context p3, int p4)
    {
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/remind/getRemindAuth?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p4);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "sourceType"}), new String[] {v3_4, v2_2.toString()}));
    }

    public static String l8()
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/app/getSubscribeApp.jspx?", new String[] {"version"}), new String[] {com.fanzhou.util.n.c}));
    }

    public static String l9(int p2)
    {
        String v1_2 = new StringBuilder();
        v1_2.append(p2);
        v1_2.append("");
        return com.chaoxing.mobile.s.e9("https://learn.chaoxing.com/apis/user/getUserStatus?", new String[] {"us"}), new String[] {v1_2.toString()}));
    }

    public static String la()
    {
        return "https://mobile3.chaoxing.com/newmobile/getCourses";
    }

    public static String lb()
    {
        return com.chaoxing.mobile.s.x8("https://money.chaoxing.com/apis/packet/packetSend?");
    }

    public static String lc()
    {
        return com.chaoxing.mobile.s.x8("https://resource.chaoxing.com/apis/cloud/insertRecs.jspx?");
    }

    public static String ld(String p6, String p7, int p8)
    {
        String v0_5 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircle?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "memberVisible"}), new String[] {v0_5, p7, v3_1.toString()}));
        } else {
            String v0_3 = new StringBuilder();
            v0_3.append(pk.d.b().a(p6));
            v0_3.append("apis/circle/updateCircle?");
            String v0_4 = v0_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v0_4, new String[] {"puid", "bbsid", "memberVisible"}), new String[] {p6, p7, v3_3.toString()}));
        }
    }

    public static String m(android.content.Context p5, int p6, String p7, int p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/addOrCancelPraise?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p8);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"type", "relationId", "isPraise", "puid"}), new String[] {v2_3, p7, v3_2.toString(), v5_4}));
    }

    public static String m0(String p2, String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/creatDeptCircle?", new String[] {"deptid", "name"}), new String[] {p2, p3}), 1);
    }

    public static String m1(String p2, String p3)
    {
        return com.chaoxing.mobile.s.A8("https://specie.chaoxing.com/apis/message/delMessageNews?", new String[] {"puid", "id"}), new String[] {p2, p3}));
    }

    public static String m2()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.a);
        v0_1.append("upload?");
        return v0_1.toString();
    }

    public static String m3(android.content.Context p14, String p15, int p16, String p17, String p18, int p19, int p20)
    {
        String v6 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v14_5 = new StringBuilder();
        v14_5.append(pk.a.f);
        v14_5.append("apis/notice/myNotices?");
        String v14_1 = v14_5.toString();
        String v9 = "kw";
        String v11 = "page";
        String[] v0_2 = new StringBuilder();
        v0_2.append(p16);
        v0_2.append("");
        String[] v0_3 = v0_2.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p19);
        v2_1.append("");
        v2_1.toString();
        String v2_3 = new StringBuilder();
        v2_3.append(p20);
        v2_3.append("");
        v2_3.toString();
        String v2 = p17;
        String v1 = v0_3;
        return com.chaoxing.mobile.s.A8(v14_1, new String[] {"type", "puid"}), new String[] {p15, v6}));
    }

    public static String m4()
    {
        return "https://mobilelearn.chaoxing.com/notice/sendNotice";
    }

    public static String m5(String p2, String p3, int p4)
    {
        try {
            String v2_3 = java.net.URLEncoder.encode(p2, "utf-8");
        } catch (Object[] v0_3) {
            v0_3.printStackTrace();
        }
        String v3_1 = com.fanzhou.util.y.j0(p3);
        if (com.fanzhou.util.w.q(v3_1)) {
            v3_1 = "";
        }
        Integer v4_1 = Integer.valueOf(p4);
        Object[] v0_2 = new Object[3];
        v0_2[0] = v2_3;
        v0_2[1] = v3_1;
        v0_2[2] = v4_1;
        return com.chaoxing.mobile.s.L1("https://sso.chaoxing.com/apis/login/userLogin.do?username=%s&password=%s&encrypted=0&ptype=%s", v0_2);
    }

    public static String m6(android.content.Context p5, String p6, int p7, int p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_note/getNoteReadPersons?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p7);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p8);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "noteCid", "page", "pageSize"}), new String[] {v5_4, p6, v2_3, v3_2.toString()}));
    }

    public static String m7(String p5, String p6, String p7, int p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/invitation/getReplyCheckListWithPoff?");
        String v0_2 = v0_1.toString();
        Integer v8_1 = Integer.valueOf(p8);
        Object[] v2_2 = new Object[4];
        v2_2[0] = p5;
        v2_2[1] = p6;
        v2_2[2] = p7;
        v2_2[3] = v8_1;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "bbsid", "lastValue", "pageSize"}), v2_2);
    }

    public static String m8(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "showPic"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "showPic"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String m9(android.content.Context p2, String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/user/getUsersDepts?", new String[] {"puid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid()}), 1);
    }

    public static String ma()
    {
        return "https://creditbank.chaoxing.com/mobile/course/kecheng";
    }

    public static String mb(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://money.chaoxing.com/apis/packet/packetStatus?", new String[] {"id"}), new String[] {p2}));
    }

    public static String mc(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/facade/subsStuCourseBatch.jspx?", new String[] {"keys"}), new String[] {p2}));
    }

    public static String md(String p4, String p5, int p6)
    {
        String v5_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.d.b().a(p4));
        v0_2.append("apis/circle/updateCircleExtend?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "bbsid", "isShowPrice"}), new String[] {v5_2, p4, v2_2.toString()}));
    }

    public static String n()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/persongroup/addUser2PersonGroupV2?");
    }

    public static String n0(String p10, String p11, String p12, String p13, String p14)
    {
        String v2 = "public";
        String v4 = "approval";
        String v6 = "invite";
        v4 = "2000";
        v6 = p12;
        String v8 = p14;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/creatUnitDeptChatGroups?", new String[] {"owner", "desc"}), new String[] {p10, ""}), 1);
    }

    public static String n1(long p3, long p5, String p7, String p8)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/invitation/deleteReply?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"topicId", "replyId", "uid"}), new String[] {String.valueOf(p3), String.valueOf(p5), p7}));
    }

    public static String n2(String p2)
    {
        if (!ve.f.o(p2)) {
            p2 = pk.a.a;
        }
        StringBuilder v0_2 = new StringBuilder();
        v0_2.append(p2);
        v0_2.append("upload?");
        return v0_2.toString();
    }

    public static String n3(android.content.Context p20, String p21, int p22, String p23, String p24, int p25, String p26, int p27, int p28, String p29)
    {
        com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_5 = new StringBuilder();
        v0_5.append(pk.a.f);
        v0_5.append("apis/notice/myNotices_v2?");
        String v0_1 = v0_5.toString();
        String v12 = "kw";
        String v14 = "contSize";
        String v16 = "page";
        String[] v1_2 = new StringBuilder();
        v1_2.append(p22);
        v1_2.append("");
        v1_2.toString();
        String v3_1 = new StringBuilder();
        v3_1.append(p25);
        v3_1.append("");
        v3_1.toString();
        String v3_3 = new StringBuilder();
        v3_3.append(p27);
        v3_3.append("");
        v3_3.toString();
        String v3_5 = new StringBuilder();
        v3_5.append(p28);
        v3_5.append("");
        v3_5.toString();
        String v3 = p23;
        String v6 = p26;
        return com.chaoxing.mobile.s.A8(v0_1, new String[] {"type", "lastGetId"}), new String[] {p21, p29}));
    }

    public static String n4(String p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("http://cloud.ananas.chaoxing.com/status?token=");
        v0_1.append(p2);
        v0_1.append("&d=");
        v0_1.append(p3);
        return v0_1.toString();
    }

    public static String n5(String p2, String p3, String p4, String p5, int p6, int p7)
    {
        String v4_1 = com.fanzhou.util.m.b(p4);
        String v5_1 = com.fanzhou.util.m.b(p5);
        Integer v6_1 = Integer.valueOf(p6);
        Integer v7_1 = Integer.valueOf(p7);
        Object[] v0_1 = new Object[6];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = v4_1;
        v0_1[3] = v5_1;
        v0_1[4] = v6_1;
        v0_1[5] = v7_1;
        return com.chaoxing.mobile.s.L1("https://auth.chaoxing.com/apis/passport/login4DX?sid=%s&fid=%s&uname=%s&pwd=%s&loginId=%d&loginType=%d", v0_1);
    }

    public static String n6(String p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.d);
        v0_1.append("apis/userprivacy/getActivityTimeLimit?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid"}), new String[] {p2}));
    }

    public static String n7(String p6, String p7, String p8, String p9, int p10)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p7));
        v0_1.append("apis/invitation/getReplyCheckListWithPoff2?");
        String v0_2 = v0_1.toString();
        Integer v10_1 = Integer.valueOf(p10);
        Object[] v2_2 = new Object[5];
        v2_2[0] = p6;
        v2_2[1] = p7;
        v2_2[2] = p8;
        v2_2[3] = p9;
        v2_2[4] = v10_1;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "bbsid", "lastValue", "kw", "pageSize"}), v2_2);
    }

    public static String n8(android.content.Context p3, String p4, String p5)
    {
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/pptactive/qlfileList?", new String[] {"uid", "classId", "courseId"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid(), p4, p5}), 0);
    }

    public static String n9(String p7, int p8, String p9)
    {
        String[] v1_4 = new StringBuilder();
        v1_4.append(p7);
        v1_4.append(com.chaoxing.mobile.secrets.Keys.KEY_23);
        String v0_2 = com.fanzhou.util.j.d(v1_4.toString());
        if (!com.fanzhou.util.w.q(p9)) {
            StringBuilder v3_2 = new StringBuilder();
            v3_2.append(p8);
            v3_2.append("");
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/sendRandomPwd4Update?", new String[] {"account", "enc", "accountstyle", "countrycode"}), new String[] {p7, v0_2, v3_2.toString(), p9}));
        } else {
            String[] v1_6 = new StringBuilder();
            v1_6.append(p8);
            v1_6.append("");
            return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/sendRandomPwd4Update?", new String[] {"account", "enc", "accountstyle"}), new String[] {p7, v0_2, v1_6.toString()}));
        }
    }

    public static String na(String p3)
    {
        String v3_1 = new StringBuilder();
        v3_1.append(gc.b.d);
        v3_1.append("mycourse/backclazzdata?view=json&getTchClazzType=1&mcode=%s");
        String v3_3 = v3_1.toString();
        Object[] v0_3 = new Object[1];
        v0_3[0] = "";
        return String.format(v3_3, v0_3);
    }

    public static String nb(String p3, String p4, String p5)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p5));
        v0_1.append("apis/topic/choiceCancel?");
        String v5_1 = v0_1.toString();
        String v1_2 = new StringBuilder();
        v1_2.append(p3);
        v1_2.append("");
        String v1_3 = v1_2.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v5_1, new String[] {"uuid", "puid"}), new String[] {v1_3, v2_1.toString()}));
    }

    public static String nc()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/subscribe/addSpecialSubscribe.jspx?");
    }

    public static String nd(java.util.List p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/updateCircle?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String o(boolean p4, String p5)
    {
        if (p4 == null) {
            return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/addUsersToGroupBatch?", new String[] {"groupid", "vs"}), new String[] {p5, "1"}), 1);
        } else {
            return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/addUsersToGroupBatchFor104?", new String[] {"groupid", "vs"}), new String[] {p5, "1"}), 1);
        }
    }

    public static String o0(String p8, String p9)
    {
        int v2 = "desc";
        String v4 = "maxusers";
        String v6 = "false";
        String v3 = "";
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/creatChatGroups?", new String[] {"owner", "vs"}), new String[] {p8, p9}), 1);
    }

    public static String o1(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/invitation/deleteReplyWithCheck?");
        String v0_2 = v0_1.toString();
        Object[] v2_2 = new Object[3];
        v2_2[0] = p4;
        v2_2[1] = p5;
        v2_2[2] = p6;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "uuid", "bbsid"}), v2_2);
    }

    public static String o2(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p3;
        v0_1[1] = p2;
        return String.format("https://x.chaoxing.com/apis/choiceClass/choice?courseId=%s&classId=%s", v0_1);
    }

    public static String o3()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("phone/courses");
        Object[] v1_3 = new Object[0];
        return String.format(v0_1.toString(), v1_3);
    }

    public static String o4()
    {
        return "https://mobilelearn.chaoxing.com/ppt/activeAPI/personalActiveLibraryV2?";
    }

    public static String o5(String p2, String p3, String p4, String p5, String p6)
    {
        Object[] v0_1 = new Object[5];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        v0_1[3] = p5;
        v0_1[4] = p6;
        return com.chaoxing.mobile.s.L1("https://passport2-api.chaoxing.com/oauth2/weixin/user_info?token=%s&unionid=%s&fid=%s&refer=%s&enc=%s&version=1", v0_1);
    }

    public static String o6(String p2, int p3)
    {
        Integer v3_1 = Integer.valueOf(p3);
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = v3_1;
        return String.format("https://x.chaoxing.com/apis/toScreen/noteToScreen?uuid=%s&opt=%s", v0_1);
    }

    public static String o7(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://specie.chaoxing.com/apis/message/getUnreadPraiseCount?", new String[] {"puid"}), new String[] {p2}));
    }

    public static String o8(String p2, String p3, String p4, String p5)
    {
        Object[] v0_1 = new Object[4];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        v0_1[3] = p5;
        return String.format("https://live.chaoxing.com/liveAPI/sendMessageM?puid=%s&realName=%s&content=%s&liveId=%s", v0_1);
    }

    public static String o9(java.util.List p1)
    {
        return com.chaoxing.mobile.s.y8("https://apps.chaoxing.com/apis/right/verifyIncode.jspx?", p1);
    }

    public static String oa(String p3, int p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/myJoinCircles?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "maxW"}), new String[] {p3, v2_1.toString()}));
    }

    public static String ob(String p6, String p7, String p8, int p9, String p10)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/invitation/addCommonReply?");
        String v0_2 = v0_1.toString();
        String v2_0 = "";
        if (p9 != 0) {
            StringBuilder v3_2 = new StringBuilder();
            v3_2.append(p9);
            v3_2.append("");
            v2_0 = v3_2.toString();
        }
        return com.chaoxing.mobile.s.f9(v0_2, new String[] {"puid", "relationId", "beRepliedUuid", "maxW", "uuid"}), new String[] {p6, p7, p8, v2_0, p10}), 1);
    }

    public static String oc()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/subscribe/addSubscribe.jspx?");
    }

    public static String od(String p6, String p7, long p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircle?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "expireTime"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircle?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "expireTime"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String p(android.content.Context p4, String p5, String p6, String p7)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/addUserFriendGroup?", new String[] {"uid", "gid", "fids", "dfids"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), p5, p6, p7}), 1);
    }

    public static String p0(android.content.Context p4, String p5, double p6, double p8)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p6);
        v1_1.append("");
        String v7 = v1_1.toString();
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append(p8);
        v1_3.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/contact/createContactCode?", new String[] {"code", "puid", "latitude", "longitude"}), new String[] {p5, v4_4, v7, v1_3.toString()}));
    }

    public static String p1(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://yz4.chaoxing.com/selfBuiltProject/deleteFolderOrSubject?id=%s", v0_1);
    }

    public static String p2(android.content.Context p4, String p5, String p6)
    {
        Object[] v1_1 = new Object[4];
        v1_1[0] = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        v1_1[1] = p5;
        v1_1[2] = p6;
        v1_1[3] = "1";
        return com.chaoxing.mobile.s.z8("https://learn.chaoxing.com/apis/user/updateValidateMsgStatus?", new String[] {"puid", "mid", "status", "vs"}), v1_1);
    }

    public static String p3(String p2, String p3, String p4, String p5)
    {
        Object[] v0_1 = new Object[4];
        v0_1[0] = p2;
        v0_1[1] = p3;
        v0_1[2] = p4;
        v0_1[3] = p5;
        return String.format("https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=%s&page=%s&pageSize=%s", v0_1);
    }

    public static String p4(String p5, String p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/note_notebook/getFixedNotebook?");
        String v1_0 = v1_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p5);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"puid", "noteBookType", "tag"}), new String[] {v0_2, v3_2.toString(), p6}));
    }

    public static String p5(String p5, String p6, String p7, String p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/score/topicReplyScoreIn?");
        String v0_2 = v0_1.toString();
        Object[] v2_2 = new Object[4];
        v2_2[0] = p5;
        v2_2[1] = p6;
        v2_2[2] = p7;
        v2_2[3] = p8;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "replyId", "score", "bbsid"}), v2_2);
    }

    public static String p6(String p7, String p8, int p9, int p10)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/praise/getNotebookPraises?");
        String v1_0 = v1_2.toString();
        String v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        String v3_3 = v3_2.toString();
        StringBuilder v4_2 = new StringBuilder();
        v4_2.append(p10);
        v4_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"notebookCid", "puid", "lastValue", "pageSize", "page"}), new String[] {p7, v0_2, p8, v3_3, v4_2.toString()}));
    }

    public static String p7(String p5, String p6, int p7, String p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/getReplyPageNumber?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "noticeId", "replyId", "from"}), new String[] {p5, p6, v2_1.toString(), p8}));
    }

    public static String p8(int p3, int p4, int p5)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/getUserTalents?", new String[] {"page", "pageSize", "praiseStatus"}), new String[] {String.valueOf(p3), String.valueOf(p4), String.valueOf(p5)}));
    }

    public static String p9(java.util.List p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append("https://learn.chaoxing.com/apis/user/userLogin4Third?");
        v0_1.append(com.fanzhou.util.y.T(com.chaoxing.mobile.secrets.Keys.INF_ENC_TOKEN_74f68bad, com.chaoxing.mobile.secrets.Keys.INF_ENC_KEY_74f68bad, p3));
        return v0_1.toString();
    }

    public static String pb(String p17, String p18, String p19, String p20, String p21, String p22, String p23, String p24)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(p18);
        v0_1.append("A*1~Gq0L):_&8^e!@s");
        com.fanzhou.util.j.b(v0_1.toString());
        String v0_3 = new StringBuilder();
        v0_3.append(pk.a.c);
        v0_3.append("comm/apis/reply/addCommonReply?");
        String[] v10 = "sid2";
        String v12 = "uuid";
        String v14 = "enc";
        String v4 = p20;
        String v6 = p22;
        return com.chaoxing.mobile.s.f9(v0_3.toString(), new String[] {"puid", "notePartContent"}), new String[] {p17, p24}), 1);
    }

    public static String pc()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/subscribe/addExternalSubscribe.jspx?");
    }

    public static String pd(String p6, String p7, int p8)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p6)) {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircle?");
            String v6_3 = v6_2.toString();
            StringBuilder v3_1 = new StringBuilder();
            v3_1.append(p8);
            v3_1.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "circleId", "check"}), new String[] {v0_2, p7, v3_1.toString()}));
        } else {
            String[] v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircle?");
            String[] v7_4 = v7_3.toString();
            StringBuilder v3_3 = new StringBuilder();
            v3_3.append(p8);
            v3_3.append("");
            return com.chaoxing.mobile.s.A8(v7_4, new String[] {"puid", "bbsid", "check"}), new String[] {v0_2, p6, v3_3.toString()}));
        }
    }

    public static String q()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/note_note/addReadNote?");
        return com.chaoxing.mobile.s.x8(v0_1.toString());
    }

    public static String q0(String p3)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("phone/coursecontroller/create?opertaion=%s");
        String v0_2 = v0_1.toString();
        Object[] v1_3 = new Object[1];
        v1_3[0] = p3;
        return String.format(v0_2, v1_3);
    }

    public static String q1()
    {
        return "https://yz4.chaoxing.com/selfBuiltProject/batchDelete";
    }

    public static String q2(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://special.chaoxing.com/apis/special/getSpecialChapters?", new String[] {"courseId"}), new String[] {p2}));
    }

    public static String q3()
    {
        return "https://special.rhky.com/mobile/mooc/tocourse/91687483";
    }

    public static String q4(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/app/getRecDatasCnts.jspx?", new String[] {"cataid"}), new String[] {p2}));
    }

    public static String q5(String p5, String p6, String p7, String p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/score/topicReplyScoreIn?");
        String v0_2 = v0_1.toString();
        Object[] v2_2 = new Object[4];
        v2_2[0] = p5;
        v2_2[1] = p6;
        v2_2[2] = p7;
        v2_2[3] = p8;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "topicId", "score", "bbsid"}), v2_2);
    }

    public static String q6(String p7, String p8, int p9, int p10)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/read/getNotebookReadPersons?");
        String v1_0 = v1_2.toString();
        String v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        String v3_3 = v3_2.toString();
        StringBuilder v4_2 = new StringBuilder();
        v4_2.append(p10);
        v4_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"puid", "notebookCid", "lastValue", "pageSize", "page"}), new String[] {v0_2, p7, p8, v3_3, v4_2.toString()}));
    }

    public static String q7()
    {
        return "https://home-yd.chaoxing.com/html/resCenter/index.html";
    }

    public static String q8(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/getCntForPubSub.jspx?", new String[] {"puids"}), new String[] {p2}));
    }

    public static String q9(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/v2apis/friend/getFollowStatus?", new String[] {"tid"}), new String[] {p2}));
    }

    public static String qa(android.content.Context p7, String p8, String p9, String p10, int p11, int p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.f);
        v7_5.append("apis/notice/myNotices_v2?");
        String v7_1 = v7_5.toString();
        String v3 = "type";
        String v1_3 = new StringBuilder();
        v1_3.append(p11);
        v1_3.append("");
        v1_3.toString();
        String v1_5 = new StringBuilder();
        v1_5.append(p12);
        v1_5.append("");
        String v2 = p9;
        return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "pageSize"}), new String[] {v0, v1_5.toString()}));
    }

    public static String qb(String p12, int p13, String p14, int p15, int p16, int p17)
    {
        // Both branches of the condition point to the same code.
        // if (!com.fanzhou.util.w.q(p14)) {
            String v7 = "kw";
            String v9 = "page";
            StringBuilder v0_2 = new StringBuilder();
            v0_2.append(p13);
            v0_2.append("");
            v0_2.toString();
            String v13_2 = new StringBuilder();
            v13_2.append(p15);
            v13_2.append("");
            v13_2.toString();
            String v13_4 = new StringBuilder();
            v13_4.append(p16);
            v13_4.append("");
            v13_4.toString();
            String v13_6 = new StringBuilder();
            v13_6.append(p17);
            v13_6.append("");
            v13_6.toString();
            return com.chaoxing.mobile.s.A8("https://specie.chaoxing.com/apis/message/getMessageNewsList?", new String[] {"puid", "version"}), new String[] {p12, "20160429"}));
        // }
    }

    public static String qc()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/subscribe/addSubscribeBatch.jspx?");
    }

    public static String qd(android.content.Context p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/updatetUserImPass?", new String[] {"uid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid()}), 1);
    }

    public static String r()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/recommend/addRecommend.jspx?");
    }

    public static String r0()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/createCataLog");
        return v0_1.toString();
    }

    public static String r1(String p2, String p3, String p4, String p5, String p6)
    {
        if (!com.fanzhou.util.w.s(p4)) {
            String v3_3 = new StringBuilder();
            v3_3.append(pk.d.b().a(p4));
            v3_3.append("apis/topic/deleteTopic?");
            return com.chaoxing.mobile.s.A8(v3_3.toString(), new String[] {"puid", "bbsid", "uuid"}), new String[] {p2, p4, p5}));
        } else {
            return com.chaoxing.mobile.s.t1(p3, p2, p6);
        }
    }

    public static String r2(String p2, int p3)
    {
        Integer v3_1 = Integer.valueOf(p3);
        Object[] v0_1 = new Object[2];
        v0_1[0] = p2;
        v0_1[1] = v3_1;
        return String.format("https://mobilelearn.chaoxing.com/phoneactivehistory/phonetimelist?chatId=%s&from=%d", v0_1);
    }

    public static String r3()
    {
        return "https://passport2-api.chaoxing.com/v11/importcourse";
    }

    public static String r4(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://floweryd.chaoxing.com/apis/flower/getUserTong?", new String[] {"puid"}), new String[] {p2}));
    }

    public static String r5(String p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/other/getMediaUrl?");
        return com.chaoxing.mobile.s.e9(v0_1.toString(), new String[] {"crc"}), new String[] {p2}));
    }

    public static String r6(android.content.Context p5, String p6, String p7, String p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_rtfnote/getNotesVersion?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "lastUpdateTime", "page", "pageSize"}), new String[] {v5_4, p6, p7, p8}));
    }

    public static String r7(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p3;
        v0_1[1] = p2;
        return String.format("https://fanya.zyk2.chaoxing.com/mobile/prep/searchMoocName?title=%s&type=3&courseid=%s#INNER", v0_1);
    }

    public static String r8(String p4, String p5)
    {
        return com.chaoxing.mobile.s.A8("https://appswh.chaoxing.com/apis/teach/getTeachPlan?", new String[] {"puid", "courseId", "uuid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid(), p4, p5}));
    }

    public static String r9(String p2, String p3)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/v2apis/friend/getFollowStatus?", new String[] {"puids", "tid"}), new String[] {p2, p3}));
    }

    public static String ra(android.content.Context p9, String p10, String p11, String p12, int p13, int p14, int p15, String p16)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v9_5 = new StringBuilder();
        v9_5.append(pk.a.f);
        v9_5.append("apis/notice/myNotices_v2?");
        String v9_1 = v9_5.toString();
        String v3 = "type";
        String v5 = "from";
        String v1_3 = new StringBuilder();
        v1_3.append(p13);
        v1_3.append("");
        v1_3.toString();
        String v1_5 = new StringBuilder();
        v1_5.append(p14);
        v1_5.append("");
        v1_5.toString();
        StringBuilder v14_2 = new StringBuilder();
        v14_2.append(p15);
        v14_2.append("");
        v14_2.toString();
        String v1 = p10;
        v3 = p12;
        return com.chaoxing.mobile.s.A8(v9_1, new String[] {"puid", "read"}), new String[] {v0, p16}));
    }

    public static String rb(String p5, long p6, String p8)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p8));
        v0_1.append("apis/circle/curDataRecord?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p6);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "replyId", "version", "bbsid"}), new String[] {p5, v2_2.toString(), "20171130", p8}));
    }

    public static String rc()
    {
        String[] v1_4 = new StringBuilder();
        v1_4.append(com.fanzhou.util.n.a);
        v1_4.append("");
        String[] v1_1 = v1_4.toString();
        StringBuilder v4_1 = new StringBuilder();
        v4_1.append(com.fanzhou.util.n.b);
        v4_1.append("");
        return com.chaoxing.mobile.s.A8("https://apps.chaoxing.com/apis/subscribe/getGuestSubscirbe.jspx?", new String[] {"productId", "version", "clientType"}), new String[] {v1_1, com.fanzhou.util.n.c, v4_1.toString()}));
    }

    public static String rd(android.content.Context p2)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/updateNotice?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid"}), new String[] {v2_4}));
    }

    public static String s(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/invitation/addReplyWithCheck?");
        String v0_2 = v0_1.toString();
        Object[] v2_2 = new Object[3];
        v2_2[0] = p4;
        v2_2[1] = p5;
        v2_2[2] = p6;
        return com.chaoxing.mobile.s.z8(v0_2, new String[] {"puid", "uuid", "bbsid"}), v2_2);
    }

    public static String s0(String p3, String p4)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/dept/createDept?", new String[] {"name", "pid", "needCode"}), new String[] {p3, p4, "1"}), 1);
    }

    public static String s1(String p3, String p4, String p5, String p6, String p7, String p8)
    {
        if (!com.fanzhou.util.w.s(p5)) {
            String v4_3 = new StringBuilder();
            v4_3.append(pk.d.b().a(p5));
            v4_3.append("apis/topic/deleteTopic?");
            return com.chaoxing.mobile.s.A8(v4_3.toString(), new String[] {"puid", "bbsid", "uuid", "reason"}), new String[] {p3, p5, p6, p8}));
        } else {
            return com.chaoxing.mobile.s.t1(p4, p3, p7);
        }
    }

    public static String s2(String p5, String p6, String p7, int p8)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p8);
        v1_3.append("");
        return com.chaoxing.mobile.s.A8("https://im.chaoxing.com/apis/message/getChatAttachmentList?", new String[] {"chat_id", "kw", "lastTime", "pageSize", "order"}), new String[] {p5, p6, p7, v1_3.toString(), "2"}));
    }

    public static String s3(String p3, String p4, long p5)
    {
        StringBuilder v1_2 = new StringBuilder();
        v1_2.append(p5);
        v1_2.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/im/updateChatGroupIncode?", new String[] {"cgid", "incode", "expireTime"}), new String[] {p3, p4, v1_2.toString()}));
    }

    public static String s4(int p3, int p4, int p5)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p3);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        String v4_1 = v2_1.toString();
        StringBuilder v2_3 = new StringBuilder();
        v2_3.append(p5);
        v2_3.append("");
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/user/getSuperFlowerConfigs?", new String[] {"ftype", "version", "vs"}), new String[] {v1_1, v4_1, v2_3.toString()}));
    }

    public static String s5(android.content.Context p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = com.chaoxing.study.account.AccountManager.C().D().getDxfid();
        return com.chaoxing.mobile.s.L1("https://mc.m.5read.com/apis/message/menus.jspx?unitid=%s&clientType=android", v0_1);
    }

    public static String s6(android.content.Context p5, String p6, String p7, String p8)
    {
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.c);
        v0_2.append("apis/note_note/getNotesVersion?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid", "lastUpdateTime", "page", "pageSize"}), new String[] {v5_4, p6, p7, p8}));
    }

    public static String s7(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p3;
        v0_1[1] = p2;
        return String.format("https://fanya.zyk2.chaoxing.com/mobile/prep/searchMoocName?title=%s&type=2&courseid=%s#INNER", v0_1);
    }

    public static String s8()
    {
        return "https://home-yd.chaoxing.com/jsp/home/tools.jsp";
    }

    public static String s9()
    {
        return "https://authen.chaoxing.com/apis/meet/toMeet";
    }

    public static String sa(String p6, String p7, int p8, int p9, int p10)
    {
        if (com.fanzhou.util.w.q(p7)) {
            p7 = "";
        }
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p8);
        v2_1.append("");
        String v8_1 = v2_1.toString();
        StringBuilder v2_3 = new StringBuilder();
        v2_3.append(p9);
        v2_3.append("");
        String v9_1 = v2_3.toString();
        StringBuilder v2_5 = new StringBuilder();
        v2_5.append(p10);
        v2_5.append("");
        return com.chaoxing.mobile.s.A8("https://specie.chaoxing.com/apis/message/myReplys2?", new String[] {"puid", "kw", "page", "pageSize", "maxW"}), new String[] {p6, p7, v8_1, v9_1, v2_5.toString()}));
    }

    public static String sb(String p6, long p7, String p9, String p10)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.c);
        v0_1.append("apis/note_note/curNoteReply?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "replyId", "noteId", "noteCid", "version"}), new String[] {p6, v2_1.toString(), p9, p10, "20171130"}));
    }

    public static String sc()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("edit/coursebulletFormat?");
        return v0_1.toString();
    }

    public static String sd(android.content.Context p6, String p7, int p8, int p9, String p10)
    {
        String v6_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/other/updateNoticeApprove?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p8);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"puid", "noticeId", "source_type", "status", "remark"}), new String[] {v6_4, p7, v2_3, v3_2.toString(), p10}));
    }

    public static String t()
    {
        return com.chaoxing.mobile.s.x8("https://appswh.chaoxing.com/apis/teach/addTeachPlan?");
    }

    public static String t0(String p3, String p4, String p5)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/contact/createContact?", new String[] {"id", "dataType", "dataKey"}), new String[] {p3, p4, p5}));
    }

    public static String t2()
    {
        return "https://x.chaoxing.com/apis/toScreen/imMessageToScreen";
    }

    public static String t3()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassPhoneManage/phone/createTeachingClass");
        return v0_1.toString();
    }

    public static String t4(android.content.Context p2)
    {
        String v2_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/getFolders?");
        return com.chaoxing.mobile.s.A8(v0_2.toString(), new String[] {"puid"}), new String[] {v2_4}));
    }

    public static String t5(android.content.Context p2, String p3, String p4)
    {
        String v2_5 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        Object[] v0_1 = new Object[3];
        v0_1[0] = p3;
        v0_1[1] = v2_5;
        v0_1[2] = p4;
        return com.chaoxing.mobile.s.L1("https://mc.m.5read.com/apis/message/messageDetail.jspx?id=%s&uid=%s&receiver=%s&clientType=android", v0_1);
    }

    public static String t6(String p7, String p8, String p9, int p10)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.c);
        v1_2.append("apis/note_note/getNotesVersionWithPoff?");
        String v1_0 = v1_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p10);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v1_0, new String[] {"puid", "lastUpdateTime", "lastAuxValue", "pageSize", "needCount"}), new String[] {v0_2, p7, p8, p9, v3_2.toString()}));
    }

    public static String t7(String p16, boolean p17)
    {
        String v3_0;
        String v0_1 = Integer.valueOf(-1);
        Integer v2 = Integer.valueOf(1);
        if (!com.fanzhou.util.w.q(p16)) {
            v3_0 = p16;
        } else {
            v3_0 = "";
        }
        if (!p17) {
            String v12 = "splitData";
            Object[] v11_1 = new Object[6];
            v11_1[0] = v0_1;
            v11_1[1] = v2;
            v11_1[2] = v2;
            v11_1[3] = v3_0;
            v11_1[4] = com.fanzhou.util.n.c;
            v11_1[5] = v2;
            return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/subscribe/getSubscribe.jspx?", new String[] {"cataid", "rmSelfZT"}), v11_1);
        } else {
            Object[] v8_1 = new Object[5];
            v8_1[0] = v0_1;
            v8_1[1] = v2;
            v8_1[2] = v2;
            v8_1[3] = v3_0;
            v8_1[4] = com.fanzhou.util.n.c;
            return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/subscribe/getSubscribe.jspx?", new String[] {"cataid", "refresh", "splitData", "mcode", "version"}), v8_1);
        }
    }

    public static String t8(String p2, String p3)
    {
        Object[] v0_1 = new Object[2];
        v0_1[0] = p3;
        v0_1[1] = p2;
        return String.format("https://mobilelearn.chaoxing.com/task/getTeaWorkAndExamSkipUrl?courseId=%s&classId=%s#INNER", v0_1);
    }

    public static String t9()
    {
        return "https://mobilelearn.chaoxing.com/widget/coursewareChileActive/toVideoControlPage";
    }

    public static String ta(String p6, String p7, String p8, int p9, int p10)
    {
        if (com.fanzhou.util.w.q(p7)) {
            p7 = "";
        }
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p8);
        v2_1.append("");
        String v8_1 = v2_1.toString();
        StringBuilder v2_3 = new StringBuilder();
        v2_3.append(p9);
        v2_3.append("");
        String v9_1 = v2_3.toString();
        StringBuilder v2_5 = new StringBuilder();
        v2_5.append(p10);
        v2_5.append("");
        return com.chaoxing.mobile.s.A8("https://specie.chaoxing.com/apis/message/myReplysWithPoff?", new String[] {"puid", "kw", "lastValue", "pageSize", "maxW"}), new String[] {p6, p7, v8_1, v9_1, v2_5.toString()}));
    }

    public static String tb(String p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/curDataRecord?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "noticeId", "replyId"}), new String[] {p4, p5, v2_1.toString()}));
    }

    public static String tc(String p3, String p4, int p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/moveTop?courseId=%s&classId=%s&top=%d&cpi=%s");
        String v0_2 = v0_1.toString();
        Integer v5_1 = Integer.valueOf(p5);
        Object[] v1_1 = new Object[4];
        v1_1[0] = p3;
        v1_1[1] = p4;
        v1_1[2] = v5_1;
        v1_1[3] = p6;
        return String.format(v0_2, v1_1);
    }

    public static String td(java.util.List p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/replyUpdate?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String u(android.content.Context p4, String p5, String p6, int p7)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p7);
        v1_1.append("");
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/addToFolder?", new String[] {"puid", "folderId", "msgId", "type"}), new String[] {v4_4, p5, p6, v1_1.toString()}));
    }

    public static String u0(android.content.Context p3)
    {
        String v3_5 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        Object[] v1_1 = new Object[2];
        v1_1[0] = v3_5;
        v1_1[1] = v0_0;
        return String.format("https://mobilelearn.chaoxing.com/pingfen/chatPingfen?tid=%s&uid=%s", v1_1);
    }

    public static String u1(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p4));
        v0_1.append("apis/circle/disCircle?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "circleId"}), new String[] {p3, p4}));
    }

    public static String u2(String p3)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("courseapi/helloinfo?");
        return com.chaoxing.mobile.s.f9(v0_1.toString(), new String[] {"chatid"}), new String[] {p3}), 0);
    }

    public static String u3(String p5, String p6, int p7, android.content.Context p8)
    {
        if (com.fanzhou.util.w.q(p5)) {
            p5 = "";
        }
        String v1_2 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p7);
        v2_1.append("");
        return com.chaoxing.mobile.s.w3(new String[] {"pid", "cfname", "uid", "shareType", "version"}), new String[] {p5, p6, v1_2, v2_1.toString(), com.fanzhou.util.n.c}));
    }

    public static String u4(android.content.Context p3, int p4, int p5)
    {
        int v4_1;
        String v3_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v1_0 = "";
        if (p4 != 0) {
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p4);
            v2_1.append("");
            v4_1 = v2_1.toString();
        } else {
            v4_1 = "";
        }
        if (p5 != null) {
            StringBuilder v2_3 = new StringBuilder();
            v2_3.append(p5);
            v2_3.append("");
            v1_0 = v2_3.toString();
        }
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/getUserFriendGroup?", new String[] {"uid", "cpage", "pageSize"}), new String[] {v3_4, v4_1, v1_0}), 1);
    }

    public static String u5(android.content.Context p2, int p3, String p4, long p5, int p7, int p8)
    {
        String v2_0 = Integer.valueOf(p3);
        String v3_3 = com.chaoxing.study.account.AccountManager.C().D().getDxfid();
        String v0_1 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        Long v5_1 = Long.valueOf(p5);
        Integer v6 = Integer.valueOf(p7);
        Integer v7_1 = Integer.valueOf(p8);
        Object[] v8_2 = new Object[8];
        v8_2[0] = v2_0;
        v8_2[1] = p4;
        v8_2[2] = "274";
        v8_2[3] = v3_3;
        v8_2[4] = v0_1;
        v8_2[5] = v5_1;
        v8_2[6] = v6;
        v8_2[7] = v7_1;
        return com.chaoxing.mobile.s.L1("https://mc.m.5read.com/apis/message/messageList.jspx?cataid=%d&clientid=%s&areaid=%s&unitid=%s&uid=%s&time=%d&cpage=%d&pageSize=%d&clientType=android", v8_2);
    }

    public static String u6(android.content.Context p6, int p7, String p8, String p9, int p10)
    {
        String v6_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/getNotice?");
        String v0_0 = v0_2.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p7);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        String v9_1 = v3_2.toString();
        StringBuilder v3_4 = new StringBuilder();
        v3_4.append(p10);
        v3_4.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"id", "sid", "s_noticeId", "maxW", "puid"}), new String[] {v2_3, p8, v9_1, v3_4.toString(), v6_4}));
    }

    public static String u7(long p4, long p6, int p8, int p9)
    {
        String v4_6 = Long.valueOf(p4);
        Long v5 = Long.valueOf(p6);
        Integer v6_1 = Integer.valueOf(p8);
        Integer v7 = Integer.valueOf(p9);
        Object[] v8_2 = new Object[4];
        v8_2[0] = v4_6;
        v8_2[1] = v5;
        v8_2[2] = v6_1;
        v8_2[3] = v7;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/app/recommendResByPid.jspx?", new String[] {"pid", "lastRequestTime", "page", "pageSize"}), v8_2);
    }

    public static String u8()
    {
        return "https://oss.iclass.cn/formFile?";
    }

    public static String u9(android.content.Context p3)
    {
        return com.chaoxing.mobile.s.A8("https://money.chaoxing.com/apis/pay/getPurse?", new String[] {"uid", "puid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid()}));
    }

    public static String ua(String p13, int p14, int p15, int p16, int p17, String p18)
    {
        String v6;
        if (!com.fanzhou.util.w.q(p18)) {
            v6 = p18;
        } else {
            v6 = "";
        }
        String v0_4 = new StringBuilder();
        v0_4.append(pk.a.e);
        v0_4.append("apis/topic/myTopics?");
        String v0_1 = v0_4.toString();
        String v9 = "order";
        String.valueOf(p14);
        String.valueOf(p15);
        String.valueOf(p16);
        String.valueOf(p17);
        return com.chaoxing.mobile.s.A8(v0_1, new String[] {"uid", "kw"}), new String[] {p13, v6}));
    }

    public static String ub(java.util.List p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p3));
        v0_1.append("apis/invitation/addReply?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String uc(String p4, String p5)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(p5)) {
            String v5_2 = new StringBuilder();
            v5_2.append(pk.d.b().a(p4));
            v5_2.append("apis/circle/topSet?");
            return com.chaoxing.mobile.s.A8(v5_2.toString(), new String[] {"circleId", "puid"}), new String[] {p4, v0_2}));
        } else {
            String v4_4 = new StringBuilder();
            v4_4.append(pk.d.b().a(p5));
            v4_4.append("apis/circle/topSet?");
            return com.chaoxing.mobile.s.A8(v4_4.toString(), new String[] {"bbsid", "puid"}), new String[] {p5, v0_2}));
        }
    }

    public static String ud()
    {
        return com.chaoxing.mobile.s.x8("https://money.chaoxing.com/apis/packet/updateAttachs?");
    }

    public static String v(String p3, String p4, String p5)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p5));
        v0_1.append("apis/topic/choiceSet?");
        String v5_1 = v0_1.toString();
        String v1_2 = new StringBuilder();
        v1_2.append(p3);
        v1_2.append("");
        String v1_3 = v1_2.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p4);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v5_1, new String[] {"uuid", "puid"}), new String[] {v1_3, v2_1.toString()}));
    }

    public static String v0(String p3, String p4, String p5)
    {
        if (android.text.TextUtils.isEmpty(p4)) {
            String v4_4 = new StringBuilder();
            v4_4.append(pk.a.e);
            v4_4.append("apis/circle_folder/addCircleFolder?");
            return com.chaoxing.mobile.s.A8(v4_4.toString(), new String[] {"uid", "name"}), new String[] {p3, p5}));
        } else {
            String v3_4 = new StringBuilder();
            v3_4.append(pk.a.e);
            v3_4.append("apis/circle_folder/addCircleFolder?");
            return com.chaoxing.mobile.s.A8(v3_4.toString(), new String[] {"puid", "name"}), new String[] {p4, p5}));
        }
    }

    public static String v1(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/disCircle?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "circleId"}), new String[] {p3, p4}));
    }

    public static String v2(String p2, String p3, java.util.List p4, int p5)
    {
        org.json.JSONObject v0_1 = new org.json.JSONObject();
        v0_1.put("id", p2);
        v0_1.put("name", p3);
        if (p4 != null) {
            String v2_6 = new org.json.JSONArray();
            String v3_1 = p4.iterator();
            while (v3_1.hasNext()) {
                v2_6.put(((String) v3_1.next()));
            }
            v0_1.put("logo", v2_6);
        }
        String v3_4 = v0_1.toString();
        String v4_3 = new StringBuilder();
        v4_3.append(p5);
        v4_3.append("");
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/createChatGroupIncode?", new String[] {"cg", "op"}), new String[] {v3_4, v4_3.toString()}), 1);
    }

    public static String v3(String p3, String p4, android.content.Context p5)
    {
        if (com.fanzhou.util.w.q(p3)) {
            p3 = "";
        }
        return com.chaoxing.mobile.s.w3(new String[] {"pid", "cfname", "uid", "version"}), new String[] {p3, p4, com.chaoxing.study.account.AccountManager.C().D().getUid(), com.fanzhou.util.n.c}));
    }

    public static String v4()
    {
        return "https://learn.chaoxing.com/friend/readrank/rankList?pageSize=50";
    }

    public static String v5(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return com.chaoxing.mobile.s.L1("https://mc.m.5read.com/apis/bookrack/epubBookDetail.jspx?dxid=%s", v0_1);
    }

    public static String v6(android.content.Context p6, String p7, String p8, String p9, int p10)
    {
        String v6_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_2 = new StringBuilder();
        v0_2.append(pk.a.f);
        v0_2.append("apis/notice/myNotices_v2?");
        String v0_0 = v0_2.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p10);
        v2_2.append("");
        return com.chaoxing.mobile.s.A8(v0_0, new String[] {"type", "tag", "puid", "lastGetId", "pageSize"}), new String[] {p7, p8, v6_4, p9, v2_2.toString()}));
    }

    public static String v7(android.content.Context p10, String p11)
    {
        String v10_2 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v2 = "fid";
        Integer v4 = "version";
        Integer v6 = "cataid";
        int v1_1 = Integer.valueOf(com.fanzhou.util.n.a);
        String v2_2 = com.chaoxing.study.account.AccountManager.C().D().getDxfid();
        String v3_2 = com.chaoxing.study.account.AccountManager.C().D().getFid();
        Integer v4_1 = Integer.valueOf(com.fanzhou.util.n.b);
        v6 = Integer.valueOf(1);
        Integer v7_1 = Integer.valueOf(10000);
        Object[] v8_1 = new Object[9];
        v8_1[0] = v1_1;
        v8_1[1] = v2_2;
        v8_1[2] = v3_2;
        v8_1[3] = v10_2;
        v8_1[4] = com.fanzhou.util.n.c;
        v8_1[5] = v4_1;
        v8_1[6] = p11;
        v8_1[7] = v6;
        v8_1[8] = v7_1;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/app/appInfos.jspx?", new String[] {"productId", "pageSize"}), v8_1);
    }

    public static java.util.ArrayList v8(String[] p5, Object[] p6)
    {
        java.util.ArrayList v0_1 = new java.util.ArrayList();
        if ((p5 != null) && ((p6 != null) && (p5.length == p6.length))) {
            int v1_0 = 0;
            while (v1_0 < p5.length) {
                String v2_0 = p6[v1_0];
                if (v2_0 != null) {
                    v0_1.add(new org.apache.http.message.BasicNameValuePair(p5[v1_0], v2_0.toString()));
                } else {
                    v0_1.add(new org.apache.http.message.BasicNameValuePair(p5[v1_0], ""));
                }
                v1_0++;
            }
        }
        return v0_1;
    }

    public static String v9(long p1)
    {
        Object[] v2_1 = new Object[1];
        v2_1[0] = Long.valueOf(p1);
        return String.format("https://mobilelearn.chaoxing.com/widget/discuss/wordCloud?topicId=%s", v2_1);
    }

    public static String va(String p3, String p4, String p5)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/friend/needValidate?", new String[] {"uid", "friendid", "friendPuid"}), new String[] {p3, p4, p5}));
    }

    public static String vb(String p2, String p3)
    {
        String v2_1 = com.chaoxing.mobile.s.M9(p2);
        String v3_1 = com.chaoxing.mobile.s.M9(p3);
        Object[] v0_1 = new Object[2];
        v0_1[0] = v2_1;
        v0_1[1] = v3_1;
        return String.format("https://live.chaoxing.com/liveAPI/newLiveDetail?streamName=%s&vdoid=%s", v0_1);
    }

    public static String vc(String p4, String p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle_folder/topCircleFolder?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p6);
        v2_1.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"uid", "folderId", "isTop"}), new String[] {p4, p5, v2_1.toString()}));
    }

    public static String vd(String p5, String p6, String p7, int p8)
    {
        if (android.text.TextUtils.isEmpty(p7)) {
            String v7_3 = new StringBuilder();
            v7_3.append(pk.d.b().a(p6));
            v7_3.append("apis/circle/updateCircleExtend?");
            String v7_1 = v7_3.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p8);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "circleId", "replyListOrderType"}), new String[] {p5, p6, v2_1.toString()}));
        } else {
            String v6_2 = new StringBuilder();
            v6_2.append(pk.d.b().a(p7));
            v6_2.append("apis/circle/updateCircleExtend?");
            String v6_3 = v6_2.toString();
            StringBuilder v2_4 = new StringBuilder();
            v2_4.append(p8);
            v2_4.append("");
            return com.chaoxing.mobile.s.A8(v6_3, new String[] {"puid", "bbsid", "replyListOrderType"}), new String[] {p5, p7, v2_4.toString()}));
        }
    }

    public static String w(String p3)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/im/addUser2Chatgroup4C?", new String[] {"groupid"}), new String[] {p3}), 1);
    }

    public static String w0()
    {
        return com.chaoxing.mobile.s.x8("https://resource.chaoxing.com/apis/cloud/createFolder.jspx?");
    }

    public static String w1()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassPhoneManage/phone/clsSetting");
        return v0_1.toString();
    }

    public static String w2(String p2)
    {
        return com.chaoxing.mobile.s.A8("https://learn.chaoxing.com/apis/im/getChartGroup?", new String[] {"chatgroupid", "vs"}), new String[] {p2, "2"}));
    }

    public static String w4(java.util.List p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/getBarCircle?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String w5(android.content.Context p2, String p3, String p4)
    {
        String v2_5 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        Object[] v0_1 = new Object[3];
        v0_1[0] = p3;
        v0_1[1] = v2_5;
        v0_1[2] = p4;
        return com.chaoxing.mobile.s.L1("https://mc.m.5read.com/apis/message/readReceipts.jspx?clientid=%s&receiver=%s&msgids=%s&clientType=android", v0_1);
    }

    public static String w6(android.content.Context p17, String p18, int p19, String p20, String p21, int p22, int p23, int p24)
    {
        String v8 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v0_5 = new StringBuilder();
        v0_5.append(pk.a.f);
        v0_5.append("apis/notice/myNotices?");
        String v0_1 = v0_5.toString();
        String v11 = "kw";
        String v13 = "contSize";
        String[] v1_2 = new StringBuilder();
        v1_2.append(p19);
        v1_2.append("");
        String[] v1_3 = v1_2.toString();
        String v3_1 = new StringBuilder();
        v3_1.append(p22);
        v3_1.append("");
        v3_1.toString();
        String v3_3 = new StringBuilder();
        v3_3.append(p23);
        v3_3.append("");
        v3_3.toString();
        String v3_5 = new StringBuilder();
        v3_5.append(p24);
        v3_5.append("");
        v3_5.toString();
        String v3 = p20;
        String v2 = v1_3;
        return com.chaoxing.mobile.s.A8(v0_1, new String[] {"type", "puid"}), new String[] {p18, v8}));
    }

    public static String w7()
    {
        return "https://x.chaoxing.com/apis/toScreen/resourceToScreen";
    }

    public static java.util.Map w8(String[] p4, Object[] p5)
    {
        java.util.HashMap v0_1 = new java.util.HashMap();
        if ((p4 != null) && ((p5 != null) && (p4.length == p5.length))) {
            int v1_0 = 0;
            while (v1_0 < p4.length) {
                String v2_0 = p5[v1_0];
                if (v2_0 != null) {
                    v0_1.put(p4[v1_0], v2_0.toString());
                } else {
                    v0_1.put(p4[v1_0], "");
                }
                v1_0++;
            }
        }
        return v0_1;
    }

    public static String w9(long p1)
    {
        Object[] v2_1 = new Object[1];
        v2_1[0] = Long.valueOf(p1);
        return String.format("https://mobilelearn.chaoxing.com/widget/discuss/wordCloudPage?topicId=%s", v2_1);
    }

    public static String wa(String p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/check/msgCheck?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid"}), new String[] {p2}));
    }

    public static String wb(String p4, int p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/check/checkState?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append("");
        v2_1.append(p5);
        String v5_1 = v2_1.toString();
        StringBuilder v2_3 = new StringBuilder();
        v2_3.append("");
        v2_3.append(p6);
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"uid", "checkId", "isCheck"}), new String[] {p4, v5_1, v2_3.toString()}));
    }

    public static String wc(String p7, String p8, String p9, int p10, int p11, String p12)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p9));
        v0_1.append("apis/label/getTopLabelTopicByPoff?");
        String v0_2 = v0_1.toString();
        String v3 = "bbsid";
        String.valueOf(p10);
        String.valueOf(p11);
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"puid", "tags"}), new String[] {p7, p12}));
    }

    public static String wd()
    {
        return com.chaoxing.mobile.s.x8("https://apps.chaoxing.com/apis/subscribe/updateCustomFolder.jspx?");
    }

    public static String x(android.content.Context p8, String p9, String p10, String p11)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v6 = "gids";
        String v4 = "followedUid";
        String v3 = p10;
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/addUserFollow?", new String[] {"uid", "alias"}), new String[] {v0, 0}), 1);
    }

    public static String x0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://live.chaoxing.com/zhibo/newchatzhibo?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String x1()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("phone/coursecontroller/updateCourseCover_client?");
        return v0_1.toString();
    }

    public static String x2(String p3, String p4, java.util.List p5)
    {
        int v1_1 = new org.json.JSONArray();
        String v5_5 = p5.iterator();
        while (v5_5.hasNext()) {
            v1_1.put(((String) v5_5.next()));
        }
        try {
            String v4_1 = java.net.URLEncoder.encode(p4, "UTF-8");
            String v5_3 = java.net.URLEncoder.encode(v1_1.toString().toString(), "UTF-8");
        } catch (String v5_4) {
            v5_4.printStackTrace();
            v5_3 = "";
        }
        Object[] v0_2 = new Object[3];
        v0_2[0] = p3;
        v0_2[1] = v4_1;
        v0_2[2] = v5_3;
        return String.format("https://learn.chaoxing.com/im/addcg?cgid=%s&cgname=%s&logo=%s", v0_2);
    }

    public static String x3(String p6, String p7, String p8, String p9, String p10, String p11)
    {
        if (android.text.TextUtils.isEmpty(p9)) {
            if (android.text.TextUtils.isEmpty(p7)) {
                String v7_2 = new StringBuilder();
                v7_2.append(pk.d.b().a(p8));
                v7_2.append("apis/circle/circleGroupChat2?");
                return com.chaoxing.mobile.s.A8(v7_2.toString(), new String[] {"uid", "circleId", "pcode", "invite"}), new String[] {p6, p8, p10, p11}));
            } else {
                String v6_4 = new StringBuilder();
                v6_4.append(pk.d.b().a(p8));
                v6_4.append("apis/circle/circleGroupChat2?");
                return com.chaoxing.mobile.s.A8(v6_4.toString(), new String[] {"puid", "circleId", "pcode", "invite"}), new String[] {p7, p8, p10, p11}));
            }
        } else {
            if (android.text.TextUtils.isEmpty(p7)) {
                String v7_6 = new StringBuilder();
                v7_6.append(pk.d.b().a(p9));
                v7_6.append("apis/circle/circleGroupChat2?");
                return com.chaoxing.mobile.s.A8(v7_6.toString(), new String[] {"uid", "bbsid", "pcode", "invite"}), new String[] {p6, p9, p10, p11}));
            } else {
                String v6_10 = new StringBuilder();
                v6_10.append(pk.d.b().a(p9));
                v6_10.append("apis/circle/circleGroupChat2?");
                return com.chaoxing.mobile.s.A8(v6_10.toString(), new String[] {"puid", "bbsid", "pcode", "invite"}), new String[] {p7, p9, p10, p11}));
            }
        }
    }

    public static String x4(String p4, int p5, int p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/activity/circleActivity?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "page", "pageSize"}), new String[] {p4, String.valueOf(p5), String.valueOf(p6)}));
    }

    public static String x5(String p4)
    {
        return com.chaoxing.mobile.s.f9("https://message.chaoxing.com/apis/msg/messageDetail?", new String[] {"puid", "id", "version"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid(), p4, "20190725"}), 1);
    }

    public static String x6(String p6)
    {
        String v0_2 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v1_2 = new StringBuilder();
        v1_2.append(pk.a.f);
        v1_2.append("apis/notice/getNoReadCount?");
        return com.chaoxing.mobile.s.A8(v1_2.toString(), new String[] {"puid", "productId", "sign", "red_dots"}), new String[] {v0_2, String.valueOf(com.fanzhou.util.n.a), p6, "1"}));
    }

    public static String x7(android.content.Context p10)
    {
        String v2 = "fid";
        Integer v4 = "rights";
        Integer v6 = "clientType";
        String v0_1 = Integer.valueOf(com.fanzhou.util.n.a);
        int v1_2 = com.chaoxing.study.account.AccountManager.C().D().getDxfid();
        String v2_2 = com.chaoxing.study.account.AccountManager.C().D().getFid();
        String v3_2 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        Integer v4_3 = Integer.valueOf(com.chaoxing.study.account.AccountManager.C().D().getRights());
        Integer v5_1 = Integer.valueOf(com.fanzhou.util.n.b);
        Integer v6_1 = Integer.valueOf(20);
        Object[] v7_1 = new Object[10];
        v7_1[0] = v0_1;
        v7_1[1] = v1_2;
        v7_1[2] = v2_2;
        v7_1[3] = v3_2;
        v7_1[4] = v4_3;
        v7_1[5] = com.fanzhou.util.n.c;
        v7_1[6] = v5_1;
        v7_1[7] = "all";
        v7_1[8] = "p_a_g_e";
        v7_1[9] = v6_1;
        return com.chaoxing.mobile.s.z8("https://apps.chaoxing.com/apis/app/resourceCatas.jspx?", new String[] {"productId", "pageSize"}), v7_1);
    }

    public static String x9(String p13, String p14, String p15, String p16, String p17, String p18, String p19, int p20, int p21, int p22)
    {
        String v2 = "relationId";
        String v4 = "cpuid";
        String v6 = "tagnumber";
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p20);
        v1_1.append("");
        v1_1.toString();
        StringBuilder v1_3 = new StringBuilder();
        v1_3.append(p21);
        v1_3.append("");
        v1_3.toString();
        StringBuilder v1_5 = new StringBuilder();
        v1_5.append(p22);
        v1_5.append("");
        String v5 = p15;
        String v7 = p17;
        String v9 = p19;
        return com.chaoxing.mobile.s.f9("https://commendyd.chaoxing.com/apis/commend/queryCommend2Part?", new String[] {"keyword", "pageSize"}), new String[] {p13, v1_5.toString()}), 1);
    }

    public static String xa(String p8, int p9, String p10, int p11, int p12, String p13)
    {
        // Both branches of the condition point to the same code.
        // if (!com.fanzhou.util.w.q(p10)) {
            String v4 = "kw";
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p9);
            v2_1.append("");
            v2_1.toString();
            StringBuilder v2_3 = new StringBuilder();
            v2_3.append(p11);
            v2_3.append("");
            v2_3.toString();
            StringBuilder v2_5 = new StringBuilder();
            v2_5.append(p12);
            v2_5.append("");
            v2_5.toString();
            return com.chaoxing.mobile.s.A8("https://specie.chaoxing.com/apis/message/getMsgNewsListWithPoff?", new String[] {"puid", "lastValue"}), new String[] {p8, p13}));
        // }
    }

    public static String xb(android.content.Context p4, int p5, String p6, String p7)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        StringBuilder v1_1 = new StringBuilder();
        v1_1.append(p5);
        v1_1.append("");
        return com.chaoxing.mobile.s.e9("https://im.chaoxing.com/apis/message/revokeMessage?", new String[] {"isGroup", "hxMsgId", "tuid", "chatManId"}), new String[] {v1_1.toString(), p7, v4_4, p6}));
    }

    public static String xc(int p5, String p6, String p7, String p8, int p9)
    {
        String v1_3 = new StringBuilder();
        v1_3.append(p5);
        v1_3.append("");
        String v1_1 = v1_3.toString();
        StringBuilder v2_1 = new StringBuilder();
        v2_1.append(p9);
        v2_1.append("");
        return com.chaoxing.mobile.s.f9("https://resource.chaoxing.com/apis/cloud/updateTopsign.jspx?", new String[] {"ownertype", "ownerId", "recIds", "folderIds", "topsign"}), new String[] {v1_1, p6, p7, p8, v2_1.toString()}), 1);
    }

    public static String xd(String p2, String p3, int p4, int p5)
    {
        String v2_1 = com.chaoxing.mobile.s.M9(p2);
        String v3_1 = com.chaoxing.mobile.s.M9(p3);
        Integer v4_1 = Integer.valueOf(p4);
        Integer v5_1 = Integer.valueOf(p5);
        Object[] v0_1 = new Object[4];
        v0_1[0] = v2_1;
        v0_1[1] = v3_1;
        v0_1[2] = v4_1;
        v0_1[3] = v5_1;
        return String.format("https://live.chaoxing.com/liveAPI/updateLiveStatus?streamName=%s&vdoid=%s&liveStatus=%d&forbiddenReview=%d", v0_1);
    }

    public static String y()
    {
        return com.chaoxing.mobile.s.x8("https://learn.chaoxing.com/apis/friend/addUserFriendGroup?");
    }

    public static String y0(android.content.Context p2, int p3)
    {
        return com.chaoxing.mobile.s.f9("https://live.chaoxing.com/zhibo/noteLive?", new String[] {"userId", "type"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid(), String.valueOf(p3)}), 0);
    }

    public static String y1()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("mycourse/cataLogReName");
        return v0_1.toString();
    }

    public static String y2(android.content.Context p5, String p6, boolean p7, long p8, int p10)
    {
        String v7_1;
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        if (p7 == null) {
            v7_1 = "1";
        } else {
            v7_1 = "0";
        }
        String v8_1;
        if (p8 != 0) {
            StringBuilder v1_2 = new StringBuilder();
            v1_2.append(p8);
            v1_2.append("");
            v8_1 = v1_2.toString();
        } else {
            v8_1 = "";
        }
        String v9_1 = new StringBuilder();
        v9_1.append(p10);
        v9_1.append("");
        return com.chaoxing.mobile.s.e9("https://im.chaoxing.com/apis/message/getHistory?", new String[] {"tuid", "chat_man_id", "msg_status", "last_msg_time", "pageSize"}), new String[] {v5_4, p6, v7_1, v8_1, v9_1.toString()}));
    }

    public static String y3(String p3, String p4)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/createCircleAnnouncement?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "circleId"}), new String[] {p3, p4}));
    }

    public static String y4(String p6, String p7, int p8, int p9)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/cmem/managers?");
        String v0_2 = v0_1.toString();
        String v2_2 = new StringBuilder();
        v2_2.append(p8);
        v2_2.append("");
        String v2_3 = v2_2.toString();
        StringBuilder v3_2 = new StringBuilder();
        v3_2.append(p9);
        v3_2.append("");
        return com.chaoxing.mobile.s.A8(v0_2, new String[] {"circleId", "uid", "order", "page", "pageSize"}), new String[] {p6, p7, "0", v2_3, v3_2.toString()}));
    }

    public static String y5(android.content.Context p7, int p8, String p9, String p10, int p11, int p12)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.e);
        v7_5.append("apis/message/getMessageList?");
        String v7_1 = v7_5.toString();
        String v3 = "extend_param";
        String v1_3 = new StringBuilder();
        v1_3.append(p8);
        v1_3.append("");
        v1_3.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p11);
        v2_1.append("");
        v2_1.toString();
        StringBuilder v11_2 = new StringBuilder();
        v11_2.append(p12);
        v11_2.append("");
        v3 = p10;
        return com.chaoxing.mobile.s.f9(v7_1, new String[] {"tuid", "pageSize"}), new String[] {v0, v11_2.toString()}), 1);
    }

    public static String y6(android.content.Context p8, int p9, String p10, String p11, String p12, String p13, int p14)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v8_5 = new StringBuilder();
        v8_5.append(pk.a.f);
        v8_5.append("apis/notice/getOtherReaders?");
        String v8_1 = v8_5.toString();
        String v3 = "sid";
        String v5 = "kw";
        String v1_3 = new StringBuilder();
        v1_3.append(p9);
        v1_3.append("");
        v1_3.toString();
        String v2_1 = new StringBuilder();
        v2_1.append(p14);
        v2_1.append("");
        v3 = p11;
        v5 = p13;
        return com.chaoxing.mobile.s.A8(v8_1, new String[] {"puid", "pageSize"}), new String[] {v0, v2_1.toString()}));
    }

    public static String y7()
    {
        return "https://learn.chaoxing.com/mobilelib/app/index?stuff=3";
    }

    public static String y9(String p4, String p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle_category/getCircleCategoryList?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"uid", "pid", "order"}), new String[] {p4, p5, p6}));
    }

    public static String ya(String p2)
    {
        Object[] v0_1 = new Object[1];
        v0_1[0] = p2;
        return String.format("https://mooc1-api.chaoxing.com/editnewcatalelog?specialType=BOOK&courseId=%s&siblingNodeId=undefined", v0_1);
    }

    public static String yb()
    {
        return com.chaoxing.mobile.s.Kb();
    }

    public static String yc(String p15, String p16, String p17, int p18, int p19, int p20, String p21, String p22)
    {
        String v7_1;
        if (android.text.TextUtils.isEmpty(p22)) {
            v7_1 = p22;
        } else {
            v7_1 = p22;
            if (p22.equals("0")) {
                String v0_11 = new StringBuilder();
                v0_11.append(pk.d.b().a(p15));
                v0_11.append("apis/topic/getTopTopicList?");
                String v0_12 = v0_11.toString();
                String v3 = "kw";
                String v5 = "order";
                String.valueOf(p18);
                String.valueOf(p19);
                String v7 = "";
                String v4 = p17;
                return com.chaoxing.mobile.s.A8(v0_12, new String[] {"bbsid", "tags"}), new String[] {p15, p21}));
            }
        }
        if (android.text.TextUtils.isEmpty(v7_1)) {
            String v0_3 = new StringBuilder();
            v0_3.append(pk.d.b().a(p15));
            v0_3.append("apis/topic/getTopTopicList?");
            String v7_0 = v0_3.toString();
            String v10 = "kw";
            String v12 = "order";
            String.valueOf(p18);
            String.valueOf(p19);
            String.valueOf(p20);
            String v2 = p17;
            return com.chaoxing.mobile.s.A8(v7_0, new String[] {"bbsid", "tags"}), new String[] {p15, p21}));
        } else {
            String v0_6 = new StringBuilder();
            v0_6.append(pk.d.b().a(p15));
            v0_6.append("apis/topic/getTopTopicList?");
            String v0_8 = v0_6.toString();
            v10 = "kw";
            v12 = "order";
            String.valueOf(p18);
            String.valueOf(p19);
            v4 = p17;
            return com.chaoxing.mobile.s.A8(v0_8, new String[] {"bbsid", "tags"}), new String[] {p15, p21}));
        }
    }

    public static String yd(java.util.List p2, String p3)
    {
        StringBuilder v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p3));
        v0_1.append("apis/invitation/updateReply?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String z(android.content.Context p4, String p5)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/persongroup/addPersonGroup?", new String[] {"tid", "puid", "name"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), com.chaoxing.study.account.AccountManager.C().D().getPuid(), p5}), 1);
    }

    public static String z0(android.content.Context p4, int p5)
    {
        String v4_4 = com.chaoxing.study.account.AccountManager.C().D().getUid();
        String v0_0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9("https://mobilelearn.chaoxing.com/answer/productAnswerView?", new String[] {"tid", "uid", "appType"}), new String[] {v4_4, v0_0, v2_2.toString()}), 0);
    }

    public static String z1()
    {
        String v0_1 = new StringBuilder();
        v0_1.append(gc.b.d);
        v0_1.append("teachingClassManage/updateCourseInfoContent?");
        return v0_1.toString();
    }

    public static String z2(android.content.Context p5, String p6, long p7, int p9)
    {
        String v7_1;
        String v5_4 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v3_0 = "";
        if (p7 != 0) {
            StringBuilder v1_2 = new StringBuilder();
            v1_2.append(p7);
            v1_2.append("");
            v7_1 = v1_2.toString();
        } else {
            v7_1 = "";
        }
        if (p9 > 0) {
            StringBuilder v8_1 = new StringBuilder();
            v8_1.append(p9);
            v8_1.append("");
            v3_0 = v8_1.toString();
        }
        return com.chaoxing.mobile.s.e9("https://specie.chaoxing.com/apis/folder/getChatList?", new String[] {"puid", "folderId", "msgId", "pageSize"}), new String[] {v5_4, p6, v7_1, v3_0}));
    }

    public static String z3(String p7, String p8, int p9, int p10, String p11, String p12)
    {
        String v10_5 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        if (android.text.TextUtils.isEmpty(v10_5)) {
            String v10_2 = new StringBuilder();
            v10_2.append(pk.a.e);
            v10_2.append("apis/circle/addCircle?");
            String v10_3 = v10_2.toString();
            StringBuilder v2_1 = new StringBuilder();
            v2_1.append(p9);
            v2_1.append("");
            return com.chaoxing.mobile.s.A8(v10_3, new String[] {"uid", "name", "check", "folderId", "introduce"}), new String[] {p7, p8, v2_1.toString(), p11, p12}));
        } else {
            String v7_4 = new StringBuilder();
            v7_4.append(pk.a.e);
            v7_4.append("apis/circle/addCircle?");
            String v7_5 = v7_4.toString();
            StringBuilder v2_3 = new StringBuilder();
            v2_3.append(p9);
            v2_3.append("");
            return com.chaoxing.mobile.s.A8(v7_5, new String[] {"puid", "name", "check", "folderId", "introduce"}), new String[] {v10_5, p8, v2_3.toString(), p11, p12}));
        }
    }

    public static String z4(String p4, String p5)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.e);
        v0_1.append("apis/circle/circleGroupChat3?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "circleId", "autoJoin"}), new String[] {p4, p5, "0"}));
    }

    public static String z5(android.content.Context p4, String p5, String p6)
    {
        return com.chaoxing.mobile.s.f9("https://specie.chaoxing.com/apis/message/getSpecies?", new String[] {"puid", "sign", "version", "fid"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getPuid(), p5, "20220629", p6}), 1);
    }

    public static String z6(android.content.Context p7, String p8, String p9, int p10, int p11)
    {
        String v0 = com.chaoxing.study.account.AccountManager.C().D().getPuid();
        String v7_5 = new StringBuilder();
        v7_5.append(pk.a.f);
        v7_5.append("apis/notice/getPraises_v2?");
        String v7_1 = v7_5.toString();
        String v3 = "relationId";
        String.valueOf(p9);
        String.valueOf(p10);
        String v2 = p8;
        return com.chaoxing.mobile.s.A8(v7_1, new String[] {"puid", "order"}), new String[] {v0, String.valueOf(p11)}));
    }

    public static String z7()
    {
        String v0_1 = new Object[0];
        return String.format("https://x.chaoxing.com/apis/resControl/scroll", v0_1);
    }

    public static String z9(String p6, String p7, int p8, int p9, String p10)
    {
        return com.chaoxing.mobile.s.A9(p6, p7, p8, p9, p10, 0);
    }

    public static String za(java.util.List p2)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.a.f);
        v0_1.append("apis/notice/replyAdd?");
        return com.chaoxing.mobile.s.y8(v0_1.toString(), p2);
    }

    public static String zb(String p4, int p5, String p6)
    {
        String v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p6));
        v0_1.append("apis/circle/getCircle?");
        String v0_2 = v0_1.toString();
        StringBuilder v2_2 = new StringBuilder();
        v2_2.append(p5);
        v2_2.append("");
        return com.chaoxing.mobile.s.f9(v0_2, new String[] {"uid", "maxW", "s_circleId"}), new String[] {p4, v2_2.toString(), p6}), 1);
    }

    public static String zc(String p4, int p5, String p6, String p7)
    {
        String[] v0_1 = new StringBuilder();
        v0_1.append(pk.d.b().a(p7));
        v0_1.append("apis/topic/getTopic?");
        return com.chaoxing.mobile.s.A8(v0_1.toString(), new String[] {"puid", "maxW", "version", "s_topicId"}), new String[] {p4, String.valueOf(p5), "20180323", p6}));
    }

    public static String zd(android.content.Context p3, String p4, String p5)
    {
        return com.chaoxing.mobile.s.f9("https://learn.chaoxing.com/apis/friend/updateUserFriendGroup?", new String[] {"uid", "gid", "name"}), new String[] {com.chaoxing.study.account.AccountManager.C().D().getUid(), p4, p5}), 1);
    }
}
