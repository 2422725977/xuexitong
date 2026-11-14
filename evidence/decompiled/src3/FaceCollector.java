package com.chaoxing.facedetection;
public class FaceCollector {
    public com.chaoxing.facedetection.a a;
    public com.chaoxing.facedetection.b b;

    public FaceCollector()
    {
        return;
    }

    public synthetic FaceCollector(com.chaoxing.facedetection.FaceCollector$1 p1)
    {
        return;
    }

    public static synthetic com.chaoxing.facedetection.a a(com.chaoxing.facedetection.FaceCollector p0, com.chaoxing.facedetection.a p1)
    {
        p0.a = p1;
        return p1;
    }

    public static synthetic com.chaoxing.facedetection.b b(com.chaoxing.facedetection.FaceCollector p0, com.chaoxing.facedetection.b p1)
    {
        p0.b = p1;
        return p1;
    }

    public static com.chaoxing.facedetection.FaceCollector g()
    {
        return com.chaoxing.facedetection.FaceCollector$a.a;
    }

    public void c(android.content.Context p3, androidx.lifecycle.LifecycleOwner p4, Class p5, com.chaoxing.facedetection.a p6, com.chaoxing.facedetection.b p7)
    {
        if ((p4 != null) && (p4.getLifecycle().getCurrentState() != androidx.lifecycle.Lifecycle$State.DESTROYED)) {
            this.a = p6;
            this.b = p7;
            p4.getLifecycle().addObserver(new com.chaoxing.facedetection.FaceCollector$1(this));
            p3.startActivity(new android.content.Intent(p3, p5));
        }
        return;
    }

    public void d(android.content.Context p3, androidx.lifecycle.LifecycleOwner p4, Class p5, com.chaoxing.facedetection.bean.CollectConfig p6, com.chaoxing.facedetection.a p7, com.chaoxing.facedetection.b p8)
    {
        if ((p4 != null) && (p4.getLifecycle().getCurrentState() != androidx.lifecycle.Lifecycle$State.DESTROYED)) {
            this.a = p7;
            this.b = p8;
            p4.getLifecycle().addObserver(new com.chaoxing.facedetection.FaceCollector$2(this));
            android.content.Intent v4_3 = new android.content.Intent(p3, p5);
            if (p6 != null) {
                v4_3.putExtra("collect_config", p6);
            }
            p3.startActivity(v4_3);
        }
        return;
    }

    public void e(androidx.appcompat.app.AppCompatActivity p7, com.chaoxing.facedetection.a p8, com.chaoxing.facedetection.b p9)
    {
        this.c(p7, p7, 0, p8, p9);
        return;
    }

    public void f(androidx.fragment.app.Fragment p7, com.chaoxing.facedetection.a p8, com.chaoxing.facedetection.b p9)
    {
        this.c(p7.getContext(), p7, 0, p8, p9);
        return;
    }

    public com.chaoxing.facedetection.b h()
    {
        return this.b;
    }

    public void i(com.chaoxing.facedetection.CollectResult p2)
    {
        com.chaoxing.facedetection.a v0 = this.a;
        if (v0 != null) {
            v0.a(p2);
        }
        return;
    }
}
