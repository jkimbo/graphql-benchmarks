import http from "k6/http";
import { check } from "k6";

export let options = {
  stages: [
    {
      duration: "15s",
      target: 1
    }
  ]
};

export default function() {
  const params = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  const url = "http://localhost:8000";
  const response = http.get(`${url}/movies/`, null, params);

  check(response, {
    "is status 200": r => r.status === 200
  });
  check(response, {
    "is response correct": r => {
      return (
        response.json().length === 250 &&
        response.json()[0].title === "The Shawshank Redemption"
      );
    }
  });
}
