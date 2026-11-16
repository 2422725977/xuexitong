'use strict';
// 最小脚本：只报告存在，不做任何 hook，用于测量 App 在 frida 挂载下的自然存活时间。
setInterval(function () {}, 100000);
send("MIN ready");
