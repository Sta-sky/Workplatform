/**
 * Created by jiachenpan on 16/11/18.
 */

export function isvalidUsername(str) {
  const valid_map = ["admin", "editor"];
  return valid_map.indexOf(str.trim()) >= 0;
}

/* 合法uri*/
export function validateURL(textval) {
  const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
  return urlregex.test(textval);
}

/* 手机号码*/
export function validatePhonenumber(str) {
  const reg = /^[0-9]+$/;
  return reg.test(str) && str.length === 11;
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
export function validateAlphabets(str) {
  const reg = /^[A-Za-z]+$/;
  return reg.test(str);
}

/* 大小写字母数字*/
export function validateAlpnum(str) {
  const reg = /^[0-9A-Za-z]+$/;
  return reg.test(str);
}

/* 不能小于8不能大于20位  不能纯数字或者纯字母*/
export function accountReg(str) {
  var reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[^]{7,19}$/;
  var r = reg.test(str);
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

export function unicode(str) {
  var isChinese = /^[\u4e00-\u9fa5\uf900-\ufa2d]+$/;
  if (!str) {
    return;
  }
  var unicode = "";
  for (var i = 0; i < str.length; i++) {
    var temp = str.charAt(i);
    if (isChinese.test(temp)) {
      unicode += "\\u" + temp.charCodeAt(0).toString(16);
    } else {
      unicode += temp;
    }
  }
  return unicode.length;
}

/**
 * validate email
 * @param email
 * @returns {boolean}
 */
export function validateEmail(email) {
  // eslint-disable-next-line no-useless-escape
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}
