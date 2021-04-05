import request from "@/request/request";

export function loginByUsername(data) {
  return request({
    url: "/user/v1/login",
    method: "post",
    data
  });
}
export function saveInfo(data) {
  return request({
    url: "/users/saveInfo",
    method: "post",
    data
  });
}
export function changePsd(data) {
  return request({
    url: "/users/changePsd",
    method: "post",
    data
  });
}
export function getUserInfo(token) {
  return request({
    url: "/users/info",
    method: "get",
    params: { token }
  });
}

export function getOwnTasksList(data) {
  return request({
    url: "/resource/task/ownTasksList",
    method: "post",
    data: data
  });
}
export function getOwnLeaksList(data) {
  return request({
    url: "/resource/task/ownLeaksList",
    method: "post",
    data: data
  });
}
export function getOwnSocialList(data) {
  return request({
    url: "/resource/task/ownSocialList",
    method: "post",
    data: data
  });
}
export function getOwnTequeList(data) {
  return request({
    url: "/task/user/skill",
    method: "post",
    data
  });
}
export function getOwnTequeDetail(id) {
  return request({
    url: "/technology/skill",
    method: "get",
    params: { id }
  });
}
export function getOwnUsersList(data) {
  return request({
    url: "/users/createdList",
    method: "post",
    data: data
  });
}
export function getTaskReviewList(data) {
  return request({
    url: "/resource/task/taskReviewList",
    method: "post",
    data: data
  });
}

export function getTaskScoreList() {
  return request({
    url: "/task/user/score/list",
    method: "get"
  });
}
export function getTaskScoreOrgList(id) {
  return request({
    url: "/resource/taskScore/orgList",
    method: "get",
    params: { id }
  });
}
export function sureChangeScore(data) {
  return request({
    url: "/resource/taskScore/change",
    method: "post",
    data: data
  });
}
