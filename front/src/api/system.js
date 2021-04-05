import request from "@/request/request";

export function logList(data) {
  return request({
    url: "/system/Operation/list",
    method: "post",
    data: data
  });
}
export function systemInformation() {
  return request({
    url: "/system/summary",
    method: "get"
  });
}
export function logDel(data) {
  return request({
    url: "/system/Operation/list",
    method: "delete",
    data: data
  });
}
export function backupProgress() {
  return request({
    url: "/system/backup",
    method: "get"
  });
}

export function backupChange(data) {
  return request({
    url: "sysytem/chgbackup",
    method: "post",
    data: data
  });
}
export function download(id) {
  return request({
    url: "/system/backupdownload",
    method: "get",
    params: { id }
  });
}
export function backupDel(data) {
  return request({
    url: "/system/backups",
    method: "delete",
    data: data
  });
}
export function backupList(data) {
  return request({
    url: "/system/backups",
    method: "get",
    params: data
  });
}
export function backupListPost(data) {
  return request({
    url: "/system/backups",
    method: "post",
    params: data
  });
}
