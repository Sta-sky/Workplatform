import request from "@/request/request";

export function sourceReview() {
  return request({
    url: "/resource/summary/",
    method: "get"
  });
}
export function modalsReview(data) {
  return request({
    url: "/resource/template/list/",
    method: "post",
    data
  });
}
export function sinModalDetail(data) {
  return request({
    url: "/resource/template/detail",
    method: "post",
    data
  });
}
export function linksReview(data) {
  return request({
    url: "/resource/links",
    method: "get",
    params: data
  });
}
export function linksAdd(data) {
  return request({
    url: "/resource/links",
    method: "post",
    data
  });
}
export function linksUpdate(data) {
  return request({
    url: "/resource/links",
    method: "put",
    data
  });
}
export function linksDel(data) {
  return request({
    url: "/resource/links",
    method: "delete",
    data
  });
}
export function weaponCategory() {
  return request({
    url: "/resource/weapon/category",
    method: "get"
  });
}
export function weaponReview(data) {
  return request({
    url: "/resource/weapon/list/",
    method: "post",
    data
  });
}
export function weaponAdd(data) {
  return request({
    method: "post",
    url: "/resource/weapon/add/",
    headers: {
      "Content-Type": "multipart/form-data"
    },
    data
  });
}
// 武器文件状态监测
export function weaponStatus(data) {
  return request({
    url: "/resource/fileStatus/check/",
    method: "post",
    data
  });
}
// 保存文件
export function weaponFileSave(data) {
  return request({
    url: "/resource/weapon/save/",
    method: "post",
    data
  });
}
// 浏览文件
export function weaponFileDetail(data) {
  return request({
    // url: "/resource/fileManage/detail/",
    url: "/resource/fileManage/analysis/",
    method: "post",
    data
  });
}
// 分数说明
export function taskFileDetail(data) {
  return request({
    url: "/resource/fileManage/detail/",
    method: "post",
    data
  });
}
// 删除
export function weaponDel(data) {
  return request({
    url: "/resource/weapon/delete/",
    method: "post",
    data
  });
}
