import { onRequest as __api_eat_tick_js_onRequest } from "/Users/nicholas/clawd/csoai-static-deploy2/functions/api/eat-tick.js"
import { onRequest as __api_health_js_onRequest } from "/Users/nicholas/clawd/csoai-static-deploy2/functions/api/health.js"
import { onRequest as __api_leaderboard_js_onRequest } from "/Users/nicholas/clawd/csoai-static-deploy2/functions/api/leaderboard.js"
import { onRequest as __api_sov_bridge_js_onRequest } from "/Users/nicholas/clawd/csoai-static-deploy2/functions/api/sov-bridge.js"
import { onRequest as __api_stats_js_onRequest } from "/Users/nicholas/clawd/csoai-static-deploy2/functions/api/stats.js"
import { onRequest as __api__middleware_js_onRequest } from "/Users/nicholas/clawd/csoai-static-deploy2/functions/api/_middleware.js"

export const routes = [
    {
      routePath: "/api/eat-tick",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_eat_tick_js_onRequest],
    },
  {
      routePath: "/api/health",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_health_js_onRequest],
    },
  {
      routePath: "/api/leaderboard",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_leaderboard_js_onRequest],
    },
  {
      routePath: "/api/sov-bridge",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_sov_bridge_js_onRequest],
    },
  {
      routePath: "/api/stats",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_stats_js_onRequest],
    },
  {
      routePath: "/api",
      mountPath: "/api",
      method: "",
      middlewares: [__api__middleware_js_onRequest],
      modules: [],
    },
  ]