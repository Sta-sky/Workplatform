import request from "@/request/request";

export function getFourData() {
  return request({
    url: "/home/getFourData",
    method: "get"
  });
}

export function getLastTwoData() {
  return request({
    url: "/system/systeminfo",
    method: "get"
  });
}
