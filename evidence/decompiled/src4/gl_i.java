package gl;
public class i {
    public static volatile gl.i a;

    public i()
    {
        return;
    }

    public static gl.i d()
    {
        if (gl.i.a == null) {
            if (gl.i.a == null) {
                gl.i.a = new gl.i();
            }
        }
        return gl.i.a;
    }

    public androidx.lifecycle.LiveData a(com.chaoxing.mobile.office.bean.ASQueryParams p10, String p11, String p12)
    {
        return ((cl.b) qe.s.a().k(new gl.i$d(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).I(Integer.valueOf(p10.getDeptId()), p10.getUid(), p11, p12, p10.getDateTime(), p10.getSign(), p10.getEnc());
    }

    public androidx.lifecycle.LiveData b(com.chaoxing.mobile.office.bean.ASQueryParams p9, String p10)
    {
        return ((cl.b) qe.s.a().k(new gl.i$f(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).F(Integer.valueOf(p9.getDeptId()), p9.getUid(), p10, p9.getDateTime(), p9.getSign(), p9.getEnc());
    }

    public androidx.lifecycle.LiveData c(com.chaoxing.mobile.office.bean.ASQueryParams p10, String p11, String p12)
    {
        return ((cl.b) qe.s.a().k(new gl.i$e(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).c(Integer.valueOf(p10.getDeptId()), p10.getUid(), p11, p12, p10.getDateTime(), p10.getSign(), p10.getEnc());
    }

    public androidx.lifecycle.LiveData e(com.chaoxing.mobile.office.bean.ASQueryParams p9)
    {
        if (p9.getShare() != 1) {
            return ((cl.b) qe.s.a().k(new gl.i$b(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).U(p9.getDeptId(), p9.getUid(), p9.getDate(), p9.getDateTime(), p9.getSign(), p9.getEnc());
        } else {
            return ((cl.b) qe.s.a().k(new gl.i$a(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).h(p9.getDeptId(), p9.getUid(), p9.getDate(), p9.getDateTime(), p9.getSign(), p9.getEnc());
        }
    }

    public androidx.lifecycle.LiveData f(com.chaoxing.mobile.office.bean.ASQueryParams p8)
    {
        return ((cl.b) qe.s.a().k(new gl.i$c(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).A(p8.getDeptId(), p8.getUid(), p8.getDateTime(), p8.getSign(), p8.getEnc());
    }

    public androidx.lifecycle.LiveData g(com.chaoxing.mobile.office.bean.ASQueryParams p11, String p12, String p13, String p14)
    {
        return ((cl.b) qe.s.a().c("https://supportoffice.chaoxing.com").g(cl.b)).D(p11.getDeptId(), p12, p13, p11.getUid(), p14, p11.getDateTime(), p11.getSign(), p11.getEnc());
    }

    public androidx.lifecycle.LiveData h(com.chaoxing.mobile.office.bean.PunchRecord p27)
    {
        return ((cl.b) qe.s.a().k(new gl.i$h(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).z(Integer.parseInt(p27.getDeptId()), p27.getUid(), p27.getId(), p27.getDevice(), p27.getMsign(), p27.getDuty(), p27.getSeq(), p27.getClockinAddress(), p27.getAutomatic(), p27.getCode(), p27.getPunchValidType(), p27.getRemark(), p27.getObjectId(), p27.getClockinLngLat(), p27.getWifiName(), p27.getWifiMac(), p27.getBluetoothName(), p27.getBluetoothMac(), p27.getFacePicture(), p27.getDatetime(), p27.getSign(), p27.getEnc());
    }

    public androidx.lifecycle.LiveData i(com.chaoxing.mobile.office.bean.PunchRecord p26)
    {
        return ((cl.b) qe.s.a().k(new gl.i$g(this)).c("https://supportoffice.chaoxing.com").g(cl.b)).a(Integer.parseInt(p26.getDeptId()), p26.getUid(), p26.getDevice(), p26.getMsign(), p26.getDuty(), p26.getSeq(), p26.getClockinAddress(), p26.getAutomatic(), p26.getCode(), p26.getPunchValidType(), p26.getRemark(), p26.getObjectId(), p26.getClockinLngLat(), p26.getWifiName(), p26.getWifiMac(), p26.getBluetoothName(), p26.getBluetoothMac(), p26.getFacePicture(), p26.getDatetime(), p26.getSign(), p26.getEnc());
    }
}
