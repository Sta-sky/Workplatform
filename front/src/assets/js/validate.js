/* eslint-disable no-irregular-whitespace */
/* eslint-disable camelcase */
/**
 * Created by jiachenpan on 16/11/18.
 */

export function isvalidUsername(str) {
  const valid_map = ["admin", "editor"];
  return valid_map.indexOf(str.trim()) >= 0;
}

/* 判断字符串是不是域名*/
export function regDomain(textval) {
  const domainregex = /^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$/;
  return domainregex.test(textval);
}

/* url规则*/
export function regURL(url) {
  const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
  return urlregex.test(url);
}

/* 小写字母*/
export function validateLowerCase(str) {
  const reg = /^[a-z]+$/;
  return reg.test(str);
}

/* 大写字母*/
export function validateUpperCase(str) {
  const reg = /^[A-Z]+$/;
  return reg.test(str);
}

/* 大小写字母*/
export function validatAlphabets(str) {
  const reg = /^[A-Za-z]+$/;
  return reg.test(str);
}

/* 要求密码有大写小写和数字且不得小于8位*/
export function regPsd(str) {
  var reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{7,}$/;
  var r = reg.test(str);
  return r;
}
/* 不能小于8不能大于20位  不能纯数字或者纯字母*/
export function accountReg(str) {
  var reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[^]{7,19}$/;
  var r = reg.test(str);
  return r;
}
/* 不能小于6  不能大于16位  以字母开头且不能为纯数字或者字母 */
export function passwordReg(str) {
  var reg = /^(?!^\d+$)(?!^[a-zA-Z]+$)[a-zA-Z][A-Za-z0-9]{5,15}$/;
  var r = reg.test(str);
  return r;
}
/* 检查是否是数字ip*/
export function IPShow(ip) {
  // 检查是否是数字ip
  if (!isNaN(ip)) {
    var ip_vl = parseInt(ip);
    return (
      ((ip_vl >> 24) & 0xff) +
      "." +
      ((ip_vl >> 16) & 0xff) +
      "." +
      ((ip_vl >> 8) & 0xff) +
      "." +
      (ip_vl & 0xff)
    );
  }
  return ip; // 返回原始数据
}
/* 检查邮箱格式是否正确*/
export function isEmail(email) {
  var reg = /^[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$/;
  var r = reg.test(email);
  return r;
}
/* 检查是否是电话号码*/
export function isPhone(phNum) {
  var reg = /^1[345789]\d{9}$/;
  var r = reg.test(phNum);
  return r;
}

/* 判断是否是ip */
export function isIp(con) {
  con = con.replace(/(^\s*)|(\s*$)/g, "");
  var reg = /^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$/;
  var r = reg.test(con);
  return r;
}

/* 判断字符串字节长度 */
export function GetLen(str) {
  var regEx = /^[\u4e00-\u9fa5\uf900-\ufa2d]+$/;
  if (regEx.test(str)) {
    return str.length * 2;
  }
  /* eslint-disable-next-line */
  var oMatches = str.match(/[\x00-\xff]/g);
  var oLength = 0;
  if (oMatches == null) {
    oLength = str.length * 2;
  } else {
    oLength = str.length * 2 - oMatches.length;
  }
  return oLength;
}

/* 判断是否为内网IP */
// 10.0.0.0~10.255.255.255（A类）
// 172.16.0.0~172.31.255.255（B类）
// 192.168.0.0~192.168.255.255（C类）
export function IsLanIp(str) {
  var regEx1 = /^10\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])$/;
  var regEx2 = /^172\.(1[6789]|2[0-9]|3[01])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])$/;
  var regEx3 = /^192\.168\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])$/;
  var r = regEx1.test(str);
  var r2 = regEx2.test(str);
  var r3 = regEx3.test(str);
  return r || r2 || r3;
}

// B---KB---GB
export function bytesToSize(bytes) {
  if (bytes === 0) return "0 B";
  var k = 1024;
  var sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  var i = Math.floor(Math.log(bytes) / Math.log(k));
  return (bytes / Math.pow(k, i)).toPrecision(3) + " " + sizes[i];
}
/* 判断密码(密码包含字母、数字，长度6-18字节) */
export function isPass(con) {
  var reg = /^(?=.*[a-z])(?=.*\d)[^]{8,16}$/;
  var r = reg.test(con);
  return r;
}
/* 判断端口号是否为0-65535*/
export function isPort(con) {
  var reg = /^([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$/;
  var r = reg.test(con);
  return r;
}
