import request from "@/request/request";

export function userList(data) {
  return request({
    url: "/user/v1/userinfo",
    method: "get",
    params: data
  });
}
export function apiList(data) {
  return request({
    url: "/user/v1/key_modify_query",
    method: "get",
    params: data
  });
}
export function modifySave(data) {
  return request({
    url: "/user/v1/modify_del_user",
    method: "post",
    data: data
  });
}

export function modifyApiSave(data) {
  return request({
    url: "/user/v1/key_modify_query",
    method: "post",
    data: data
  });
}

export function usertypeList() {
  return request({
    method: "get",
    url: "/user/v1/usertype"
  });
}
export function userDel(data) {
  return request({
    url: "/user/v1/modify_del_user",
    method: "get",
    params: data
  });
}
export function apiDel(data) {
  return request({
    url: "/user/v1/key_create_del",
    method: "get",
    params: data
  });
}
export function userAdd(data) {
  return request({
    url: "/user/v1/create",
    method: "post",
    data: data
  });
}
export function apiAdd(data) {
  return request({
    url: "/user/v1/key_create_del",
    method: "post",
    data: data
  });
}
// -----------------------
//
//

export function taskAddArr() {
  return request({
    url: "/task/add",
    method: "get"
  });
}
export function userDetails(id) {
  return request({
    url: "/users/detail",
    method: "post",
    data: { id: id }
  });
}
