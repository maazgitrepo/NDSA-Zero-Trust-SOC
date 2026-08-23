import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
  url: "http://192.168.2.211:8081",
  realm: "ndsa",
  clientId: "ndsa-frontend",
});

export default keycloak;
