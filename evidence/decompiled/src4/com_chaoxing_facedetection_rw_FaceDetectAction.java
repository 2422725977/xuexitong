package com.chaoxing.facedetection.rw;
public final enum class FaceDetectAction extends java.lang.Enum {
    private static final synthetic com.chaoxing.facedetection.rw.FaceDetectAction[] $VALUES;
    public static final enum com.chaoxing.facedetection.rw.FaceDetectAction Eye;
    public static final enum com.chaoxing.facedetection.rw.FaceDetectAction Mouth;
    public static final enum com.chaoxing.facedetection.rw.FaceDetectAction Nod;
    public static final enum com.chaoxing.facedetection.rw.FaceDetectAction ShakeHead;
    private int action;
    private int desc;

    private FaceDetectAction(String p1, int p2, int p3, int p4)
    {
        super(p1, p2);
        super.action = p3;
        super.desc = p4;
        return;
    }

    private static synthetic com.chaoxing.facedetection.rw.FaceDetectAction[] $values()
    {
        com.chaoxing.facedetection.rw.FaceDetectAction[] v0_1 = new com.chaoxing.facedetection.rw.FaceDetectAction[4];
        v0_1[0] = com.chaoxing.facedetection.rw.FaceDetectAction.Mouth;
        v0_1[1] = com.chaoxing.facedetection.rw.FaceDetectAction.ShakeHead;
        v0_1[2] = com.chaoxing.facedetection.rw.FaceDetectAction.Nod;
        v0_1[3] = com.chaoxing.facedetection.rw.FaceDetectAction.Eye;
        return v0_1;
    }

    static FaceDetectAction()
    {
        com.chaoxing.facedetection.rw.FaceDetectAction.Mouth = new com.chaoxing.facedetection.rw.FaceDetectAction("Mouth", 0, 0, com.chaoxing.facedetection.rw.R$string.face_action_mouth);
        com.chaoxing.facedetection.rw.FaceDetectAction.ShakeHead = new com.chaoxing.facedetection.rw.FaceDetectAction("ShakeHead", 1, 1, com.chaoxing.facedetection.rw.R$string.face_action_shakeHead);
        com.chaoxing.facedetection.rw.FaceDetectAction.Nod = new com.chaoxing.facedetection.rw.FaceDetectAction("Nod", 2, 2, com.chaoxing.facedetection.rw.R$string.face_action_nod);
        com.chaoxing.facedetection.rw.FaceDetectAction.Eye = new com.chaoxing.facedetection.rw.FaceDetectAction("Eye", 3, 3, com.chaoxing.facedetection.rw.R$string.face_action_eye);
        com.chaoxing.facedetection.rw.FaceDetectAction.$VALUES = com.chaoxing.facedetection.rw.FaceDetectAction.$values();
        return;
    }

    public static com.chaoxing.facedetection.rw.FaceDetectAction valueOf(String p1)
    {
        return ((com.chaoxing.facedetection.rw.FaceDetectAction) Enum.valueOf(com.chaoxing.facedetection.rw.FaceDetectAction, p1));
    }

    public static com.chaoxing.facedetection.rw.FaceDetectAction[] values()
    {
        return ((com.chaoxing.facedetection.rw.FaceDetectAction[]) com.chaoxing.facedetection.rw.FaceDetectAction.$VALUES.clone());
    }

    public int getAction()
    {
        return this.action;
    }

    public int getDesc()
    {
        return this.desc;
    }
}
