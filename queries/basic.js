import http from "k6/http";
import { check } from "k6";

export let options = {
  stages: [
    {
      duration: "5s",
      target: 20
    },
    {
      duration: "10s",
      target: 20
    }
  ]
};

export default function() {
  const payload = JSON.stringify({
    query: "query { string }"
  });
  const params = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  const response = http.post("http://localhost:8000/graphql/", payload, params);

  check(response, {
    "is status 200": r => r.status === 200
  });
  check(response, {
    "is response correct": r => response.json("data.string") === "Hello World!"
  });
}
