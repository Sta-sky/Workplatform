import Cookies from "js-cookie";

const TokenKey = "token";
const RoleKey = "role";
const UsernameKey = "username";

export function getToken() {
  return Cookies.get(TokenKey);
}

export function setToken(token) {
  return Cookies.set(TokenKey, token);
}

export function getRole() {
  return Cookies.get(RoleKey);
}

export function setRole(role) {
  return Cookies.set(RoleKey, role);
}
export function getUsername() {
  return Cookies.get(UsernameKey);
}

export function setUsername(name) {
  return Cookies.set(UsernameKey, name);
}

export function removeToken() {
  return Cookies.remove(TokenKey);
}
export function removeUsername() {
  return Cookies.remove(UsernameKey);
}
export function removeRole() {
  return Cookies.remove(RoleKey);
}
