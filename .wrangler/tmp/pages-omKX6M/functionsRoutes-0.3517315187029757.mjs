import { onRequestPost as __api_ask_js_onRequestPost } from "/home/user/study-planner/functions/api/ask.js"
import { onRequestGet as __api_push_js_onRequestGet } from "/home/user/study-planner/functions/api/push.js"
import { onRequestPost as __api_push_js_onRequestPost } from "/home/user/study-planner/functions/api/push.js"

export const routes = [
    {
      routePath: "/api/ask",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_ask_js_onRequestPost],
    },
  {
      routePath: "/api/push",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_push_js_onRequestGet],
    },
  {
      routePath: "/api/push",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_push_js_onRequestPost],
    },
  ]