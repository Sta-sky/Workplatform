import request from "@/request/request";

export function memberDel(data) {
  return request({
    url: "/resource/organization/memberdel",
    method: "post",
    data: data
  });
}
export function organizationList() {
  return request({
    url: "/resource/region/list",
    method: "get"
  });
}
export function orgAdd(data) {
  return request({
    url: "/users/group",
    method: "post",
    data
  });
}
export function orgEdit(data) {
  return request({
    url: "/users/group",
    method: "put",
    data
  });
}
export function memberList(data) {
  return request({
    url: "/resource/organization/memberlist",
    method: "post",
    data: data
  });
}
// export function memberDetail(id) {
//   return request({
//     url: "/organization/detail",
//     method: "get",
//     params: { id }
//   });
// }
export function changeMember(data) {
  return request({
    url: "/resource/organization/memberchange",
    method: "post",
    data: data
  });
}
export function getOrgsList(data) {
  return request({
    url: "/resource/organization/list",
    method: "post",
    data: data
  });
}
export function userList(data) {
  return request({
    url: "/task/user/list",
    method: "post",
    data: data
  });
}
